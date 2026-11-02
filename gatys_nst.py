import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from PIL import Image
from torchvision import transforms
from torchvision.models import VGG19_Weights, vgg19
import matplotlib.pyplot as plt


# =====================================================================
# 1. CẤU TRÚC LƯU TRỮ KẾT QUẢ BENCHMARK (Dùng chung cho mọi phương pháp)
# =====================================================================
@dataclass
class BenchmarkResult:
    method_name: str
    output_image: Image.Image
    inference_time_sec: float
    time_per_step_ms: float
    peak_memory_mb: float
    total_steps: int
    loss_history: List[float]
    device_name: str


# =====================================================================
# 2. TIỆN ÍCH PHẦN CỨNG APPLE SILICON (MPS) & XỬ LÝ ẢNH
# =====================================================================
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def get_optimal_device() -> torch.device:
    """Tự động nhận diện GPU Apple Silicon (MPS), CUDA hoặc CPU."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def sync_device(device: torch.device) -> None:
    """Đồng bộ hóa hàng đợi GPU trước khi bấm giờ để đo thời gian chính xác."""
    if device.type == "mps":
        torch.mps.synchronize()
    elif device.type == "cuda":
        torch.cuda.synchronize()


def get_memory_mb(device: torch.device) -> float:
    """Lấy dung lượng bộ nhớ GPU đang cấp phát (MB) trên MPS hoặc CUDA."""
    if device.type == "mps":
        # Trên Apple Silicon Unified Memory, đo bộ nhớ driver đang cấp cho Metal
        return torch.mps.driver_allocated_memory() / (1024 ** 2)
    elif device.type == "cuda":
        return torch.cuda.max_memory_allocated() / (1024 ** 2)
    return 0.0


def load_image_tensor(
    path: str, img_size: int = 512, device: Optional[torch.device] = None
) -> torch.Tensor:
    """Đọc ảnh và chuẩn hóa sang Tensor trên thiết bị đích."""
    if device is None:
        device = get_optimal_device()
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size), interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])
    img = Image.open(path).convert("RGB")
    return transform(img).unsqueeze(0).to(device)


def tensor_to_pil(tensor: torch.Tensor) -> Image.Image:
    """Giải chuẩn hóa (de-normalize) Tensor về lại ảnh PIL."""
    t = tensor.detach().cpu().clone().squeeze(0)
    for c, m, s in zip(t, IMAGENET_MEAN, IMAGENET_STD):
        c.mul_(s).add_(m)
    t = torch.clamp(t, 0.0, 1.0)
    return transforms.ToPILImage()(t)


# =====================================================================
# 3. KIẾN TRÚC MẠNG VGG-19 & HÀM TOÁN HỌC GATYS
# =====================================================================
def compute_gram_matrix(feature_map: torch.Tensor) -> torch.Tensor:
    b, c, h, w = feature_map.size()
    features = feature_map.view(b * c, h * w)
    gram = torch.mm(features, features.t())
    return gram.div(b * c * h * w)


def compute_tv_loss(img: torch.Tensor) -> torch.Tensor:
    tv_h = torch.mean(torch.abs(img[:, :, 1:, :] - img[:, :, :-1, :]))
    tv_w = torch.mean(torch.abs(img[:, :, :, 1:] - img[:, :, :, :-1]))
    return tv_h + tv_w


class GatysFeatureExtractor(nn.Module):
    def __init__(self, use_avg_pool: bool = True):
        super().__init__()
        vgg_features = vgg19(weights=VGG19_Weights.DEFAULT).features[:29]
        self.layers = nn.ModuleList()

        for layer in vgg_features:
            if isinstance(layer, nn.MaxPool2d) and use_avg_pool:
                self.layers.append(nn.AvgPool2d(kernel_size=2, stride=2))
            elif isinstance(layer, nn.ReLU):
                self.layers.append(nn.ReLU(inplace=False))
            else:
                self.layers.append(layer)

        for param in self.parameters():
            param.requires_grad = False

        self.style_indices = {
            0: "conv1_1",
            5: "conv2_1",
            10: "conv3_1",
            19: "conv4_1",
            28: "conv5_1",
        }
        self.content_indices = {21: "conv4_2"}

    def forward(self, x: torch.Tensor) -> Tuple[Dict[str, torch.Tensor], Dict[str, torch.Tensor]]:
        content_feats, style_feats = {}, {}
        for idx, layer in enumerate(self.layers):
            x = layer(x)
            if idx in self.style_indices:
                style_feats[self.style_indices[idx]] = x
            if idx in self.content_indices:
                content_feats[self.content_indices[idx]] = x
        return content_feats, style_feats


# =====================================================================
# 4. HÀM CHẠY CHÍNH & VẼ SO SÁNH (Gọi trực tiếp từ Notebook)
# =====================================================================
def run_gatys(
    content_path: str,
    style_path: str,
    img_size: int = 512,
    steps: int = 300,
    alpha: float = 1.0,
    beta: float = 1e6,
    gamma: float = 1e-3,
    optimizer_type: str = "lbfgs",  # Chọn 'lbfgs' hoặc 'adam'
    lr: float = 0.03,               # Dùng khi chọn 'adam'
    init_mode: str = "content",     # 'content' hoặc 'noise'
    verbose_every: int = 50,
    device: Optional[torch.device] = None,
) -> BenchmarkResult:
    """
    Thực thi thuật toán Gatys et al. (2016) và trả về đối tượng BenchmarkResult.
    """
    if device is None:
        device = get_optimal_device()

    if device.type == "mps":
        torch.mps.empty_cache()

    content_t = load_image_tensor(content_path, img_size=img_size, device=device)
    style_t = load_image_tensor(style_path, img_size=img_size, device=device)

    extractor = GatysFeatureExtractor(use_avg_pool=True).to(device).eval()

    with torch.no_grad():
        target_content, _ = extractor(content_t)
        _, raw_style = extractor(style_t)
        target_grams = {k: compute_gram_matrix(v) for k, v in raw_style.items()}

    if init_mode == "content":
        opt_img = content_t.clone().detach().requires_grad_(True)
    else:
        opt_img = torch.randn_like(content_t, device=device).requires_grad_(True)

    opt_type = optimizer_type.lower()
    if opt_type == "lbfgs":
        optimizer = optim.LBFGS([opt_img], max_iter=1, history_size=10)
    elif opt_type == "adam":
        optimizer = optim.Adam([opt_img], lr=lr)
    else:
        raise ValueError("optimizer_type chỉ hỗ trợ 'lbfgs' hoặc 'adam'.")

    loss_history: List[float] = []
    peak_mem = get_memory_mb(device)

    # Đồng bộ phần cứng trước khi bấm giờ
    sync_device(device)
    start_time = time.perf_counter()

    step_counter = [0]

    while step_counter[0] < steps:
        def closure():
            optimizer.zero_grad()
            c_feats, s_feats = extractor(opt_img)

            c_loss = torch.mean((c_feats["conv4_2"] - target_content["conv4_2"]) ** 2)

            s_loss = torch.tensor(0.0, device=device)
            for k in s_feats:
                gram_opt = compute_gram_matrix(s_feats[k])
                s_loss = s_loss + 0.2 * torch.mean((gram_opt - target_grams[k]) ** 2)

            tv_loss = compute_tv_loss(opt_img)
            total_loss = alpha * c_loss + beta * s_loss + gamma * tv_loss
            total_loss.backward()

            step_counter[0] += 1
            loss_val = float(total_loss.item())
            loss_history.append(loss_val)

            if verbose_every > 0 and (step_counter[0] % verbose_every == 0 or step_counter[0] == 1):
                print(
                    f"[Gatys-{opt_type.upper()} | {device.type.upper()}] "
                    f"Step {step_counter[0]:03d}/{steps} | "
                    f"Content: {(alpha * c_loss).item():.3f} | "
                    f"Style: {(beta * s_loss).item():.3f} | "
                    f"Total: {loss_val:.3f}"
                )
            return total_loss

        optimizer.step(closure)
        current_mem = get_memory_mb(device)
        if current_mem > peak_mem:
            peak_mem = current_mem

    # Đồng bộ phần cứng sau khi kết thúc vòng lặp
    sync_device(device)
    total_time = time.perf_counter() - start_time
    actual_steps = step_counter[0]

    out_pil = tensor_to_pil(opt_img)

    return BenchmarkResult(
        method_name=f"Gatys ({opt_type.upper()})",
        output_image=out_pil,
        inference_time_sec=total_time,
        time_per_step_ms=(total_time / actual_steps) * 1000.0,
        peak_memory_mb=peak_mem,
        total_steps=actual_steps,
        loss_history=loss_history,
        device_name=f"Apple Silicon ({device.type.upper()})",
    )


def plot_gatys_analysis(
    content_path: str,
    style_path: str,
    result: BenchmarkResult,
    save_path: Optional[str] = None,
) -> None:
    """Hiển thị trực quan: Ảnh Content, Ảnh Style, Ảnh Output và Đường cong hội tụ Loss."""
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))

    img_size = result.output_image.size
    axes[0].imshow(Image.open(content_path).convert("RGB").resize(img_size))
    axes[0].set_title("Content (yosemite.jpg)", fontsize=11, fontweight="bold")
    axes[0].axis("off")

    axes[1].imshow(Image.open(style_path).convert("RGB").resize(img_size))
    axes[1].set_title("Style (yosemite_paint.jpg)", fontsize=11, fontweight="bold")
    axes[1].axis("off")

    axes[2].imshow(result.output_image)
    axes[2].set_title(
        f"{result.method_name}\n"
        f"Time: {result.inference_time_sec:.2f}s ({result.time_per_step_ms:.1f} ms/step)\n"
        f"Mem: {result.peak_memory_mb:.1f} MB | Steps: {result.total_steps}",
        fontsize=10,
        fontweight="bold",
    )
    axes[2].axis("off")

    axes[3].plot(result.loss_history, color="#d95f02", linewidth=1.8)
    axes[3].set_yscale("log")
    axes[3].set_title("Loss Convergence (Log Scale)", fontsize=11, fontweight="bold")
    axes[3].set_xlabel("Iterations")
    axes[3].set_ylabel("Total Loss")
    axes[3].grid(True, which="both", linestyle="--", alpha=0.5)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
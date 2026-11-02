"""
AdaIN — Arbitrary Style Transfer in Real-time with Adaptive Instance Normalization
Huang & Belongie, ICCV 2017  ·  arxiv.org/abs/1703.06868

Kiến trúc: naoto0804/pytorch-AdaIN (canonical PyTorch implementation).
• Encoder : VGG-19 normalised, up to relu4_1  (layer 0–30 của naoto0804 flat-VGG)
• AdaIN   : chuyển (μ, σ) của style sang content trong feature space  — 1 phép tính
• Decoder : mirror của encoder, được train riêng  (decoder.pth)
• Inference: 1 forward pass duy nhất, không vòng lặp tối ưu

Weights (vgg_normalised.pth + decoder.pth) tải tự động qua gdown lần đầu dùng.
Input ảnh: [0, 1] RGB — KHÔNG normalize ImageNet (khác Gatys).
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import List, Optional

import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt

from gatys_nst import BenchmarkResult, get_optimal_device, sync_device, get_memory_mb


# ─────────────────────────────────────────────────────────────────────────────
# 1. WEIGHTS MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
WEIGHTS_DIR = Path(__file__).parent / "weights"

# GitHub Release URLs — naoto0804/pytorch-AdaIN v0.0.0
_RELEASE_URLS: dict = {
    "vgg_normalised.pth": "https://github.com/naoto0804/pytorch-AdaIN/releases/download/v0.0.0/vgg_normalised.pth",
    "decoder.pth":        "https://github.com/naoto0804/pytorch-AdaIN/releases/download/v0.0.0/decoder.pth",
}


def download_adain_weights(weights_dir: Optional[Path] = None) -> None:
    """
    Tải vgg_normalised.pth (~80 MB) và decoder.pth (~14 MB)
    từ GitHub Release naoto0804/pytorch-AdaIN v0.0.0.
    Không cần gdown hay Google Drive.
    """
    import urllib.request

    if weights_dir is None:
        weights_dir = WEIGHTS_DIR
    weights_dir.mkdir(parents=True, exist_ok=True)

    for fname, url in _RELEASE_URLS.items():
        dst = weights_dir / fname
        if dst.exists():
            print(f"  ✓ {fname}  ({dst.stat().st_size // 1_048_576} MB, đã có)")
        else:
            print(f"  ↓ Đang tải {fname} từ GitHub …")
            def _progress(block, block_size, total):
                done = block * block_size
                if total > 0:
                    pct = min(done / total * 100, 100)
                    mb  = done / 1_048_576
                    print(f"\r    {pct:5.1f}%  ({mb:.0f} MB)", end="", flush=True)
            urllib.request.urlretrieve(url, dst, reporthook=_progress)
            print(f"\n  ✓ Lưu → {dst}  ({dst.stat().st_size // 1_048_576} MB)")


# ─────────────────────────────────────────────────────────────────────────────
# 2. IMAGE UTILITIES  ([0,1] — không có ImageNet normalize)
# ─────────────────────────────────────────────────────────────────────────────
def load_image_adain(path: str, img_size: int, device: torch.device) -> torch.Tensor:
    """Load ảnh về [0,1] tensor, không chuẩn hóa ImageNet."""
    tf = transforms.Compose([
        transforms.Resize((img_size, img_size), interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.ToTensor(),
    ])
    return tf(Image.open(path).convert("RGB")).unsqueeze(0).to(device)


def tensor_to_pil_adain(t: torch.Tensor) -> Image.Image:
    """Tensor [0,1] → PIL Image (decoder output đã ở range [0,1])."""
    return transforms.ToPILImage()(torch.clamp(t.detach().cpu().squeeze(0), 0.0, 1.0))


# ─────────────────────────────────────────────────────────────────────────────
# 3. VGG-19 NORMALISED ARCHITECTURE (naoto0804 variant)
# ─────────────────────────────────────────────────────────────────────────────
#
# Khác với torchvision VGG-19:
#   - Layer 0: Conv2d(3,3,1×1) — bakes pixel normalization vào weights
#   - Dùng ReflectionPad2d + Conv2d thay vì Conv2d với padding
#   - MaxPool dùng ceil_mode=True
#   - Đầu vào: [0,1] RGB (không subtract ImageNet mean bên ngoài)
#
# Indices trong flat Sequential:
#   3  → relu1_1 | 10 → relu2_1 | 17 → relu3_1 | 30 → relu4_1
#
def _build_vgg_full() -> nn.Sequential:
    """Full naoto0804 VGG-19 (relu1_1 … relu5_1) để load vgg_normalised.pth."""
    return nn.Sequential(
        nn.Conv2d(3, 3, (1, 1)),                                     # 0  pixel norm
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 1
        nn.Conv2d(3, 64, (3, 3)),                                     # 2  conv1_1
        nn.ReLU(inplace=False),                                       # 3  relu1_1
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 4
        nn.Conv2d(64, 64, (3, 3)),                                    # 5  conv1_2
        nn.ReLU(inplace=False),                                       # 6  relu1_2
        nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),        # 7
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 8
        nn.Conv2d(64, 128, (3, 3)),                                   # 9  conv2_1
        nn.ReLU(inplace=False),                                       # 10 relu2_1
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 11
        nn.Conv2d(128, 128, (3, 3)),                                  # 12 conv2_2
        nn.ReLU(inplace=False),                                       # 13 relu2_2
        nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),        # 14
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 15
        nn.Conv2d(128, 256, (3, 3)),                                  # 16 conv3_1
        nn.ReLU(inplace=False),                                       # 17 relu3_1
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 18
        nn.Conv2d(256, 256, (3, 3)),                                  # 19 conv3_2
        nn.ReLU(inplace=False),                                       # 20 relu3_2
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 21
        nn.Conv2d(256, 256, (3, 3)),                                  # 22 conv3_3
        nn.ReLU(inplace=False),                                       # 23 relu3_3
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 24
        nn.Conv2d(256, 256, (3, 3)),                                  # 25 conv3_4
        nn.ReLU(inplace=False),                                       # 26 relu3_4
        nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),        # 27
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 28
        nn.Conv2d(256, 512, (3, 3)),                                  # 29 conv4_1
        nn.ReLU(inplace=False),                                       # 30 relu4_1  ← stop here
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 31
        nn.Conv2d(512, 512, (3, 3)),                                  # 32 conv4_2
        nn.ReLU(inplace=False),                                       # 33 relu4_2
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 34
        nn.Conv2d(512, 512, (3, 3)),                                  # 35 conv4_3
        nn.ReLU(inplace=False),                                       # 36 relu4_3
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 37
        nn.Conv2d(512, 512, (3, 3)),                                  # 38 conv4_4
        nn.ReLU(inplace=False),                                       # 39 relu4_4
        nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),        # 40
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 41
        nn.Conv2d(512, 512, (3, 3)),                                  # 42 conv5_1
        nn.ReLU(inplace=False),                                       # 43 relu5_1
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 44
        nn.Conv2d(512, 512, (3, 3)),                                  # 45 conv5_2
        nn.ReLU(inplace=False),                                       # 46 relu5_2
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 47
        nn.Conv2d(512, 512, (3, 3)),                                  # 48 conv5_3
        nn.ReLU(inplace=False),                                       # 49 relu5_3
        nn.ReflectionPad2d((1, 1, 1, 1)),                            # 50
        nn.Conv2d(512, 512, (3, 3)),                                  # 51 conv5_4
        nn.ReLU(inplace=False),                                       # 52 relu5_4
    )


class VGGEncoder(nn.Module):
    """
    VGG encoder (naoto0804) cắt tại relu4_1 (index 30).
    forward() trả về tensor relu4_1.
    forward(return_multi=True) trả về dict {relu1_1, relu2_1, relu3_1, relu4_1}.
    """
    _HOOKS = {3: "relu1_1", 10: "relu2_1", 17: "relu3_1", 30: "relu4_1"}

    def __init__(self, vgg_state_dict: dict):
        super().__init__()
        full = _build_vgg_full()
        full.load_state_dict(vgg_state_dict)
        # Slice: indices 0–30 inclusive = 31 layers
        self.net = nn.Sequential(*list(full.children())[:31])
        for p in self.parameters():
            p.requires_grad_(False)

    def forward(self, x: torch.Tensor, return_multi: bool = False):
        if not return_multi:
            return self.net(x)
        feats = {}
        for i, layer in enumerate(self.net):
            x = layer(x)
            if i in self._HOOKS:
                feats[self._HOOKS[i]] = x
        return feats


# ─────────────────────────────────────────────────────────────────────────────
# 4. ADAIN LAYER
# ─────────────────────────────────────────────────────────────────────────────
def adain(
    content: torch.Tensor,
    style: torch.Tensor,
    eps: float = 1e-5,
) -> torch.Tensor:
    """
    AdaIN(x, y) = σ(y) · (x − μ(x)) / σ(x) + μ(y)

    Chuyển thống kê không gian (mean, std per channel) của style sang content.
    Giữ nguyên spatial structure của content, khoác tông màu của style.
    Đây là toàn bộ "style transfer" — một phép tính O(1) trên feature map.

    Args:
        content : [B, C, H, W]  features của ảnh content từ relu4_1
        style   : [B, C, H, W]  features của tranh style từ relu4_1
        eps     : tránh chia cho 0
    Returns:
        [B, C, H, W]  normalized content mang thống kê của style
    """
    B, C = content.shape[:2]
    cm = content.view(B, C, -1).mean(2).view(B, C, 1, 1)
    cs = content.view(B, C, -1).std(2).view(B, C, 1, 1).clamp_min(eps)
    sm = style.view(B, C, -1).mean(2).view(B, C, 1, 1)
    ss = style.view(B, C, -1).std(2).view(B, C, 1, 1).clamp_min(eps)
    return ss * (content - cm) / cs + sm


# ─────────────────────────────────────────────────────────────────────────────
# 5. DECODER (mirror of encoder, trained weights required)
# ─────────────────────────────────────────────────────────────────────────────
class AdaINDecoder(nn.Module):
    """
    Decoder mirror của naoto0804 VGGEncoder.
    Kiến trúc khớp chính xác với decoder.pth để load_state_dict thành công.

    Conv indices có trainable weights: 1, 5, 8, 11, 14, 18, 21, 25, 28
    (tương ứng keys trong state dict: '1.weight', '1.bias', '5.weight', …)
    """
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 0
            nn.Conv2d(512, 256, (3, 3)),                  # 1
            nn.ReLU(inplace=False),                       # 2
            nn.Upsample(scale_factor=2, mode="nearest"),  # 3  ×2  64→128
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 4
            nn.Conv2d(256, 256, (3, 3)),                  # 5
            nn.ReLU(inplace=False),                       # 6
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 7
            nn.Conv2d(256, 256, (3, 3)),                  # 8
            nn.ReLU(inplace=False),                       # 9
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 10
            nn.Conv2d(256, 256, (3, 3)),                  # 11
            nn.ReLU(inplace=False),                       # 12
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 13
            nn.Conv2d(256, 128, (3, 3)),                  # 14
            nn.ReLU(inplace=False),                       # 15
            nn.Upsample(scale_factor=2, mode="nearest"),  # 16  ×2  128→256
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 17
            nn.Conv2d(128, 128, (3, 3)),                  # 18
            nn.ReLU(inplace=False),                       # 19
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 20
            nn.Conv2d(128, 64, (3, 3)),                   # 21
            nn.ReLU(inplace=False),                       # 22
            nn.Upsample(scale_factor=2, mode="nearest"),  # 23  ×2  256→512
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 24
            nn.Conv2d(64, 64, (3, 3)),                    # 25
            nn.ReLU(inplace=False),                       # 26
            nn.ReflectionPad2d((1, 1, 1, 1)),            # 27
            nn.Conv2d(64, 3, (3, 3)),                     # 28  → RGB, không ReLU
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def _load_decoder(path: Path, device: torch.device) -> AdaINDecoder:
    """Load decoder.pth vào AdaINDecoder.net (flat Sequential)."""
    try:
        state = torch.load(path, map_location=device, weights_only=True)
    except Exception:
        # Fallback cho file .pth cũ không dùng weights_only
        state = torch.load(path, map_location=device)
    d = AdaINDecoder()
    d.net.load_state_dict(state)
    return d.to(device).eval()


# ─────────────────────────────────────────────────────────────────────────────
# 6. MAIN INFERENCE
# ─────────────────────────────────────────────────────────────────────────────
def run_adain(
    content_path: str,
    style_path: str,
    img_size: int = 512,
    alpha: float = 1.0,
    weights_dir: Optional[Path] = None,
    device: Optional[torch.device] = None,
) -> BenchmarkResult:
    """
    Chạy AdaIN style transfer — 1 forward pass duy nhất (không vòng lặp).

    Args:
        content_path : đường dẫn ảnh content
        style_path   : đường dẫn tranh style
        img_size     : resize ảnh về img_size × img_size trước khi xử lý
        alpha        : cường độ style [0,1]  (0 = giữ nguyên, 1 = full transfer)
        weights_dir  : thư mục chứa .pth files (mặc định: ./weights/)
        device       : MPS / CUDA / CPU (auto-detect nếu None)

    Returns:
        BenchmarkResult  tương thích với Gatys để so sánh trong notebook
    """
    if device is None:
        device = get_optimal_device()
    if weights_dir is None:
        weights_dir = WEIGHTS_DIR

    vgg_path     = weights_dir / "vgg_normalised.pth"
    decoder_path = weights_dir / "decoder.pth"

    if not vgg_path.exists() or not decoder_path.exists():
        print("Weights chưa có, đang tải tự động …")
        download_adain_weights(weights_dir)

    if device.type == "mps":
        torch.mps.empty_cache()

    # Build model
    vgg_state = torch.load(vgg_path, map_location=device, weights_only=True)
    encoder   = VGGEncoder(vgg_state).to(device).eval()
    decoder   = _load_decoder(decoder_path, device)

    # Load images ([0,1] — no ImageNet normalization)
    content_t = load_image_adain(content_path, img_size, device)
    style_t   = load_image_adain(style_path,   img_size, device)

    peak_mem  = get_memory_mb(device)

    # ── Single forward pass ──────────────────────────────────────────────────
    sync_device(device)
    t0 = time.perf_counter()

    with torch.no_grad():
        cf  = encoder(content_t)                          # relu4_1 content
        sf  = encoder(style_t)                            # relu4_1 style
        t   = adain(cf, sf)                               # statistics transfer
        t   = alpha * t + (1.0 - alpha) * cf             # blend (α controls strength)
        out = decoder(t)                                  # decode → RGB [0,1]

    sync_device(device)
    elapsed = time.perf_counter() - t0

    cur_mem  = get_memory_mb(device)
    peak_mem = max(peak_mem, cur_mem)
    out_pil  = tensor_to_pil_adain(out)

    print(
        f"[AdaIN | {device.type.upper()}] "
        f"α={alpha:.2f} | "
        f"{elapsed * 1000:.1f} ms  (1 forward pass) | "
        f"Peak RAM: {peak_mem:.0f} MB"
    )

    return BenchmarkResult(
        method_name        = f"AdaIN (α={alpha})",
        output_image       = out_pil,
        inference_time_sec = elapsed,
        time_per_step_ms   = elapsed * 1000.0,  # 1 "step" = toàn bộ forward pass
        peak_memory_mb     = peak_mem,
        total_steps        = 1,
        loss_history       = [],                 # feed-forward: không có loss curve
        device_name        = f"Apple Silicon ({device.type.upper()})",
    )


# ─────────────────────────────────────────────────────────────────────────────
# 7. VISUALISATION
# ─────────────────────────────────────────────────────────────────────────────
def plot_adain_analysis(
    content_path: str,
    style_path: str,
    result: BenchmarkResult,
    save_path: Optional[str] = None,
) -> None:
    """3 panels: Content | Style | Output với thông số hiệu năng."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    sz = result.output_image.size

    panels = [
        (Image.open(content_path).convert("RGB").resize(sz), "Content (yosemite.jpg)"),
        (Image.open(style_path).convert("RGB").resize(sz),   "Style (yosemite_paint.jpg)"),
        (
            result.output_image,
            f"{result.method_name}\n"
            f"Time: {result.inference_time_sec * 1000:.1f} ms  (1 forward pass)\n"
            f"Peak RAM: {result.peak_memory_mb:.0f} MB",
        ),
    ]
    for ax, (img, title) in zip(axes, panels):
        ax.imshow(img)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.axis("off")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_adain_alpha_grid(
    content_path: str,
    style_path: str,
    alphas: Optional[List[float]] = None,
    img_size: int = 256,
    weights_dir: Optional[Path] = None,
    device: Optional[torch.device] = None,
    save_path: Optional[str] = None,
) -> None:
    """
    Tính năng độc đáo của AdaIN: điều chỉnh cường độ style liên tục qua α.
    Hiển thị grid: Content | α=0 | α=0.25 | … | α=1.0 | Style
    """
    if alphas is None:
        alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    if device is None:
        device = get_optimal_device()
    if weights_dir is None:
        weights_dir = WEIGHTS_DIR

    vgg_state = torch.load(weights_dir / "vgg_normalised.pth", map_location=device, weights_only=True)
    encoder   = VGGEncoder(vgg_state).to(device).eval()
    decoder   = _load_decoder(weights_dir / "decoder.pth", device)

    content_t = load_image_adain(content_path, img_size, device)
    style_t   = load_image_adain(style_path,   img_size, device)

    with torch.no_grad():
        cf      = encoder(content_t)
        sf      = encoder(style_t)
        t_full  = adain(cf, sf)        # pre-compute AdaIN once

    n = len(alphas) + 2
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4.2))

    axes[0].imshow(Image.open(content_path).convert("RGB"))
    axes[0].set_title("Content", fontsize=11, fontweight="bold")
    axes[0].axis("off")

    for i, alpha in enumerate(alphas):
        with torch.no_grad():
            t_blend = alpha * t_full + (1.0 - alpha) * cf
            out     = decoder(t_blend)
        axes[i + 1].imshow(tensor_to_pil_adain(out))
        axes[i + 1].set_title(f"α = {alpha}", fontsize=11)
        axes[i + 1].axis("off")

    axes[-1].imshow(Image.open(style_path).convert("RGB"))
    axes[-1].set_title("Style", fontsize=11, fontweight="bold")
    axes[-1].axis("off")

    plt.suptitle(
        "AdaIN — Điều chỉnh cường độ style liên tục (α)\n"
        "Gatys không có tính năng này — phải chạy lại từ đầu với β khác",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()

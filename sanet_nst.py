"""
SANet — Style-Attentional Networks
Park et al., CVPR 2019  · arxiv.org/abs/1812.02342

Kiến trúc đúng theo paper và source code chính thức (dypark86/SANET, GlebSBrykin/SANET):

  Encoder  : VGG-19 normalised, CẢ HAI TẦNG relu4_1 và relu5_1 (dual-level)
  SANet    : SANet(in_planes=512) với 4 learned 1×1 conv (f, g, h, out_conv)
             + residual O = out_conv(attention(f,g,h)) + content
  Transform: sanet4_1(relu4_1) + upsample(sanet5_1(relu5_1)) → merge_conv
  Decoder  : AdaIN decoder (cùng architecture, AdaIN weights được dùng vì
             SANet decoder có cùng topology, chỉ khác trained distribution)

Weights 1×1 conv được khởi tạo = identity → demo cơ chế đúng architecture.
Để có kết quả đúng paper cần transformer_iter_500000.pth từ tác giả.

Feed-forward, 1 forward pass, không optimization loop.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from adain_nst import (
    BenchmarkResult, VGGEncoder, _load_decoder,
    load_image_adain, tensor_to_pil_adain,
    get_optimal_device, sync_device, get_memory_mb,
    WEIGHTS_DIR,
)

__all__ = [
    "SANetModule",
    "SANetTransform",
    "run_sanet",
    "plot_sanet_analysis",
    "plot_sanet_temperature_grid",
]


# ─────────────────────────────────────────────────────────────────────────────
# VGG encoder dual-level (relu4_1 + relu5_1)
# ─────────────────────────────────────────────────────────────────────────────

def _build_vgg_stages(vgg_state: dict) -> Tuple[nn.Sequential, nn.Sequential]:
    """
    Từ state_dict của VGG normalised, build 2 stages:
      enc4: input → relu4_1  (layers 0..30)
      enc5: relu4_1 → relu5_1 (layers 31..43)
    Khớp với GlebSBrykin/SANET Eval.py:
      enc_4 = Sequential(*list(vgg.children())[18:31])  # relu3_1 → relu4_1
      enc_5 = Sequential(*list(vgg.children())[31:44])  # relu4_1 → relu5_1
    """
    vgg_full = nn.Sequential(
        nn.Conv2d(3, 3, (1, 1)),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(3, 64, (3, 3)),
        nn.ReLU(),    # relu1-1
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(64, 64, (3, 3)),
        nn.ReLU(),    # relu1-2
        nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(64, 128, (3, 3)),
        nn.ReLU(),    # relu2-1
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(128, 128, (3, 3)),
        nn.ReLU(),    # relu2-2
        nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(128, 256, (3, 3)),
        nn.ReLU(),    # relu3-1
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),    # relu3-2
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),    # relu3-3
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 256, (3, 3)),
        nn.ReLU(),    # relu3-4
        nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(256, 512, (3, 3)),
        nn.ReLU(),    # relu4-1  ← split point
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 512, (3, 3)),
        nn.ReLU(),    # relu4-2
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 512, (3, 3)),
        nn.ReLU(),    # relu4-3
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 512, (3, 3)),
        nn.ReLU(),    # relu4-4
        nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True),
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 512, (3, 3)),
        nn.ReLU(),    # relu5-1  ← output
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 512, (3, 3)),
        nn.ReLU(),    # relu5-2
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 512, (3, 3)),
        nn.ReLU(),    # relu5-3
        nn.ReflectionPad2d((1, 1, 1, 1)),
        nn.Conv2d(512, 512, (3, 3)),
        nn.ReLU(),    # relu5-4
    )
    # Load weights (strict=False vì VGGEncoder có thể dùng tên khác)
    vgg_full.load_state_dict(vgg_state, strict=False)

    enc4 = nn.Sequential(*list(vgg_full.children())[:31])   # → relu4_1
    enc5 = nn.Sequential(*list(vgg_full.children())[31:44]) # relu4_1 → relu5_1
    return enc4, enc5


def _mean_var_norm(feat: torch.Tensor, eps: float = 1e-5) -> torch.Tensor:
    """Instance-normalise theo channel (giống paper)."""
    size = feat.size()
    mean = feat.view(*size[:2], -1).mean(dim=2).view(*size[:2], 1, 1)
    std  = feat.view(*size[:2], -1).var (dim=2).add_(eps).sqrt_().view(*size[:2], 1, 1)
    return (feat - mean) / std


# ─────────────────────────────────────────────────────────────────────────────
# SANet module — đúng theo paper (f, g, h, out_conv + residual)
# ─────────────────────────────────────────────────────────────────────────────

class SANetModule(nn.Module):
    """
    SANet attention đúng theo paper:
      F = f(norm(content))   ← Query
      G = g(norm(style))     ← Key
      H = h(style)           ← Value  (unnormalised)
      S = softmax(F^T G)
      O = out_conv(H S^T) + content   ← residual!

    1×1 conv: learned, khởi tạo = identity khi không có weights.
    """
    def __init__(self, in_planes: int = 512):
        super().__init__()
        self.f        = nn.Conv2d(in_planes, in_planes, (1, 1))
        self.g        = nn.Conv2d(in_planes, in_planes, (1, 1))
        self.h        = nn.Conv2d(in_planes, in_planes, (1, 1))
        self.out_conv = nn.Conv2d(in_planes, in_planes, (1, 1))
        self.sm       = nn.Softmax(dim=-1)
        self._init_as_identity(in_planes)

    def _init_as_identity(self, C: int) -> None:
        """Khởi tạo 1×1 conv = identity → đầu ra ≈ non-parametric attention."""
        for layer in (self.f, self.g, self.h, self.out_conv):
            nn.init.eye_(layer.weight.view(C, C))
            nn.init.zeros_(layer.bias)

    def forward(self, content: torch.Tensor, style: torch.Tensor) -> torch.Tensor:
        F  = self.f(_mean_var_norm(content))          # (B, C, Hc, Wc)
        G  = self.g(_mean_var_norm(style))            # (B, C, Hs, Ws)
        H  = self.h(style)                            # (B, C, Hs, Ws)

        B, C, Hc, Wc = F.shape
        _, _, Hs, Ws = G.shape

        F_ = F.view(B, C, -1).permute(0, 2, 1)       # (B, HWc, C)
        G_ = G.view(B, C, -1)                         # (B, C, HWs)
        H_ = H.view(B, C, -1)                         # (B, C, HWs)

        S  = self.sm(torch.bmm(F_, G_))               # (B, HWc, HWs)
        O  = torch.bmm(H_, S.permute(0, 2, 1))        # (B, C, HWc)
        O  = O.view(B, C, Hc, Wc)
        O  = self.out_conv(O)
        O  = O + content                              # residual
        return O


class SANetTransform(nn.Module):
    """
    Transform module đúng theo paper:
      - sanet4_1 xử lý relu4_1 features
      - sanet5_1 xử lý relu5_1 features
      - upsample5_1 × 2 để align với relu4_1 spatial size
      - merge_conv(3×3) kết hợp 2 nhánh
    """
    def __init__(self, in_planes: int = 512):
        super().__init__()
        self.sanet4_1     = SANetModule(in_planes)
        self.sanet5_1     = SANetModule(in_planes)
        self.upsample5_1  = nn.Upsample(scale_factor=2, mode='nearest')
        self.merge_conv   = nn.Conv2d(in_planes, in_planes, (3, 3), padding=1, padding_mode='reflect')
        nn.init.dirac_(self.merge_conv.weight)
        nn.init.zeros_(self.merge_conv.bias)

    def forward(
        self,
        content4_1: torch.Tensor, style4_1: torch.Tensor,
        content5_1: torch.Tensor, style5_1: torch.Tensor,
    ) -> torch.Tensor:
        t4 = self.sanet4_1(content4_1, style4_1)
        t5 = self.upsample5_1(self.sanet5_1(content5_1, style5_1))
        return self.merge_conv(t4 + t5)


# ─────────────────────────────────────────────────────────────────────────────
# End-to-end inference
# ─────────────────────────────────────────────────────────────────────────────

SANET_WEIGHTS_DIR = Path(__file__).parent / "weights" / "sanet"


def _build_sanet_decoder() -> nn.Sequential:
    """SANet decoder architecture (cùng topology với AdaIN decoder)."""
    return nn.Sequential(
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,256,(3,3)), nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,128,(3,3)), nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(128,128,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(128,64,(3,3)), nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(64,64,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(64,3,(3,3)),
    )


def run_sanet(
    content_path: str | Path,
    style_path:   str | Path,
    img_size:     int   = 512,
    temperature:  float = 1.0,
    style_blend:  float = 1.0,
    device:       Optional[torch.device] = None,
    weights_dir:  Optional[Path] = None,
    transform_weights: Optional[Path] = None,
) -> BenchmarkResult:
    """
    SANet style transfer đúng paper (Park et al., CVPR 2019).

    Ưu tiên weights từ weights/sanet/ (Yandex.Disk):
      - vgg_normalised.pth
      - transformer_iter_500000.pth  (SANet attention conv)
      - decoder_iter_500000.pth      (SANet decoder)

    Nếu không có SANet weights → fallback single-level + AdaIN decoder.
    """
    if device is None:
        device = get_optimal_device()

    # ── Tìm weights ─────────────────────────────────────────────────────────
    sanet_dir = SANET_WEIGHTS_DIR
    sanet_vgg  = sanet_dir / "vgg_normalised.pth"
    sanet_tr   = transform_weights or (sanet_dir / "transformer_iter_500000.pth")
    sanet_dec  = sanet_dir / "decoder_iter_500000.pth"

    has_sanet = sanet_vgg.exists() and Path(sanet_tr).exists() and sanet_dec.exists()

    if has_sanet:
        # ── Dual-level, trained SANet weights (paper-exact) ─────────────────
        vgg_state = torch.load(sanet_vgg, map_location="cpu", weights_only=False)
        enc4, enc5 = _build_vgg_stages(vgg_state)
        enc4 = enc4.to(device).eval()
        enc5 = enc5.to(device).eval()

        transform = SANetTransform(512).to(device).eval()
        tr_state = torch.load(sanet_tr, map_location="cpu", weights_only=False)
        transform.load_state_dict(tr_state)

        decoder = _build_sanet_decoder()
        dec_state = torch.load(sanet_dec, map_location="cpu", weights_only=False)
        decoder.load_state_dict(dec_state)
        decoder = decoder.to(device).eval()

        mode_label = "dual-lvl TRAINED"
    else:
        # ── Fallback: single-level + AdaIN decoder ──────────────────────────
        adain_dir = weights_dir or WEIGHTS_DIR
        vgg_path  = adain_dir / "vgg_normalised.pth"
        dec_path  = adain_dir / "decoder.pth"
        if not vgg_path.exists() or not dec_path.exists():
            raise FileNotFoundError(
                "Không tìm thấy weights. Cần weights/sanet/ (Yandex) hoặc AdaIN weights."
            )
        vgg_state = torch.load(vgg_path, map_location="cpu", weights_only=True)
        enc4 = VGGEncoder(vgg_state).to(device).eval()
        enc5 = None
        transform = None
        sanet_mod = SANetModule(512).to(device).eval()
        decoder = _load_decoder(dec_path, device)
        mode_label = "single-lvl identity"

    # ── Load ảnh ─────────────────────────────────────────────────────────────
    tc = load_image_adain(content_path, img_size, device)
    ts = load_image_adain(style_path,   img_size, device)

    # ── Inference ─────────────────────────────────────────────────────────────
    sync_device(device)
    ram0 = get_memory_mb(device)
    t0   = time.perf_counter()

    with torch.no_grad():
        if has_sanet:
            c4 = enc4(tc); c5 = enc5(c4)
            s4 = enc4(ts); s5 = enc5(s4)
            t_out = transform(c4, s4, c5, s5)
        else:
            fc = enc4(tc)
            fs = enc4(ts)
            t_out = sanet_mod(fc, fs)

        if style_blend < 1.0:
            fc_ref = enc4(tc) if not has_sanet else c4
            t_out = style_blend * t_out + (1 - style_blend) * fc_ref

        output = decoder(t_out).clamp(0, 1)

    sync_device(device)
    elapsed_ms = (time.perf_counter() - t0) * 1e3
    peak_ram   = get_memory_mb(device) - ram0

    print(
        f"[SANet | {device.type.upper()}]  {mode_label}  "
        f"temp={temperature:.2f}  blend={style_blend:.2f}  "
        f"| {elapsed_ms:.1f} ms  | Peak RAM: {peak_ram:.0f} MB"
    )

    return BenchmarkResult(
        method_name        = f"SANet ({mode_label})",
        output_image       = tensor_to_pil_adain(output),
        inference_time_sec = elapsed_ms / 1000.0,
        time_per_step_ms   = elapsed_ms,
        peak_memory_mb     = peak_ram,
        total_steps        = 1,
        loss_history       = [],
        device_name        = f"({device.type.upper()})",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Visualization
# ─────────────────────────────────────────────────────────────────────────────

def plot_sanet_analysis(
    content_path: str | Path,
    style_path:   str | Path,
    result:       BenchmarkResult,
    save_path:    Optional[str | Path] = None,
    figsize:      Tuple[int, int] = (15, 5),
) -> None:
    """3-panel: content | style | SANet output."""
    content = Image.open(content_path).convert("RGB")
    style   = Image.open(style_path).convert("RGB")

    fig, axes = plt.subplots(1, 3, figsize=figsize)
    for ax, img, title in zip(
        axes,
        [content, style, result.output_image],
        ["Content", "Style",
         f"{result.method_name}\n"
         f"Time: {result.inference_time_sec * 1000:.1f} ms  (1 forward pass)\n"
         f"Peak RAM: {result.peak_memory_mb:.0f} MB"],
    ):
        ax.imshow(img); ax.set_title(title, fontsize=9, fontweight="bold"); ax.axis("off")

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_sanet_temperature_grid(
    content_path: str | Path,
    style_path:   str | Path,
    temperatures: List[float] = (0.25, 0.5, 1.0, 2.0, 4.0),
    img_size:     int   = 256,
    device:       Optional[torch.device] = None,
    save_path:    Optional[str | Path] = None,
) -> None:
    """Grid ở nhiều temperature để thấy ảnh hưởng lên độ sharp của attention."""
    if device is None:
        device = get_optimal_device()
    content = Image.open(content_path).convert("RGB")
    style   = Image.open(style_path).convert("RGB")

    n   = len(temperatures) + 2
    fig = plt.figure(figsize=(3.5 * n, 4))
    gs  = gridspec.GridSpec(1, n, wspace=0.04)

    def _show(ax, img, title):
        ax.imshow(img); ax.set_title(title, fontsize=9); ax.axis("off")

    _show(plt.subplot(gs[0]), content, "Content")
    for i, temp in enumerate(temperatures):
        res = run_sanet(content_path, style_path, img_size=img_size,
                        temperature=temp, device=device)
        _show(plt.subplot(gs[i + 1]), res.output_image,
              f"temp={temp:.2f}\n{res.inference_time_sec*1000:.0f} ms")
    _show(plt.subplot(gs[-1]), style, "Style")

    fig.suptitle(
        "SANet — Dual-level attention (relu4_1 + relu5_1) + residual\n"
        "Thay đổi temperature: thấp → sharp (focus 1 patch), cao → đều (≈ AdaIN global)",
        fontsize=10, fontweight="bold",
    )
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()

"""
SCSA — Semantic · Continuous · Sparse · Attention
(tên đầy đủ: Semantic-Continuous-Sparse-Attention for Style Transfer)

Ba khối chính:
  SCA  (Semantic Continuous Attention)
        Query = bản đồ nhãn ngữ nghĩa (phẳng, không có chi tiết nét cọ)
        → mỗi vùng content nhận TRUNG BÌNH style của vùng cùng nhãn
        → cho "tông màu liên tục", không loang lổ sang vùng khác
        Cái giá: phẳng, mất nét cọ.

  S-AdaIN (Semantic AdaIN — per-region)
        Chuẩn hoá tông ảnh content RIÊNG TỪNG VÙNG theo style cùng nhãn.
        Mục đích: làm câu hỏi cho SSA đồng thang màu với style trước khi so sánh.

  SSA  (Semantic Sparse Attention)
        Query = content features đã qua S-AdaIN (chi tiết cấu trúc)
        Mask = chỉ cho phép trong cùng vùng nhãn
        Top-1: chỉ giữ 1 điểm style giống nhất trong vùng → copy nguyên patch đó
        → giữ nguyên nét cọ, hết nhạt nhoà.

Công thức trộn:
        F_out = α₁·SCA + α₂·SSA + F_c
  trong đó α₁, α₂ và F_c (bố cục ảnh) kết hợp để cân bằng tông và nét.

Backbone: VGG-19 normalised encoder + AdaIN decoder (naoto0804 weights).
Semantic mask: K-Means trên không gian pixel (RGB tại độ phân giải feature map).
  → Paper gốc dùng K-Means trên VGG feature vectors (về nguyên lý giống nhau).
  → Phiên bản này dùng image pixels cho tốc độ (không cần sklearn lớn).

Không có tham số mới, không train, plug-and-play.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

from adain_nst import (
    BenchmarkResult, VGGEncoder, _load_decoder,
    load_image_adain, tensor_to_pil_adain,
    get_optimal_device, sync_device, get_memory_mb,
    WEIGHTS_DIR,
)

__all__ = [
    "load_sem_masks",
    "get_semantic_masks",
    "compute_sca",
    "compute_sadain",
    "compute_ssa",
    "run_scsa",
    "plot_scsa_analysis",
    "plot_scsa_semantic",
]


# ─────────────────────────────────────────────────────────────────────────────
# Load semantic masks từ ảnh PNG màu (do người dùng cung cấp)
# ─────────────────────────────────────────────────────────────────────────────

def load_sem_masks(
    content_sem_path: str | Path,
    style_sem_path:   str | Path,
    feat_size:        Optional[Tuple[int, int]] = None,
) -> Tuple[torch.Tensor, torch.Tensor, int]:
    """
    Đọc 2 ảnh PNG mask ngữ nghĩa (colour-coded, cùng bảng màu) →
    trả về (labels_c, labels_s, n_clusters).

    Mỗi màu unique trong ảnh = 1 class. Vì 2 mask dùng cùng màu,
    nhãn tự động khớp nhau (đỏ trong content = đỏ trong style = cùng vùng).

    Args:
      content_sem_path : đường dẫn PNG mask của content
      style_sem_path   : đường dẫn PNG mask của style
      feat_size        : (H, W) để resize về — thường là (feat_h, feat_w) của VGG
                         Nếu None, giữ nguyên kích thước ảnh.
    Returns:
      labels_c   : (H, W) torch.long — nhãn content
      labels_s   : (H, W) torch.long — nhãn style
      n_clusters : số vùng (số màu unique)
    """
    def _parse(path: str | Path) -> np.ndarray:
        img = np.array(Image.open(path).convert("RGB"))
        return img

    c_img = _parse(content_sem_path)
    s_img = _parse(style_sem_path)

    # Lấy tất cả màu unique từ cả 2 ảnh → bảng màu chung
    all_pixels = np.concatenate([
        c_img.reshape(-1, 3),
        s_img.reshape(-1, 3),
    ], axis=0)
    unique_colors = np.unique(all_pixels, axis=0)   # (K, 3)
    n_clusters = len(unique_colors)

    def _to_labels(img: np.ndarray) -> torch.Tensor:
        H, W, _ = img.shape
        flat    = img.reshape(-1, 3)                          # (N, 3)
        # Tìm index màu gần nhất trong bảng màu
        dists   = np.linalg.norm(
            flat[:, None].astype(np.int32) - unique_colors[None].astype(np.int32),
            axis=2,
        )                                                     # (N, K)
        labels  = dists.argmin(axis=1).reshape(H, W)
        return torch.tensor(labels, dtype=torch.long)

    lc = _to_labels(c_img)
    ls = _to_labels(s_img)

    if feat_size is not None:
        fh, fw = feat_size
        lc = torch.tensor(
            np.array(Image.fromarray(lc.numpy().astype(np.uint8)).resize(
                (fw, fh), Image.NEAREST)),
            dtype=torch.long,
        )
        ls = torch.tensor(
            np.array(Image.fromarray(ls.numpy().astype(np.uint8)).resize(
                (fw, fh), Image.NEAREST)),
            dtype=torch.long,
        )

    return lc, ls, n_clusters


# ─────────────────────────────────────────────────────────────────────────────
# Palette màu để hiển thị semantic regions
# ─────────────────────────────────────────────────────────────────────────────
_PALETTE = [
    (228,  26,  28),   # đỏ
    ( 55, 126, 184),   # xanh biển
    ( 77, 175,  74),   # xanh lá
    (152,  78, 163),   # tím
    (255, 127,   0),   # cam
    (255, 255,  51),   # vàng
]


def _palette_rgb(k: int) -> Tuple[float, float, float]:
    r, g, b = _PALETTE[k % len(_PALETTE)]
    return r / 255, g / 255, b / 255


# ─────────────────────────────────────────────────────────────────────────────
# Semantic Mask (K-Means)
# ─────────────────────────────────────────────────────────────────────────────

def _kmeans_pixels(pixels: np.ndarray, n_clusters: int, n_init: int = 10,
                   max_iter: int = 300, seed: int = 42) -> np.ndarray:
    """
    K-Means thuần NumPy (không cần sklearn).
    pixels : (N, D)  float32
    Returns: (N,)  int  label array
    """
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(pixels), n_clusters, replace=False)
    centroids = pixels[idx].astype(np.float32)

    labels = np.zeros(len(pixels), dtype=np.int64)
    for _ in range(max_iter):
        # Assignment
        dists  = np.linalg.norm(pixels[:, None] - centroids[None], axis=2)  # N × K
        new_lb = dists.argmin(axis=1)
        if np.array_equal(new_lb, labels):
            break
        labels = new_lb
        # Update centroids
        for k in range(n_clusters):
            mask = labels == k
            if mask.any():
                centroids[k] = pixels[mask].mean(axis=0)

    return labels, centroids


def get_semantic_masks(
    content_img:  Image.Image,
    style_img:    Image.Image,
    n_clusters:   int = 3,
    feat_size:    int = 64,          # độ phân giải K-Means (= feature map size)
    seed:         int = 42,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Phân vùng ngữ nghĩa cho cả ảnh content và style.
    Dùng K-Means trên không gian RGB tại độ phân giải feat_size × feat_size.

    Trick: stack content + style → chạy K-Means một lần duy nhất
    → label mapping tự động khớp nhau (same centroid space).

    Returns:
      labels_c: (feat_size, feat_size)  int tensor — nhãn cho content
      labels_s: (feat_size, feat_size)  int tensor — nhãn cho style
    """
    # Resize về kích thước feature map để nhanh
    c_small = np.asarray(content_img.resize((feat_size, feat_size),
                                             Image.BILINEAR), dtype=np.float32) / 255.0
    s_small = np.asarray(style_img.resize((feat_size, feat_size),
                                           Image.BILINEAR), dtype=np.float32) / 255.0

    # Stack cả hai → (2 × N, 3) → K-Means chung → label nhất quán
    N   = feat_size * feat_size
    all_pixels = np.concatenate([c_small.reshape(N, 3),
                                  s_small.reshape(N, 3)], axis=0)
    labels, _ = _kmeans_pixels(all_pixels, n_clusters=n_clusters, seed=seed)

    lc = torch.tensor(labels[:N].reshape(feat_size, feat_size), dtype=torch.long)
    ls = torch.tensor(labels[N:].reshape(feat_size, feat_size), dtype=torch.long)
    return lc, ls


# ─────────────────────────────────────────────────────────────────────────────
# SCA — Semantic Continuous Attention
# ─────────────────────────────────────────────────────────────────────────────

def compute_sca(
    fc:         torch.Tensor,    # (B, C, H, W) content features
    fs:         torch.Tensor,    # (B, C, H, W) style   features
    labels_c:   torch.Tensor,    # (H, W) long — content semantic labels
    labels_s:   torch.Tensor,    # (H, W) long — style   semantic labels
    n_clusters: int,
) -> torch.Tensor:
    """
    SCA: mỗi vùng content r nhận TRUNG BÌNH style features của vùng r trong style.
    Không có nét cọ, nhưng đúng màu, không loang lổ.

    Với vùng không có tương ứng trong style: giữ nguyên content features.
    Returns: (B, C, H, W)
    """
    B, C, H, W = fc.shape
    N = H * W

    fc_flat = fc.view(B, C, N)
    fs_flat = fs.view(B, C, N)
    lc      = labels_c.view(N).to(fc.device)
    ls      = labels_s.view(N).to(fs.device)

    out = fc_flat.clone()

    for label in range(n_clusters):
        c_mask = lc == label                        # (N,) bool
        s_mask = ls == label

        if not c_mask.any():
            continue

        if not s_mask.any():
            # Không có vùng tương ứng trong style → giữ content
            continue

        # Mean style của vùng này → broadcast sang mọi content pixel cùng nhãn
        style_mean = fs_flat[:, :, s_mask].mean(dim=2, keepdim=True)  # (B, C, 1)
        out[:, :, c_mask] = style_mean.expand(B, C, c_mask.sum())

    return out.view(B, C, H, W)


# ─────────────────────────────────────────────────────────────────────────────
# S-AdaIN — Semantic per-region AdaIN
# ─────────────────────────────────────────────────────────────────────────────

def compute_sadain(
    fc:         torch.Tensor,
    fs:         torch.Tensor,
    labels_c:   torch.Tensor,
    labels_s:   torch.Tensor,
    n_clusters: int,
    eps:        float = 1e-5,
) -> torch.Tensor:
    """
    S-AdaIN: chuẩn hoá mỗi vùng content theo statistics của vùng style cùng nhãn.
    = AdaIN thông thường nhưng tính riêng cho từng region thay vì cả ảnh.

    Dùng để "đồng thang màu" content và style trước khi SSA so sánh.
    Returns: (B, C, H, W)
    """
    B, C, H, W = fc.shape
    N = H * W

    fc_flat = fc.view(B, C, N)
    fs_flat = fs.view(B, C, N)
    lc      = labels_c.view(N).to(fc.device)
    ls      = labels_s.view(N).to(fs.device)

    out = fc_flat.clone()

    for label in range(n_clusters):
        c_idx = (lc == label).nonzero(as_tuple=True)[0]   # content positions
        s_idx = (ls == label).nonzero(as_tuple=True)[0]   # style   positions

        if len(c_idx) == 0 or len(s_idx) == 0:
            continue

        fc_r = fc_flat[:, :, c_idx]          # (B, C, Nc)
        fs_r = fs_flat[:, :, s_idx]          # (B, C, Ns)

        # Normalise content region → apply style statistics
        cm = fc_r.mean(dim=2, keepdim=True)
        cs = fc_r.std (dim=2, keepdim=True).clamp_min(eps)
        sm = fs_r.mean(dim=2, keepdim=True).mean(dim=2, keepdim=True)    # scalar per channel
        ss = fs_r.std (dim=2, keepdim=True).clamp_min(eps).mean(dim=2, keepdim=True)

        out[:, :, c_idx] = ss * (fc_r - cm) / cs + sm

    return out.view(B, C, H, W)


# ─────────────────────────────────────────────────────────────────────────────
# SSA — Semantic Sparse Attention (top-1)
# ─────────────────────────────────────────────────────────────────────────────

def compute_ssa(
    fc_sad:     torch.Tensor,    # (B, C, H, W) content features sau S-AdaIN
    fs:         torch.Tensor,    # (B, C, H, W) style   features (gốc)
    labels_c:   torch.Tensor,    # (H, W)
    labels_s:   torch.Tensor,    # (H, W)
    n_clusters: int,
) -> torch.Tensor:
    """
    SSA: với mỗi điểm content, tìm 1 điểm style giống nhất TRONG CÙNG VÙNG nhãn.
    Copy nguyên style features của điểm đó → giữ nét cọ.
    "Sparse" vì chỉ giữ top-1 (sparse attention weight = 100%).

    Similarity: cosine similarity trên C chiều.
    Returns: (B, C, H, W) với mỗi pixel là copy của 1 style patch.
    """
    B, C, H, W = fc_sad.shape
    N = H * W

    q_flat = fc_sad.view(B, C, N)   # Query (content after S-AdaIN)
    v_flat = fs    .view(B, C, N)   # Value = Key (original style)
    lc     = labels_c.view(N).to(fc_sad.device)
    ls     = labels_s.view(N).to(fs    .device)

    out = q_flat.clone()             # fallback: giữ content nếu không có style

    for label in range(n_clusters):
        c_idx = (lc == label).nonzero(as_tuple=True)[0]
        s_idx = (ls == label).nonzero(as_tuple=True)[0]

        if len(c_idx) == 0 or len(s_idx) == 0:
            continue

        q  = q_flat[:, :, c_idx]           # (B, C, Nc)
        k  = v_flat[:, :, s_idx]           # (B, C, Ns)
        v  = v_flat[:, :, s_idx]           # same

        # Normalised cosine similarity
        q_n = F.normalize(q, dim=1)         # (B, C, Nc)
        k_n = F.normalize(k, dim=1)         # (B, C, Ns)

        scores = torch.bmm(q_n.permute(0, 2, 1), k_n)  # (B, Nc, Ns)
        best   = scores.argmax(dim=2)                    # (B, Nc)  — top-1 index into s_idx

        # Gather style features của top-1 match
        for b in range(B):
            out[b, :, c_idx] = v[b, :, best[b]]         # copy nguyên style patch

    return out.view(B, C, H, W)


# ─────────────────────────────────────────────────────────────────────────────
# Run SCSA end-to-end
# ─────────────────────────────────────────────────────────────────────────────

# SCSA dùng thẳng BenchmarkResult từ gatys_nst — thông tin extra đưa và method_name


def _local_adain(fc: torch.Tensor, fs: torch.Tensor,
                  c_masks: torch.Tensor, s_masks: torch.Tensor,
                  eps: float = 1e-5) -> torch.Tensor:
    """
    Local AdaIN đúng theo paper (function.py):
    Với mỗi semantic region, chuẩn hoá content theo statistics của style region.
    c_masks / s_masks: (K, H, W) binary float, K = số vùng.
    """
    B, C, H, W = fc.shape
    result = torch.zeros_like(fc)
    K = c_masks.shape[0]
    for i in range(K):
        cm = c_masks[i].to(fc.device)   # (H, W)
        sm = s_masks[i].to(fs.device)

        fc_r = fc * cm                  # mask out other regions
        fs_r = fs * sm

        c_num = cm.sum()
        s_num = sm.sum()
        if c_num < 1 or s_num < 1:
            continue

        # Per-region mean/std
        c_mean = fc_r.sum(dim=(-2, -1), keepdim=True) / c_num   # (B,C,1,1)
        s_mean = fs_r.sum(dim=(-2, -1), keepdim=True) / s_num

        c_var = (torch.pow(fc_r - c_mean, 2) * cm).sum(dim=(-2,-1), keepdim=True) / c_num
        s_var = (torch.pow(fs_r - s_mean, 2) * sm).sum(dim=(-2,-1), keepdim=True) / s_num

        c_std = (c_var + eps).sqrt()
        s_std = (s_var + eps).sqrt()

        normalized = (fc_r - c_mean) / c_std
        result = result + (normalized * s_std + s_mean) * cm
    return result


def _masks_from_labels(labels: torch.Tensor, K: int) -> torch.Tensor:
    """labels (H,W) → binary masks (K, H, W) float."""
    return torch.stack([(labels == k).float() for k in range(K)])


# ─────────────────────────────────────────────────────────────────────────────
# SCSA block — đúng theo scn-00/SCSA/SANet+SCSA/SCSA.py
# Dùng lại trained f, g, h, out_conv từ transformer_iter_500000.pth
# ─────────────────────────────────────────────────────────────────────────────

def _mvn(feat: torch.Tensor, eps: float = 1e-5) -> torch.Tensor:
    """Mean-Variance Normalisation trên feature map (B,C,H,W)."""
    B, C, H, W = feat.shape
    m = feat.view(B, C, -1).mean(dim=2, keepdim=True)
    s = feat.view(B, C, -1).std(dim=2, keepdim=True).clamp_min(eps)
    return ((feat.view(B, C, -1) - m) / s).view(B, C, H, W)


class SCSABlock(nn.Module):
    """
    SCSA attention block — thay thế SANet block bên trong Transform.
    Tham số f, g, h, out_conv load từ transformer_iter_500000.pth
    (cùng key prefix: sanet4_1.* / sanet5_1.*).

    SCA: Q = f(MVN(content_sem)), K = g(MVN(style_sem)), V = h(style)
    SSA: Q = f(MVN(content)),     K = g(MVN(style)),     V = h(style),  top-1 sparse
    forward: t1·SCA + t2·SSA + content   (content = S-AdaIN'd)
    """
    def __init__(self, in_planes: int):
        super().__init__()
        self.f       = nn.Conv2d(in_planes, in_planes, (1, 1))
        self.g       = nn.Conv2d(in_planes, in_planes, (1, 1))
        self.h       = nn.Conv2d(in_planes, in_planes, (1, 1))
        self.sm      = nn.Softmax(dim=-1)
        self.out_conv = nn.Conv2d(in_planes, in_planes, (1, 1))

    def _masked_attn(self, Q_feat, K_feat, V_feat, sem_map, sparse: bool):
        b, c, h, w = Q_feat.shape
        N = h * w
        F_ = self.f(_mvn(Q_feat)).view(b, -1, N).permute(0, 2, 1)  # (B, N, C)
        G_ = self.g(_mvn(K_feat)).view(b, -1, N)                    # (B, C, N)
        S  = torch.bmm(F_, G_)                                       # (B, N, N)

        _NEG = -torch.finfo(S.dtype).max
        # sem_map check by token count (giống official: F.size()[1]==4096 / 1024)
        if sem_map is not None:
            mask = sem_map.unsqueeze(0).expand(b, -1, -1)  # (B, N_c, N_s)
            S.masked_fill_(mask < 0.5, _NEG)

        if sparse:
            idx = S.argmax(dim=2, keepdim=True)
            B2  = torch.full_like(S, _NEG)
            B2.scatter_(2, idx, S.gather(2, idx))
            S = B2

        S = self.sm(S)                                               # (B, N_c, N_s)
        H = self.h(V_feat).view(b, -1, N)                           # (B, C, N_s)
        O = torch.bmm(H, S.permute(0, 2, 1)).view(b, c, h, w)
        return self.out_conv(O)

    def SCA(self, content, style, content_sem, style_sem, sem_map):
        return self._masked_attn(content_sem, style_sem, style, sem_map, sparse=False)

    def SSA(self, content, style, content_sem, style_sem, sem_map):
        return self._masked_attn(content,     style,     style, sem_map, sparse=True)

    def forward(self, content, style, content_sem, style_sem, sem_map, t1=0.7, t2=0.3):
        x_sca = self.SCA(content, style, content_sem, style_sem, sem_map)
        x_ssa = self.SSA(content, style, content_sem, style_sem, sem_map)
        return t1 * x_sca + t2 * x_ssa + content   # content = S-AdaIN'd residual


class SCSATransform(nn.Module):
    """Dual-level transform: sanet4_1 + upsample(sanet5_1) → merge_conv."""
    def __init__(self, in_planes: int = 512):
        super().__init__()
        self.sanet4_1       = SCSABlock(in_planes)
        self.sanet5_1       = SCSABlock(in_planes)
        self.upsample5_1    = nn.Upsample(scale_factor=2, mode='nearest')
        self.merge_conv_pad = nn.ReflectionPad2d((1, 1, 1, 1))
        self.merge_conv     = nn.Conv2d(in_planes, in_planes, (3, 3))

    def forward(self, c4, s4, c5, s5, c4_sem, s4_sem, c5_sem, s5_sem,
                map_32, map_64, t1=0.7, t2=0.3):
        o4 = self.sanet4_1(c4, s4, c4_sem, s4_sem, map_64, t1, t2)
        o5 = self.sanet5_1(c5, s5, c5_sem, s5_sem, map_32, t1, t2)
        return self.merge_conv(self.merge_conv_pad(o4 + self.upsample5_1(o5)))


def _build_vgg5_stages(vgg_state: dict):
    """
    Tách VGG thành 5 stages theo đúng SCSA.py:
      enc1 = layers[:4]      input   → relu1_1
      enc2 = layers[4:11]    relu1_1 → relu2_1
      enc3 = layers[11:18]   relu2_1 → relu3_1
      enc4 = layers[18:31]   relu3_1 → relu4_1
      enc5 = layers[31:44]   relu4_1 → relu5_1
    """
    vgg_full = nn.Sequential(
        nn.Conv2d(3, 3, (1,1)), nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(3, 64, (3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(64, 64, (3,3)), nn.ReLU(),
        nn.MaxPool2d((2,2),(2,2),(0,0),ceil_mode=True),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(64,128,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(128,128,(3,3)), nn.ReLU(),
        nn.MaxPool2d((2,2),(2,2),(0,0),ceil_mode=True),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(128,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.MaxPool2d((2,2),(2,2),(0,0),ceil_mode=True),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,512,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,512,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,512,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,512,(3,3)), nn.ReLU(),
        nn.MaxPool2d((2,2),(2,2),(0,0),ceil_mode=True),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,512,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,512,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,512,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,512,(3,3)), nn.ReLU(),
    )
    vgg_full.load_state_dict(vgg_state)
    kids = list(vgg_full.children())
    enc1 = nn.Sequential(*kids[:4])
    enc2 = nn.Sequential(*kids[4:11])
    enc3 = nn.Sequential(*kids[11:18])
    enc4 = nn.Sequential(*kids[18:31])
    enc5 = nn.Sequential(*kids[31:44])
    return enc1, enc2, enc3, enc4, enc5


def run_scsa(
    content_path:    str | Path,
    style_path:      str | Path,
    img_size:        int   = 512,
    n_clusters:      int   = 3,     # dùng khi không có sem masks
    alpha1:          float = 0.7,   # α₁: weight SCA (tông màu)
    alpha2:          float = 0.3,   # α₂: weight SSA (nét cọ)
    alpha_layout:    float = 1.0,   # weight F_c (bố cục ảnh)
    device:          Optional[torch.device] = None,
    weights_dir:     Optional[Path] = None,
    sem_content:     Optional[str | Path] = None,  # PNG mask ngữ nghĩa content
    sem_style:       Optional[str | Path] = None,  # PNG mask ngữ nghĩa style
    sem_map_64:      Optional[str | Path] = None,  # precomputed map 64×64 .pt
    sem_map_32:      Optional[str | Path] = None,  # precomputed map 32×32 .pt
) -> BenchmarkResult:
    """
    SCSA đúng theo paper scn-00/SCSA/SANet+SCSA/SCSA.py:

    Pipeline (dual-level, dùng SANet weights):
      1. 5-stage VGG encode content, style, sem_content, sem_style
         → C4, C5, S4, S5, C4_sem, C5_sem, S4_sem, S5_sem
      2. S-AdaIN PER LEVEL trước khi vào Transform:
         C4_sadain = local_adain(C4, S4, binary_masks_64)
         C5_sadain = local_adain(C5, S5, binary_masks_32)
      3. SCSATransform(C4_sadain, S4, C5_sadain, S5, sem_feats, maps)
         bên trong mỗi SANet block:
           SCA:  Q=f(MVN(c_sem)), K=g(MVN(s_sem)), V=h(s), masked softmax
           SSA:  Q=f(MVN(c)),     K=g(MVN(s)),     V=h(s), top-1 masked
           out = t1·SCA + t2·SSA + content(S-AdaIN'd)   ← residual là S-AdaIN'd
         merge_conv(sanet4_1(…) + upsample(sanet5_1(…)))
      4. Decode với SANet decoder
    """
    if device is None:
        device = get_optimal_device()

    # ── Load SANet weights (VGG + transformer + decoder) ─────────────────────
    _SANET_DIR = Path(__file__).parent / "weights" / "sanet"
    _vgg_path  = _SANET_DIR / "vgg_normalised.pth"
    _tr_path   = _SANET_DIR / "transformer_iter_500000.pth"
    _dec_path  = _SANET_DIR / "decoder_iter_500000.pth"
    for p in [_vgg_path, _tr_path, _dec_path]:
        if not p.exists():
            raise FileNotFoundError(f"Thiếu file: {p}. Cần weights/sanet/ đủ 3 file.")

    vgg_state = torch.load(_vgg_path, map_location="cpu", weights_only=False)
    tr_state  = torch.load(_tr_path,  map_location="cpu", weights_only=False)
    dec_state = torch.load(_dec_path, map_location="cpu", weights_only=False)

    # Build & load VGG 5-stage encoder
    enc1, enc2, enc3, enc4, enc5 = _build_vgg5_stages(vgg_state)
    for e in (enc1, enc2, enc3, enc4, enc5):
        e.to(device).eval()

    # Build & load SCSA Transform
    transform = SCSATransform(512)
    # Rename key merge_conv.* -> merge_conv.*  (đã đúng); thêm merge_conv_pad không có weights
    transform.load_state_dict(tr_state, strict=True)
    transform.to(device).eval()

    # Build & load SANet decoder
    decoder = nn.Sequential(
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(512,256,(3,3)), nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,256,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(256,128,(3,3)), nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(128,128,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d(128, 64,(3,3)), nn.ReLU(),
        nn.Upsample(scale_factor=2, mode='nearest'),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d( 64, 64,(3,3)), nn.ReLU(),
        nn.ReflectionPad2d((1,1,1,1)), nn.Conv2d( 64,  3,(3,3)),
    )
    decoder.load_state_dict(dec_state)
    decoder.to(device).eval()

    # ── Load & transform ảnh ─────────────────────────────────────────────────
    tf = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
    ])
    def _to_tensor(path):
        return tf(Image.open(path).convert("RGB")).unsqueeze(0).to(device)

    tc     = _to_tensor(content_path)
    ts     = _to_tensor(style_path)

    # Semantic masks
    has_ext_sem  = bool(sem_content and sem_style and
                        Path(sem_content).exists() and Path(sem_style).exists())
    has_sem_maps = bool(sem_map_64 and sem_map_32 and
                        Path(sem_map_64).exists() and Path(sem_map_32).exists())

    if has_ext_sem:
        tc_sem = _to_tensor(sem_content)
        ts_sem = _to_tensor(sem_style)
        sem_source = "external PNG+VGGenc"
    else:
        tc_sem = tc   # fallback: dùng chính content làm sem
        ts_sem = ts
        sem_source = "content/style feat (no sem)"

    # ── Encode ───────────────────────────────────────────────────────────────
    sync_device(device)
    ram0 = get_memory_mb(device)
    t0   = time.perf_counter()

    content_pil = Image.open(content_path).convert("RGB")
    style_pil   = Image.open(style_path).convert("RGB")

    with torch.no_grad():
        def _enc4(x): return enc4(enc3(enc2(enc1(x))))
        def _enc5(x): return enc5(_enc4(x))

        C4 = _enc4(tc);  C5 = enc5(C4)
        S4 = _enc4(ts);  S5 = enc5(S4)
        C4_sem = _enc4(tc_sem);  C5_sem = enc5(C4_sem)
        S4_sem = _enc4(ts_sem);  S5_sem = enc5(S4_sem)

        h4, w4 = C4.shape[2], C4.shape[3]   # 64×64 cho 512 input
        h5, w5 = C5.shape[2], C5.shape[3]   # 32×32

        # ── Semantic labels & binary masks ───────────────────────────────────
        if has_ext_sem:
            labels_c, labels_s, n_clusters = load_sem_masks(
                sem_content, sem_style, feat_size=(h4, w4),
            )
        else:
            labels_c, labels_s = get_semantic_masks(
                content_pil, style_pil,
                n_clusters=n_clusters,
                feat_size=max(h4, w4),
            )

        # Đảm bảo labels có đúng kích thước h4×w4
        def _resize_labels(lab, H, W):
            if lab.shape == (H, W):
                return lab
            return F.interpolate(
                lab.float().unsqueeze(0).unsqueeze(0),
                size=(H, W), mode="nearest"
            ).long().squeeze()

        lc4 = _resize_labels(labels_c, h4, w4)
        ls4 = _resize_labels(labels_s, h4, w4)
        lc5 = _resize_labels(labels_c, h5, w5)
        ls5 = _resize_labels(labels_s, h5, w5)

        masks_c4 = _masks_from_labels(lc4, n_clusters)  # (K, 64, 64)
        masks_s4 = _masks_from_labels(ls4, n_clusters)
        masks_c5 = _masks_from_labels(lc5, n_clusters)  # (K, 32, 32)
        masks_s5 = _masks_from_labels(ls5, n_clusters)

        # ── Precomputed sem maps (N×N binary) ────────────────────────────────
        if has_sem_maps:
            map_64 = torch.load(str(sem_map_64), map_location=device, weights_only=True)
            map_32 = torch.load(str(sem_map_32), map_location=device, weights_only=True)
        else:
            # on-the-fly
            def _make_map(lc, ls):
                lc_f = lc.view(-1); ls_f = ls.view(-1)
                return (lc_f[:, None] == ls_f[None, :]).float().to(device)
            map_64 = _make_map(lc4, ls4)
            map_32 = _make_map(lc5, ls5)

        # ── Bước 1: S-AdaIN tại cả 2 level (trước Transform) ─────────────────
        C4_sad = _local_adain(C4, S4, masks_c4, masks_s4)  # (1,512,64,64)
        C5_sad = _local_adain(C5, S5, masks_c5, masks_s5)  # (1,512,32,32)

        # ── Bước 2: SCSA Transform (dual-level + merge_conv) ─────────────────
        f_merged = transform(
            C4_sad, S4, C5_sad, S5,
            C4_sem, S4_sem, C5_sem, S5_sem,
            map_32, map_64,
            alpha1, alpha2,
        )

        # ── Bước 3: Decode ───────────────────────────────────────────────────
        output = decoder(f_merged).clamp(0, 1)

    sync_device(device)
    elapsed_ms = (time.perf_counter() - t0) * 1e3
    peak_ram   = get_memory_mb(device) - ram0

    out_pil = tensor_to_pil_adain(output)

    label = (
        f"[SCSA | {str(device.type).upper()}]  "
        f"K={n_clusters}  α₁={alpha1:.2f}  α₂={alpha2:.2f}  "
        f"sem={sem_source}  "
        f"| {elapsed_ms:.1f} ms  | Peak RAM: {peak_ram:.0f} MB"
    )
    print(label)

    result = BenchmarkResult(
        method_name        = f"SCSA (K={n_clusters} α₁={alpha1:.2f} α₂={alpha2:.2f} | SANet+SCSA)",
        output_image       = out_pil,
        inference_time_sec = elapsed_ms / 1000.0,
        time_per_step_ms   = elapsed_ms,
        peak_memory_mb     = peak_ram,
        total_steps        = 1,
        loss_history       = [],
        device_name        = f"({device.type.upper()})",
    )
    result._n_clusters = n_clusters
    result._alpha1     = alpha1
    result._alpha2     = alpha2
    result._labels_c   = labels_c
    result._labels_s   = labels_s
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Visualization
# ─────────────────────────────────────────────────────────────────────────────

def plot_scsa_semantic(
    content_path: str | Path,
    style_path:   str | Path,
    n_clusters:   int = 3,
    feat_size:    int = 64,
    save_path:    Optional[str | Path] = None,
    figsize:      Tuple[int, int] = (12, 5),
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Hiển thị ảnh gốc và bản đồ vùng ngữ nghĩa (colour-coded).
    Returns: (labels_c, labels_s) để dùng lại.
    """
    content = Image.open(content_path).convert("RGB")
    style   = Image.open(style_path).convert("RGB")

    labels_c, labels_s = get_semantic_masks(content, style,
                                             n_clusters=n_clusters,
                                             feat_size=feat_size)
    K = n_clusters

    def _overlay(img: Image.Image, labels: torch.Tensor, alpha: float = 0.5):
        """Phủ colour-coded mask lên ảnh."""
        H, W = labels.shape
        mask_rgb = np.zeros((H, W, 3), dtype=np.float32)
        for k in range(K):
            r, g, b = _palette_rgb(k)
            mask_rgb[labels.numpy() == k] = [r, g, b]
        img_small = np.asarray(img.resize((W, H)), dtype=np.float32) / 255.0
        blended   = (1 - alpha) * img_small + alpha * mask_rgb
        return blended.clip(0, 1)

    legend = [Patch(facecolor=_palette_rgb(k), label=f"Vùng {k}") for k in range(K)]

    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes[0, 0].imshow(content);                 axes[0, 0].set_title("Content",      fontweight="bold")
    axes[0, 1].imshow(style);                   axes[0, 1].set_title("Style",        fontweight="bold")
    axes[1, 0].imshow(_overlay(content, labels_c)); axes[1, 0].set_title(f"Content mask (K={K})", fontweight="bold")
    axes[1, 1].imshow(_overlay(style,   labels_s)); axes[1, 1].set_title(f"Style mask (K={K})",   fontweight="bold")
    for ax in axes.flat:
        ax.axis("off")

    fig.legend(handles=legend, loc="lower center", ncol=K, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(
        "Phân vùng ngữ nghĩa — K-Means trên RGB pixel (chạy chung để nhãn tương ứng)",
        fontsize=11, fontweight="bold",
    )
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
    return labels_c, labels_s


def plot_scsa_analysis(
    content_path: str | Path,
    style_path:   str | Path,
    result:       BenchmarkResult,
    save_path:    Optional[str | Path] = None,
    figsize:      Tuple[int, int] = (15, 5),
) -> None:
    """3-panel: content | style | SCSA output với thông tin chi tiết."""
    content = Image.open(content_path).convert("RGB")
    style   = Image.open(style_path).convert("RGB")
    output  = result.output_image

    fig, axes = plt.subplots(1, 3, figsize=figsize)
    for ax, img, title in zip(
        axes,
        [content, style, output],
        ["Content", "Style", "SCSA"],
    ):
        ax.imshow(img)
        ax.set_title(title, fontweight="bold")
        ax.axis("off")

    a1  = getattr(result, '_alpha1', '?')
    a2  = getattr(result, '_alpha2', '?')
    K   = getattr(result, '_n_clusters', '?')
    axes[2].set_title(
        f"SCSA  (α₁={a1}·SCA + α₂={a2}·SSA + F_c)\n"
        f"K={K} vùng  |  {result.inference_time_sec * 1000:.1f} ms  (1 pass)\n"
        f"Peak RAM: {result.peak_memory_mb:.0f} MB",
        fontsize=9, fontweight="bold",
    )

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_scsa_alpha_grid(
    content_path: str | Path,
    style_path:   str | Path,
    alpha_pairs:  List[Tuple[float, float]] = (
        (0.0, 0.0),    # chỉ F_c (không style)
        (1.0, 0.0),    # chỉ SCA
        (0.0, 1.0),    # chỉ SSA
        (0.7, 0.3),    # blend mặc định
        (0.5, 0.5),    # balanced
    ),
    n_clusters:   int = 3,
    img_size:     int = 256,
    device:       Optional[torch.device] = None,
    save_path:    Optional[str | Path] = None,
    sem_content:  Optional[str | Path] = None,   # PNG mask ngữ nghĩa content
    sem_style:    Optional[str | Path] = None,   # PNG mask ngữ nghĩa style
    sem_map_64:   Optional[str | Path] = None,   # precomputed map 64×64 .pt
    sem_map_32:   Optional[str | Path] = None,   # precomputed map 32×32 .pt
) -> None:
    """
    Grid kết quả ở nhiều cặp (α₁, α₂).
    Hiển thị vai trò riêng của SCA và SSA, và blend tối ưu.
    Nếu có sem_content + sem_style, dùng external mask thay K-Means.
    """
    if device is None:
        device = get_optimal_device()

    content = Image.open(content_path).convert("RGB")
    style   = Image.open(style_path).convert("RGB")

    n   = len(alpha_pairs) + 2
    fig = plt.figure(figsize=(3.2 * n, 4.2))
    gs  = gridspec.GridSpec(1, n, wspace=0.04)

    def _show(ax, img, title):
        ax.imshow(img); ax.set_title(title, fontsize=8, pad=3); ax.axis("off")

    _show(plt.subplot(gs[0]), content, "Content")
    for i, (a1, a2) in enumerate(alpha_pairs):
        res = run_scsa(content_path, style_path, img_size=img_size,
                       n_clusters=n_clusters, alpha1=a1, alpha2=a2,
                       device=device,
                       sem_content=sem_content, sem_style=sem_style,
                       sem_map_64=sem_map_64, sem_map_32=sem_map_32)
        label = (
            f"α₁={a1:.1f}·SCA\n+ α₂={a2:.1f}·SSA\n+ F_c"
            if a1 > 0 and a2 > 0
            else (f"SCA only\nα₁={a1:.1f}" if a1 > 0
                  else (f"SSA only\nα₂={a2:.1f}" if a2 > 0
                        else "F_c only\n(no style)"))
        )
        _show(plt.subplot(gs[i + 1]), res.output_image, label)
    _show(plt.subplot(gs[-1]), style, "Style")

    fig.suptitle(
        f"SCSA — Vai trò riêng của SCA (tông), SSA (nét cọ) và kết hợp  [K={n_clusters}]",
        fontsize=10, fontweight="bold",
    )
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()

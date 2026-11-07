"""
StyTr2 (Deng et al., CVPR 2022) và StyTr2 + SCSA (Shen et al., CVPR 2025).

Mô hình là mã của tác giả SCSA, chép vào third_party/stytr2_scsa/ (xem README trong đó).
File này chỉ nạp trọng số, chuẩn bị mặt nạ vùng và đo thời gian, giống các file *_nst.py khác.

Tham số StyTr2 + SCSA theo SCSA.py của tác giả: α₁ (t1) = 1.2, α₂ (t2) = 0.5, b = 0.7;
SCSA thay attention ảnh–tranh ở các lớp chẵn của transformer decoder.
Trọng số StyTr2: weights/stytr2/ (vgg_normalised, decoder/transformer/embedding_iter_160000).
"""
from __future__ import annotations

import sys
import time
from argparse import Namespace
from collections import OrderedDict
from pathlib import Path
from typing import Optional

import numpy as np
import torch
import torch.nn as nn
from PIL import Image

from gatys_nst import BenchmarkResult, get_optimal_device, sync_device, get_memory_mb

ROOT = Path(__file__).resolve().parent
CODE = ROOT / "third_party" / "stytr2_scsa"
WEIGHTS = ROOT / "weights" / "stytr2"
MASKS = ROOT / "sem_precomputed_feats"


def _import():
    if str(CODE) not in sys.path:
        sys.path.insert(0, str(CODE))
    import models.StyTR as StyTR
    import models.transformer as tr_scsa
    import models.transformer_StyTr2 as tr_plain
    import other
    return StyTR, tr_scsa, tr_plain, other


def _load_sd(path):
    return OrderedDict(torch.load(path, map_location="cpu", weights_only=True).items())


def _build(scsa: bool, args, device):
    StyTR, tr_scsa, tr_plain, _ = _import()
    vgg = StyTR.vgg
    vgg.load_state_dict(_load_sd(WEIGHTS / "vgg_normalised.pth"))
    vgg = nn.Sequential(*list(vgg.children())[:44])
    decoder = StyTR.decoder
    decoder.load_state_dict(_load_sd(WEIGHTS / "decoder_iter_160000.pth"))
    trans = (tr_scsa if scsa else tr_plain).Transformer()
    trans.load_state_dict(_load_sd(WEIGHTS / "transformer_iter_160000.pth"))
    emb = StyTR.PatchEmbed()
    emb.load_state_dict(_load_sd(WEIGHTS / "embedding_iter_160000.pth"))
    cls = StyTR.StyTrans if scsa else StyTR.StyTrans_StyTr2
    return cls(vgg, decoder, emb, trans, args).eval().to(device)


def _img(path, device):
    im = Image.open(path).convert("RGB").resize((512, 512), Image.BILINEAR)
    return torch.from_numpy(np.asarray(im).astype(np.float32) / 255).permute(2, 0, 1)[None].to(device)


def _write_masks(content_path, style_path, content_sem, style_sem):
    """Mặt nạ từng vùng (n_vùng, h, w) như sem.py của SCSA, đặt theo tên file mà other.local_adain tìm."""
    from styleid_nst import _label_maps
    labels, n = _label_maps(content_sem, style_sem, sizes=(32, 64))
    for path, side in ((content_path, 0), (style_path, 1)):
        stem = Path(path).stem
        d = MASKS / stem.split("_")[0]
        d.mkdir(parents=True, exist_ok=True)
        for size in (32, 64):
            lab = labels[size][side]
            m = torch.from_numpy(np.stack([(lab == i).astype(np.float32) for i in range(n)]))
            torch.save(m, d / f"{stem}_masks_{size}.pt")


def _run(scsa, content_path, style_path, device, **kw):
    device = device or get_optimal_device()
    try:
        return _run_on(scsa, content_path, style_path, device, dict(kw))
    except RuntimeError as e:
        if device.type == "cpu":
            raise
        # MPS chưa hỗ trợ adaptive_avg_pool2d với kích thước không chia hết (dùng trong StyTr2) → chạy CPU
        print(f"[{'StyTr2 + SCSA' if scsa else 'StyTr2'}] {device.type.upper()} lỗi ({str(e).splitlines()[0][:60]}…) → chạy CPU")
        return _run_on(scsa, content_path, style_path, torch.device("cpu"), dict(kw))


def _run_on(scsa, content_path, style_path, device, kw):
    sem_imgs = (kw.pop("content_sem_img", None), kw.pop("style_sem_img", None))
    args = Namespace(content=str(content_path), style=str(style_path), hidden_dim=512, position_embedding="sine", **kw)
    if scsa:
        _, _, _, other = _import()
        other.MASK_ROOT = str(MASKS) + "/"
        _write_masks(content_path, style_path, *sem_imgs)
    net = _build(scsa, args, device)
    c, s = _img(content_path, device), _img(style_path, device)
    inputs = (c, s)
    if scsa:
        inputs += (_img(args.content_sem, device), _img(args.style_sem, device))

    sync_device(device)
    ram0 = get_memory_mb(device)
    t0 = time.perf_counter()
    with torch.no_grad():
        out = net(*inputs)
    sync_device(device)
    elapsed = time.perf_counter() - t0
    peak = get_memory_mb(device) - ram0

    arr = (out[0].clamp(0, 1).permute(1, 2, 0).cpu().numpy() * 255).round().astype(np.uint8)
    name = "StyTr2 + SCSA" if scsa else "StyTr2"
    print(f"[{name} | {device.type.upper()}]  một lượt qua mạng  | {elapsed * 1e3:.1f} ms | Peak RAM: {peak:.0f} MB")
    return BenchmarkResult(
        method_name=name, output_image=Image.fromarray(arr), inference_time_sec=elapsed,
        time_per_step_ms=elapsed * 1e3, peak_memory_mb=peak, total_steps=1, loss_history=[],
        device_name=f"({device.type.upper()})",
    )


def run_stytr2(content_path, style_path, device: Optional[torch.device] = None) -> BenchmarkResult:
    return _run(False, content_path, style_path, device)


def run_stytr2_scsa(content_path, style_path, content_sem, style_sem, sem_map_64, sem_map_32,
                    t1=1.2, t2=0.5, b=0.7, device: Optional[torch.device] = None) -> BenchmarkResult:
    return _run(True, content_path, style_path, device,
                content_sem=str(content_sem), style_sem=str(style_sem),
                content_sem_img=str(content_sem), style_sem_img=str(style_sem),
                sem_map_64=str(sem_map_64), sem_map_32=str(sem_map_32), t1=t1, t2=t2, b=b)


if __name__ == "__main__":
    r = run_stytr2("img/yosemite.jpg", "img/yosemite_paint.jpg")
    r.output_image.save("img/yosemite_out_stytr2.jpg", quality=95)
    r = run_stytr2_scsa("img/yosemite.jpg", "img/yosemite_paint.jpg", "img/yosemite_sem.png", "img/yosemite_paint_sem.png",
                        "sem_precomputed_feats/yosemite/yosemite_yosemite_paint_map_64.pt",
                        "sem_precomputed_feats/yosemite/yosemite_yosemite_paint_map_32.pt")
    r.output_image.save("img/yosemite_out_stytr2_scsa.jpg", quality=95)

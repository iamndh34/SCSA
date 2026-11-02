"""
Precompute semantic attention maps đúng theo paper SCSA (scn-00/SCSA).

Đọc 2 PNG mask (cùng bảng màu) → tính binary map (N_c × N_s):
  map[i, j] = 1  nếu content pixel i và style pixel j cùng semantic region
  map[i, j] = 0  nếu khác vùng

Lưu: sem_precomputed_feats/<name>/
  <c>_<s>_map_64.pt    (64×64 → 4096×4096)
  <c>_<s>_map_32.pt    (32×32 → 1024×1024)

Usage:
  python precompute_sem_maps.py \\
      --content_sem img/yosemite_sem.png \\
      --style_sem   img/yosemite_paint_sem.png \\
      --out_dir     sem_precomputed_feats/yosemite
"""
from __future__ import annotations
import argparse, os
from pathlib import Path

import cv2
import numpy as np
import torch
from sklearn.cluster import KMeans


# ── Màu chuẩn của paper (từ sem.py) ──────────────────────────────────────────
_RED    = [0,   0,   230]
_CYAN   = [230, 230, 0  ]
_PINK   = [230, 0,   230]
_BLUE   = [230, 0,   0  ]
_GREEN  = [0,   230, 0  ]
_YELLOW = [0,   230, 230]


def _read_and_label(mask_path: str | Path, size: int,
                    label_colors: np.ndarray,
                    kmeans: KMeans) -> tuple[np.ndarray, np.ndarray]:
    """Đọc mask PNG → resize → predict label với KMeans đã fit."""
    img = cv2.imread(str(mask_path))          # BGR
    img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_NEAREST)
    img = cv2.resize(img, (size, size),  interpolation=cv2.INTER_NEAREST)
    flat = img.reshape(-1, 3).astype(np.float64)   # (N, 3)
    labels = kmeans.predict(flat)                  # (N,)
    label_map = labels.reshape(size, size)
    return labels, label_map


def compute_sem_maps(
    content_sem_path: str | Path,
    style_sem_path:   str | Path,
    out_dir:          str | Path,
    sizes:            list[int] = (32, 64),
) -> dict[int, torch.Tensor]:
    """
    Trả về dict: {32: map_32_tensor, 64: map_64_tensor}
    map shape: (1, N_c, N_s)  với N = size×size
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    c_name = Path(content_sem_path).stem.replace("_sem", "")
    s_name = Path(style_sem_path).stem.replace("_sem", "")

    # Lấy màu unique từ cả 2 mask (BGR) → dùng làm cluster centers
    c_img = cv2.imread(str(content_sem_path))
    s_img = cv2.imread(str(style_sem_path))
    all_px = np.concatenate([
        c_img.reshape(-1, 3).astype(np.float64),
        s_img.reshape(-1, 3).astype(np.float64),
    ])
    unique = np.unique(all_px, axis=0)         # (K, 3)
    n_clusters = len(unique)
    print(f"  Số vùng: {n_clusters}  (từ {unique.shape[0]} unique colors)")

    # KMeans fit trên bảng màu chuẩn (giữ label consistent)
    km = KMeans(n_clusters=n_clusters, n_init=10, random_state=0)
    km.fit(unique)

    result = {}
    for size in sizes:
        c_flat, _ = _read_and_label(content_sem_path, size, unique, km)
        s_flat, _ = _read_and_label(style_sem_path,   size, unique, km)

        N_c = size * size
        N_s = size * size

        # Binary map: (N_c, N_s)
        map_mat = (c_flat[:, None] == s_flat[None, :]).astype(np.float32)
        t = torch.from_numpy(map_mat)          # (N_c, N_s)

        fname = out_dir / f"{c_name}_{s_name}_map_{size}.pt"
        torch.save(t, fname)
        print(f"  Saved {fname}  shape={tuple(t.shape)}")
        result[size] = t

    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content_sem", default="img/yosemite_sem.png")
    ap.add_argument("--style_sem",   default="img/yosemite_paint_sem.png")
    ap.add_argument("--out_dir",     default="sem_precomputed_feats/yosemite")
    ap.add_argument("--sizes",       default="32,64")
    args = ap.parse_args()

    sizes = [int(s) for s in args.sizes.split(",")]
    compute_sem_maps(args.content_sem, args.style_sem,
                     args.out_dir, sizes=sizes)
    print("Done.")


if __name__ == "__main__":
    main()

# StyTr2 + SCSA (mã của tác giả)

Chép từ github.com/scn-00/SCSA, thư mục `StyTr2+SCSA/` (commit 0d004dc, 2025-04-11), chỉ phần mô hình:
`function.py`, `other.py`, `MultiAttention.py`, `models/`, `util/`. Repo gốc không kèm file LICENSE;
dùng cho mục đích học tập (seminar). StyTr2 gốc: github.com/diyiiyiii/StyTR-2.

Hai chỗ vá, đánh dấu `[SCSA-seminar patch]`:
- `other.py`: `local_adain` đọc mặt nạ vùng từ `MASK_ROOT` (do `stytr2_nst.py` đặt) thay vì đường dẫn cố định trên máy tác giả.
- `models/transformer.py`: `local_adain` chạy trên thiết bị của tensor thay vì `cuda:2` cố định.

Cách dùng: `stytr2_nst.py` ở thư mục gốc dự án (`run_stytr2`, `run_stytr2_scsa`).
Trọng số StyTr2 (vgg, decoder, transformer, embedding) đặt trong `weights/stytr2/`.

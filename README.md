# SCSA — Tài liệu seminar & bộ slide

Tài liệu nghiên cứu, đề xuất đề tài và bộ slide trình bày cho bài báo:

> **SCSA: A Plug-and-Play Semantic Continuous-Sparse Attention for Arbitrary Semantic Style Transfer** (CVPR 2025, Highlight)
> Chunnan Shang, Hongwei Wang, Zhizhong Wang, Xiangming Meng — Zhejiang University
> Paper: https://arxiv.org/abs/2503.04119 · Code gốc: https://github.com/scn-00/SCSA

**Tóm tắt một câu:** SCSA thay khối Universal Attention trong các mô hình style transfer dựa trên attention (SANet, StyTr2, StyleID) bằng hai attention có ràng buộc ngữ nghĩa (SCA + SSA), không cần huấn luyện lại, để mỗi vùng của ảnh kết quả chỉ lấy style từ vùng cùng nhãn trong tranh.

## Nội dung repo

| File / thư mục | Nội dung |
| --- | --- |
| [`01_Seminar_Outline_SCSA.md`](01_Seminar_Outline_SCSA.md) | Dàn ý seminar (~90 phút): kiến thức nền, ba lỗi của Universal Attention, phương pháp SCA / S-AdaIN / SSA, thực nghiệm, phân tích phản biện, lộ trình đọc code |
| [`02_Proposal_SCSA.md`](02_Proposal_SCSA.md) | Research proposal **Auto-SCSA**: tương ứng ngữ nghĩa tự động, attention theo vùng hiệu quả, benchmark MS-COCO × WikiArt, kế hoạch 16 tuần |
| [`03_Script_Trinh_Bay_SCSA.md`](03_Script_Trinh_Bay_SCSA.md) | Lời thoại theo từng slide cho bộ slide bản 1 (33 slide, artifact trên claude.ai) |
| [`04_Script_HyperFrames_SCSA.md`](04_Script_HyperFrames_SCSA.md) | Lời thoại cho bộ slide bản 2 (HyperFrames, 36 slide) — số lần bấm, thời lượng, nguồn hình từng slide |
| [`slides_export/`](slides_export) | Bộ slide bản 2 đã xuất thành một file HTML chạy offline |
| [`scsa-deck/`](scsa-deck) | Mã nguồn bộ slide bản 2 (dự án HyperFrames) |

## Trình chiếu nhanh

Mở `slides_export/SCSA_trinh_chieu.html` bằng trình duyệt (bấm đúp là được, không cần mạng). Khi mang sang máy khác, chép **cả thư mục** `slides_export/`.

| Phím | Tác dụng |
| --- | --- |
| `→` / `Space` / click | Bước tiếp theo (chạy hoạt hình) |
| `←` | Lùi lại |
| `F` | Toàn màn hình |
| `P` | Cửa sổ ghi chú người trình bày |
| `H` | Bảng phím tắt |

Thời lượng gợi ý: 75–85 phút nói + 10–15 phút hỏi đáp. Lời thoại đầy đủ nằm trong `04_Script_HyperFrames_SCSA.md` và trong cửa sổ ghi chú (phím `P`).

## Bộ slide `scsa-deck/`

Cả buổi dùng một ví dụ thật xuyên suốt: mẫu số 29 trong repo của tác giả (ảnh Yosemite, tranh núi và hai bản đồ nhãn bốn vùng: trời, vách núi, rừng, dãy xa). Các con số trên lưới 12 × 12 là **phép tính minh hoạ** trên ảnh mẫu, không phải số đo của mô hình; số liệu thật của paper chỉ có ở slide SSL và ablation.

Tài liệu thiết kế:

- [`SPEC.md`](scsa-deck/SPEC.md) — mục tiêu, màu, chữ, chuyển động, quy tắc QA
- [`STORYLINES.md`](scsa-deck/STORYLINES.md) — ba cách kể chuyện đã cân nhắc và lý do chọn
- [`REVIEW.md`](scsa-deck/REVIEW.md) — các quyết định thiết kế và nguồn dữ liệu

Cấu trúc:

```
scsa-deck/
├── index.html, compositions/   # dự án HyperFrames (sinh ra từ _build/)
├── assets/
│   ├── img/                    # ảnh mẫu 29 và kết quả từ paper
│   ├── data/scsa-data.json     # số liệu minh hoạ tính trên ảnh mẫu
│   ├── fonts/                  # Be Vietnam Pro, JetBrains Mono (OFL)
│   ├── deck.css, deck-motion.js
└── _build/
    ├── build.py                # ghép các slide (s_*.py) thành dự án HyperFrames
    ├── export_html.py          # xuất bản HTML độc lập
    ├── s_open.py … s_res.py    # nội dung từng chặng
    └── compute/                # tính scsa-data.json bằng Chrome headless
```

### Dựng lại

Yêu cầu: Python 3, Node.js (dùng `npx`).

```bash
cd scsa-deck

# Sinh lại index.html + compositions/ từ mã nguồn Python
python3 _build/build.py

# Kiểm tra (lint, runtime, layout, contrast) và xem trước
npm run check
npx hyperframes preview

# Xuất bản HTML chạy offline
python3 _build/export_html.py ../slides_export
```

`export_html.py` gọi lại `build.py`, nhúng font vào file HTML; ảnh và `gsap.min.js` cần nằm cạnh file xuất trong `assets/img/` và `lib/`.

`_build/compute/run.mjs` đang trỏ cứng tới đường dẫn Chrome headless và gói `hyperframes` trong cache npx của máy tác giả; sửa hai đường dẫn đó nếu muốn tính lại `scsa-data.json` trên máy khác.

## Ghi chú

- Số liệu của SCSA trong tài liệu đã đối chiếu với bản PDF arXiv v1. Mọi con số trong proposal là mục tiêu, chưa phải kết quả.
- Ảnh mẫu và ảnh kết quả lấy từ paper và repo gốc của tác giả, chỉ dùng cho mục đích học tập.

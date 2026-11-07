# REVIEW — SCSA deck v2 (2026-10-22)

## Creative calls
- Làm lại hoàn toàn, không theo bố cục artifact cũ. Chọn storyline A trong STORYLINES.md: một ví dụ thật (mẫu 29 của repo: Yosemite + tranh núi + hai bản đồ nhãn) đi qua mọi bước. Không dựng B (câu đố) và C (một sơ đồ lớn dần).
- Look "tường triển lãm và bản in" (SPEC.md): nền #EDEFF1, ảnh là bản in viền trắng, magenta #C2185B chỉ cho "chỗ cần nhìn / chỗ sai", Be Vietnam Pro nhúng trong assets/fonts.
- Bỏ hết: nhãn in hoa kiểu kicker, pill, thẻ xếp hàng, ô callout, số trang trong khung, hoạt hình lặp vô hạn, demo sinh phần tử bằng script.
- Mọi chuyển động nằm trong timeline của từng cảnh (seek được, deterministic). `assets/deck-motion.js` chỉ bật khi chạy trong `hyperframes present`, để bấm tới thì đoạn hoạt hình chạy ở tốc độ thật.

## Dữ liệu
- `assets/data/scsa-data.json` sinh bởi `_build/compute/` (canvas trong Chrome headless) từ mẫu 29: nhãn 144 ô, UA (softmax trên khoảng cách màu Lab, nhiệt độ theo từng hàng), SCA (trung bình màu vùng), SSA (top-1 cùng nhãn trên ảnh S-AdaIN), AdaIN và S-AdaIN trên pixel. Đây là minh hoạ đơn giản hoá, slide nào dùng đều ghi "minh hoạ".
- Số của paper: Table 1 (SSL, FID, CFSD, phiếu), Fig. 6 / Appendix F (ablation StyleID). Ảnh kết quả: cắt từ fig/2.png của repo.

## Đã đo / đã xem
- `npx hyperframes check`: 0 lỗi. Cảnh báo giữ lại có chủ ý: `line_unread` (deck giữ yên mỗi bước đến khi bấm, không áp dụng), `film_silent` (deck trình chiếu, không yêu cầu âm thanh), `composition_file_too_large` (index.html dài vì ghi chú người trình bày), `duplicate_media_discovery_risk` (cùng một ảnh dùng lại trong một slide, có chủ ý).
- Snapshot trạng thái cuối của cả 36 slide, đã xem và sửa chồng chữ, tràn hộp, nhãn bị che.
- Trình chiếu thật trong Chrome headless: 123 lần bấm tới 36/36, không lỗi JavaScript; xác nhận timeline UA chạy dần khi bấm tới.
- Chưa ai xem trên máy chiếu thật; chưa kiểm tra ở chế độ hai màn hình với Zoom.

## Điểm yếu nhất
- Slide "Bốn thước đo" và các thẻ chương còn nhiều khoảng trống ở nửa dưới. Có thêm thời gian: đặt hình minh hoạ cho từng thước đo lớn hơn, và cho thẻ chương một ảnh nền mờ từ ví dụ.
- Bức ghép 12 × 12 thô so với kết quả thật; đã ghi rõ là minh hoạ và đặt cạnh kết quả thật.

# REVIEW — bản 3 (2026-10-31): theo khung Seminar Guidelines của giảng viên

## Cấu trúc
- Năm chặng đổi theo khung: Giới thiệu → Bài toán và tổng quan → Chi tiết kỹ thuật → So sánh và thảo luận → Kết luận (`CH`, `CHL`, `QS` trong `s_open.py`).
- Nền tảng (lưới, attention, softmax, AdaIN, UA) và ba lỗi gộp vào chặng 2: định nghĩa bài toán → mô hình hiện nay làm thế nào → thách thức → tổng quan SCSA (slide "SCSA trong một phút" chuyển xuống cuối chặng 2).
- Chặng 3 giảng mỗi khối ba lớp: hình → công thức → thuật toán. Chặng 4 theo thứ tự thực nghiệm: thiết lập → định tính → định lượng → so sánh → ablation → mạnh/yếu.
- 10 slide mới: apps, task (s_ctx); uaf (s_base); scaf, ssaf, algo, train (s_meth); compare, strengths, future (s_res). Tổng 45 slide, ~110 phút.

## Công thức
- Ký hiệu theo paper (Q, K, V, f_q…, F̄, G₁, G₂). Viết bằng HTML (`eq`, `v`, `ob`, `cases` trong lib.py), không dùng MathJax để deck vẫn chạy offline. Chỉ số trên/dưới đặt cạnh nhau, không xếp chồng (xếp chồng bị check báo đè dòng chú thích); cỡ tối thiểu 28 px.
- Mỗi slide công thức có ma trận 6 × 6 động (`mini_matrix`) và đường phân bố (`gauss`) chạy theo từng dòng; giá trị là minh hoạ.

## Đã đo / đã xem
- `npm run check`: 0 lỗi; cảnh báo còn lại cùng loại đã giữ ở bản 2 (line_unread…).
- Snapshot trạng thái cuối của 12 slide mới/sửa; đã sửa chồng chữ ở slide ứng dụng, hướng phát triển, nhãn trục ma trận.
- Chưa bấm thử toàn bộ 45 slide trong `hyperframes present`.

# REVIEW — bản 4 (2026-10-31): công thức dễ hiểu + rà soát toàn deck

- Người dùng: công thức phải dễ hiểu cho cả lớp, không đi sâu. Ba slide công thức (UA, SCA, SSA với F̄, f_q, G₁/G₂ dạng ngoặc nhọn) thay bằng hai: `uaf` (Attention = softmax(Q Kᵀ)·V, thay đúng 4 con số của slide softmax) và `maskf` (cộng mặt nạ M, cùng 4 con số → 0/0/100/0%). Helper `ex_head/ex_row` trong s_base.py. Thuật toán viết bằng lời, không chỉ số.
- Rà soát độc lập 168 khung hình (cuối mỗi bước), đối chiếu README, dàn ý, paper, repo. Đã sửa: pipe (bố cục cộng từ sau S-AdaIN), softmax (luật xét nhãn, không nói "SCSA chỉ là cấm"), fixmap (ba lỗi ba gốc), err23 (lỗi 3 minh hoạ bằng 4 mảnh cùng vùng vách núi), metrics (1.200 phiếu = hai phần khảo sát), ablation/strengths ("SSL cũng tăng", không "tệ hơn mọi mặt"; nguồn Fig. 6), algo (bước 2–6 là SCSA; hai bảng điểm), limits (+CFSD StyleID, chú thích lưới), future (lộ trước nội dung), slide 2 và 7 (hình nét đứt hiện sớm), train (bỏ S-AdaIN khỏi "điểm mới"). Dàn ý A.5.2: sửa ghi chú Pref.
- Chưa sửa (nhẹ): một số chữ mồ côi khi ngắt dòng; cột bị cấm ở slide softmax vẫn vẽ sọc cao hết cỡ; slide plug dùng chung sơ đồ cho cả ba backbone.

## Bản 4.1 — slide 29 "Trộn"
- Bỏ thanh trượt (ở 0,7 lớp SCA che gần hết nét cọ, nhìn như SCA thuần; "một nút" cũng sai vì α₁, α₂ độc lập).
- Thay bằng phép cộng bằng hình: SCA × 0,7 + SSA × 0,3 + bố cục (ảnh sau S-AdaIN) = kết quả thật, cuối slide là công thức với α₁, α₂.
- Người dùng muốn giữ thanh trượt → khôi phục, nhưng bỏ đường lưới trắng trên ô trộn để vệt cọ hiện ở mức 0,7/0,3 (phép trộn opacity thật). Đổi tiền tố id mx2-/mx- → mz-: `#mx-end`, `#mx-d*` trùng với slide "matrices" khiến dòng cuối bị mờ khi trình chiếu. Đã quét: 0 id trùng giữa các composition.
- Lùi từ SCA về 0,7 gần như không đổi hình (chỉ 30% nét lộ ra). Thêm lớp `#mz-tone` (mix-blend-mode: color, màu vùng của SCA) trên ô SSA, lớp SCA thường giảm còn 0,35: màu đều theo vùng mà vệt cọ hiện rõ. Đây là minh hoạ, không phải trộn tuyến tính; lời thoại đã ghi "minh hoạ".

## Bản 4.2 — bỏ slide "Chạy code"
- Bỏ slide `code` khỏi ORDER và NOTES (module s_res vẫn giữ định nghĩa); xoá compositions/code.html. Deck còn 43 slide, ~103 phút.
- Script tạo lại bằng rewrite_script.py (đánh lại số slide, mục "Nếu thiếu thời gian"); lời mở chặng 3 bỏ "cách chạy code".

## Bản 4.3 — slide kết thúc
- Thêm slide `end` (cuối deck, s_res.py). Người dùng thấy bản "Cảm ơn / Câu hỏi" quá sến → chỉ còn tên bài báo (SCSA, tên đầy đủ, CVPR 2025) và bốn ảnh kết quả trang trí. Lời cảm ơn chỉ nằm trong ghi chú người nói. Deck 44 slide.

## Bản 4.4 — xuất một file
- export_html.py nhúng hết ảnh (nền: một biến CSS mỗi ảnh; `<img>`: bảng IM gán src lúc tải) và GSAP (`_build/gsap.min.js`) vào SCSA_trinh_chieu.html (~6,4 MB). File chạy một mình, không cần assets/ hay lib/; đã thử mở bản sao ở thư mục trống: 0 lỗi, đủ ảnh và hoạt hình.

## Bản 4.5 (2026-11-07) — so sánh bằng ảnh thật + StyleGallery
- Slide mới `gens` (slide 8, cuối chặng 1, ngay sau "Mười năm"): "Cùng một cặp ảnh, bốn phương pháp". Ảnh lấy từ `compare_style_transfer.ipynb` (mẫu 29, 512 × 512, Apple MPS), chép vào `assets/img/cmp_{gatys,adain,sanet,scsa}.jpg`. Mỗi bấm hiện một kết quả, khoanh vách núi (magenta = sai; SCSA = nét đứt màu mực như slide hook), ghi thời gian đo: Gatys L-BFGS 26,8 s / 300 bước, AdaIN 97 ms, SANet 124 ms, SANet + SCSA 473 ms. Lời thoại nói rõ: đo trên một máy, một ảnh, chỉ để so thứ bậc.
- Slide mới `next` (slide 45, trước slide kết thúc): StyleGallery (He et al., CVPR 2026, arXiv 2603.10354) bỏ yêu cầu bản đồ nhãn: tự gom cụm K-means trên đặc trưng SD 1.5 → ghép cụm với một hoặc nhiều tranh → tối ưu khi lấy mẫu, không train. Hình: Fig. 1(b) của paper (`assets/img/stylegallery_fig1b.jpg`, cắt từ teaser trên project page). Mọi con số (≈30 s trên RTX 4090, 150 bước; ≈8 s / 28 bước) và câu hạn chế lấy nguyên văn từ arXiv HTML. Paper chỉ so với SCSA bằng hình (Fig. 7), không có số, nên slide không kết luận bên nào tốt hơn.
- Đã thử rồi bỏ: minh hoạ "tự gom vùng" bằng K-means trên đặc trưng VGG của ảnh mẫu, vì cụm chỉ bắt viền chứ không ra vùng, dễ gây hiểu nhầm.
- Script: chèn hai mục, đánh lại số slide (46 slide, ~109,5 phút). `npm run check`: 0 lỗi. Export một file: bấm qua 46/46 slide trong Chrome headless, 0 lỗi JS.

## Bản 5 (2026-11-07) — một mạch hỏi → đáp, hết khựng
- Câu hỏi mở màn "vì sao vách núi bị tô sai?" thành sợi chỉ xuyên suốt. Năm câu hỏi chương (`QS` trong s_open.py): Style transfer là gì, đã đi tới đâu? → Vì sao vách núi bị tô sai? → SCSA sửa thế nào? → Sửa được bao nhiêu, kém ở đâu? → Mang về gì, đi tiếp đâu? Tên chặng theo khung giảng viên giữ nguyên (`CHL`).
- Thẻ chương 2–5 có dòng "Chặng k trả lời: …" (`ANS`). Mỗi slide có câu "Dẫn:" nói vì sao sang slide sau (`BRIDGE` trong notes.py, build.py nối vào bước cuối).
- Thứ tự: bỏ slide `idea` (trùng "SCSA trong một phút" và "Tóm tắt"; phần tên gọi S·C·S·A chuyển vào `minute`). AdaIN chuyển từ chặng 2 sang chặng 3, giữa SCA và S-AdaIN (đi theo sơ đồ toàn cảnh, AdaIN → S-AdaIN liền nhau). Slide softmax bỏ bước "cấm" (giải pháp trước vấn đề); giờ chốt "softmax không nhìn nhãn: dãy xa sai vùng vẫn nhận 63%". Luật cấm giải thích ở `maskf`. Deck 45 slide, ~107 phút.
- `pipe`: sơ đồ ghi rõ là SANet, thêm hai bước đổi dòng phụ sang StyTr2, StyleID (khung encoder/decoder chuyển magenta = phần đổi theo mô hình). `plug`: vẽ lại thành ba cột kiến trúc riêng (SANet: encoder VGG / StyTr2: transformer encoder, SCSA ở lớp chẵn của transformer decoder / StyleID: DDIM inversion, SCSA ở self-attention U-Net, VAE decoder), theo README §4 và Appendix C. Câu chữ nói rõ SCSA cắm vào từng mô hình một, không phải cả ba cùng lúc.
- Hết khựng: trình chiếu dừng đúng tại điểm fragment, nên hoạt hình còn chạy qua điểm đó bị đóng băng (slide lưới điểm dừng khi các hàng dưới đang trượt). `_build/settle.py` (gọi trong build.py) đẩy mỗi điểm dừng ra sau khi mọi tween bắt đầu trước nó đã xong về mặt thị giác (tính theo ease), và báo nếu đụng tween của bước sau. Sửa tay: grid (stagger nhanh hơn), maps, fixmap, chấm chạy trên dây ở pipe (bỏ repeat). Còn một báo động giả ở `results` (bộ đếm stagger), slide thực tế không khựng.
- Script .md dựng lại theo thứ tự mới (bảng tổng quan, đánh số, khung giảng viên, mục thiếu thời gian). `npm run check` 0 lỗi; export bấm qua 45/45, 0 lỗi JS.

## Bản 5.1 (2026-11-07)

- Slide mới `sslx` "SSL: chấm style theo từng cặp vùng" (sau "Bốn thước đo"). Paper §4.3 chỉ mô tả SSL bằng lời: loss style của AdaIN [19] (μ, σ đặc trưng VGG) tính theo từng vùng, "similar to Eq. 8"; không ghi lớp, cách cộng; repo chính thức không có code đo SSL. Công thức trên slide ghi "viết lại từ lời mô tả ở §4.3".
- Minh hoạ trên slide: μ, σ màu Lab trên 4 ảnh `cmp_*.jpg` so với tranh, cắt theo 29_sem / 29_paint_sem. Cả ảnh: Gatys 1,6 · AdaIN 5,1 · SANet 5,4 · SCSA 6,7 (SCSA tệ nhất). Từng vùng: 94,9 · 88,4 · 85,1 · 21,0 (SCSA tốt nhất).
- Slide "Mười năm": thêm ảnh kết quả dưới mỗi mốc (cmp_* mẫu 29; StyleID dùng ex3_styleid.png từ paper vì notebook không chạy StyleID).
- Sửa: notes metrics "chữ ký màu kiểu Gatys" → μ, σ kiểu AdaIN; README/outline "Gram" → AdaIN μ, σ. Deck 46 slide, ~110 phút.
- Slide "Mười năm": ảnh StyleID nay là `cmp_styleid.jpg` (chạy thật trên mẫu 29, `styleid_nst.py`). Slide vẫn lấy SANet + SCSA làm ví dụ chính (theo yêu cầu người dùng); StyleID + SCSA chỉ có trong notebook.
- Slide "Kết quả thật" thêm bước 4: lưới 2 × 3 trên mẫu 29 (gốc / + SCSA × SANet, StyTr2, StyleID), ảnh từ compare_style_transfer.ipynb (`cmp_stytr2*.jpg`, `cmp_styleid*.jpg`). Ba bước đầu vẫn là ví dụ của paper; SANet + SCSA vẫn là ví dụ chính ở các slide khác.
- Slide "Mười năm" tách mốc "2019–22 SANet, StyTr2" thành hai mốc 2019 SANet và 2022 StyTr2, mỗi mốc một ảnh mẫu 29 (`cmp_stytr2.jpg`); tiêu đề thành "sáu bước", 7 bước bấm.

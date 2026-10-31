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

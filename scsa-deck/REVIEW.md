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

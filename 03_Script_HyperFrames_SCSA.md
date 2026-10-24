# Script trình bày — bộ slide HyperFrames SCSA (bản 2)

> Bộ slide: thư mục `scsa-deck/`, 35 slide, theme sáng. Thiết kế: `scsa-deck/SPEC.md`.
> Paper: SCSA, CVPR 2025 — arXiv 2503.04119 · Code: github.com/scn-00/SCSA
> Soạn ngày 2026-10-22. Đối tượng: người mới, chưa biết style transfer.
> Tổng thời lượng gợi ý: **75–85 phút** nói + 10–15 phút hỏi đáp.

## Một ví dụ xuyên suốt

Cả buổi dùng **một bộ dữ liệu thật**: mẫu số 29 trong repo của tác giả, gồm ảnh chụp thung lũng Yosemite, một bức tranh núi, và hai bản đồ nhãn với bốn vùng: trời, vách núi, rừng, dãy xa. Kết quả SANet và SANet + SCSA trên đúng cặp ảnh này có trong hình kết quả của paper, nên câu hỏi mở màn và câu trả lời cuối buổi là cùng một bức ảnh.

Các con số trên lưới 12 × 12 (phần trăm trọng số, bức ghép SCA, SSA) là **phép tính minh hoạ** trên màu trung bình của từng mảnh ảnh mẫu, không phải số đo của mô hình thật. Slide nào dùng chúng đều ghi rõ. Số liệu thật của paper chỉ nằm ở slide SSL và ablation.

## Cách mở và điều khiển

- Mở `slides_export/SCSA_trinh_chieu.html` bằng trình duyệt (bấm đúp). Không cần mạng. Chép cả thư mục `slides_export` khi mang sang máy khác.
- **→ / Space / click**: bước tiếp theo, hoạt hình chạy. **←**: lùi, nhảy thẳng. **F**: toàn màn hình. **P**: cửa sổ ghi chú người trình bày. **H**: bảng phím tắt.
- Mỗi “Bấm” trong lời thoại là một lần mũi tên phải. Lời thoại cũng hiện trong cửa sổ ghi chú (phím P).
- Slide UA có một đoạn quét dài khoảng 8 giây sau lần bấm thứ hai: nói trong lúc nó chạy.

Cấu trúc: tổng quát trước, chi tiết sau. Mỗi chặng mở bằng một thẻ chương có câu hỏi riêng; lạc thì quay về thẻ chương hoặc slide “SCSA trong một phút”.

## Bảng tổng quan

| # | Slide | Số lần bấm | Thời lượng | Nguồn hình |
| --- | --- | --- | --- | --- |
| 1 | SCSA | 1 | 1 phút |  |
| 2 | Cùng ảnh, cùng tranh, hai kết quả | 3 | 2 phút | ảnh thật từ paper |
| 3 | SCSA trong một phút | 3 | 2,5 phút |  |
| 4 | Năm chặng, từ tổng quát tới chi tiết | 2 | 1 phút |  |
| 5 | Chặng 1 · Style transfer là gì? | 1 | 0,5 phút |  |
| 6 | Style transfer: giữ bố cục, thay lớp áo | 4 | 2,5 phút | ảnh thật |
| 7 | Mười năm style transfer, năm bước | 6 | 3 phút |  |
| 8 | Semantic: mỗi ảnh có thêm một bản đồ nhãn | 5 | 2,5 phút | bản đồ nhãn thật trong repo |
| 9 | Chặng 2 · Attention chọn style thế nào? | 1 | 0,5 phút |  |
| 10 | Ảnh được cắt thành lưới điểm | 4 | 2,5 phút |  |
| 11 | Attention: hỏi, so, cân, trộn | 5 | 4 phút |  |
| 12 | Chia trọng số, và cách “cấm” một ô | 4 | 3,5 phút |  |
| 13 | AdaIN: đổi tông bằng hai con số | 4 | 3 phút | phép tính thật trên pixel |
| 14 | Universal Attention: ai cũng nhìn tất cả | 3 | 3 phút |  |
| 15 | Chặng 3 · Vì sao tô nhầm vùng? | 1 | 0,5 phút |  |
| 16 | Lỗi 1: lấy style từ sai vùng | 4 | 3,5 phút | tính minh hoạ + ảnh thật của paper |
| 17 | Lỗi 2 và 3: loang lổ, nhạt nhoà | 3 | 3 phút | dải trời cắt từ kết quả thật |
| 18 | Ba lỗi, ba cách sửa | 4 | 2,5 phút |  |
| 19 | Chặng 4 · Sửa bằng cách nào? | 1 | 0,5 phút |  |
| 20 | Chỉ nhìn trong vùng cùng nhãn | 4 | 2,5 phút |  |
| 21 | Toàn cảnh: SCSA nằm ở giữa | 6 | 3,5 phút |  |
| 22 | SCA: hỏi bằng bản đồ nhãn | 5 | 3,5 phút | tính minh hoạ trên ảnh mẫu |
| 23 | S-AdaIN: đổi tông riêng từng vùng | 4 | 2,5 phút | phép tính thật trên pixel |
| 24 | SSA: chỉ giữ một mảnh giống nhất | 5 | 3,5 phút | tính minh hoạ trên ảnh mẫu |
| 25 | Ba ma trận attention, nhìn là thấy khác | 4 | 2,5 phút |  |
| 26 | Trộn hai nhánh: một nút chỉnh tông và nét | 5 | 3 phút | tính minh hoạ + kết quả thật |
| 27 | Cắm vào ba họ mô hình, không train lại | 5 | 2,5 phút |  |
| 28 | Chặng 5 · Tốt tới đâu? | 1 | 0,5 phút |  |
| 29 | Kết quả thật trên ba họ mô hình | 3 | 3 phút | ảnh thật từ paper |
| 30 | Bốn thước đo, đọc trước khi xem số | 5 | 2,5 phút |  |
| 31 | Lỗi style theo vùng giảm 29–47% | 3 | 3 phút | số từ Table 1 |
| 32 | Bỏ bớt một mảnh, lỗi tăng bao nhiêu? | 5 | 2,5 phút | số từ Fig. 6 và Appendix F |
| 33 | Những điều SCSA chưa giải quyết | 3 | 2,5 phút | tính minh hoạ trên ảnh mẫu |
| 34 | Chạy code gốc trên đúng ví dụ này | 3 | 2 phút | file thật trong repo |
| 35 | Chỉ lấy style từ vùng cùng nhãn | 3 | 2 phút |  |

## Mở đầu (slide 1–4, ~6 phút)

### Slide 1 · SCSA

**Số lần bấm:** 1 · **Thời lượng:** 1 phút

**Nói:** Chào mọi người. Hôm nay mình trình bày SCSA, một paper ở CVPR 2025: dạy attention nhìn đúng vùng khi chuyển phong cách cho ảnh. Mình giả định mọi người chưa biết style transfer. Ba ảnh bên phải là thật, lấy từ repo của tác giả: ảnh chụp thung lũng Yosemite, một bức tranh núi, và kết quả khi tô ảnh theo tranh bằng SCSA. Cả buổi mình dùng đúng cặp ảnh này.

### Slide 2 · Cùng ảnh, cùng tranh, hai kết quả

**Số lần bấm:** 3 · **Thời lượng:** 2 phút · **Nguồn:** ảnh thật từ paper

**Nói:** Câu hỏi mở màn. Hai ảnh này là kết quả thật trong paper, cùng một đầu vào ở giữa. Trái là SANet, một mô hình có sẵn. Phải là SANet cộng SCSA. Bấm: nhìn vách núi lớn. SANet tô nó bằng màu kem của trời; SCSA tô đúng màu xanh của núi. Bấm: vì sao bên trái tô nhầm? Cả buổi hôm nay trả lời câu này. Giữ nó trong đầu.

### Slide 3 · SCSA trong một phút

**Số lần bấm:** 3 · **Thời lượng:** 2,5 phút

**Nói:** Cả paper trong một sơ đồ. Ảnh và tranh đi vào khối attention. Khối này chọn cho mỗi điểm của ảnh nên lấy style từ đâu trong tranh. Nó chọn theo kiểu “trông giống”, nên tô nhầm vùng, như SANet vừa rồi. Bấm: SCSA thêm bản đồ nhãn, mỗi màu là một vùng. Attention giờ chỉ lấy style từ vùng cùng nhãn, nên đúng vùng. Bấm: bên trong có hai cách nhìn. SCA nhìn cả vùng, lấy tông chung. SSA nhìn một điểm, lấy nét cọ, tức vệt sơn của tranh. Và không phải train lại. Chưa cần hiểu hết, cả buổi mình đi từng cái.

### Slide 4 · Năm chặng, từ tổng quát tới chi tiết

**Số lần bấm:** 2 · **Thời lượng:** 1 phút

**Nói:** Năm chặng, mỗi chặng là một câu hỏi. Bối cảnh: style transfer là gì. Nền tảng: attention chọn style thế nào. Vấn đề: vì sao tô nhầm vùng. SCSA: sửa bằng cách nào. Kết quả: tốt tới đâu. Bấm: chặng 4 là trọng tâm. Lạc thì hỏi, mình quay về đầu chặng.

## Chặng 1 · Bối cảnh (slide 5–8, ~9 phút)

### Slide 5 · Chặng 1 · Style transfer là gì?

**Số lần bấm:** 1 · **Thời lượng:** 0,5 phút

**Nói:** Chặng 1, bối cảnh. Câu hỏi: style transfer là gì?

### Slide 6 · Style transfer: giữ bố cục, thay lớp áo

**Số lần bấm:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** ảnh thật

**Nói:** Ảnh chụp cho bố cục: trời ở trên, vách núi ở giữa, rừng ở dưới. Bấm: bức tranh cho lớp áo: màu, nét cọ, bề mặt. Bấm: kết quả là bố cục cũ, áo mới. Để ý: trời mang màu kem của trời trong tranh, vách núi mang màu xanh của núi. Bấm: arbitrary nghĩa là một mô hình dùng cho mọi bức tranh, không train lại từng tranh. Hỏi nhanh: vách núi bị tô màu trời thì có thành công không? Không: vẫn là áo của tranh, nhưng mặc sai chỗ.

### Slide 7 · Mười năm style transfer, năm bước

**Số lần bấm:** 6 · **Thời lượng:** 3 phút

**Nói:** Mười năm, năm mốc, mỗi lần bấm một mốc. 2016, Gatys: chỉnh từng pixel cho tới khi ảnh vừa giống bố cục, vừa giống màu của tranh. Đẹp nhưng chậm, mỗi ảnh vài phút. Bấm: 2017, AdaIN: một mạng cho mọi tranh, khớp tông cả ảnh. Nhanh nhưng thô; ta gặp lại nó ở chặng 2. Bấm: 2019 đến 2022, SANet và StyTr2: attention, mỗi điểm của ảnh tự đi tìm style. Bấm: 2024, StyleID: attention bên trong Stable Diffusion. Bấm: 2025, SCSA: attention biết nhãn vùng. Bấm: khung cam bao ba mô hình ở giữa, đó là ba mô hình SCSA cắm vào. SCSA không thay chúng.

### Slide 8 · Semantic: mỗi ảnh có thêm một bản đồ nhãn

**Số lần bấm:** 5 · **Thời lượng:** 2,5 phút · **Nguồn:** bản đồ nhãn thật trong repo

**Nói:** Đây là ảnh chụp và bức tranh của ta. Bấm: thêm hai bản đồ nhãn, gọi là semantic map; mỗi màu là một vùng. Đây là file thật trong repo. Bấm: đỏ là trời, vàng là vách núi, xanh lá là rừng, xanh dương là dãy xa. Màu chỉ là mã nhãn, không phải màu thật. Bấm: nối đúng cặp, trời với trời, vách núi với vách núi. Bấm: mỗi vùng chỉ lấy style từ vùng cùng tên. Đầu vào giờ là bộ bốn: ảnh, map ảnh, tranh, map tranh. Ai vẽ map? Người dùng tự vẽ hoặc dùng mô hình phân đoạn. Paper không tự sinh map, đó là một hạn chế.

## Chặng 2 · Nền tảng (slide 9–14, ~17 phút)

### Slide 9 · Chặng 2 · Attention chọn style thế nào?

**Số lần bấm:** 1 · **Thời lượng:** 0,5 phút

**Nói:** Chặng 2, nền tảng. Câu hỏi: attention chọn style thế nào? Bốn khái niệm: lưới điểm, attention, softmax với mask, và AdaIN. Rồi gộp lại thành Universal Attention. Đừng bỏ chặng này: cả phần SCSA chỉ là thay đổi nhỏ trên những thứ này.

### Slide 10 · Ảnh được cắt thành lưới điểm

**Số lần bấm:** 4 · **Thời lượng:** 2,5 phút

**Nói:** Từ “điểm” dùng suốt phần sau. Đây là ảnh 512 nhân 512 pixel. Bấm: encoder cắt ảnh thành lưới. Ở đây mình cắt 12 nhân 12 cho dễ nhìn; mô hình thật là 64 nhân 64, tức 4.096 điểm. Bấm: mỗi điểm là một vector, ví dụ 512 số, mô tả mảng ảnh quanh nó: màu, cạnh, bề mặt. Nó không phải một pixel. Bấm: decoder vẽ lưới ngược lại thành ảnh. SCSA chỉ sửa ở giữa, trên lưới điểm.

### Slide 11 · Attention: hỏi, so, cân, trộn

**Số lần bấm:** 5 · **Thời lượng:** 4 phút

**Nói:** Attention giống tra từ điển, nhưng mềm. Một điểm vách núi của ảnh hỏi: “style nào hợp với tôi?”. Đây là query. Bấm: nó so với các điểm của tranh. Mỗi điểm có thẻ để so, gọi là key, và nội dung để lấy, gọi là value. Ở đây mình chỉ vẽ 4 trong 4.096 điểm: trời, dãy xa, vách núi, rừng. Mỗi điểm là một vị trí trên lưới, không phải pixel. Đường càng dày càng giống. Bấm: độ giống đổi thành trọng số: 35, 63, 1 và 1 phần trăm. Bấm: màu chảy về theo trọng số rồi trộn lại. Bấm: chú ý, điểm vách núi xám nhạt của ảnh giống dãy xa và trời của tranh hơn là vách núi của tranh, nên 99 phần trăm màu lấy từ sai vùng. Đó chính là lỗi ta thấy ở SANet. Số này tính minh hoạ trên màu của ảnh mẫu, không phải số của mô hình thật.

### Slide 12 · Chia trọng số, và cách “cấm” một ô

**Số lần bấm:** 4 · **Thời lượng:** 3,5 phút

**Nói:** Vẫn bốn điểm đó. Đây là điểm số giống nhau: dãy xa cao nhất, khoảng 4,6; rồi trời, khoảng 4; vách núi và rừng chỉ quanh 0,5. Bấm: softmax đổi điểm số thành phần trăm, cộng lại đủ 100: 35, 63, 1, 1. Điểm cao được phần lớn, nhưng không ai bị bỏ hẳn. Bấm: giờ đặt luật: điểm vách núi chỉ được lấy từ vách núi, ba điểm kia bị cấm. Cách cấm là đặt âm vô cực vào điểm số của chúng; e mũ âm vô cực bằng 0, nên ba cột rơi về đúng 0 và vách núi nhận 100 phần trăm. Không phải sửa gì khác trong mô hình, nên SCSA cắm được vào mô hình đã train. Bấm: toàn bộ SCSA chỉ là quyết định ô nào bị cấm.

### Slide 13 · AdaIN: đổi tông bằng hai con số

**Số lần bấm:** 4 · **Thời lượng:** 3 phút · **Nguồn:** phép tính thật trên pixel

**Nói:** AdaIN là phương pháp 2017 ở slide lịch sử; SCSA dùng lại nó. Tông của một ảnh tóm trong hai con số: μ là màu trung bình, σ là độ tương phản. Đọc là “miu” và “xích-ma”. Ảnh chụp này xám ấm. Bấm: bức tranh có μ, σ riêng: kem xanh, tương phản thấp hơn. Bấm: AdaIN bỏ μ, σ của ảnh rồi khoác μ, σ của tranh. Ảnh bên phải là phép tính thật trên pixel: cả ảnh ngả về tông của tranh. Trong mô hình, phép này làm trên lưới điểm, không phải pixel. Bấm: giới hạn là chỉ một cặp số cho cả ảnh, nên trời, vách núi, rừng bị kéo về cùng một tông. S-AdaIN ở chặng 4 sẽ sửa điều này.

### Slide 14 · Universal Attention: ai cũng nhìn tất cả

**Số lần bấm:** 3 · **Thời lượng:** 3 phút

**Nói:** Paper gọi khối attention trong SANet, StyTr2, StyleID là Universal Attention, viết tắt UA. Trái là 144 điểm của ảnh, phải là 144 điểm của tranh. Bấm: khung magenta là câu hỏi đang xét, nó chạy qua vài điểm. Mỗi lần, các đường nối tới 8 điểm tranh giống nhất; số 8 mình chọn để nhìn cho rõ. Đường đen là cùng vùng, magenta là sang vùng khác. Dòng chữ giữa là phần trăm trọng số rơi sang vùng khác, tính trên cả 144 điểm. Đoạn này chạy khoảng 8 giây, mình nói trong lúc đó. Bấm: chốt, mỗi điểm nhìn tất cả 144 thẻ, không ai hỏi điểm đó thuộc vùng nào. Với lưới 64 nhân 64 thật, bảng so khớp có 16 triệu ô. Số tính minh hoạ trên màu của ảnh mẫu.

## Chặng 3 · Vấn đề (slide 15–18, ~10 phút)

### Slide 15 · Chặng 3 · Vì sao tô nhầm vùng?

**Số lần bấm:** 1 · **Thời lượng:** 0,5 phút

**Nói:** Chặng 3, vấn đề. Câu hỏi: vì sao tô nhầm vùng? Ta chạy attention trên chính ảnh Yosemite và đếm xem bao nhiêu style lấy sai chỗ.

### Slide 16 · Lỗi 1: lấy style từ sai vùng

**Số lần bấm:** 4 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ + ảnh thật của paper

**Nói:** Chạy UA cho cả 144 điểm của ảnh, ta được bức ghép bên trái: mỗi ô là màu trộn mà điểm đó lấy về. Bấm: phủ magenta lên những ô lấy style từ vùng khác, càng đậm càng nhiều. Trung bình 36 phần trăm trọng số rơi sang vùng sai, và 36 trên 144 điểm lấy phần lớn style từ vùng sai, dồn vào vách núi. Bấm: so với kết quả thật của SANet trong paper: đúng chỗ đó, vách núi mang màu trời. Bấm: phép tính của mình chỉ dùng màu trung bình nên chỉ là minh hoạ, nhưng nó chỉ ra cùng một chỗ sai với mô hình thật. Đây là lỗi 1: lấy style từ sai vùng.

### Slide 17 · Lỗi 2 và 3: loang lổ, nhạt nhoà

**Số lần bấm:** 3 · **Thời lượng:** 3 phút · **Nguồn:** dải trời cắt từ kết quả thật

**Nói:** Lỗi 2, loang lổ. Đây là dải trời cắt từ hai kết quả thật của paper. Trên là SANet: trời lẫn vệt xanh của núi, mỗi chỗ một kiểu, vì mỗi điểm tự chọn style theo cấu trúc riêng. Dưới là SANet cộng SCSA: cả vùng trời một tông, đó là điều ta muốn. Bấm: lỗi 3, nhạt nhoà. Bốn điểm tranh mà điểm vách núi lấy nhiều nhất đều sắc nét, nhưng trộn lại thành một màu đục, mất nét cọ. Bấm: hai lỗi kéo ngược nhau. Lỗi 2 muốn các điểm trong vùng giống nhau, lỗi 3 muốn mỗi điểm giữ nét riêng. Vì vậy SCSA cần hai cách nhìn, không phải một.

### Slide 18 · Ba lỗi, ba cách sửa

**Số lần bấm:** 4 · **Thời lượng:** 2,5 phút

**Nói:** Bản đồ nối sang phần SCSA. Sai vùng: sửa bằng luật cấm theo nhãn, có sẵn trong cả SCA và SSA, nên lỗi 1 được sửa miễn phí. Bấm: loang lổ, sửa bằng SCA: cả vùng dùng chung một tông. Bấm: nhạt nhoà, sửa bằng SSA: chỉ lấy một điểm, giữ nguyên nét cọ. Bấm: cả ba lỗi chung một gốc: attention không biết nhãn vùng. Các slide sau chỉ phóng to cột phải.

## Chặng 4 · SCSA (slide 19–27, ~25 phút)

### Slide 19 · Chặng 4 · Sửa bằng cách nào?

**Số lần bấm:** 1 · **Thời lượng:** 0,5 phút

**Nói:** Chặng 4, SCSA, phần trọng tâm. Câu hỏi: sửa bằng cách nào? Đi từ ý tưởng, sơ đồ, rồi từng khối: SCA, S-AdaIN, SSA, phép trộn.

### Slide 20 · Chỉ nhìn trong vùng cùng nhãn

**Số lần bấm:** 4 · **Thời lượng:** 2,5 phút

**Nói:** Câu cần nhớ nhất của paper: chỉ nhìn trong vùng cùng nhãn. Đây là một điểm vách núi của ảnh. Bấm: cách nhìn thứ nhất, SCA. Nó nhìn tất cả điểm vách núi của tranh; các vùng khác bị gạch chéo, tức là bị cấm. Kết quả là tông chung của cả vùng. Bấm: cách nhìn thứ hai, SSA. Chỉ một đường nối, tới đúng một điểm vách núi giống nhất, lấy nguyên nét cọ, tức vệt sơn, của điểm đó. Bấm: giải nghĩa cái tên. S là Semantic, dùng nhãn vùng. C là Continuous, nhìn liên tục cả vùng, tức SCA. S là Sparse, thưa, chỉ một điểm, tức SSA. A là Attention.

### Slide 21 · Toàn cảnh: SCSA nằm ở giữa

**Số lần bấm:** 6 · **Thời lượng:** 3,5 phút

**Nói:** Bốn đầu vào: ảnh, map ảnh, tranh, map tranh. Encoder biến cả bốn thành lưới điểm. Bấm: nhánh trên, SCA: hỏi bằng map, lấy tông chung của cả vùng. Bấm: nhánh dưới hai bước: S-AdaIN đổi tông ảnh theo từng vùng, rồi SSA tìm một điểm giống nhất trong cùng vùng. Bấm: trộn tông chung, nét cọ, và cộng bố cục của ảnh vào, đường đứt nét magenta. Bấm: decoder vẽ ra ảnh. Bấm: encoder, decoder giữ nguyên; chỉ ba khối ở giữa là SCSA.

### Slide 22 · SCA: hỏi bằng bản đồ nhãn

**Số lần bấm:** 5 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:** SCA khác UA ở hai chỗ. Chỗ một: câu hỏi không lấy từ ảnh mà từ bản đồ nhãn. Bấm: map là mảng màu phẳng, nên mọi điểm vách núi hỏi cùng một câu. Bấm: chỗ hai, luật G1: khác nhãn thì cấm. Vì mọi điểm vách núi hỏi giống nhau, trọng số chia đều cho mọi điểm vách núi của tranh. Bấm: mỗi điểm vách núi nhận cùng một màu, là trung bình của vách núi trong tranh, màu xanh. Làm tương tự cho các vùng khác, ta được bức ghép bên phải, tính thật trên ảnh mẫu. Bấm: liền mạch, đúng vùng, hết loang lổ. Cái giá: phẳng, mất nét cọ. Hỏi nhanh: giữ luật cấm mà hỏi bằng ảnh thì sửa được lỗi nào? Chỉ lỗi sai vùng, loang lổ vẫn còn.

### Slide 23 · S-AdaIN: đổi tông riêng từng vùng

**Số lần bấm:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** phép tính thật trên pixel

**Nói:** Nhớ AdaIN ở chặng 2: hai con số, màu trung bình và độ tương phản. Đây là ảnh gốc. Bấm: AdaIN cả ảnh dùng một cặp số cho mọi vùng, nên cả ảnh ngả một tông. Bấm: S-AdaIN tính riêng cho từng vùng nhãn. Vách núi nhận tông xanh của vách núi trong tranh, dãy xa nhận tông hồng của dãy xa. Ba ảnh này là phép tính thật trên pixel của ảnh mẫu. Bấm: để làm gì? Để SSA so “giống” trên cùng một thang màu với tranh. Ảnh chụp có vách núi xám, tranh có vách núi xanh; so ngay thì “giống” bị lệch. Trong mô hình, phép này làm trên lưới điểm, không phải pixel.

### Slide 24 · SSA: chỉ giữ một mảnh giống nhất

**Số lần bấm:** 5 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:** SSA hỏi bằng ảnh đã qua S-AdaIN. Đây là một điểm vách núi đang hỏi. Bấm: luật G2, bước một: khác nhãn thì cấm, chỉ còn vùng vách núi của tranh. Bấm: bước hai: trong vùng đó chỉ giữ đúng một điểm giống nhất, khung magenta; bốn khung đen là các ứng viên tiếp theo, bị bỏ. Chỉ còn một điểm thì trọng số của nó là 100 phần trăm, tức là copy nguyên mảnh đó. Bấm: mảnh bay sang đúng vị trí trong kết quả. Làm cho cả 144 điểm, ta được bức ghép bên phải: mỗi ô là một mảnh tranh thật, giữ nguyên nét cọ. Bấm: hết nhạt nhoà. Ý tưởng giống Style-Swap năm 2016, nhưng khoá trong vùng ngữ nghĩa và không cần train.

### Slide 25 · Ba ma trận attention, nhìn là thấy khác

**Số lần bấm:** 4 · **Thời lượng:** 2,5 phút

**Nói:** Mỗi ma trận: hàng là điểm của ảnh, ba trời và ba vách núi; cột là điểm của tranh. Ô càng đậm, trọng số càng lớn. Đây là UA: dày đặc, mỗi hàng trải khắp nơi; ô magenta là trọng số tràn sang vùng khác. Lỗi 1 nằm ở đó. Bấm: SCA, luật G1 gạch bỏ hai khối chéo, phần còn lại đều nhau vì hỏi bằng map phẳng. Hết loang lổ. Bấm: SSA, mỗi hàng giữ đúng một ô, luôn trong khối đúng. Hết nhạt nhoà. Bấm: nếu chỉ nhớ một hình của cả buổi, hãy nhớ hình này. Giá trị trong hình là minh hoạ.

### Slide 26 · Trộn hai nhánh: một nút chỉnh tông và nét

**Số lần bấm:** 5 · **Thời lượng:** 3 phút · **Nguồn:** tính minh hoạ + kết quả thật

**Nói:** Kết quả cuối là tông chung từ SCA, cộng nét cọ từ SSA, cộng bố cục của ảnh. Hai hệ số là một nút chỉnh. Đây là nút ở SSA thuần: toàn mảnh tranh thật, sắc nét nhưng màu nhảy giữa các ô. Bấm: kéo hết sang SCA thuần: đều màu nhưng phẳng. Bấm: SANet dùng 0,7 tông chung và 0,3 nét cọ. Bức ghép này tính trên lưới 12 nhân 12 nên còn thô. Bấm: bên phải là kết quả thật của SANet cộng SCSA trên cùng cặp ảnh, ở độ phân giải đầy đủ. Bấm: chốt, kết quả là tông chung cộng nét cọ cộng bố cục. Các mô hình khác dùng hệ số khác: StyTr2 là 1,2 và 0,5, StyleID là 0,8 và 0,2.

### Slide 27 · Cắm vào ba họ mô hình, không train lại

**Số lần bấm:** 5 · **Thời lượng:** 2,5 phút

**Nói:** Mỗi mô hình có một khối attention nằm giữa encoder và decoder. Đây là SANet, một mạng CNN, tỉ lệ trộn 0,7 và 0,3. Bấm: SCSA thay đúng khối đó; encoder, decoder và trọng số gốc giữ nguyên. Bấm: StyTr2, một transformer, tỉ lệ 1,2 và 0,5. Bấm: StyleID, một mô hình diffusion, tỉ lệ 0,8 và 0,2. Với StyleID có thêm chi tiết: hỏi thuần bằng map làm mất chi tiết, nên tác giả pha thêm feature của ảnh; chi tiết ở Appendix C của paper. Bấm: chốt, không train lại, dùng ngay với mô hình có sẵn.

## Chặng 5 · Kết quả (slide 28–35, ~18 phút)

### Slide 28 · Chặng 5 · Tốt tới đâu?

**Số lần bấm:** 1 · **Thời lượng:** 0,5 phút

**Nói:** Chặng 5, kết quả. Câu hỏi: tốt tới đâu? Ảnh thật, số thật từ paper, ablation, hạn chế, và cách chạy code.

### Slide 29 · Kết quả thật trên ba họ mô hình

**Số lần bấm:** 3 · **Thời lượng:** 3 phút · **Nguồn:** ảnh thật từ paper

**Nói:** Ba ví dụ lấy nguyên từ hình kết quả của paper. Mỗi hàng: ảnh nội dung, ảnh phong cách, mô hình gốc, và mô hình cộng SCSA. Hàng đầu là SANet, đúng cặp ảnh ta theo dõi cả buổi: vách núi chuyển từ màu trời sang màu núi. Bấm: StyTr2, ví dụ thác nước: bản gốc màu loang lổ, bản SCSA giữ dòng thác trắng và đá tối. Bấm: StyleID, ví dụ chân dung: áo, mặt, nền lấy nét từ đúng vùng tương ứng trong tranh. Mình chỉ mô tả những gì thấy trên ba ảnh này; con số tổng quát ở slide sau.

### Slide 30 · Bốn thước đo, đọc trước khi xem số

**Số lần bấm:** 5 · **Thời lượng:** 2,5 phút

**Nói:** Bốn thước đo, mỗi lần bấm một cái. SSL, Semantic Style Loss: cắt kết quả và tranh theo nhãn, rồi so style trời với trời, vách núi với vách núi. Thấp là tốt. Bấm: FID: cả tập kết quả có trông như tranh không, xét tổng thể. Thấp là tốt. Bấm: CFSD: kết quả còn giữ bố cục của ảnh gốc không. Thấp là tốt. Bấm: người xem: 40 người, 1.200 phiếu, so từng cặp có và không có SCSA. Cao là tốt. Bấm: lưu ý quan trọng: SSL do chính tác giả đề xuất và đo đúng điều SCSA tối ưu, nên SCSA thắng ở SSL gần như chắc chắn. Nhìn thêm FID và CFSD.

### Slide 31 · Lỗi style theo vùng giảm 29–47%

**Số lần bấm:** 3 · **Thời lượng:** 3 phút · **Nguồn:** số từ Table 1

**Nói:** Thước đo SSL, thấp là tốt. Cột xám là mô hình gốc: SANet 1,66, StyTr2 1,98, StyleID 1,75. Bấm: cột đen là cộng SCSA: 0,88, 1,22 và 1,24. Lỗi style theo vùng giảm 47, 38 và 29 phần trăm. SANet cộng SCSA còn có SSL tốt hơn cả năm phương pháp semantic chuyên biệt. Bấm: các thước đo khác. FID tốt hơn nhẹ ở cả ba, tức style tổng thể không tệ đi. CFSD: riêng StyleID cộng SCSA giữ bố cục kém hơn, 0,092 lên 0,118; đó là cái giá. Người xem chọn bản SCSA 83, 84 và 78 phần trăm. Số lấy từ Table 1, đánh giá trên 91 bộ do tác giả tự tuyển.

### Slide 32 · Bỏ bớt một mảnh, lỗi tăng bao nhiêu?

**Số lần bấm:** 5 · **Thời lượng:** 2,5 phút · **Nguồn:** số từ Fig. 6 và Appendix F

**Nói:** Thí nghiệm bỏ từng khối, trên StyleID. Đủ cả ba khối: 1,245, làm mốc. Bấm: bỏ SSA: 1,33, mất texture. Bấm: bỏ S-AdaIN: 1,76, kém chính xác, ít chi tiết. Bấm: bỏ SCA: 2,30, gần gấp đôi, lệch màu giữa các vùng. Bấm: SCA lo tông chung, SSA lo nét cọ; thiếu cái nào cũng tệ hơn. Một điểm nên phản biện: trên SANet, bỏ S-AdaIN gần như không đổi SSL, 0,876 so với 0,877. Với mô hình yếu hơn, không phải khối nào cũng cần. Số từ Fig. 6 và Appendix F.

### Slide 33 · Những điều SCSA chưa giải quyết

**Số lần bấm:** 3 · **Thời lượng:** 2,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:** Sáu điều SCSA chưa giải quyết. Hai điều nhìn thấy ngay trên ví dụ của ta. Một: phải tự có bản đồ nhãn, và nhãn hai bên phải khớp nhau; tác giả tự nêu điều này. Bấm: hai: SSA chỉ lấy một điểm, nên một mảnh tranh có thể bị dùng lại nhiều lần. Trên lưới minh hoạ, một mảnh bị dùng 19 lần, khung magenta. Ở độ phân giải thật, điều này có thể gây lặp texture. Bấm: bốn điều để thảo luận: chỉ 91 bộ dữ liệu tự tuyển; SSL do tác giả tự đặt; chậm và tốn bộ nhớ hơn; và nếu một vùng của ảnh không có vùng cùng nhãn bên tranh thì cả hàng bị cấm, paper không nói xử lý thế nào. Mỗi điều là một hướng mở rộng cho proposal.

### Slide 34 · Chạy code gốc trên đúng ví dụ này

**Số lần bấm:** 3 · **Thời lượng:** 2 phút · **Nguồn:** file thật trong repo

**Nói:** Bốn file bên trái chính là bộ bốn ta dùng cả buổi, nằm trong sem_data/29 của repo. Bấm: bốn lệnh. Clone repo; chạy sem.py để tạo mặt nạ nhãn từ semantic map; vào thư mục SANet+SCSA; chạy SCSA.py với mẫu 29. Môi trường là Python 3.8 và PyTorch 2.4.1; tải trọng số gốc của SANet vào thư mục models. Muốn so với bản gốc thì chạy SANet.py cùng ảnh. Bấm: lệnh đầy đủ có thêm hai cờ sem_map_64 và sem_map_32, trỏ tới sem_precomputed_feats/29. StyleID dùng tên cờ khác, và sem.py có bảng màu cứng theo số thư mục.

### Slide 35 · Chỉ lấy style từ vùng cùng nhãn

**Số lần bấm:** 3 · **Thời lượng:** 2 phút

**Nói:** Một câu mang về: chỉ lấy style từ vùng cùng nhãn. Bấm: đây là câu trả lời cho câu hỏi đầu buổi. SANet tô vách núi bằng màu vùng khác vì attention không biết nhãn vùng; SCSA cấm điều đó. Bấm: bên trong là hai cách nhìn. SCA lấy tông chung của cả vùng, SSA giữ nét cọ của một điểm. Không train lại, và lỗi style theo vùng giảm 29 đến 47 phần trăm. Nếu chỉ nhớ một hình: ba ma trận ở slide 25. Mình xin nhận câu hỏi.

## Câu hỏi thường gặp

| Câu hỏi | Trả lời ngắn |
| --- | --- |
| Không có semantic map thì sao? | Không dùng được: map là đầu vào bắt buộc. Hướng mở: sinh map bằng mô hình phân đoạn rồi khớp nhãn hai bên. |
| Vì sao SCA hỏi bằng map mà không bằng ảnh? | Để mọi điểm trong vùng hỏi cùng một câu, nhận cùng một tông. Hỏi bằng ảnh thì chỉ sửa được lỗi sai vùng. |
| Top-1 có làm lặp texture không? | Có thể. Trên lưới minh hoạ, một mảnh tranh bị SSA dùng lại 19 lần. Paper không đo điều này. |
| Vì sao StyleID + SCSA giữ bố cục kém hơn? | Paper không giải thích sâu. Giả thuyết: hỏi bằng map làm mất chi tiết, phần pha feature ảnh chưa bù đủ. |
| Có phải train gì không? | Không. Luật cấm chỉ thay điểm số bằng âm vô cực, trọng số của backbone giữ nguyên. |
| Số phần trăm trong các slide nền tảng có phải của paper? | Không. Đó là phép tính minh hoạ trên màu của ảnh mẫu 29. Số của paper chỉ ở slide SSL và ablation. |
| SSL có công bằng không? | Nó đo đúng mục tiêu nhưng do tác giả đề xuất. Nên nhìn kèm FID và CFSD. |
| Ký hiệu hay gặp trong paper? | F_c, F_s là lưới điểm của ảnh và tranh; F gạch ngang là bản đã chuẩn hoá; α1, α2 là hai hệ số trộn; μ đọc “miu”, σ đọc “xích-ma”. |

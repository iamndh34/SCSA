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
- Mỗi slide có vài **bước**. Bước đầu tự chạy khi bạn vào slide; mỗi “Bấm k” sau đó là một lần mũi tên phải. Lời thoại cũng hiện trong cửa sổ ghi chú (phím P), bước đang chiếu được tô sáng.
- Slide UA có một đoạn quét dài khoảng 8 giây sau “Bấm 1”: nói trong lúc nó chạy.

Cấu trúc: tổng quát trước, chi tiết sau. Mỗi chặng mở bằng một thẻ chương có câu hỏi riêng; lạc thì quay về thẻ chương hoặc slide “SCSA trong một phút”.

## Bảng tổng quan

| # | Slide | Số bước | Thời lượng | Nguồn hình |
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

**Số bước:** 1 · **Thời lượng:** 1 phút

**Nói:**

- **Mở đầu:** Chào mọi người. Hôm nay mình trình bày SCSA, paper CVPR 2025: dạy attention nhìn đúng vùng khi chuyển phong cách cho ảnh. Mình giả định mọi người chưa biết style transfer. Ba ảnh bên phải là thật, từ repo của tác giả: ảnh chụp Yosemite, một bức tranh núi, và kết quả tô ảnh theo tranh bằng SCSA. Cả buổi dùng đúng cặp ảnh này.

### Slide 2 · Cùng ảnh, cùng tranh, hai kết quả

**Số bước:** 3 · **Thời lượng:** 2 phút · **Nguồn:** ảnh thật từ paper

**Nói:**

- **Hai kết quả:** Kết quả thật trong paper, cùng một đầu vào ở giữa. Trái là SANet, mô hình có sẵn. Phải là SANet cộng SCSA.
- **Bấm 1 · Vách núi:** Nhìn vách núi lớn. SANet tô nó bằng màu kem của trời. SCSA tô đúng màu xanh của núi.
- **Bấm 2 · Câu hỏi:** Vì sao bên trái tô nhầm? Cả buổi trả lời câu này. Giữ nó trong đầu.

### Slide 3 · SCSA trong một phút

**Số bước:** 3 · **Thời lượng:** 2,5 phút

**Nói:**

- **Attention chọn style:** Cả paper trong một sơ đồ. Ảnh và tranh vào khối attention; khối này chọn mỗi điểm của ảnh lấy style từ đâu trong tranh. Nó chọn theo kiểu “trông giống”, nên tô nhầm vùng, như SANet vừa rồi.
- **Bấm 1 · Thêm nhãn vùng:** SCSA thêm bản đồ nhãn, mỗi màu một vùng. Attention chỉ lấy style từ vùng cùng nhãn, nên đúng vùng.
- **Bấm 2 · Hai cách nhìn:** Bên trong có hai cách. SCA nhìn cả vùng, lấy tông chung. SSA nhìn một điểm, lấy nét cọ, tức vệt sơn của tranh. Không train lại. Chưa cần hiểu hết, cả buổi đi từng cái.

### Slide 4 · Năm chặng, từ tổng quát tới chi tiết

**Số bước:** 2 · **Thời lượng:** 1 phút

**Nói:**

- **Năm chặng:** Mỗi chặng là một câu hỏi. Bối cảnh: style transfer là gì. Nền tảng: attention chọn style thế nào. Vấn đề: vì sao tô nhầm vùng. SCSA: sửa bằng cách nào. Kết quả: tốt tới đâu.
- **Bấm 1 · Trọng tâm:** Chặng 4 là trọng tâm. Lạc thì hỏi, mình quay về đầu chặng.

## Chặng 1 · Bối cảnh (slide 5–8, ~9 phút)

### Slide 5 · Chặng 1 · Style transfer là gì?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Chặng 1, bối cảnh. Câu hỏi: style transfer là gì?

### Slide 6 · Style transfer: giữ bố cục, thay lớp áo

**Số bước:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** ảnh thật

**Nói:**

- **Ảnh chụp:** Ảnh chụp cho bố cục: trời ở trên, vách núi ở giữa, rừng ở dưới.
- **Bấm 1 · Bức tranh:** Bức tranh cho lớp áo: màu, nét cọ, bề mặt.
- **Bấm 2 · Kết quả:** Bố cục cũ, áo mới. Để ý: trời mang màu kem của tranh, vách núi mang màu xanh của núi.
- **Bấm 3 · Arbitrary:** Một mô hình dùng cho mọi bức tranh, không train lại. Hỏi nhanh: vách núi bị tô màu trời có thành công không? Không: vẫn là áo của tranh, nhưng mặc sai chỗ.

### Slide 7 · Mười năm style transfer, năm bước

**Số bước:** 6 · **Thời lượng:** 3 phút

**Nói:**

- **2016 · Gatys:** Chỉnh từng pixel cho tới khi ảnh vừa giống bố cục, vừa giống màu tranh. Đẹp nhưng chậm, mỗi ảnh vài phút.
- **Bấm 1 · 2017 · AdaIN:** Một mạng cho mọi tranh, khớp tông cả ảnh. Nhanh nhưng thô. Sẽ gặp lại ở chặng 2.
- **Bấm 2 · 2019–22 · SANet, StyTr2:** Attention: mỗi điểm của ảnh tự đi tìm style.
- **Bấm 3 · 2024 · StyleID:** Attention bên trong Stable Diffusion.
- **Bấm 4 · 2025 · SCSA:** Attention biết nhãn vùng.
- **Bấm 5 · Khung cam:** Ba mô hình ở giữa là ba mô hình SCSA cắm vào. SCSA không thay chúng.

### Slide 8 · Semantic: mỗi ảnh có thêm một bản đồ nhãn

**Số bước:** 5 · **Thời lượng:** 2,5 phút · **Nguồn:** bản đồ nhãn thật trong repo

**Nói:**

- **Ảnh và tranh:** Ảnh chụp và bức tranh của ta.
- **Bấm 1 · Hai bản đồ nhãn:** Thêm hai bản đồ nhãn (semantic map). Mỗi màu là một vùng. Đây là file thật trong repo.
- **Bấm 2 · Màu là mã nhãn:** Đỏ là trời, vàng là vách núi, xanh lá là rừng, xanh dương là dãy xa. Màu chỉ là mã, không phải màu thật.
- **Bấm 3 · Nối cặp:** Nối đúng cặp: trời với trời, vách núi với vách núi.
- **Bấm 4 · Luật:** Mỗi vùng chỉ lấy style từ vùng cùng tên. Đầu vào giờ là bộ bốn: ảnh, map ảnh, tranh, map tranh. Ai vẽ map? Người dùng, hoặc mô hình phân đoạn. Paper không tự sinh map, đó là một hạn chế.

## Chặng 2 · Nền tảng (slide 9–14, ~17 phút)

### Slide 9 · Chặng 2 · Attention chọn style thế nào?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Chặng 2, nền tảng. Câu hỏi: attention chọn style thế nào? Bốn khái niệm: lưới điểm, attention, softmax với mask, AdaIN; rồi gộp lại thành Universal Attention. Đừng bỏ chặng này: SCSA chỉ là thay đổi nhỏ trên những thứ này.

### Slide 10 · Ảnh được cắt thành lưới điểm

**Số bước:** 4 · **Thời lượng:** 2,5 phút

**Nói:**

- **Ảnh 512×512:** Từ “điểm” dùng suốt phần sau. Đây là ảnh 512 nhân 512 pixel.
- **Bấm 1 · Lưới điểm:** Encoder cắt ảnh thành lưới. Ở đây 12×12 cho dễ nhìn; mô hình thật 64×64, tức 4.096 điểm.
- **Bấm 2 · Điểm là vector:** Mỗi điểm là một vector, ví dụ 512 số, mô tả mảng ảnh quanh nó: màu, cạnh, bề mặt. Không phải một pixel.
- **Bấm 3 · Decoder:** Decoder vẽ lưới ngược lại thành ảnh. SCSA chỉ sửa ở giữa, trên lưới điểm.

### Slide 11 · Attention: hỏi, so, cân, trộn

**Số bước:** 5 · **Thời lượng:** 4 phút

**Nói:**

- **Query:** Attention giống tra từ điển, nhưng mềm. Một điểm vách núi của ảnh hỏi: “style nào hợp với tôi?”. Đây là query.
- **Bấm 1 · Key và value:** Nó so với các điểm của tranh. Mỗi điểm có key để so và value để lấy về. Mình chỉ vẽ 4 trong 4.096 điểm: trời, dãy xa, vách núi, rừng. Mỗi điểm là một vị trí trên lưới, không phải pixel. Đường càng dày càng giống.
- **Bấm 2 · Trọng số:** Độ giống đổi thành trọng số: 35, 63, 1 và 1 phần trăm.
- **Bấm 3 · Trộn:** Màu chảy về theo trọng số rồi trộn lại.
- **Bấm 4 · Lỗi:** Chú ý: điểm vách núi xám nhạt giống dãy xa và trời của tranh hơn vách núi của tranh, nên 99% màu lấy từ sai vùng. Đó là lỗi ta thấy ở SANet. Số tính minh hoạ trên màu của ảnh mẫu, không phải số của mô hình thật.

### Slide 12 · Chia trọng số, và cách “cấm” một ô

**Số bước:** 4 · **Thời lượng:** 3,5 phút

**Nói:**

- **Điểm số:** Vẫn bốn điểm đó. Điểm số giống nhau: dãy xa cao nhất, khoảng 4,6; trời khoảng 4; vách núi và rừng quanh 0,5.
- **Bấm 1 · Softmax:** Đổi điểm số thành phần trăm, cộng lại đủ 100: 35, 63, 1, 1. Điểm cao được phần lớn, nhưng không ai bị bỏ hẳn.
- **Bấm 2 · Cấm:** Luật: điểm vách núi chỉ lấy từ vách núi, ba điểm kia bị cấm. Cách cấm: đặt âm vô cực vào điểm số của chúng; e mũ âm vô cực bằng 0 nên ba cột về đúng 0, vách núi nhận 100%. Không sửa gì khác, nên SCSA cắm được vào mô hình đã train.
- **Bấm 3 · Chốt:** Toàn bộ SCSA chỉ là quyết định ô nào bị cấm.

### Slide 13 · AdaIN: đổi tông bằng hai con số

**Số bước:** 4 · **Thời lượng:** 3 phút · **Nguồn:** phép tính thật trên pixel

**Nói:**

- **Tông của ảnh:** AdaIN là phương pháp 2017; SCSA dùng lại. Tông của một ảnh tóm trong hai số: μ là màu trung bình, σ là độ tương phản (đọc “miu” và “xích-ma”). Ảnh chụp này xám ấm.
- **Bấm 1 · Tông của tranh:** Bức tranh có μ, σ riêng: kem xanh, tương phản thấp hơn.
- **Bấm 2 · Khoác tông:** Bỏ μ, σ của ảnh, khoác μ, σ của tranh. Ảnh bên phải là phép tính thật trên pixel: cả ảnh ngả về tông của tranh. Trong mô hình, phép này làm trên lưới điểm, không phải pixel.
- **Bấm 3 · Giới hạn:** Chỉ một cặp số cho cả ảnh, nên trời, vách núi, rừng bị kéo về cùng một tông. S-AdaIN ở chặng 4 sẽ sửa.

### Slide 14 · Universal Attention: ai cũng nhìn tất cả

**Số bước:** 3 · **Thời lượng:** 3 phút

**Nói:**

- **Hai lưới:** Paper gọi khối attention của SANet, StyTr2, StyleID là Universal Attention, viết tắt UA. Trái: 144 điểm của ảnh. Phải: 144 điểm của tranh.
- **Bấm 1 · Quét:** Khung magenta là câu hỏi đang xét, chạy qua vài điểm. Mỗi lần nối tới 8 điểm tranh giống nhất (số 8 mình chọn cho dễ nhìn). Đường đen là cùng vùng, magenta là sang vùng khác. Chữ ở giữa là phần trăm trọng số sang vùng khác, tính trên cả 144 điểm. Đoạn này chạy khoảng 8 giây, nói trong lúc đó.
- **Bấm 2 · Chốt:** Mỗi điểm nhìn tất cả 144 thẻ, không ai hỏi điểm đó thuộc vùng nào. Với lưới thật 64×64, bảng so có 16 triệu ô. Số tính minh hoạ.

## Chặng 3 · Vấn đề (slide 15–18, ~10 phút)

### Slide 15 · Chặng 3 · Vì sao tô nhầm vùng?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Chặng 3, vấn đề. Câu hỏi: vì sao tô nhầm vùng? Ta chạy attention trên chính ảnh Yosemite và đếm xem bao nhiêu style lấy sai chỗ.

### Slide 16 · Lỗi 1: lấy style từ sai vùng

**Số bước:** 4 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ + ảnh thật của paper

**Nói:**

- **Bức ghép UA:** Chạy UA cho cả 144 điểm của ảnh. Mỗi ô là màu trộn mà điểm đó lấy về.
- **Bấm 1 · Phủ magenta:** Phủ magenta lên ô lấy style từ vùng khác, càng đậm càng nhiều. Trung bình 36% trọng số sang vùng sai; 36 trên 144 điểm lấy phần lớn style từ vùng sai, dồn vào vách núi.
- **Bấm 2 · Kết quả thật:** So với kết quả thật của SANet: đúng chỗ đó, vách núi mang màu trời.
- **Bấm 3 · Lỗi 1:** Phép tính của mình dùng màu trung bình nên chỉ là minh hoạ, nhưng nó chỉ ra cùng một chỗ sai với mô hình thật. Lỗi 1: lấy style từ sai vùng.

### Slide 17 · Lỗi 2 và 3: loang lổ, nhạt nhoà

**Số bước:** 3 · **Thời lượng:** 3 phút · **Nguồn:** dải trời cắt từ kết quả thật

**Nói:**

- **Lỗi 2 · loang lổ:** Dải trời cắt từ hai kết quả thật của paper. Trên là SANet: trời lẫn vệt xanh của núi, vì mỗi điểm tự chọn style theo cấu trúc riêng. Dưới là SANet cộng SCSA: cả vùng trời một tông, đó là điều ta muốn.
- **Bấm 1 · Lỗi 3 · nhạt nhoà:** Bốn điểm tranh mà điểm vách núi lấy nhiều nhất đều sắc nét, nhưng trộn lại thành màu đục, mất nét cọ.
- **Bấm 2 · Hai lỗi kéo ngược:** Lỗi 2 muốn các điểm trong vùng giống nhau; lỗi 3 muốn mỗi điểm giữ nét riêng. Vì vậy SCSA cần hai cách nhìn.

### Slide 18 · Ba lỗi, ba cách sửa

**Số bước:** 4 · **Thời lượng:** 2,5 phút

**Nói:**

- **Sai vùng:** Sửa bằng luật cấm theo nhãn, có sẵn trong cả SCA và SSA, nên lỗi 1 được sửa miễn phí.
- **Bấm 1 · Loang lổ:** Sửa bằng SCA: cả vùng dùng chung một tông.
- **Bấm 2 · Nhạt nhoà:** Sửa bằng SSA: chỉ lấy một điểm, giữ nguyên nét cọ.
- **Bấm 3 · Một gốc chung:** Cả ba lỗi chung một gốc: attention không biết nhãn vùng. Các slide sau phóng to cột phải.

## Chặng 4 · SCSA (slide 19–27, ~25 phút)

### Slide 19 · Chặng 4 · Sửa bằng cách nào?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Chặng 4, SCSA, phần trọng tâm. Câu hỏi: sửa bằng cách nào? Đi từ ý tưởng, sơ đồ, rồi từng khối: SCA, S-AdaIN, SSA, phép trộn.

### Slide 20 · Chỉ nhìn trong vùng cùng nhãn

**Số bước:** 4 · **Thời lượng:** 2,5 phút

**Nói:**

- **Câu cần nhớ:** Câu nhớ nhất của paper: chỉ nhìn trong vùng cùng nhãn. Đây là một điểm vách núi của ảnh.
- **Bấm 1 · SCA:** Cách nhìn thứ nhất. Nó nhìn tất cả điểm vách núi của tranh; vùng khác bị gạch chéo, tức bị cấm. Kết quả: tông chung của cả vùng.
- **Bấm 2 · SSA:** Cách nhìn thứ hai. Chỉ một đường nối, tới đúng một điểm vách núi giống nhất, lấy nguyên nét cọ (vệt sơn) của điểm đó.
- **Bấm 3 · Tên gọi:** S là Semantic, dùng nhãn vùng. C là Continuous, nhìn cả vùng, tức SCA. S là Sparse, thưa, một điểm, tức SSA. A là Attention.

### Slide 21 · Toàn cảnh: SCSA nằm ở giữa

**Số bước:** 6 · **Thời lượng:** 3,5 phút

**Nói:**

- **Đầu vào:** Bốn đầu vào: ảnh, map ảnh, tranh, map tranh. Encoder biến cả bốn thành lưới điểm.
- **Bấm 1 · SCA:** Nhánh trên: hỏi bằng map, lấy tông chung của cả vùng.
- **Bấm 2 · S-AdaIN và SSA:** Nhánh dưới hai bước: S-AdaIN đổi tông ảnh theo từng vùng, rồi SSA tìm một điểm giống nhất trong cùng vùng.
- **Bấm 3 · Trộn:** Trộn tông chung, nét cọ, và cộng bố cục của ảnh vào (đường đứt nét magenta).
- **Bấm 4 · Decoder:** Decoder vẽ ra ảnh.
- **Bấm 5 · Chốt:** Encoder, decoder giữ nguyên; chỉ ba khối ở giữa là SCSA.

### Slide 22 · SCA: hỏi bằng bản đồ nhãn

**Số bước:** 5 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:**

- **Câu hỏi từ map:** SCA khác UA ở hai chỗ. Chỗ một: câu hỏi không lấy từ ảnh mà từ bản đồ nhãn.
- **Bấm 1 · Cùng một câu:** Map là mảng màu phẳng, nên mọi điểm vách núi hỏi cùng một câu.
- **Bấm 2 · Luật G1:** Chỗ hai: khác nhãn thì cấm. Trọng số chia đều cho mọi điểm vách núi của tranh.
- **Bấm 3 · Bức ghép:** Mỗi điểm vách núi nhận cùng một màu: trung bình của vách núi trong tranh, màu xanh. Làm tương tự các vùng khác, ta được bức ghép bên phải, tính thật trên ảnh mẫu.
- **Bấm 4 · Ưu và nhược:** Liền mạch, đúng vùng, hết loang lổ. Cái giá: phẳng, mất nét cọ. Hỏi nhanh: giữ luật cấm mà hỏi bằng ảnh thì sửa được lỗi nào? Chỉ lỗi sai vùng.

### Slide 23 · S-AdaIN: đổi tông riêng từng vùng

**Số bước:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** phép tính thật trên pixel

**Nói:**

- **Ảnh gốc:** Nhớ AdaIN: hai số, màu trung bình và độ tương phản. Đây là ảnh gốc.
- **Bấm 1 · AdaIN cả ảnh:** Một cặp số cho mọi vùng, nên cả ảnh ngả một tông.
- **Bấm 2 · S-AdaIN:** Tính riêng cho từng vùng nhãn. Vách núi nhận tông xanh của vách núi trong tranh, dãy xa nhận tông hồng. Ba ảnh này là phép tính thật trên pixel.
- **Bấm 3 · Để làm gì:** Để SSA so “giống” trên cùng thang màu với tranh. Ảnh chụp có vách núi xám, tranh có vách núi xanh; so ngay thì bị lệch. Trong mô hình, phép này làm trên lưới điểm.

### Slide 24 · SSA: chỉ giữ một mảnh giống nhất

**Số bước:** 5 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:**

- **Câu hỏi:** SSA hỏi bằng ảnh đã qua S-AdaIN. Đây là một điểm vách núi đang hỏi.
- **Bấm 1 · Luật G2 · cấm:** Khác nhãn thì cấm, chỉ còn vùng vách núi của tranh.
- **Bấm 2 · Giữ một điểm:** Trong vùng đó chỉ giữ đúng một điểm giống nhất (khung magenta); bốn khung đen là ứng viên tiếp theo, bị bỏ. Chỉ còn một điểm thì trọng số 100%, tức copy nguyên mảnh đó.
- **Bấm 3 · Bức ghép:** Mảnh bay sang đúng vị trí trong kết quả. Làm cho cả 144 điểm: mỗi ô là một mảnh tranh thật, giữ nguyên nét cọ.
- **Bấm 4 · Chốt:** Hết nhạt nhoà. Ý tưởng giống Style-Swap 2016, nhưng khoá trong vùng ngữ nghĩa và không cần train.

### Slide 25 · Ba ma trận attention, nhìn là thấy khác

**Số bước:** 4 · **Thời lượng:** 2,5 phút

**Nói:**

- **UA:** Mỗi ma trận: hàng là điểm của ảnh (ba trời, ba vách núi), cột là điểm của tranh; ô càng đậm, trọng số càng lớn. UA dày đặc, mỗi hàng trải khắp nơi; ô magenta là trọng số tràn sang vùng khác. Lỗi 1 nằm ở đó.
- **Bấm 1 · SCA:** Luật G1 gạch bỏ hai khối chéo, phần còn lại đều nhau vì hỏi bằng map phẳng. Hết loang lổ.
- **Bấm 2 · SSA:** Mỗi hàng giữ đúng một ô, luôn trong khối đúng. Hết nhạt nhoà.
- **Bấm 3 · Chốt:** Nếu chỉ nhớ một hình của cả buổi, hãy nhớ hình này. Giá trị trong hình là minh hoạ.

### Slide 26 · Trộn hai nhánh: một nút chỉnh tông và nét

**Số bước:** 5 · **Thời lượng:** 3 phút · **Nguồn:** tính minh hoạ + kết quả thật

**Nói:**

- **SSA thuần:** Kết quả cuối là tông chung từ SCA, cộng nét cọ từ SSA, cộng bố cục của ảnh; hai hệ số là một nút chỉnh. Đây là nút ở SSA thuần: toàn mảnh tranh thật, sắc nét nhưng màu nhảy giữa các ô.
- **Bấm 1 · SCA thuần:** Kéo hết sang SCA: đều màu nhưng phẳng.
- **Bấm 2 · SANet dùng:** 0,7 tông chung và 0,3 nét cọ. Bức ghép này tính trên lưới 12×12 nên còn thô.
- **Bấm 3 · Kết quả thật:** Bên phải là kết quả thật của SANet cộng SCSA trên cùng cặp ảnh, ở độ phân giải đầy đủ.
- **Bấm 4 · Chốt:** Kết quả = tông chung + nét cọ + bố cục. Mô hình khác dùng hệ số khác: StyTr2 là 1,2 và 0,5; StyleID là 0,8 và 0,2.

### Slide 27 · Cắm vào ba họ mô hình, không train lại

**Số bước:** 5 · **Thời lượng:** 2,5 phút

**Nói:**

- **SANet:** Mỗi mô hình có một khối attention giữa encoder và decoder. Đây là SANet, một mạng CNN, tỉ lệ trộn 0,7 và 0,3.
- **Bấm 1 · SCSA thay khối:** SCSA thay đúng khối đó; encoder, decoder và trọng số gốc giữ nguyên.
- **Bấm 2 · StyTr2:** Một transformer, tỉ lệ 1,2 và 0,5.
- **Bấm 3 · StyleID:** Một mô hình diffusion, tỉ lệ 0,8 và 0,2. Hỏi thuần bằng map làm mất chi tiết nên tác giả pha thêm feature của ảnh (Appendix C).
- **Bấm 4 · Chốt:** Không train lại, dùng ngay với mô hình có sẵn.

## Chặng 5 · Kết quả (slide 28–35, ~18 phút)

### Slide 28 · Chặng 5 · Tốt tới đâu?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Chặng 5, kết quả. Câu hỏi: tốt tới đâu? Ảnh thật, số thật từ paper, ablation, hạn chế, và cách chạy code.

### Slide 29 · Kết quả thật trên ba họ mô hình

**Số bước:** 3 · **Thời lượng:** 3 phút · **Nguồn:** ảnh thật từ paper

**Nói:**

- **SANet:** Ba ví dụ lấy nguyên từ hình kết quả của paper. Mỗi hàng: ảnh nội dung, ảnh phong cách, mô hình gốc, mô hình cộng SCSA. Hàng đầu là cặp ảnh ta theo dõi cả buổi: vách núi từ màu trời sang màu núi.
- **Bấm 1 · StyTr2:** Ví dụ thác nước: bản gốc màu loang lổ, bản SCSA giữ dòng thác trắng và đá tối.
- **Bấm 2 · StyleID:** Ví dụ chân dung: áo, mặt, nền lấy nét từ đúng vùng tương ứng trong tranh. Mình chỉ mô tả những gì thấy trên ba ảnh; số tổng quát ở slide sau.

### Slide 30 · Bốn thước đo, đọc trước khi xem số

**Số bước:** 5 · **Thời lượng:** 2,5 phút

**Nói:**

- **SSL:** Bốn thước đo, mỗi lần bấm một cái. SSL (Semantic Style Loss): cắt kết quả và tranh theo nhãn, so style trời với trời, vách núi với vách núi. Thấp là tốt.
- **Bấm 1 · FID:** Cả tập kết quả có trông như tranh không, xét tổng thể. Thấp là tốt.
- **Bấm 2 · CFSD:** Kết quả còn giữ bố cục của ảnh gốc không. Thấp là tốt.
- **Bấm 3 · Người xem:** 40 người, 1.200 phiếu, so từng cặp có và không có SCSA. Cao là tốt.
- **Bấm 4 · Lưu ý:** SSL do chính tác giả đề xuất và đo đúng điều SCSA tối ưu, nên SCSA thắng ở SSL gần như chắc chắn. Nhìn thêm FID và CFSD.

### Slide 31 · Lỗi style theo vùng giảm 29–47%

**Số bước:** 3 · **Thời lượng:** 3 phút · **Nguồn:** số từ Table 1

**Nói:**

- **Mô hình gốc:** Thước đo SSL, thấp là tốt. Cột xám là mô hình gốc: SANet 1,66; StyTr2 1,98; StyleID 1,75.
- **Bấm 1 · Cộng SCSA:** Cột đen là cộng SCSA: 0,88; 1,22; 1,24. Lỗi style theo vùng giảm 47, 38 và 29%. SANet cộng SCSA còn tốt hơn cả năm phương pháp semantic chuyên biệt.
- **Bấm 2 · Thước đo khác:** FID tốt hơn nhẹ ở cả ba. CFSD: riêng StyleID cộng SCSA giữ bố cục kém hơn, 0,092 lên 0,118; đó là cái giá. Người xem chọn SCSA 83, 84 và 78%. Số từ Table 1, trên 91 bộ do tác giả tự tuyển.

### Slide 32 · Bỏ bớt một mảnh, lỗi tăng bao nhiêu?

**Số bước:** 5 · **Thời lượng:** 2,5 phút · **Nguồn:** số từ Fig. 6 và Appendix F

**Nói:**

- **Đủ cả ba:** Bỏ từng khối, trên StyleID. Đủ cả ba khối: 1,245, làm mốc.
- **Bấm 1 · Bỏ SSA:** 1,33: mất texture.
- **Bấm 2 · Bỏ S-AdaIN:** 1,76: kém chính xác, ít chi tiết.
- **Bấm 3 · Bỏ SCA:** 2,30, gần gấp đôi: lệch màu giữa các vùng.
- **Bấm 4 · Chốt:** SCA lo tông chung, SSA lo nét cọ; thiếu cái nào cũng tệ hơn. Phản biện: trên SANet, bỏ S-AdaIN gần như không đổi SSL (0,876 so với 0,877); với mô hình yếu hơn không phải khối nào cũng cần. Số từ Fig. 6 và Appendix F.

### Slide 33 · Những điều SCSA chưa giải quyết

**Số bước:** 3 · **Thời lượng:** 2,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:**

- **Cần map nhãn:** Sáu điều chưa giải quyết. Một: phải tự có bản đồ nhãn, và nhãn hai bên phải khớp; tác giả tự nêu điều này.
- **Bấm 1 · Dùng lại mảnh:** Hai: SSA chỉ lấy một điểm nên một mảnh tranh có thể bị dùng lại nhiều lần. Trên lưới minh hoạ, một mảnh bị dùng 19 lần (khung magenta). Ở độ phân giải thật có thể gây lặp texture.
- **Bấm 2 · Bốn điều thảo luận:** Chỉ 91 bộ tự tuyển. SSL do tác giả tự đặt. Chậm và tốn bộ nhớ hơn. Vùng của ảnh không có vùng cùng nhãn bên tranh thì cả hàng bị cấm, paper không nói xử lý thế nào. Mỗi điều là một hướng mở rộng cho proposal.

### Slide 34 · Chạy code gốc trên đúng ví dụ này

**Số bước:** 3 · **Thời lượng:** 2 phút · **Nguồn:** file thật trong repo

**Nói:**

- **Bốn file:** Bốn file bên trái chính là bộ bốn ta dùng cả buổi, trong sem_data/29 của repo.
- **Bấm 1 · Bốn lệnh:** Clone repo; chạy sem.py tạo mặt nạ nhãn; vào SANet+SCSA; chạy SCSA.py với mẫu 29. Môi trường Python 3.8, PyTorch 2.4.1; tải trọng số gốc của SANet vào thư mục models. Muốn so với bản gốc thì chạy SANet.py cùng ảnh.
- **Bấm 2 · Lệnh đầy đủ:** Có thêm hai cờ sem_map_64 và sem_map_32, trỏ tới sem_precomputed_feats/29. StyleID dùng tên cờ khác, và sem.py có bảng màu cứng theo số thư mục.

### Slide 35 · Chỉ lấy style từ vùng cùng nhãn

**Số bước:** 3 · **Thời lượng:** 2 phút

**Nói:**

- **Một câu:** Mang về một câu: chỉ lấy style từ vùng cùng nhãn.
- **Bấm 1 · Trước và sau:** Đây là câu trả lời cho câu hỏi đầu buổi: SANet tô vách núi bằng màu vùng khác vì attention không biết nhãn vùng; SCSA cấm điều đó.
- **Bấm 2 · Bên trong:** SCA lấy tông chung của cả vùng, SSA giữ nét cọ của một điểm. Không train lại; lỗi style theo vùng giảm 29–47%. Nếu chỉ nhớ một hình: ba ma trận ở slide 25. Mình xin nhận câu hỏi.

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

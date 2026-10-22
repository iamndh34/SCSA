# Script trình bày theo slide — SCSA giải thích từ đầu

> Bộ slide: https://claude.ai/artifact/2t8fvPSsiZs4HNHZDqPwUG (33 slide, 6 chặng)
> Paper: SCSA, CVPR 2025 (Highlight) — arXiv 2503.04119 · Code: github.com/scn-00/SCSA
> Soạn ngày 2026-10-22. Đối tượng nghe: người chưa biết style transfer, biết sơ qua mạng nơ-ron.
> Tổng thời lượng gợi ý: **75–85 phút** nói + 10–15 phút hỏi đáp.

## Cách dùng file này

- Mỗi slide có 4 phần: **Thời lượng**, **Nói** (lời thoại, đọc được nguyên văn), **Chỉ vào** (thao tác trên slide), **Chuyển** (câu nối sang slide sau).
- Chữ in nghiêng trong phần *Nói* là câu hỏi tương tác, dừng 3–5 giây cho người nghe nghĩ.
- Slide 12, 18, 21, 23 có animation tự chạy; các slide có "hiện dần" cần bấm Next để hiện từng bước. Bật chế độ Present trước khi bắt đầu.
- Nếu thiếu thời gian: cắt slide 5 (lịch sử), 24 (tính tay), 25 (backbone), 30 (code). Không cắt chặng 2 (nền tảng).

Cấu trúc trình bày: **tổng quát trước, chi tiết sau**. Mỗi chặng mở bằng một slide "nhìn từ trên xuống", rồi mới đi vào từng mảnh. Khi đang ở slide chi tiết mà thấy người nghe lạc, quay về slide tổng quát của chặng đó (slide 2, 14, 15, 16, 26).

---

## Chặng 0 · Mở đầu (slide 1–3, ~5 phút)

### Slide 1 · Bìa — "SCSA: dạy attention nhìn đúng chỗ"

**Thời lượng:** 1 phút

**Nói:**
Chào mọi người. Hôm nay mình trình bày một paper ở CVPR 2025, tên viết tắt là SCSA. Tên đầy đủ hơi dài, "Semantic Continuous-Sparse Attention for Arbitrary Semantic Style Transfer", nhưng mình sẽ không bắt mọi người nhớ tên này. Đến cuối buổi, mọi người sẽ tự giải nghĩa được từng từ trong đó.

Mình giả định mọi người chưa biết style transfer là gì, nên buổi hôm nay đi từ con số 0. Ai đã biết rồi thì phần đầu sẽ hơi chậm, xin kiên nhẫn một chút, phần sau sẽ có nhiều thứ mới.

**Chỉ vào:** Hình bên phải: ảnh chụp (trời, đồi, nhà) cộng bức tranh (trời xoáy xanh, đất sọc nâu) cho ra ảnh kết quả. Chỉ vào trời trong kết quả: "trời mang nét xoáy của trời trong tranh". Chỉ vào đất: "đất mang nét sọc của đất trong tranh".

**Chuyển:** "Trước khi đi vào chi tiết, mình tóm cả paper trong một phút."

---

### Slide 2 · Tổng quan — "SCSA trong một phút"

**Thời lượng:** 2–3 phút

**Nói:**
Mọi paper đều trả lời bốn câu hỏi: làm gì, vướng gì, giải quyết thế nào, tốt đến đâu. Slide này là bốn câu trả lời ngắn, cả buổi hôm nay chỉ là phóng to từng ô.

(Bấm hiện ô 1) **Bài toán.** Có một ảnh chụp và một bức tranh. Muốn tô phong cách của tranh lên ảnh chụp, nhưng có điều kiện: trời trong ảnh phải lấy nét từ trời trong tranh, đất phải lấy từ đất. Nghe hiển nhiên, nhưng máy không tự hiểu.

(Bấm hiện ô 2) **Vấn đề.** Các mô hình tốt nhất hiện nay dùng một cơ chế gọi là attention. Attention chọn style theo kiểu "điểm nào trong tranh trông giống điểm này", chứ không hỏi "điểm này là trời hay đất". Hậu quả là ba lỗi: lấy sai vùng, cùng một vùng mà loang lổ, và nét cọ bị nhạt nhoà.

(Bấm hiện ô 3) **Giải pháp.** SCSA cho attention biết nhãn vùng, rồi chỉ cho phép nó nhìn trong vùng cùng nhãn. Trong vùng đó nó làm hai việc: nhìn cả vùng để lấy tông màu chung, và nhìn đúng một điểm để lấy nét cọ.

(Bấm hiện ô 4) **Kết quả.** Không cần huấn luyện lại gì cả. Cắm vào ba mô hình có sẵn, lỗi style theo vùng giảm 29 đến 47 phần trăm, và khi cho người xem chọn, 78 đến 84 phần trăm chọn bản có SCSA.

(Bấm hiện hộp cam) Nếu chỉ nhớ một câu thì nhớ câu này: *SCSA cho attention biết "điểm này là trời hay đất", rồi chỉ cho phép nó lấy style từ vùng cùng tên trong tranh.*

**Chỉ vào:** Đọc từng ô theo thứ tự hiện. Khi đọc hộp cam, dừng lại và đọc chậm.

**Chuyển:** "Mọi người chưa cần hiểu 'attention' là gì. Giờ mình nói lộ trình đi."

---

### Slide 3 · Lộ trình — "Năm chặng, từ tổng quát đến chi tiết"

**Thời lượng:** 1 phút

**Nói:**
Năm chặng. Chặng 1, bối cảnh: style transfer là gì và đã phát triển ra sao. Chặng 2, nền tảng: bốn khái niệm kỹ thuật, mỗi khái niệm một slide, để đọc được công thức ở phần sau. Chặng 3, vấn đề: ba lỗi mình vừa nhắc, lần này nhìn tận mắt. Chặng 4, trọng tâm: SCSA, đi từ ý tưởng, sơ đồ, rồi từng khối. Chặng 5, kết quả: cách đọc số, số thật, hạn chế, và chạy code.

Mỗi chặng mở bằng một slide tổng quát rồi mới chi tiết. Nếu lúc nào thấy lạc, cứ hỏi, mình quay về slide tổng quát của chặng đó. Hai slide cuối là phụ lục: công thức đầy đủ và từ điển thuật ngữ, ai cần tra thì tra. Trong phần chính mình không đọc công thức, chỉ nói bằng lời.

**Chuyển:** "Bắt đầu chặng 1: style transfer là gì."

---

## Chặng 1 · Bối cảnh (slide 4–6, ~8 phút)

### Slide 4 · "Style transfer: giữ bố cục, thay lớp áo"

**Thời lượng:** 3 phút

**Nói:**
(Bấm hiện ảnh content) Đây là ảnh nội dung, tiếng Anh là content. Nó cho biết bố cục: trời ở trên, đồi ở dưới, nhà ở đây. Chỉ bố cục thôi.

(Bấm hiện tranh style) Đây là ảnh phong cách, style. Nó cho biết "lớp áo": màu sắc gì, nét cọ ra sao, bề mặt sần hay mịn. Mình dùng từ "lớp áo" vì nó đúng nghĩa: mình muốn giữ nguyên cơ thể, chỉ thay áo.

(Bấm hiện kết quả) Kết quả: bố cục của ảnh content, mặc lớp áo của tranh. Nhìn kỹ: trời được vẽ lại bằng nét xoáy của trời trong tranh, đồi được vẽ bằng nét sọc của đất trong tranh.

Một từ nữa trên slide: **arbitrary**. Nghĩa là một mô hình dùng được cho mọi bức tranh. Đưa tranh Van Gogh cũng được, tranh Đông Hồ cũng được, không phải huấn luyện lại cho từng tranh.

*Câu hỏi cho mọi người: ở ảnh kết quả, nếu trời bị tô nét sọc nâu của đất thì có coi là style transfer thành công không?* Đúng, vẫn là "mặc áo của tranh", nhưng mặc sai chỗ. Đó chính là thứ paper này quan tâm.

**Chỉ vào:** Khi nói "nét xoáy", chỉ vào trời trong kết quả. Khi nói "nét sọc", chỉ vào đồi.

**Chuyển:** "Bài toán này đã có mười năm lịch sử. Mình điểm nhanh năm mốc."

---

### Slide 5 · "Mười năm style transfer, trong năm bước"

**Thời lượng:** 3 phút (có thể cắt còn 1 phút)

**Nói:**
(Bấm từng mốc)
**2016, Gatys.** Người đầu tiên làm được bằng mạng nơ-ron. Cách làm: lấy một ảnh trắng, chỉnh từng pixel cho đến khi nó vừa giống bố cục content vừa giống thống kê màu của tranh. Đẹp, nhưng mỗi ảnh tối ưu vài phút.

**2017, AdaIN và WCT.** Một mạng cho mọi style, chạy một lần là xong. Ý tưởng: lấy trung bình và độ lệch chuẩn của tranh áp lên ảnh. Nhanh, nhưng thô: cả ảnh bị kéo về cùng một tông. Mình sẽ giải thích AdaIN kỹ ở slide 10 vì SCSA dùng lại nó.

**2019 đến 2022, SANet và StyTr2.** Bước nhảy lớn: dùng attention. Mỗi điểm trên ảnh content tự đi tìm điểm trong tranh giống nó nhất rồi lấy style ở đó. Chi tiết hơn hẳn. SANet dùng mạng tích chập, StyTr2 dùng transformer.

**2024, StyleID.** Dùng mô hình diffusion, cụ thể là Stable Diffusion, không cần train. Vẫn là attention, chỉ là attention nằm trong U-Net của diffusion.

**2025, SCSA.** Thêm ngữ nghĩa vào attention.

Điểm quan trọng ở dòng cuối: SCSA không thay thế các mô hình kia. Nó là một mảnh ghép cắm vào SANet, StyTr2 và StyleID. Ba mô hình này đều có một khối attention, SCSA thay đúng khối đó.

**Chỉ vào:** Khoanh ba mốc 2019–2024 bằng tay: "ba cái này là ba backbone mà SCSA sẽ cắm vào".

**Chuyển:** "Giờ nói rõ hơn bài toán có thêm chữ 'semantic' nghĩa là gì."

---

### Slide 6 · "Semantic style transfer: thêm bản đồ ngữ nghĩa"

**Thời lượng:** 3 phút

**Nói:**
(Bấm hiện hai ảnh) Vẫn là ảnh content và tranh style như nãy.

(Bấm hiện hai map) Giờ thêm hai ảnh nữa, gọi là bản đồ ngữ nghĩa, semantic map. Mỗi map là ảnh tô màu theo nhãn: vùng trời tô một màu, vùng đất tô màu khác. Màu ở đây không phải màu thật, chỉ là mã nhãn. Quy ước duy nhất: cùng màu nghĩa là cùng ý nghĩa, ở cả hai map.

Vậy đầu vào giờ là bộ bốn: ảnh content, map của nó, tranh style, map của tranh. Ký hiệu trong paper: I_c, I_csem, I_s, I_ssem. Chữ "sem" là semantic.

(Bấm hiện hộp xanh đậm) Yêu cầu: vùng "trời" trong kết quả chỉ được lấy style từ vùng "trời" của tranh, "đất" lấy từ "đất".

*Ai cung cấp map này?* Người dùng. Tự vẽ hoặc dùng mô hình phân đoạn ảnh. Paper không tự sinh map, đây là một hạn chế mình sẽ nhắc lại ở cuối.

**Chỉ vào:** Chỉ vào hai ô màu trong chú giải: "xanh là trời, vàng là đất, ở cả hai map".

**Chuyển:** "Để hiểu mô hình làm gì với bộ bốn này, cần bốn khái niệm nền. Chặng 2."

---

## Chặng 2 · Nền tảng (slide 7–11, ~15 phút)

### Slide 7 · "Từ ảnh ra lưới điểm, từ lưới điểm ra ảnh"

**Thời lượng:** 3 phút

**Nói:**
Đây là khái niệm quan trọng nhất của chặng này, vì từ "điểm" sẽ xuất hiện trong mọi slide sau.

(Bấm hiện ảnh vào) Ảnh vào, ví dụ 512 nhân 512 pixel.

(Bấm hiện encoder) Qua một mạng gọi là encoder. Encoder nén ảnh lại.

(Bấm hiện lưới) Ra một lưới nhỏ hơn, ví dụ 64 nhân 64. Mỗi ô trên lưới gọi là một **điểm**. Nhưng mỗi điểm không phải một màu, mà là một vector dài, ví dụ 512 con số. Vector đó tóm tắt mảng ảnh quanh điểm: màu gì, có cạnh không, cạnh hướng nào, bề mặt ra sao.

Hai điểm "trông giống nhau" thì vector gần nhau. Hãy nhớ câu này, vì attention sẽ so vector để tìm "giống".

(Bấm hiện decoder và ảnh ra) Decoder làm ngược lại: từ lưới vẽ ra ảnh. Nếu không sửa gì ở giữa thì ảnh ra gần như ảnh vào.

(Bấm hiện ba thẻ dưới) Ba điều cần nhớ. Một: từ giờ "điểm" nghĩa là ô trên lưới, không phải pixel; 512 nhân 512 pixel chỉ còn 4.096 điểm. Hai: mỗi điểm mang một vector mô tả. Ba: style transfer kiểu attention làm việc ở giữa: lấy lưới của ảnh content, sửa từng ô bằng thông tin từ lưới của tranh, rồi decode. SCSA cũng nằm ở giữa. Encoder, decoder không đụng đến.

**Chỉ vào:** Ô viền cam trên lưới: "đây là một điểm, nó mang 512 số".

**Chuyển:** "Giờ câu hỏi là: sửa từng ô bằng thông tin từ tranh như thế nào? Đó là attention."

---

### Slide 8 · "Attention = tra cứu mềm: hỏi, so khớp, pha trộn"

**Thời lượng:** 4 phút

**Nói:**
Attention nghe đáng sợ nhưng bản chất là tra cứu. Có ba vai: Query, Key, Value. Mình gọi là Q, K, V.

**Q, query.** Mỗi điểm content đặt một câu hỏi: "tôi trông thế này, style nào hợp với tôi?"

**K, key.** Mỗi điểm trong tranh có một thẻ mô tả để so khớp với câu hỏi.

**V, value.** Thứ thật sự được lấy về: màu, nét cọ, texture của điểm trong tranh.

(Bấm hiện ô Q) Ví dụ: một điểm trên trời của ảnh content.

(Bấm hiện bốn ô tranh và mũi tên) Nó so với bốn điểm trong tranh. Mũi tên càng dày, càng giống.

(Bấm hiện trọng số) Độ giống được đổi thành trọng số: 0,55; 0,25; 0,15; 0,05. Tổng bằng 1. Phép đổi này gọi là softmax, slide sau mình tính tay.

(Bấm hiện ô kết quả) Kết quả là pha trộn: 55% màu của ô một, 25% ô hai, và cứ thế. Nhìn ô kết quả: trộn xanh, vàng, cam, nâu cho ra một màu xám đục.

Dòng dưới cùng tóm lại: trọng số là softmax của độ giống, kết quả là trung bình có trọng số của V. Chỉ có vậy, không có công thức nào khác.

*Mọi người để ý màu xám đục đó. Nó là mầm mống của một trong ba lỗi mình sẽ nói ở chặng 3.* Trộn nhiều màu sắc nét thì ra màu đục.

**Chỉ vào:** Khi nói "tra cứu", so sánh với tra từ điển: Q là từ cần tra, K là mục từ, V là phần giải nghĩa. Khác từ điển ở chỗ attention không lấy một mục, mà lấy tất cả các mục với trọng số khác nhau, nên gọi là "mềm".

**Chuyển:** "Softmax vừa nhắc là gì, và quan trọng hơn, làm sao cấm attention nhìn một chỗ nào đó? Slide sau."

---

### Slide 9 · "Softmax và mask −∞: đủ để hiểu SCSA"

**Thời lượng:** 4 phút

**Nói:**
Slide này hơi có số, nhưng mình tính cùng mọi người, chỉ cần máy tính bỏ túi.

(Bấm hiện thẻ trái) **Softmax.** Có ba điểm số: 2,0; 1,0; 0,5. Lấy e mũ từng số: 7,39; 2,72; 1,65. Cộng lại: 11,76. Chia từng số cho tổng: 0,63; 0,23; 0,14. Đó là trọng số. Hai tính chất: tất cả dương, tổng bằng 1. Điểm cao được phần lớn, nhưng không ai bị bỏ hẳn, kể cả điểm 0,5 vẫn được 14%.

(Bấm hiện thẻ phải) **Mask.** Giờ mình muốn cấm k2. Cách làm: thay điểm số của k2 bằng âm vô cực. e mũ âm vô cực bằng 0. Tổng còn 9,04. Chia lại: k1 được 0,82, k2 được đúng 0, k3 được 0,18. Vẫn tổng bằng 1.

Để ý: mình không "xoá" k2 rồi viết lại công thức. Chỉ thay một con số, softmax tự lo phần còn lại. Vì thế có thể cắm mask vào attention có sẵn mà không sửa gì khác. Đây chính là lý do kỹ thuật khiến SCSA cắm được vào mô hình đã train.

(Bấm hiện hộp xanh đậm) Và đây là câu quan trọng: toàn bộ SCSA chỉ làm một việc với bảng điểm attention: quyết định ô nào bị cấm. SCA cấm mọi ô khác nhãn. SSA cấm tất cả trừ một ô. Hết. Nếu mọi người hiểu slide này, phần công thức ở chặng 4 sẽ không có gì mới.

**Chỉ vào:** Dòng k2 màu cam trong bảng phải. Chỉ vào ô "0" và nói "đúng bằng không, không phải gần không".

**Chuyển:** "Khái niệm cuối của chặng này: AdaIN. SCSA có một khối tên S-AdaIN, cần hiểu gốc của nó."

---

### Slide 10 · "AdaIN: đổi tông của ảnh bằng hai con số"

**Thời lượng:** 3 phút

**Nói:**
AdaIN là phương pháp 2017 ở slide lịch sử. Dòng trên cùng là hai bước: bỏ tông của content, rồi khoác tông của tranh. Chỉ cần hai con số: μ là trung bình, σ là độ lệch chuẩn.

(Bấm hiện thẻ 1) Lấy ví dụ content có ba giá trị 1, 3, 5. Trung bình 3, độ lệch chuẩn khoảng 1,6.

(Bấm hiện thẻ 2) Bước một: trừ trung bình, chia độ lệch chuẩn. Ra −1,2; 0; 1,2. Giờ trung bình bằng 0, độ lệch chuẩn bằng 1. Đây gọi là chuẩn hoá. Ký hiệu F với gạch ngang trên đầu trong công thức attention chính là bước này. Nhớ cái này, lát gặp lại.

(Bấm hiện thẻ 3) Bước hai: nhân với độ lệch chuẩn của tranh, cộng trung bình của tranh. Giả sử tranh có μ = 8, σ = 2. Ra 5,6; 8; 10,4. Giá trị content giờ "sống" trong thang của tranh.

(Bấm hiện hai thẻ dưới) Trực giác: μ là tông chung, sáng hay tối, ngả xanh hay ngả vàng. σ là độ tương phản, nét mạnh hay nhẹ. Khớp hai số này là chuyển được phần lớn "không khí" của tranh.

Giới hạn: AdaIN gốc tính một cặp μ, σ cho cả ảnh. Thế nên trời và đất bị kéo về cùng một tông. Ở chặng 4 có S-AdaIN: tính riêng μ, σ cho từng vùng nhãn. Chỉ khác đúng chỗ đó.

**Chỉ vào:** Khi nói "F gạch ngang", viết ký hiệu lên bảng nếu có bảng.

**Chuyển:** "Giờ ghép tất cả lại thành khối attention mà SCSA sẽ thay."

---

### Slide 11 · "Universal Attention: khối mà SCSA sẽ thay"

**Thời lượng:** 3 phút

**Nói:**
Paper gọi khối attention trong SANet, StyTr2, StyleID là Universal Attention, viết tắt UA. "Universal" vì mỗi điểm nhìn tất cả.

Ba bước, đọc bằng những gì vừa học. Một, hỏi: mỗi điểm content đặt câu hỏi Q; mỗi điểm style mang thẻ K và nội dung V. Hai, so: so mọi câu hỏi với mọi thẻ, ra một bảng điểm, mỗi điểm content một hàng. Với 4.096 điểm mỗi bên, bảng này có 16 triệu ô. Ba, trộn: softmax từng hàng thành trọng số, lấy trung bình có trọng số các V, rồi cộng ngược content vào để giữ bố cục.

Bảng dưới chỉ nói Q, K, V lấy từ đâu. Công thức đầy đủ nằm ở slide phụ lục, không cần nhớ.

Câu chốt ở dòng cuối: mỗi điểm content được nhìn tất cả điểm style. Không ai hỏi điểm đó thuộc vùng nào. Đó là gốc của mọi vấn đề.

**Chỉ vào:** Ô viền cam trong lưới: "đây là một query; hàng tương ứng trong bảng S có điểm số cho mọi điểm style, kể cả điểm thuộc vùng đất".

**Chuyển:** "Chặng 3. Giờ xem tận mắt chuyện gì xảy ra khi ai cũng nhìn tất cả."

---

## Chặng 3 · Vấn đề (slide 12–14, ~10 phút)

### Slide 12 · "Attention toàn cục lấy style từ sai vùng" (animation)

**Thời lượng:** 4 phút

**Nói:**
Slide này tự chạy. Mình giải thích cách đọc trước, rồi để nó chạy một vòng.

Bên trái là ảnh content thu nhỏ thành 20 điểm: hai hàng trên là trời, hai hàng dưới là đất. Giữa là tranh, cũng 20 điểm: trời xanh có vài ô vàng là sao, đất nâu. Bên phải là kết quả, tô dần.

Ô viền cam bên trái là query đang xét. Các đường nối từ nó sang tranh là trọng số attention: càng dày càng nặng. Đường màu xanh đậm là nối đúng vùng. Đường màu cam là nối sang vùng sai nhãn.

(Để animation chạy) Nhìn: điểm trời này có đường cam sang đất. Dòng chữ giữa nói bao nhiêu phần trăm trọng số rơi vào vùng sai. Và nhìn kết quả bên phải: vài ô trời bị tô nâu.

Vì sao? Vì attention chọn theo "trông giống về cấu trúc", không theo ý nghĩa. Một mảng trời phẳng và một mảng đất phẳng có vector gần nhau, nên nó lấy nhầm.

Lưu ý: số trong animation là dữ liệu đồ chơi mình tự tạo để minh hoạ cơ chế, không phải số đo từ paper. Paper có ảnh thật ở Fig. 1 và Fig. 7.

Đây là **lỗi 1: sai vùng**.

**Chỉ vào:** Dừng ở một điểm trời có đường cam, chỉ vào ô kết quả tương ứng bị nâu.

**Chuyển:** "Còn hai lỗi nữa, tinh tế hơn."

---

### Slide 13 · "Hai lỗi nữa: loang lổ và nhạt nhoà"

**Thời lượng:** 3 phút

**Nói:**
**Lỗi 2, không liên tục.** Hai điểm trời cạnh nhau, cấu trúc hơi khác nhau một chút, thế là chọn hai điểm style khác hẳn. Nhìn hàng ô trên: xanh, vàng, xanh đậm, nâu, xanh nhạt, nâu. Bầu trời bị vá chằng vá đụp. Mong muốn là hàng dưới: cùng một không khí trời, chỉ khác nhau chút ít. Paper gọi đây là "discontinuous stylization".

**Lỗi 3, trung bình hoá.** Nhớ ô màu xám đục ở slide attention? Khi kết quả là trung bình của nhiều điểm style, màu sắc nét bị pha thành đục. Hình bên phải: xanh đậm cộng vàng sao cộng xanh nhạt cộng vàng trăng, chia đều, ra xám. Nét cọ mất, texture thành "khối mờ". Paper gọi là "block textures".

Để ý mỗi lỗi có một dòng cam: lỗi 2 sửa bằng SCA, lỗi 3 sửa bằng SSA. Đó là hai nửa của cái tên "Continuous-Sparse".

*Câu hỏi: hai lỗi này có vẻ ngược nhau không?* Lỗi 2 muốn các điểm trong vùng giống nhau hơn. Lỗi 3 muốn mỗi điểm giữ nguyên nét riêng. Đúng, chúng kéo hai hướng. Vì thế SCSA cần hai attention, không phải một.

**Chỉ vào:** Hàng ô loang lổ rồi hàng ô đều; sau đó dãy bốn ô màu và ô xám.

**Chuyển:** "Tổng kết ba lỗi thành một bảng, bảng này là bản đồ cho cả chặng sau."

---

### Slide 14 · "Ba lỗi, ba mảnh ghép"

**Thời lượng:** 3 phút

**Nói:**
Đọc bảng theo hàng.

Hàng 1, sai vùng. Thấy gì: trời mang màu đất. Vì sao: attention nhìn mọi điểm, chọn theo trông giống. Sửa bằng: mask theo nhãn, đặt âm vô cực vào mọi ô khác nhãn. Mask này có trong cả hai attention của SCSA, nên lỗi 1 được sửa "miễn phí", không cần khối riêng.

Hàng 2, loang lổ. Vì sao: mỗi điểm tự chọn theo cấu trúc riêng. Sửa bằng SCA: lấy Q và K từ bản đồ nhãn thay vì từ ảnh. Bản đồ nhãn là mảng màu phẳng, nên mọi điểm trời có cùng câu hỏi, cùng câu trả lời, cùng nhận "style trung bình của vùng trời". Liên tục.

Hàng 3, nhạt nhoà. Vì sao: trung bình của nhiều điểm. Sửa bằng SSA: chỉ giữ một điểm giống nhất trong vùng, copy nguyên nét.

(Bấm hiện hộp xanh đậm) Cả ba lỗi chung một gốc: attention không biết nhãn vùng. SCSA bổ sung đúng mảnh đó. Phần còn lại của mô hình giữ nguyên.

Mọi người nhớ cột cuối. Mọi slide tiếp theo chỉ giải thích chi tiết từng ô của cột đó.

**Chỉ vào:** Lướt tay dọc cột "SCSA sửa bằng".

**Chuyển:** "Chặng 4, phần chính. Bắt đầu từ một câu."

---

## Chặng 4 · Phương pháp SCSA (slide 15–25, ~30 phút)

### Slide 15 · "Chỉ nhìn trong vùng cùng nhãn" (ý tưởng cốt lõi)

**Thời lượng:** 2 phút

**Nói:**
Đây là câu cần nhớ nhất của cả paper. Chỉ nhìn trong vùng cùng nhãn. Trong vùng đó: nhìn **tất cả** để lấy không khí, nhìn **một điểm** để lấy nét cọ.

Giờ giải nghĩa cái tên. S-C-S-A. **Semantic**: dùng nhãn vùng. **Continuous**: nhìn liên tục cả vùng, đó là SCA. **Sparse**: thưa, chỉ nhìn một điểm, đó là SSA. **Attention**: vẫn là attention.

Ba thẻ dưới: SCA cho style tổng thể. SSA cho texture sắc nét. Plug-and-play: thay khối attention có sẵn, không huấn luyện lại.

**Chỉ vào:** Khi giải nghĩa từng chữ, chỉ vào tiêu đề slide.

**Chuyển:** "Từ câu này đến sơ đồ."

---

### Slide 16 · "Toàn cảnh: SCSA nằm giữa encoder và decoder"

**Thời lượng:** 4 phút

**Nói:**
Sơ đồ hiện cả một lúc; chỉ tay đi từ trái sang phải.

(Chỉ cột trái) Bốn đầu vào: ảnh content, map của nó, tranh, map của tranh.

(Chỉ Encoder) Encoder biến cả bốn thành lưới điểm. Kể cả hai map cũng đi qua encoder.

(Chỉ SCA, nhánh trên) SCA hỏi bằng map, không phải ảnh, và lấy tông chung của cả vùng cùng nhãn trong tranh.

(Chỉ nhánh dưới) Hai bước. S-AdaIN đổi tông của content theo từng vùng, mục đích là làm sạch câu hỏi. Rồi SSA tìm một điểm style giống nhất trong cùng vùng.

(Chỉ Trộn) Trộn: tông chung từ SCA, cộng nét cọ từ SSA, cộng content. Đường cam nét đứt: content sau S-AdaIN được cộng vào để giữ bố cục.

(Chỉ Decoder) Decoder vẽ ra ảnh.

Dòng cuối: encoder, decoder và các lớp chiếu đều của backbone, giữ nguyên. Chỉ khối attention được thay. Với StyleID thì encoder là VAE cộng DDIM inversion, và khối attention là self-attention trong U-Net; chi tiết đó ở slide backbone.

Giờ mình đi từng khối: SCA trước, S-AdaIN, rồi SSA, rồi trộn.

**Chỉ vào:** Vẽ vòng tròn quanh ba khối SCA, S-AdaIN, SSA: "ba khối này là toàn bộ SCSA".

**Chuyển:** "Khối thứ nhất: SCA."

---

### Slide 17 · "SCA: hỏi bằng bản đồ nhãn, lấy style từ tranh"

**Thời lượng:** 4 phút

**Nói:**
Hộp bên trái, so với UA ở slide 11 chỉ khác hai chỗ.

Chỗ một: Q1 lấy từ feature của **map content**, K1 lấy từ feature của **map style**. Không phải ảnh. V1 vẫn từ ảnh style, vì style thật phải đến từ tranh.

Chỗ hai: luật G1, khác nhãn thì cấm. Như slide 9, cấm nghĩa là trọng số đúng bằng 0.

Bên phải: vì sao gọi là "continuous"? Ba bước. Một: map là mảng màu phẳng, nên mọi điểm trời có Q1 gần như giống hệt nhau. Hai: cùng Q1 thì cùng một hàng attention; sau mask, trọng số trải đều lên mọi điểm style cùng nhãn. Ba: mọi điểm trời nhận cùng một "style trung bình của trời trong tranh". Liên tục, đúng tông, không còn loang lổ.

Cái giá: phẳng, mất nét cọ. Đó là việc của SSA.

*Hỏi nhanh: nếu mình lấy Q1, K1 từ ảnh thay vì map, chỉ giữ mask G1, thì sửa được lỗi nào?* Chỉ lỗi 1, sai vùng. Lỗi 2, loang lổ, vẫn còn vì mỗi điểm vẫn chọn theo cấu trúc riêng. Lấy Q, K từ map chính là mẹo để sửa lỗi 2.

**Chỉ vào:** Hai dòng Q1, K1 có chữ "từ map" màu cam.

**Chuyển:** "Xem SCA chạy trên dữ liệu đồ chơi lúc nãy."

---

### Slide 18 · "SCA: không còn đường cam, nhưng trời phẳng một màu" (animation)

**Thời lượng:** 2 phút

**Nói:**
Cùng 20 điểm như slide 12, giờ dùng SCA. Nhìn: không còn đường cam nào. Mọi trọng số nằm trong vùng cùng nhãn. Mỗi điểm trời chia đều cho 10 điểm trời trong tranh.

Nhìn kết quả: toàn bộ trời có cùng một màu, xanh pha chút vàng. Đúng vùng, liên tục. Nhưng phẳng: các ngôi sao vàng sắc nét trong tranh biến mất, vì bị trung bình hoá.

Đó là lý do cần SSA. Nhưng trước SSA có một bước chuẩn bị: S-AdaIN.

**Chỉ vào:** Lưới kết quả bên phải, phần trời đồng màu.

**Chuyển:** "S-AdaIN, khối thứ hai."

---

### Slide 19 · "S-AdaIN: đổi tông màu content theo từng vùng"

**Thời lượng:** 3 phút

**Nói:**
Nhớ AdaIN ở slide 10. Hình trên: content gốc; AdaIN toàn ảnh làm cả ảnh ngả một tông, bị đục; S-AdaIN theo vùng thì trời theo tông trời của tranh, đất theo tông đất.

Cách làm y hệt AdaIN, chỉ khác một chỗ: tông và độ tương phản tính riêng trong từng vùng nhãn, vùng trời của content nhận của vùng trời trong tranh, đất nhận của đất. Mặt nạ vùng có được bằng K-Means trên semantic map, code gốc làm sẵn.

Để làm gì? Hai việc. Một: làm sạch query cho SSA. Content gốc mang màu riêng của ảnh chụp, ví dụ trời xanh nhạt; nếu để nguyên, khi so với tranh có trời xanh đậm thì "giống" bị lệch. Kéo thống kê của content về thang của tranh trước, rồi so, sẽ chính xác hơn. Hai: content sau S-AdaIN cũng là phần được cộng vào kết quả cuối.

Lưu ý: hình minh hoạ là pixel cho dễ hình dung; thực tế phép biến đổi xảy ra trên feature, không trên pixel.

**Chỉ vào:** Ba hình trên theo thứ tự hiện.

**Chuyển:** "Query đã sạch. Giờ khối thứ ba: SSA."

---

### Slide 20 · "SSA: chỉ giữ một điểm style giống nhất, cùng nhãn"

**Thời lượng:** 4 phút

**Nói:**
Hộp bên trái. Khác SCA ở nguồn câu hỏi và thẻ: câu hỏi lấy từ content đã qua S-AdaIN, thẻ từ tranh. Tức là so khớp theo cấu trúc thật: điểm nào trong tranh trông giống điểm này nhất. Nội dung lấy về vẫn từ tranh.

Luật G2 khác G1: trong các điểm cùng nhãn, chỉ giữ đúng một điểm giống nhất, còn lại cấm hết. Chỉ còn một điểm thì trọng số của nó bằng 1, nghĩa là copy nguyên nét của điểm đó, không pha trộn gì. Texture giữ nguyên độ sắc.

Ví dụ bên phải. Một query trời, sáu key. Nền xanh là key nhãn trời, nền vàng là nhãn đất. Điểm số: k1 được 2,0; k4 được 2,2, cao nhất. Nhưng k4 là đất, khác nhãn, bị loại ngay. Trong vùng trời, k1 cao nhất. SSA giữ đúng k1, trọng số 1.

Ý tưởng này giống Style-Swap từ 2016: thay mỗi mảng content bằng mảng style giống nhất. Khác ở chỗ SSA khoá trong vùng ngữ nghĩa và nằm trong không gian attention của backbone, nên không cần train.

Đây là cách sửa lỗi 3.

**Chỉ vào:** Cột k4 (2,2, nền vàng): "cao nhất nhưng sai nhãn, loại". Cột k1: "cao nhất trong trời, giữ".

**Chuyển:** "Xem SSA chạy."

---

### Slide 21 · "SSA: mỗi điểm chỉ một đường nối" (animation)

**Thời lượng:** 2 phút

**Nói:**
Vẫn dữ liệu đó, giờ SSA. Mỗi query đúng một đường nối, tới điểm giống nó nhất trong cùng vùng. Màu được copy nguyên. Kết quả có cả sao vàng lẫn xanh đậm, texture sắc nét.

Nhược điểm: nếu chỉ dùng SSA, màu giữa các điểm cạnh nhau có thể nhảy, lệch tông tổng thể. Ablation của paper thấy đúng điều đó: SSA một mình chuyển được texture nhưng lệch màu giữa các vùng. Nên cần cả hai.

**Chỉ vào:** Lưới kết quả: các ô vàng sắc nét xuất hiện.

**Chuyển:** "Đặt ba ma trận cạnh nhau để so."

---

### Slide 22 · "Ba ma trận attention, nhìn là thấy khác biệt"

**Thời lượng:** 3 phút

**Nói:**
Nếu chỉ nhớ một hình của cả buổi, nhớ hình này.

Mỗi ma trận: hàng là điểm content, ba trời ba đất; cột là điểm style, ba trời ba đất. Ô càng đậm, trọng số càng lớn.

Trái, UA: dày đặc, mỗi hàng trải khắp nơi. Ô cam là trọng số rơi sang khối khác nhãn. Lỗi 1 nằm ở đó.

Giữa, SCA: mask G1 xoá hai khối chéo, gạch chéo là âm vô cực. Phần còn lại đều nhau, vì Q, K từ map phẳng. Lỗi 2 biến mất.

Phải, SSA: mask G2 chỉ giữ một ô mỗi hàng, luôn trong khối đúng. Hai hàng có thể chọn cùng một key, không sao. Lỗi 3 biến mất.

Giá trị trong hình là minh hoạ, không phải số đo.

**Chỉ vào:** Ô cam ở UA; hai khối gạch chéo ở SCA; một ô mỗi hàng ở SSA.

**Chuyển:** "Ghép SCA và SSA lại thế nào?"

---

### Slide 23 · "Trộn hai nhánh: α1 cho không khí, α2 cho nét cọ" (animation)

**Thời lượng:** 3 phút

**Nói:**
Dòng trên: kết quả bằng 0,7 lần tông chung từ SCA, cộng 0,3 lần nét cọ từ SSA, cộng content. Hệ số thứ nhất chỉnh mức style tổng thể, hệ số thứ hai chỉnh độ sắc của texture, content là bản sau S-AdaIN để giữ bố cục.

SANet dùng α1 = 0,7, α2 = 0,3. Các backbone khác dùng số khác vì thang feature khác nhau; có ở slide 25.

Animation: chỉ phần style, 0,7 nhân trung bình vùng cộng 0,3 nhân điểm giống nhất. Nhìn kết quả: trời có tông xanh chung, nhưng vẫn giữ chút sắc vàng của sao. Vừa liên tục, vừa có nét.

*Thử nghĩ: tăng α2 lên 1, α1 về 0 thì thành gì?* Thành SSA thuần, slide 21: sắc nhưng loang màu. Ngược lại thành SCA thuần, slide 18: đều nhưng phẳng. Hai hệ số là nút chỉnh giữa hai thái cực.

**Chỉ vào:** Lưới kết quả, so với hai animation trước.

**Chuyển:** "Để chắc là mọi người tính được, mình làm một ví dụ tay."

---

### Slide 24 · "Một query trời, sáu key: tính tay từng cách"

**Thời lượng:** 4 phút (có thể cắt)

**Nói:**
Cùng sáu key như slide 20. Cột Q·K là điểm số. Giờ tính bốn cột còn lại.

**UA**: softmax trên cả sáu. e mũ 2,0 là 7,39; e mũ 1,0 là 2,72; 0,5 là 1,65; 2,2 là 9,03; 0,3 là 1,35; 0,1 là 1,11. Tổng 23,24. Chia ra: k4 được 0,388, cao nhất, mà k4 là đất. Cộng ba key đất: 0,388 cộng 0,058 cộng 0,048, xấp xỉ 49%. Gần một nửa style của điểm trời này đến từ đất. Đó là lỗi 1 bằng số.

**SCA**: Q, K từ map nên mọi key trời có cùng điểm; mask đặt k4 đến k6 bằng âm vô cực; softmax ra 1/3 mỗi key trời. Bỏ qua điểm số hoàn toàn.

**SSA**: trong vùng trời, k1 có 2,0 cao nhất; giữ đúng k1, trọng số 1.

**Trộn**: 0,7 nhân cột SCA cộng 0,3 nhân cột SSA. k1 được 0,7 nhân 1/3 cộng 0,3 bằng 0,533; k2, k3 được 0,233. Sai vùng: 0%.

Số là đồ chơi tự đặt để luyện tay, không từ paper.

**Chỉ vào:** Hàng "Sai vùng": 49% ở UA, 0% ở ba cột còn lại.

**Chuyển:** "Cuối chặng: cắm vào ba backbone cụ thể thế nào."

---

### Slide 25 · "Cắm vào ba họ mô hình, không huấn luyện lại"

**Thời lượng:** 3 phút (có thể cắt)

**Nói:**
Bảng này cho ai muốn chạy thật. Ba backbone, ba họ: SANet là CNN với encoder VGG-19, StyTr2 là transformer, StyleID là diffusion trên Stable Diffusion.

SANet: thay khối attention của SANet; semantic map cũng đi qua VGG để lấy feature map. α 0,7 và 0,3.

StyTr2: thay ở các transformer số chẵn trong decoder. α 1,2 và 0,5. Có thêm hệ số b = 0,7 trộn content có và không có S-AdaIN, chỉ ở module đầu.

StyleID: thay self-attention của U-Net, sau DDIM inversion. α 0,8 và 0,2. Điểm riêng: nếu Q1, K1 lấy thuần từ map thì ảnh mất quá nhiều chi tiết, nên tác giả pha feature map với feature ảnh theo t1 = 0,3; Q2 pha theo t2 = 0,5. S-AdaIN chỉ áp ở bước t = T.

Câu chốt: chỉ khối attention đổi, trọng số gốc giữ nguyên, nên dùng được ngay với model đã train. Chi tiết ở Appendix C của paper.

**Chỉ vào:** Cột "SCSA thay ở đâu".

**Chuyển:** "Chặng 5: SCSA tốt đến đâu. Nhưng trước khi xem số, phải biết số đo cái gì."

---

## Chặng 5 · Kết quả (slide 26–30, ~15 phút)

### Slide 26 · "Bốn thước đo, đọc trước khi xem bảng số"

**Thời lượng:** 3 phút

**Nói:**
Bốn thước đo. Mũi tên xuống là càng thấp càng tốt, mũi tên lên là càng cao càng tốt.

(Bấm 1) **SSL**, Semantic Style Loss. Cắt kết quả và tranh theo từng nhãn, so style của vùng trời với vùng trời, đất với đất, cộng lại. "Style" ở đây đo bằng Gram matrix, cách Gatys 2016 dùng. Đây là thước đo đúng mục tiêu của bài. Do chính tác giả đề xuất.

(Bấm 2) **FID**. Toàn bộ tập ảnh kết quả có "trông như tranh" không, xét trên phân phối feature. Đo style tổng thể, không quan tâm đúng vùng.

(Bấm 3) **CFSD**. Cấu trúc của kết quả còn giống content bao nhiêu. Thước đo giữ nội dung, mượn từ StyleID.

(Bấm 4) **User study**. 40 người xem từng cặp có và không SCSA, chọn ảnh chuyển style theo vùng tốt hơn. 1.200 phiếu.

(Bấm hộp cam) Lưu ý quan trọng: SSL đo chính xác điều SCSA tối ưu, nên SCSA thắng ở SSL là gần như chắc chắn. Hãy nhìn thêm FID và CFSD để biết cái giá phải trả.

**Chuyển:** "Giờ xem số."

---

### Slide 27 · "SCSA giảm SSL 29–47% trên cả ba backbone"

**Thời lượng:** 4 phút

**Nói:**
Biểu đồ: SSL, thấp hơn là tốt. SANet từ 1,66 xuống 0,88, giảm 47%. StyTr2 từ 1,98 xuống 1,22, giảm 38%. StyleID từ 1,75 xuống 1,24, giảm 29%. Giảm mạnh ở cả ba.

Bảng dưới. FID: cả ba giảm nhẹ, tức style tổng thể không tệ đi, thậm chí tốt hơn chút. CFSD: SANet và StyTr2 giảm, tốt; nhưng StyleID **tăng** từ 0,092 lên 0,118. Tức StyleID cộng SCSA giữ nội dung kém hơn StyleID gốc. Đây là cái giá mình nhắc ở slide trước.

Hàng chọn: 83%, 84%, 78% chọn bản có SCSA.

Thêm một dòng: SANet cộng SCSA có SSL tốt nhất kể cả so với năm phương pháp semantic style transfer chuyên biệt; tốt nhất trong số đó là GLStyleNet với 1,03.

Số lấy nguyên từ Table 1. Dữ liệu đánh giá: 91 bộ bốn do tác giả tự tuyển.

**Chỉ vào:** Ô CFSD của StyleID, nhấn mạnh đây là ngoại lệ.

**Chuyển:** "Bỏ bớt một mảnh thì sao? Ablation."

---

### Slide 28 · "Bỏ bớt một mảnh, chất lượng tụt ở đâu?"

**Thời lượng:** 3 phút

**Nói:**
Ba thí nghiệm, mỗi lần bỏ một khối.

Bỏ SSA: màu đúng vùng nhưng mất texture. SSL tăng, rõ nhất ở StyTr2 từ 1,22 lên 1,42.

Bỏ SCA: có texture nhưng lệch màu giữa các vùng. SSL tăng mạnh nhất, StyleID từ 1,25 lên 2,30, gần gấp đôi.

Bỏ S-AdaIN: style tổng thể kém chính xác, ít chi tiết, nhưng giữ nội dung tốt hơn một chút. StyleID từ 1,25 lên 1,76.

Kết luận: SCA lo không khí, SSA lo nét cọ, thiếu cái nào cũng tệ hơn.

Một điểm nên phản biện: với SANet, bỏ S-AdaIN gần như không đổi SSL, 0,876 so với 0,877. Và bỏ SCA hoặc S-AdaIN lại cho FID tốt hơn bản đầy đủ. Tức với backbone yếu, không phải mảnh nào cũng cần. Tác động lớn nhất ở StyleID.

**Chỉ vào:** Cột StyleID ở "Bỏ SCA".

**Chuyển:** "Những gì paper chưa làm được."

---

### Slide 29 · "Những điều SCSA chưa giải quyết"

**Thời lượng:** 3 phút

**Nói:**
Cột trái, tác giả tự nêu ở Appendix I. Một: người dùng phải tự cung cấp semantic map, và nhãn hai bên phải khớp. Hai: tốn thêm thời gian và bộ nhớ so với backbone gốc. Ba: chất lượng phụ thuộc backbone; backbone càng mạnh, hiệu ứng càng rõ.

Cột phải, điểm mình tự đặt ra để thảo luận. Một: chỉ 91 bộ dữ liệu tự tuyển, chưa có benchmark lớn. Hai: metric chính SSL do chính tác giả đề xuất. Ba: nếu một vùng content không có vùng cùng nhãn bên style, cả hàng attention thành âm vô cực; paper không nói xử lý thế nào. Bốn: top-1 cứng có thể gây lặp texture và răng cưa ở biên vùng.

Mỗi điểm cột phải là một hướng mở rộng: tự sinh map bằng segmentation, xử lý vùng không có cặp, attention theo vùng cho nhanh hơn, SSA top-k thay vì top-1. Các hướng này nằm trong file proposal.

**Chuyển:** "Cuối cùng, chạy code."

---

### Slide 30 · "Chạy code gốc trong bốn bước"

**Thời lượng:** 3 phút (có thể cắt)

**Nói:**
Bốn bước. Một: clone repo, Python 3.8, PyTorch 2.4.1. Hai: tải trọng số gốc của ba backbone, SANet và StyleID vào models, StyTr2 vào experiments. Ba: chạy sem.py để tạo mặt nạ nhãn từ semantic map; nó dùng K-Means và lưu ở ba độ phân giải. Bốn: vào thư mục SANet+SCSA, chạy lệnh bên phải với một mẫu, ví dụ mẫu số 29.

Mỗi mẫu là một thư mục có bốn file: ảnh, tranh, map ảnh, map tranh. Đúng bộ bốn ở slide 6.

Muốn so với bản gốc: chạy SANet.py với cùng content và style.

Lưu ý khi gõ: đường dẫn sem_map trên slide bị ngắt dòng cho vừa khung, gõ thật thì viết liền. StyleID dùng tên cờ khác. sem.py có bảng màu cứng theo số thư mục, thêm dữ liệu mới thì phải thêm bảng màu.

**Chuyển:** "Tóm lại."

---

## Chặng 6 · Kết (slide 31–33, ~3 phút)

### Slide 31 · "Ba điều mang về"

**Thời lượng:** 2 phút

**Nói:**
Ba điều.

Một, vấn đề: attention toàn cục chọn style theo độ giống cấu trúc, không theo ý nghĩa. Sinh ra sai vùng, loang lổ, nhạt nhoà.

Hai, giải pháp: khoá attention trong vùng cùng nhãn. SCA nhìn cả vùng, Q và K từ map. SSA lấy một điểm, top-1. S-AdaIN làm sạch query. Trộn bằng α1, α2.

Ba, hiệu quả: không cần train, cắm vào SANet, StyTr2, StyleID. SSL giảm 29 đến 47%, 78 đến 84% phiếu chọn.

Quay lại câu ở slide 2: SCSA cho attention biết điểm này là trời hay đất, rồi chỉ cho phép lấy style từ vùng cùng tên. Giờ mọi người đã biết "cho biết" nghĩa là mask âm vô cực, "cùng tên" nghĩa là G1 và G2, và vì sao cần hai attention.

Nếu chỉ nhớ một hình: slide 22, ba ma trận.

**Chuyển:** "Hai slide cuối là phụ lục công thức và từ điển, để đó cho ai muốn tra. Mình nhận câu hỏi."

---

### Slide 32 · "Công thức đầy đủ" (phụ lục)

**Thời lượng:** không trình bày

**Nói:**
Không đọc. Mở khi có người hỏi "công thức chính xác là gì" hoặc khi đối chiếu với paper. Mỗi hàng là một khối, cột phải nhắc lại nghĩa bằng lời đã nói ở slide chính. Số Eq. trong cột đầu là số phương trình trong paper.

---

### Slide 33 · "Từ điển nhanh"

**Thời lượng:** để mở trong lúc hỏi đáp

**Nói:**
Không cần đọc. Để slide này mở trong phần hỏi đáp; khi có câu hỏi dùng thuật ngữ, chỉ vào dòng tương ứng.

---

## Câu hỏi thường gặp và cách trả lời ngắn

| Câu hỏi | Trả lời |
| --- | --- |
| Không có semantic map thì SCSA dùng được không? | Không. Map là đầu vào bắt buộc. Hướng mở: sinh map tự động bằng mô hình segmentation, ví dụ SAM, rồi khớp nhãn hai bên. |
| Vì sao Q, K của SCA lấy từ map mà không từ ảnh? | Để mọi điểm trong vùng có cùng hàng attention, sửa lỗi loang lổ. Nếu lấy từ ảnh thì chỉ sửa được lỗi sai vùng. |
| SSA top-1 có bị lặp texture không? | Có thể: nhiều query chọn cùng một key. Paper không đo. Top-k là hướng mở. |
| Vì sao StyleID cộng SCSA giữ nội dung kém hơn? | Paper không giải thích sâu. Giả thuyết: Q1, K1 từ map làm mất chi tiết nên tác giả phải pha với feature ảnh theo t1; vẫn chưa đủ. |
| Tốn thêm bao nhiêu thời gian? | Paper chỉ nói "tốn thêm", không có số cụ thể. Cần tự đo khi chạy code. |
| Có cần train gì không? | Không. Mask chỉ thay điểm số bằng âm vô cực; mọi trọng số của backbone giữ nguyên. |
| SSL có công bằng không? | Nó đo đúng mục tiêu của bài nhưng do tác giả đề xuất. Nên nhìn kèm FID và CFSD. |

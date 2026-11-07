# Script trình bày — bộ slide HyperFrames SCSA (bản 4)

> Bộ slide: thư mục `scsa-deck/`, 46 slide, theme sáng. Thiết kế: `scsa-deck/SPEC.md`.
> Paper: SCSA, CVPR 2025 — arXiv 2503.04119 · Code: github.com/scn-00/SCSA
> Cập nhật ngày 2026-10-31 theo khung *Seminar Guidelines* của giảng viên: năm chặng Giới thiệu → Bài toán và tổng quan → Chi tiết kỹ thuật → So sánh và thảo luận → Kết luận; thêm công thức (giữ ở mức dễ hiểu: thay số của ví dụ quen thuộc) và thuật toán. Đã rà soát nội dung, logic, hoạt hình toàn deck.
> Tổng thời lượng gợi ý: **~110 phút** nói + 10–15 phút hỏi đáp. Cần rút ngắn: xem mục “Nếu thiếu thời gian”.

## Cấu trúc theo khung của giảng viên

| Mục trong khung | Câu hỏi của giảng viên | Slide trả lời |
| --- | --- | --- |
| Introduction | Why is this topic important? | 6 (Vì sao quan trọng), 2 (Câu hỏi mở màn) |
| Introduction | Where is it applied? | 6 (Vì sao quan trọng) |
| Problem Statement & Overview | What task or method is discussed? | 5 (Style transfer là gì), 10 (Bản đồ nhãn), 11 (Phát biểu bài toán), 20 (SCSA trong một phút) |
| Problem Statement & Overview | What challenges does it address? | 11 (Phát biểu bài toán), 17 (Lỗi 1: sai vùng), 18 (Lỗi 2 và 3), 19 (Ba lỗi, ba cách sửa) |
| Technical Details | Model architecture or algorithm | 16 (Công thức attention), 22 (Sơ đồ toàn cảnh), 23 (SCA), 25 (S-AdaIN), 26 (SSA), 28 (Công thức SCA, SSA), 29 (Trộn hai nhánh), 30 (Thuật toán), 31 (Cắm vào backbone) |
| Technical Details | Training process and innovations | 32 (Huấn luyện và điểm mới) |
| Comparison & Discussion | Compare with similar models/methods | 8 (Bốn phương pháp, một cặp ảnh), 35 (SSL đo gì), 37 (Số liệu SSL), 38 (So với phương pháp khác), 39 (Ablation) |
| Comparison & Discussion | Strengths and limitations | 40 (Điểm mạnh), 41 (Hạn chế) |
| Conclusion | Key takeaways | 43 (Tóm tắt) |
| Conclusion | Future directions | 44 (Hướng phát triển), 45 (Bước tiếp: StyleGallery) |

Mạch đi theo thứ tự của một bài báo khoa học: **động lực** (vì sao quan trọng) → **định nghĩa bài toán** → **cơ sở** (mô hình hiện nay làm thế nào) → **thách thức** (ba lỗi) → **phương pháp** (hình → công thức → thuật toán) → **thực nghiệm** (thiết lập → định tính → định lượng → so sánh → ablation) → **thảo luận** (mạnh, yếu) → **kết luận** (điều mang về, hướng tiếp).

Công thức chỉ có hai slide và không đi sâu: slide 16 viết attention thành một dòng rồi thay đúng 4 con số cả lớp đã thấy ở slide softmax; slide 28 chỉ thêm mặt nạ M vào cùng công thức đó. Thuật toán gom lại ở slide 30, viết bằng lời.

## Một ví dụ xuyên suốt

Cả buổi dùng **một bộ dữ liệu thật**: mẫu số 29 trong repo của tác giả, gồm ảnh chụp thung lũng Yosemite, một bức tranh núi, và hai bản đồ nhãn với bốn vùng: trời, vách núi, rừng, dãy xa. Kết quả SANet và SANet + SCSA trên đúng cặp ảnh này có trong hình kết quả của paper, nên câu hỏi mở màn và câu trả lời cuối buổi là cùng một bức ảnh.

Các con số trên lưới 12 × 12 (phần trăm trọng số, bức ghép SCA, SSA) là **phép tính minh hoạ** trên màu trung bình của từng mảnh ảnh mẫu, không phải số đo của mô hình thật. Slide nào dùng chúng đều ghi rõ. Số liệu thật của paper nằm ở các slide SSL, so sánh, ablation và điểm mạnh; công thức lấy đúng ký hiệu của paper, còn ma trận 6 × 6 đi kèm là minh hoạ.

## Cách mở và điều khiển

- Mở `slides_export/SCSA_trinh_chieu.html` bằng trình duyệt (bấm đúp). Không cần mạng. Chép cả thư mục `slides_export` khi mang sang máy khác.
- **→ / Space / click**: bước tiếp theo, hoạt hình chạy. **←**: lùi, nhảy thẳng. **F**: toàn màn hình. **P**: cửa sổ ghi chú người trình bày. **H**: bảng phím tắt.
- Mỗi slide có vài **bước**. Bước đầu tự chạy khi bạn vào slide; mỗi “Bấm k” sau đó là một lần mũi tên phải. Lời thoại cũng hiện trong cửa sổ ghi chú (phím P), bước đang chiếu được tô sáng.
- Slide UA có một đoạn quét dài khoảng 8 giây sau “Bấm 1”: nói trong lúc nó chạy.

Cấu trúc: một mạch hỏi → đáp. Câu hỏi mở màn (vì sao vách núi bị tô sai?) được trả lời dần qua năm chặng; mỗi thẻ chương ghi câu trả lời của chặng trước rồi mới nêu câu hỏi mới, và cuối mỗi slide có một câu “Dẫn:” nói vì sao sang slide sau. Lạc thì quay về thẻ chương hoặc slide “SCSA trong một phút” (cuối chặng 2).

## Bảng tổng quan

| # | Slide | Số bước | Thời lượng | Nguồn hình |
| --- | --- | --- | --- | --- |
| 1 | SCSA | 1 | 1 phút |  |
| 2 | Cùng ảnh, cùng tranh, hai kết quả | 3 | 2 phút | ảnh thật từ paper |
| 3 | Năm chặng, theo khung của buổi seminar | 2 | 1,5 phút |  |
| 4 | Chặng 1 · Style transfer là gì, đã đi tới đâu? | 1 | 0,5 phút |  |
| 5 | Style transfer: giữ bố cục, thay lớp áo | 4 | 2,5 phút | ảnh thật |
| 6 | Vì sao quan trọng: style transfer dùng ở đâu | 4 | 2,5 phút | ví dụ ứng dụng có thật + ảnh thật từ paper |
| 7 | Mười năm style transfer, sáu bước | 7 | 3 phút |  |
| 8 | Cùng một cặp ảnh, bốn phương pháp | 6 | 3 phút | chạy thật: compare_style_transfer.ipynb |
| 9 | Chặng 2 · Vì sao vách núi bị tô sai? | 1 | 0,5 phút |  |
| 10 | Semantic: mỗi ảnh có thêm một bản đồ nhãn | 5 | 2,5 phút | bản đồ nhãn thật trong repo |
| 11 | Bài toán: bộ bốn vào, một ảnh ra | 3 | 2 phút | file thật trong repo |
| 12 | Ảnh được cắt thành lưới điểm | 4 | 2,5 phút |  |
| 13 | Attention: hỏi, so, cân, trộn | 5 | 4 phút |  |
| 14 | Softmax: chia trọng số theo độ giống | 3 | 2,5 phút |  |
| 15 | Universal Attention: ai cũng nhìn tất cả | 3 | 3 phút |  |
| 16 | Attention bằng một công thức | 5 | 2,5 phút | công thức thay số minh hoạ trên ảnh mẫu |
| 17 | Lỗi 1: lấy style từ sai vùng | 4 | 3,5 phút | tính minh hoạ + ảnh thật của paper |
| 18 | Lỗi 2 và 3: loang lổ, nhạt nhoà | 3 | 3 phút | dải trời cắt từ kết quả thật |
| 19 | Ba lỗi, ba cách sửa | 4 | 2,5 phút |  |
| 20 | SCSA trong một phút | 3 | 2 phút |  |
| 21 | Chặng 3 · SCSA sửa thế nào? | 1 | 0,5 phút |  |
| 22 | Toàn cảnh: SCSA nằm ở giữa | 8 | 4,5 phút |  |
| 23 | SCA: hỏi bằng bản đồ nhãn | 5 | 3,5 phút | tính minh hoạ trên ảnh mẫu |
| 24 | AdaIN: đổi tông bằng hai con số | 4 | 3 phút | phép tính thật trên pixel |
| 25 | S-AdaIN: đổi tông riêng từng vùng | 4 | 2,5 phút | phép tính thật trên pixel |
| 26 | SSA: chỉ giữ một mảnh giống nhất | 5 | 3,5 phút | tính minh hoạ trên ảnh mẫu |
| 27 | Ba ma trận attention, nhìn là thấy khác | 4 | 2,5 phút |  |
| 28 | SCA, SSA: cùng công thức, thêm mặt nạ M | 5 | 2,5 phút | công thức thay số minh hoạ trên ảnh mẫu |
| 29 | Trộn hai nhánh: chỉnh tông và nét | 5 | 3 phút | tính minh hoạ + kết quả thật |
| 30 | Thuật toán SCSA: một lượt chạy, không train | 5 | 3 phút | tổng hợp từ paper và repo |
| 31 | Cắm vào ba họ mô hình, không train lại | 5 | 2,5 phút |  |
| 32 | Huấn luyện thế nào, và điểm mới ở đâu | 3 | 2,5 phút | paper + repo |
| 33 | Chặng 4 · Sửa được bao nhiêu, kém ở đâu? | 1 | 0,5 phút |  |
| 34 | Bốn thước đo, đọc trước khi xem số | 5 | 2,5 phút |  |
| 35 | SSL: chấm style theo từng cặp vùng | 5 | 3 phút | minh hoạ: tính trên bốn ảnh của slide 8 |
| 36 | Kết quả thật trên ba họ mô hình | 4 | 3,5 phút | ảnh thật từ paper; mẫu 29 nhóm chạy lại |
| 37 | Lỗi style theo vùng giảm 29–47% | 3 | 3 phút | số từ Table 1 |
| 38 | So với năm phương pháp semantic chuyên biệt | 4 | 2,5 phút | số từ Table 1 |
| 39 | Bỏ bớt một mảnh, lỗi tăng bao nhiêu? | 5 | 2,5 phút | số từ Fig. 6 và Appendix F |
| 40 | Điểm mạnh: đúng vùng mà không phải train | 5 | 2 phút | số từ Table 1, Fig. 6 |
| 41 | Những điều SCSA chưa giải quyết | 3 | 2,5 phút | tính minh hoạ trên ảnh mẫu |
| 42 | Chặng 5 · Mang về gì, đi tiếp đâu? | 1 | 0,5 phút |  |
| 43 | Chỉ lấy style từ vùng cùng nhãn | 3 | 2 phút |  |
| 44 | Hướng phát triển: mỗi hạn chế một lối mở | 6 | 2,5 phút | proposal của nhóm |
| 45 | Bước tiếp: StyleGallery bỏ bản đồ nhãn | 4 | 2,5 phút | arXiv 2603.10354 (CVPR 2026), Fig. 1(b) |
| 46 | SCSA | 1 | 1 phút | kết quả thật từ paper |


## Mở đầu (slide 1–3, ~4,5 phút)

### Slide 1 · SCSA

**Số bước:** 1 · **Thời lượng:** 1 phút

**Nói:**

- **Mở đầu:** Chào mọi người. Hôm nay mình trình bày SCSA, paper CVPR 2025: dạy attention nhìn đúng vùng khi chuyển phong cách cho ảnh. Mình giả định mọi người chưa biết style transfer. Ba ảnh bên phải là thật, từ repo của tác giả: ảnh chụp Yosemite, một bức tranh núi, và kết quả tô ảnh theo tranh bằng SCSA. Cả buổi dùng đúng cặp ảnh này. Dẫn: Bắt đầu bằng một câu hỏi.

### Slide 2 · Cùng ảnh, cùng tranh, hai kết quả

**Số bước:** 3 · **Thời lượng:** 2 phút · **Nguồn:** ảnh thật từ paper

**Nói:**

- **Hai kết quả:** Kết quả thật trong paper, cùng một đầu vào ở giữa. Trái là SANet, mô hình có sẵn. Phải là SANet cộng SCSA.
- **Bấm 1 · Vách núi:** Nhìn vách núi lớn. SANet tô nó bằng màu kem của trời. SCSA tô đúng màu xanh của núi.
- **Bấm 2 · Câu hỏi:** Vì sao bên trái tô nhầm? Cả buổi trả lời câu này. Giữ nó trong đầu. Dẫn: Để trả lời, mình đi năm chặng.

### Slide 3 · Năm chặng, theo khung của buổi seminar

**Số bước:** 2 · **Thời lượng:** 1,5 phút

**Nói:**

- **Năm chặng:** Cả buổi là một chuỗi câu hỏi, mỗi chặng trả lời một câu và mở ra câu sau. Một: style transfer là gì, đã đi tới đâu. Hai: vì sao vách núi bị tô sai, tức câu hỏi vừa đặt ra. Ba: SCSA sửa thế nào, bằng hình, công thức và thuật toán. Bốn: sửa được bao nhiêu, kém ở đâu. Năm: mang về gì, đi tiếp đâu. Năm chặng này đúng theo khung của giảng viên: giới thiệu, bài toán và tổng quan, chi tiết kỹ thuật, so sánh và thảo luận, kết luận.
- **Bấm 1 · Trọng tâm:** Chặng 3, SCSA sửa thế nào, là trọng tâm. Mỗi thẻ chương sẽ nhắc lại câu trả lời của chặng trước; lạc thì nhìn dòng đó. Dẫn: Chặng 1: style transfer là gì.

## Chặng 1 · Giới thiệu (slide 4–8, ~11,5 phút)

> Khung giảng viên: *Why is this topic important? Where is it applied?*

### Slide 4 · Chặng 1 · Style transfer là gì, đã đi tới đâu?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Chặng 1, giới thiệu. Câu hỏi: style transfer là gì, dùng ở đâu, và đã đi tới đâu? Bốn slide: định nghĩa, ứng dụng, mười năm phát triển, và bốn phương pháp chạy thật trên cùng cặp ảnh của ta. Dẫn: Bắt đầu từ định nghĩa.

### Slide 5 · Style transfer: giữ bố cục, thay lớp áo

**Số bước:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** ảnh thật

**Nói:**

- **Ảnh chụp:** Ảnh chụp cho bố cục: trời ở trên, vách núi ở giữa, rừng ở dưới.
- **Bấm 1 · Bức tranh:** Bức tranh cho lớp áo: màu, nét cọ, bề mặt.
- **Bấm 2 · Kết quả:** Bố cục cũ, áo mới. Để ý: trời mang màu kem của tranh, vách núi mang màu xanh của núi.
- **Bấm 3 · Arbitrary:** Một mô hình dùng cho mọi bức tranh, không train lại. Hỏi nhanh: vách núi bị tô màu trời có thành công không? Không: vẫn là áo của tranh, nhưng mặc sai chỗ. Dẫn: Làm đúng điều này thì được gì? Xem nó được dùng ở đâu.

### Slide 6 · Vì sao quan trọng: style transfer dùng ở đâu

**Số bước:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** ví dụ ứng dụng có thật + ảnh thật từ paper

**Nói:**

- **Chỉnh ảnh, phim:** Style transfer không chỉ là trò chơi ảnh. Chỉnh ảnh: Prisma năm 2016 đưa nó lên điện thoại, biến ảnh chụp thành tranh trong vài giây. Phim: phim ngắn Come Swim năm 2017 dùng nó để tô các cảnh quay theo bức tranh của đạo diễn.
- **Bấm 1 · Dữ liệu, chân dung:** Tăng cường dữ liệu: Stylized-ImageNet năm 2019 đổi phong cách ảnh train để mô hình nhận dạng bớt dựa vào texture, bền hơn khi ảnh đổi miền. Chân dung, cảnh vật: áo, mặt, trời, núi, mỗi phần phải lấy nét từ đúng chỗ.
- **Bấm 2 · Lỗi sai vùng:** Và đây là lý do chủ đề quan trọng: kết quả SANet ta vừa thấy, vách núi mang màu trời. Trong bất kỳ sản phẩm nào ở trên, ảnh này không dùng được.
- **Bấm 3 · Đúng vùng:** Mọi ứng dụng đều cần một điều: trời ra trời, núi ra núi. Đó chính là thứ SCSA giải quyết. Dẫn: Người ta đã làm việc này mười năm; xem họ đi tới đâu.

### Slide 7 · Mười năm style transfer, sáu bước

**Số bước:** 7 · **Thời lượng:** 3 phút

**Nói:**

- **2016 · Gatys:** Chỉnh từng pixel cho tới khi ảnh vừa giống bố cục, vừa giống màu tranh. Đẹp nhưng chậm, mỗi ảnh vài phút. Dưới mỗi mốc là ảnh nhóm chạy lại bằng chính phương pháp đó trên cặp ảnh của ta. Mốc SCSA là SANet cộng SCSA, ví dụ chính của buổi.
- **Bấm 1 · 2017 · AdaIN:** Một mạng cho mọi tranh, khớp tông cả ảnh. Nhanh nhưng thô. Sẽ gặp lại ở chặng 3.
- **Bấm 2 · 2019 · SANet:** Attention: mỗi điểm của ảnh tự đi tìm điểm giống nó trong tranh để lấy style.
- **Bấm 3 · 2022 · StyTr2:** Cùng ý attention, nhưng làm bằng transformer: ảnh và tranh cắt thành patch, decoder cho mỗi patch của ảnh đi tìm patch giống nó trong tranh.
- **Bấm 4 · 2024 · StyleID:** Attention bên trong Stable Diffusion.
- **Bấm 5 · 2025 · SCSA:** Attention biết nhãn vùng.
- **Bấm 6 · Khung magenta:** Ba mô hình trong khung là chỗ SCSA cắm vào, nhưng từng cái một: SCSA gắn vào SANet thì ra SANet cộng SCSA, gắn vào StyTr2 thì ra StyTr2 cộng SCSA, tương tự StyleID. Không phải ghép cả ba thành một. SCSA không thay các mô hình này, nó chỉ thay khối attention bên trong. Dẫn: Ảnh nhỏ khó thấy; phóng to bốn kết quả trên cùng cặp ảnh để so.

### Slide 8 · Cùng một cặp ảnh, bốn phương pháp

**Số bước:** 6 · **Thời lượng:** 3 phút · **Nguồn:** chạy thật bằng compare_style_transfer.ipynb (Gatys L-BFGS, AdaIN, SANet, SANet + SCSA; 512 × 512, Apple MPS)

**Nói:**

- **Đầu vào:** Nói suông thì khó thấy, nên nhóm chạy lại các phương pháp trên đúng cặp ảnh của buổi hôm nay: ảnh Yosemite và bức tranh núi, cỡ 512 × 512, trên máy Mac. Code trong notebook compare_style_transfer.ipynb. Cả lớp nhìn vào một chỗ: vách núi lớn bên trái. Trong tranh, vách núi màu xanh.
- **Bấm 1 · Gatys:** Gatys 2016 tối ưu từng pixel 300 bước, mất 26,8 giây. Ảnh khá đẹp, mây của ảnh còn nguyên. Nhưng vách núi ngả hồng cam, màu của dãy núi xa trong tranh. Gatys khớp thống kê màu, nét của cả bức tranh, không biết vùng nào ứng với vùng nào.
- **Bấm 2 · AdaIN:** AdaIN 2017: một lượt qua mạng, 97 mili giây, nhanh gần 280 lần. Đổi lại, chỉ một cặp trung bình, độ lệch cho cả ảnh: mọi vùng khoác chung một tông đục, trời loang vệt xanh, vách núi xám nhạt.
- **Bấm 3 · SANet:** SANet 2019 dùng attention: mỗi điểm tự đi tìm style giống nó, 124 mili giây. Nhưng nó tìm theo hình dáng, không theo nhãn: vách núi trắng như mây vì lấy màu trời, bầu trời thì loang lổ. Đây đúng là lỗi ta sẽ mổ xẻ ở chặng 2.
- **Bấm 4 · SANet + SCSA:** Vẫn SANet, cắm thêm SCSA và hai bản đồ nhãn. Trời mang màu kem của trời trong tranh, vách núi xanh như núi trong tranh, dãy xa hồng như dãy xa. Cái giá: 473 mili giây, chậm hơn SANet khoảng 350 mili giây và cần bản đồ nhãn, nhưng vẫn nhanh hơn Gatys khoảng 57 lần.
- **Bấm 5 · Chốt:** Ba cách đầu không biết nhãn vùng nên tô nhầm. SCSA chỉ lấy style từ vùng cùng nhãn. Phần còn lại của buổi hôm nay giải thích vì sao bên trái sai, và SCSA sửa thế nào. Lưu ý: thời gian đo trên một máy, một ảnh, chỉ để so thứ bậc. Dẫn: Ba cách đầu đều tô sai vách núi; chặng 2 tìm xem vì sao.

## Chặng 2 · Bài toán và tổng quan (slide 9–20, ~30,5 phút)

> Khung giảng viên: *What task or method is discussed? What challenges does it address?*

### Slide 9 · Chặng 2 · Vì sao vách núi bị tô sai?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Dòng trên cùng là câu trả lời của chặng 1: style transfer đã nhanh và đẹp, nhưng vẫn tô vách núi sai màu. Chặng 2 hỏi: vì sao? Đi ba bước. Một: phát biểu bài toán cho rõ, có bản đồ nhãn. Hai: mở mô hình ra xem nó chọn style thế nào: lưới điểm, attention, softmax, gộp lại thành Universal Attention và công thức của nó. Ba: đo ba lỗi trên chính ảnh của ta. Cuối chặng là SCSA trong một phút. Dẫn: Trước hết, nói rõ đầu vào: SCSA cần thêm bản đồ nhãn.

### Slide 10 · Semantic: mỗi ảnh có thêm một bản đồ nhãn

**Số bước:** 5 · **Thời lượng:** 2,5 phút · **Nguồn:** bản đồ nhãn thật trong repo

**Nói:**

- **Ảnh và tranh:** Ảnh chụp và bức tranh của ta.
- **Bấm 1 · Hai bản đồ nhãn:** Thêm hai bản đồ nhãn (semantic map). Mỗi màu là một vùng. Đây là file thật trong repo.
- **Bấm 2 · Màu là mã nhãn:** Đỏ là trời, vàng là vách núi, xanh lá là rừng, xanh dương là dãy xa. Màu chỉ là mã, không phải màu thật.
- **Bấm 3 · Nối cặp:** Nối đúng cặp: trời với trời, vách núi với vách núi.
- **Bấm 4 · Luật:** Mỗi vùng chỉ lấy style từ vùng cùng tên. Đầu vào giờ là bộ bốn: ảnh, map ảnh, tranh, map tranh. Ai vẽ map? Người dùng, hoặc mô hình phân đoạn. Paper không tự sinh map, đó là một hạn chế. Dẫn: Có bản đồ nhãn rồi, phát biểu bài toán cho gọn.

### Slide 11 · Bài toán: bộ bốn vào, một ảnh ra

**Số bước:** 3 · **Thời lượng:** 2 phút · **Nguồn:** file thật trong repo

**Nói:**

- **Bộ bốn vào:** Phát biểu bài toán semantic style transfer. Đầu vào là bộ bốn: ảnh chụp và bản đồ nhãn của nó, bức tranh và bản đồ nhãn của nó. Đầu ra là một ảnh.
- **Bấm 1 · Ba yêu cầu:** Ảnh ra phải đạt ba điều. Một: giữ bố cục của ảnh chụp. Hai: đúng vùng, trời lấy style từ trời, núi lấy style từ núi. Ba: dùng cho mọi bức tranh, không train lại cho từng tranh.
- **Bấm 2 · Thách thức:** Các mô hình attention hiện nay như SANet, StyTr2, StyleID đạt yêu cầu 1 và 3, nhưng hỏng yêu cầu 2. Phần còn lại của chặng trả lời: chúng chọn style thế nào, và vì sao hỏng. Dẫn: Muốn biết vì sao hỏng yêu cầu 2, phải nhìn vào bên trong mô hình; bước đầu, ảnh thành lưới điểm.

### Slide 12 · Ảnh được cắt thành lưới điểm

**Số bước:** 4 · **Thời lượng:** 2,5 phút

**Nói:**

- **Ảnh 512×512:** Từ “điểm” dùng suốt phần sau. Đây là ảnh 512 nhân 512 pixel.
- **Bấm 1 · Lưới điểm:** Encoder cắt ảnh thành lưới. Ở đây 12×12 cho dễ nhìn; mô hình thật 64×64, tức 4.096 điểm.
- **Bấm 2 · Điểm là vector:** Mỗi điểm là một vector, ví dụ 512 số, mô tả mảng ảnh quanh nó: màu, cạnh, bề mặt. Không phải một pixel.
- **Bấm 3 · Decoder:** Decoder vẽ lưới ngược lại thành ảnh. SCSA chỉ sửa ở giữa, trên lưới điểm. Dẫn: Mỗi điểm của lưới đi tìm style thế nào? Đó là attention.

### Slide 13 · Attention: hỏi, so, cân, trộn

**Số bước:** 5 · **Thời lượng:** 4 phút

**Nói:**

- **Query:** Attention giống tra từ điển, nhưng mềm. Một điểm vách núi của ảnh hỏi: “style nào hợp với tôi?”. Đây là query.
- **Bấm 1 · Key và value:** Nó so với các điểm của tranh. Mỗi điểm có key để so và value để lấy về. Mình chỉ vẽ 4 trong 4.096 điểm: trời, dãy xa, vách núi, rừng. Mỗi điểm là một vị trí trên lưới, không phải pixel. Đường càng dày càng giống.
- **Bấm 2 · Trọng số:** Độ giống đổi thành trọng số: 35, 63, 1 và 1 phần trăm.
- **Bấm 3 · Trộn:** Màu chảy về theo trọng số rồi trộn lại.
- **Bấm 4 · Lỗi:** Chú ý: điểm vách núi xám nhạt giống dãy xa và trời của tranh hơn vách núi của tranh, nên 99% màu lấy từ sai vùng. Cùng kiểu lỗi với SANet: lấy màu từ vùng khác (ở SANet thật là màu trời). Số tính minh hoạ trên màu của ảnh mẫu, không phải số của mô hình thật. Dẫn: Bước “cân” làm bằng softmax; xem nó chia trọng số ra sao.

### Slide 14 · Softmax: chia trọng số theo độ giống

**Số bước:** 3 · **Thời lượng:** 2,5 phút

**Nói:**

- **Điểm số:** Vẫn điểm vách núi của ảnh ở slide trước (ô viền magenta góc trên) và bốn điểm của tranh. Điểm số độ giống: dãy xa cao nhất, khoảng 4,6; trời khoảng 4; vách núi và rừng quanh 0,5.
- **Bấm 1 · Softmax:** Softmax đổi điểm số thành phần trăm, cộng lại đủ 100: 35, 63, 1, 1. Điểm cao được phần lớn, nhưng không ai bị bỏ hẳn.
- **Bấm 2 · Không nhìn nhãn:** Để ý: điểm hỏi là vách núi, vậy mà dãy xa nhận 63%, còn vách núi của tranh chỉ 1%. Softmax chỉ nhìn độ giống, không nhìn nhãn vùng. Giữ con số 63% này: đó là mầm của lỗi tô sai vùng mà ta sẽ đo ở cuối chặng. Dẫn: Một điểm đã vậy; nếu cả 144 điểm cùng làm thì sao?

### Slide 15 · Universal Attention: ai cũng nhìn tất cả

**Số bước:** 3 · **Thời lượng:** 3 phút

**Nói:**

- **Hai lưới:** Paper gọi khối attention của SANet, StyTr2, StyleID là Universal Attention, viết tắt UA. Trái: 144 điểm của ảnh. Phải: 144 điểm của tranh.
- **Bấm 1 · Quét:** Khung magenta là câu hỏi đang xét, chạy qua vài điểm. Mỗi lần nối tới 8 điểm tranh giống nhất (số 8 mình chọn cho dễ nhìn). Đường đen là cùng vùng, magenta là sang vùng khác. Chữ ở giữa là phần trăm trọng số sang vùng khác, tính trên cả 144 điểm. Đoạn này chạy khoảng 8 giây, nói trong lúc đó.
- **Bấm 2 · Chốt:** Mỗi điểm nhìn tất cả 144 thẻ, không ai hỏi điểm đó thuộc vùng nào. Với lưới thật 64×64, bảng so có 16 triệu ô. Số tính minh hoạ. Dẫn: Viết gọn cả quá trình bằng một công thức.

### Slide 16 · Attention bằng một công thức

**Số bước:** 5 · **Thời lượng:** 2,5 phút · **Nguồn:** công thức thay số minh hoạ trên ảnh mẫu

**Nói:**

- **Công thức:** Những gì ta vừa xem gói trong một dòng. Không cần nhớ ký hiệu; cứ hiểu như tra cứu: Q là câu hỏi, K là nhãn của từng ngăn, V là đồ trong ngăn.
- **Bấm 1 · Q, K, V:** Q là điểm vách núi của ảnh đang hỏi. K và V là bốn điểm của tranh.
- **Bấm 2 · Q Kᵀ:** Bước một, so: được độ giống, chính là bốn con số ở slide softmax.
- **Bấm 3 · softmax:** Bước hai, chia thành phần trăm: 35, 63, 1, 1.
- **Bấm 4 · · V:** Bước ba, trộn màu theo phần trăm đó: ra màu nghiêng về dãy xa và trời. Công thức không hề nhắc tới nhãn vùng, nên mới lấy sai vùng. Dẫn: Công thức không có nhãn; giờ đo xem nó tô sai bao nhiêu trên ảnh của ta.

### Slide 17 · Lỗi 1: lấy style từ sai vùng

**Số bước:** 4 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ + ảnh thật của paper

**Nói:**

- **Bức ghép UA:** Chạy UA cho cả 144 điểm của ảnh. Mỗi ô là màu trộn mà điểm đó lấy về.
- **Bấm 1 · Phủ magenta:** Phủ magenta lên ô lấy style từ vùng khác, càng đậm càng nhiều. Trung bình 36% trọng số sang vùng sai; 36 trên 144 điểm lấy phần lớn style từ vùng sai, dồn vào vách núi.
- **Bấm 2 · Kết quả thật:** So với kết quả thật của SANet: đúng chỗ đó, vách núi mang màu trời.
- **Bấm 3 · Lỗi 1:** Phép tính của mình dùng màu trung bình nên chỉ là minh hoạ, nhưng nó chỉ ra cùng một chỗ sai với mô hình thật. Lỗi 1: lấy style từ sai vùng. Dẫn: Sai vùng chưa phải lỗi duy nhất; còn hai lỗi tinh hơn.

### Slide 18 · Lỗi 2 và 3: loang lổ, nhạt nhoà

**Số bước:** 3 · **Thời lượng:** 3 phút · **Nguồn:** dải trời cắt từ kết quả thật

**Nói:**

- **Lỗi 2 · loang lổ:** Dải trời cắt từ hai kết quả thật. Trên là SANet: cùng là trời mà mỗi chỗ một màu, vì mỗi điểm tự chọn style theo cấu trúc riêng của nó. Dưới là SANet cộng SCSA: cả vùng trời một tông, đó là điều ta muốn.
- **Bấm 1 · Lỗi 3 · nhạt nhoà:** Kể cả khi chỉ lấy đúng vùng: bốn mảnh vách núi của tranh, mỗi mảnh sắc nét, trộn mềm lại thành một màu đục, mất nét cọ.
- **Bấm 2 · Hai lỗi kéo ngược:** Sửa lỗi 2 cần các điểm trong vùng giống nhau hơn; sửa lỗi 3 cần mỗi điểm giữ nét riêng. Vì vậy SCSA cần hai cách nhìn. Dẫn: Gom ba lỗi lại, mỗi lỗi một cách sửa.

### Slide 19 · Ba lỗi, ba cách sửa

**Số bước:** 4 · **Thời lượng:** 2,5 phút

**Nói:**

- **Sai vùng:** Sửa bằng luật cấm theo nhãn, có sẵn trong cả SCA và SSA, nên lỗi 1 được sửa miễn phí.
- **Bấm 1 · Loang lổ:** Sửa bằng SCA: cả vùng dùng chung một tông.
- **Bấm 2 · Nhạt nhoà:** Sửa bằng SSA: chỉ lấy một điểm, giữ nguyên nét cọ.
- **Bấm 3 · Ba gốc:** Cả ba lỗi đều nằm trong attention gốc: lỗi 1 vì không biết nhãn, lỗi 2 vì hỏi theo cấu trúc từng điểm, lỗi 3 vì trộn mềm nhiều điểm. Đó là ba thách thức SCSA giải quyết. Slide sau là tổng quan cách giải. Dẫn: Ba cách sửa ấy chính là SCSA; xem nó trong một phút trước khi đi chi tiết.

### Slide 20 · SCSA trong một phút

**Số bước:** 3 · **Thời lượng:** 2 phút

**Nói:**

- **Attention chọn style:** Tổng quan trước khi vào chi tiết: cả paper trong một sơ đồ. Ảnh và tranh vào khối attention; khối này chọn mỗi điểm của ảnh lấy style từ đâu trong tranh. Nó chọn theo kiểu “trông giống”, nên tô nhầm vùng, đúng lỗi 1 vừa thấy.
- **Bấm 1 · Thêm nhãn vùng:** SCSA thêm bản đồ nhãn, mỗi màu một vùng. Attention chỉ lấy style từ vùng cùng nhãn, nên đúng vùng.
- **Bấm 2 · Hai cách nhìn:** Bên trong có hai cách. SCA nhìn cả vùng, lấy tông chung, sửa loang lổ. SSA nhìn một điểm, lấy nét cọ, sửa nhạt nhoà. Không train lại. Tên gọi cũng kể đúng điều này: S là Semantic, dùng nhãn vùng; C là Continuous, nhìn liền cả vùng, tức SCA; S là Sparse, thưa, một điểm, tức SSA; A là Attention. Dẫn: Chặng 3 mở từng khối.

## Chặng 3 · Chi tiết kỹ thuật (slide 21–32, ~33,5 phút)

> Khung giảng viên: *Model architecture or algorithm; training process and innovations*

### Slide 21 · Chặng 3 · SCSA sửa thế nào?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Câu trả lời của chặng 2: attention chọn style theo “trông giống” và không nhìn nhãn, nên sai vùng, loang lổ, nhạt nhoà. Chặng 3, trọng tâm, hỏi: SCSA sửa thế nào? Đi theo sơ đồ toàn cảnh từ trên xuống: SCA; rồi AdaIN và S-AdaIN; rồi SSA. Sau đó xem ba ma trận, công thức có mặt nạ, phép trộn, thuật toán một trang, cách cắm vào ba mô hình và chuyện huấn luyện. Dẫn: Bắt đầu từ sơ đồ toàn cảnh.

### Slide 22 · Toàn cảnh: SCSA nằm ở giữa

**Số bước:** 8 · **Thời lượng:** 4,5 phút

**Nói:**

- **Đầu vào:** Sơ đồ vẽ theo SANet trước, vì ví dụ xuyên suốt của buổi dùng SANet; cuối slide sẽ đổi sang StyTr2 và StyleID. Bốn đầu vào: ảnh, map ảnh, tranh, map tranh. Encoder VGG của SANet biến cả bốn thành lưới điểm. Trong SANet thật, khối attention chạy ở hai tầng đặc trưng (relu4_1 và relu5_1); sơ đồ vẽ gọn thành một.
- **Bấm 1 · SCA:** Nhánh trên: hỏi bằng map, lấy tông chung của cả vùng.
- **Bấm 2 · S-AdaIN và SSA:** Nhánh dưới hai bước: S-AdaIN đổi tông ảnh theo từng vùng, rồi SSA tìm một điểm giống nhất trong cùng vùng.
- **Bấm 3 · Trộn:** Trộn tông chung, nét cọ, và cộng bố cục của ảnh, lấy từ sau S-AdaIN (đường đứt nét magenta).
- **Bấm 4 · Decoder:** Decoder của SANet vẽ ra ảnh: đây chính là kết quả SANet cộng SCSA.
- **Bấm 5 · StyTr2:** Đổi sang StyTr2, mô hình transformer: hai đầu đổi thành transformer encoder ở trước, transformer decoder và decoder CNN ở sau. Khung magenta là phần đổi theo mô hình. SCSA nằm trong transformer decoder, thay attention giữa ảnh và tranh; phần giữa vẫn y nguyên.
- **Bấm 6 · StyleID:** Đổi sang StyleID, mô hình diffusion: trước là DDIM inversion đưa ảnh và tranh về nhiễu, sau là U-Net khử nhiễu và VAE decoder của Stable Diffusion. SCSA nằm trong self-attention của U-Net. Vẫn phần giữa ấy.
- **Bấm 7 · Chốt:** Hai đầu là của mô hình gốc và giữ nguyên; các khối ở giữa là SCSA. Slide cắm vào ba họ mô hình sẽ chỉ chính xác chỗ cắm trong từng mô hình. Dẫn: Đi từng khối theo sơ đồ, từ trên xuống: SCA trước.

### Slide 23 · SCA: hỏi bằng bản đồ nhãn

**Số bước:** 5 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:**

- **Câu hỏi từ map:** SCA khác UA ở hai chỗ. Chỗ một: câu hỏi không lấy từ ảnh mà từ bản đồ nhãn.
- **Bấm 1 · Cùng một câu:** Map là mảng màu phẳng, nên mọi điểm vách núi hỏi gần như cùng một câu.
- **Bấm 2 · Luật G1:** Chỗ hai: khác nhãn thì cấm. Trọng số chia đều cho mọi điểm vách núi của tranh.
- **Bấm 3 · Bức ghép:** Mỗi điểm vách núi nhận cùng một màu: trung bình của vách núi trong tranh, màu xanh. Làm tương tự các vùng khác, ta được bức ghép bên phải, tính thật trên ảnh mẫu.
- **Bấm 4 · Ưu và nhược:** Liền mạch, đúng vùng, hết loang lổ. Cái giá: phẳng, mất nét cọ. Hỏi nhanh: giữ luật cấm mà hỏi bằng ảnh thì sửa được lỗi nào? Chỉ lỗi sai vùng. Dẫn: Nhánh dưới phải đổi tông trước khi tìm nét; để hiểu S-AdaIN, nhắc lại AdaIN.

### Slide 24 · AdaIN: đổi tông bằng hai con số

**Số bước:** 4 · **Thời lượng:** 3 phút · **Nguồn:** phép tính thật trên pixel

**Nói:**

- **Tông của ảnh:** Nhánh dưới của sơ đồ bắt đầu bằng S-AdaIN; để hiểu nó, nhắc lại AdaIN, phương pháp 2017 đã thấy ở chặng 1. Tông của một ảnh tóm trong hai số: μ là màu trung bình, σ là độ tương phản (đọc “miu” và “xích-ma”). Ảnh chụp này xám ấm.
- **Bấm 1 · Tông của tranh:** Bức tranh có μ, σ riêng: kem xanh, tương phản thấp hơn.
- **Bấm 2 · Khoác tông:** Bỏ μ, σ của ảnh, khoác μ, σ của tranh. Ảnh bên phải là phép tính thật trên pixel: cả ảnh ngả về tông của tranh. Trong mô hình, phép này làm trên lưới điểm, không phải pixel.
- **Bấm 3 · Giới hạn:** Chỉ một cặp số cho cả ảnh, nên trời, vách núi, rừng bị kéo về cùng một tông. Slide sau, S-AdaIN, sửa đúng chỗ này. Dẫn: S-AdaIN làm đúng phép này, nhưng riêng từng vùng.

### Slide 25 · S-AdaIN: đổi tông riêng từng vùng

**Số bước:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** phép tính thật trên pixel

**Nói:**

- **Ảnh gốc:** Nhớ AdaIN: hai số, màu trung bình và độ tương phản. Đây là ảnh gốc.
- **Bấm 1 · AdaIN cả ảnh:** Một cặp số cho mọi vùng, nên cả ảnh ngả một tông.
- **Bấm 2 · S-AdaIN:** Tính riêng cho từng vùng nhãn. Vách núi nhận tông xanh của vách núi trong tranh, dãy xa nhận tông hồng. Ba ảnh này là phép tính thật trên pixel.
- **Bấm 3 · Để làm gì:** Để SSA so “giống” trên cùng thang màu với tranh. Ảnh chụp có vách núi xám, tranh có vách núi xanh; so ngay thì bị lệch. Trong mô hình, phép này làm trên lưới điểm. Dẫn: Tông đã đúng vùng; giờ lấy nét cọ bằng SSA.

### Slide 26 · SSA: chỉ giữ một mảnh giống nhất

**Số bước:** 5 · **Thời lượng:** 3,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:**

- **Câu hỏi:** SSA hỏi bằng ảnh đã qua S-AdaIN. Đây là một điểm vách núi đang hỏi.
- **Bấm 1 · Luật G2 · cấm:** Khác nhãn thì cấm, chỉ còn vùng vách núi của tranh.
- **Bấm 2 · Giữ một điểm:** Trong vùng đó chỉ giữ đúng một điểm giống nhất (khung magenta); bốn khung đen là ứng viên tiếp theo, bị bỏ. Chỉ còn một điểm thì trọng số 100%, tức copy nguyên mảnh đó.
- **Bấm 3 · Bức ghép:** Mảnh bay sang đúng vị trí trong kết quả. Làm cho cả 144 điểm: mỗi ô là một mảnh tranh thật, giữ nguyên nét cọ.
- **Bấm 4 · Chốt:** Hết nhạt nhoà. Ý tưởng giống Style-Swap 2016, nhưng khoá trong vùng ngữ nghĩa và không cần train. Dẫn: Đặt UA, SCA, SSA cạnh nhau bằng ma trận attention.

### Slide 27 · Ba ma trận attention, nhìn là thấy khác

**Số bước:** 4 · **Thời lượng:** 2,5 phút

**Nói:**

- **UA:** Mỗi ma trận: hàng là điểm của ảnh (ba trời, ba vách núi), cột là điểm của tranh; ô càng đậm, trọng số càng lớn. UA dày đặc, mỗi hàng trải khắp nơi; ô magenta là trọng số tràn sang vùng khác. Lỗi 1 nằm ở đó.
- **Bấm 1 · SCA:** Luật G1 gạch bỏ hai khối chéo, phần còn lại đều nhau vì hỏi bằng map phẳng. Hết loang lổ.
- **Bấm 2 · SSA:** Mỗi hàng giữ đúng một ô, luôn trong khối đúng. Hết nhạt nhoà.
- **Bấm 3 · Chốt:** Nếu chỉ nhớ một hình của cả buổi, hãy nhớ hình này. Giá trị trong hình là minh hoạ. Dẫn: Ba ma trận khác nhau chỉ nhờ một thứ thêm vào công thức: mặt nạ M.

### Slide 28 · SCA, SSA: cùng công thức, thêm mặt nạ M

**Số bước:** 5 · **Thời lượng:** 2,5 phút · **Nguồn:** công thức thay số minh hoạ trên ảnh mẫu

**Nói:**

- **Thêm M:** Nhớ slide softmax ở chặng 2: điểm vách núi bị dãy xa lấy mất 63%. SCSA sửa bằng đúng một thứ thêm vào công thức: mặt nạ M. M bằng 0 là được lấy, âm vô cực là bị cấm.
- **Bấm 1 · Độ giống:** Vẫn bốn con số cũ.
- **Bấm 2 · Cộng M:** Điểm hỏi là vách núi, nên ba vùng khác bị cộng âm vô cực. Luật này xét nhãn, không xét ai cao điểm: dãy xa đang cao nhất vẫn bị cấm, vì nó cao mà sai vùng nên mới có lỗi tô nhầm.
- **Bấm 3 · softmax:** e mũ âm vô cực bằng 0, nên ô bị cấm còn 0%; softmax chia lại 100% cho phần còn lại. Vách núi chỉ có 1% nhưng còn một mình nên nhận trọn 100%: lấy đúng màu vách núi. Không cần train thêm gì.
- **Bấm 4 · SCA và SSA:** Hai nhánh của SCSA dùng đúng công thức này, chỉ khác cách đặt M. SCA hỏi bằng bản đồ nhãn nên cả vùng ra một tông. SSA chỉ chừa một ô giống nhất trong vùng nên giữ được nét cọ. Dẫn: Có hai nhánh rồi; trộn chúng thế nào?

### Slide 29 · Trộn hai nhánh: chỉnh tông và nét

**Số bước:** 5 · **Thời lượng:** 3 phút · **Nguồn:** tính minh hoạ + kết quả thật

**Nói:**

- **SSA thuần:** Kết quả cuối trộn hai nhánh: tông chung từ SCA và nét cọ từ SSA, rồi cộng bố cục của ảnh. Thanh trượt cho biết trộn bao nhiêu mỗi bên. Nút đang ở SSA thuần: toàn mảnh tranh thật, sắc nét nhưng màu nhảy giữa các ô.
- **Bấm 1 · SCA thuần:** Kéo hết sang SCA: mỗi vùng một màu, đều nhưng phẳng, mất nét cọ.
- **Bấm 2 · 0,7 / 0,3:** SANet đặt nút ở 0,7 phần SCA và 0,3 phần SSA. Nhìn ô hình: màu đã đều theo từng vùng như SCA, nhưng vẫn thấy vệt cọ của SSA ở mép trời và vách núi. Ô hình là minh hoạ trên lưới 12×12: lấy màu từng vùng của SCA, giữ vệt cọ của SSA.
- **Bấm 3 · Kết quả thật:** Bên phải là kết quả thật của SANet cộng SCSA trên cùng cặp ảnh, ở độ phân giải đầy đủ: cũng đều màu theo vùng mà vẫn có nét.
- **Bấm 4 · Chốt:** Viết gọn: kết quả bằng α₁ nhân SCA cộng α₂ nhân SSA cộng bố cục. Thật ra α₁, α₂ là hai hệ số riêng; ở SANet chúng cộng lại bằng 1 nên vẽ được thành một thanh trượt. StyTr2 dùng 1,2 và 0,5; StyleID 0,8 và 0,2. Dẫn: Gom tất cả thành thuật toán một trang.

### Slide 30 · Thuật toán SCSA: một lượt chạy, không train

**Số bước:** 5 · **Thời lượng:** 3 phút · **Nguồn:** tổng hợp từ paper và repo

**Nói:**

- **Chuẩn bị:** Toàn bộ thuật toán trên một trang. Vào: ảnh, map ảnh, tranh, map tranh và hai hệ số trộn. Bước 1: encoder biến tất cả thành lưới điểm. Bước 2: K-Means trên hai map ra mặt nạ nhãn; bước này làm sẵn một lần bằng sem.py.
- **Bấm 1 · Ba khối:** Bước 3: SCA với mặt nạ cùng nhãn, cho tông chung. Bước 4: S-AdaIN đổi tông ảnh riêng từng vùng. Bước 5: SSA với mặt nạ top-1 cùng nhãn, cho nét cọ.
- **Bấm 2 · Trộn và giải mã:** Bước 6: trộn theo α₁, α₂, cộng lưới điểm của ảnh. Dòng Ra: decoder vẽ thành ảnh. Không vòng lặp, không bước train: một lượt chạy.
- **Bấm 3 · Chi phí:** Với lưới 64 nhân 64, mỗi bảng điểm có khoảng 16,8 triệu ô; SCA và SSA mỗi nhánh một bảng, và SCSA tính đủ bảng rồi mới cấm, nên tốn hơn mô hình gốc.
- **Bấm 4 · Chốt:** Bước 2 đến 6 là phần SCSA thêm vào; encoder và decoder giữ nguyên. Dẫn: Thuật toán này cắm được vào ba mô hình; xem chỗ cắm cụ thể.

### Slide 31 · Cắm vào ba họ mô hình, không train lại

**Số bước:** 5 · **Thời lượng:** 2,5 phút

**Nói:**

- **SANet:** Slide mười năm nói SCSA cắm vào ba mô hình; đây là chỗ cắm cụ thể. SANet là mạng CNN: encoder VGG, ở giữa là khối attention SANet (ô xám), cuối là decoder CNN. Đây chính là sơ đồ ở slide toàn cảnh.
- **Bấm 1 · SCSA thay khối:** SCSA thay đúng khối SANet đó, ở cả hai tầng đặc trưng; encoder, decoder và trọng số gốc giữ nguyên. Tỉ lệ trộn tông và nét 0,7 và 0,3.
- **Bấm 2 · StyTr2:** StyTr2 là transformer: hai transformer encoder cho ảnh và tranh, rồi transformer decoder, trong đó có attention giữa ảnh và tranh, cuối là decoder CNN. SCSA thay attention ảnh–tranh đó ở các lớp chẵn của transformer decoder. Tỉ lệ 1,2 và 0,5; riêng lớp đầu cộng thêm bố cục sau S-AdaIN với hệ số 0,7.
- **Bấm 3 · StyleID:** StyleID là diffusion, dùng Stable Diffusion có sẵn: đảo ảnh và tranh về nhiễu bằng DDIM inversion, rồi khi khử nhiễu ảnh, self-attention của U-Net lấy K, V của tranh. SCSA thay self-attention đó. Tỉ lệ 0,8 và 0,2. Hỏi thuần bằng map làm mất chi tiết nên tác giả pha thêm feature của ảnh (Appendix C); S-AdaIN chỉ dùng ở bước đầu.
- **Bấm 4 · Chốt:** Ba kiến trúc rất khác nhau, nhưng đều có một khối attention ảnh–tranh. Mỗi lần SCSA cắm vào một mô hình, thay đúng khối đó; paper làm ba lần, ra ba phiên bản, và so từng phiên bản với mô hình gốc của nó. Không train lại, dùng ngay với mô hình có sẵn. Dẫn: Không train lại thì huấn luyện nằm ở đâu, và điểm mới là gì?

### Slide 32 · Huấn luyện thế nào, và điểm mới ở đâu

**Số bước:** 3 · **Thời lượng:** 2,5 phút · **Nguồn:** paper + repo

**Nói:**

- **Huấn luyện:** Câu hỏi hay gặp: SCSA train thế nào? Câu trả lời: không train. Backbone đã được tác giả gốc train sẵn: SANet và StyTr2 train trên ảnh MS-COCO làm nội dung và tranh WikiArt làm phong cách, với loss nội dung và loss style; StyleID dùng Stable Diffusion có sẵn. SCSA không thêm tham số nào, không có loss mới. Lúc chạy chỉ làm ba việc: tạo mặt nạ nhãn từ bản đồ màu bằng K-Means, thay khối attention, và trộn theo α1, α2.
- **Bấm 1 · Điểm mới:** Năm điểm mới. SCA: hỏi bằng bản đồ nhãn nên cả vùng chung một tông. SSA: chỉ giữ top-1 trong cùng vùng nên giữ nguyên nét cọ. S-AdaIN: đổi tông theo từng vùng trước khi so. Cắm được: một khối dùng cho cả CNN, Transformer và Diffusion. Và SSL: một thước đo style theo từng vùng.
- **Bấm 2 · Chốt:** Cái mới nằm ở luật cấm theo nhãn, không nằm ở trọng số. Vì vậy nó rẻ để thử trên mô hình có sẵn. Dẫn: Chặng 4: sửa được bao nhiêu.

## Chặng 4 · So sánh và thảo luận (slide 33–41, ~22 phút)

> Khung giảng viên: *Compare with similar models/methods; strengths and limitations*

### Slide 33 · Chặng 4 · Sửa được bao nhiêu, kém ở đâu?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Câu trả lời của chặng 3: SCSA cấm vùng khác nhãn; SCA lấy tông chung, SSA lấy nét cọ. Chặng 4 hỏi: sửa được bao nhiêu, kém ở đâu? Theo thứ tự một bài thực nghiệm: thước đo, ảnh kết quả, số so với mô hình gốc và với năm phương pháp chuyên biệt, ablation, rồi điểm mạnh và hạn chế. Dẫn: Trước khi xem số, cần biết đo bằng gì.

### Slide 34 · Bốn thước đo, đọc trước khi xem số

**Số bước:** 5 · **Thời lượng:** 2,5 phút

**Nói:**

- **SSL:** Bốn thước đo, mỗi lần bấm một cái. SSL (Semantic Style Loss): cắt kết quả và tranh theo nhãn, so style trời với trời, vách núi với vách núi. Thấp là tốt. Slide sau nói kỹ.
- **Bấm 1 · FID:** Cả tập kết quả có trông như tranh không, xét tổng thể. Thấp là tốt.
- **Bấm 2 · CFSD:** Kết quả còn giữ bố cục của ảnh gốc không. Thấp là tốt.
- **Bấm 3 · Người xem:** 40 người, mỗi người 30 câu, tổng 1.200 phiếu: một nửa so bản có và không có SCSA, một nửa so với năm phương pháp khác. Cao là tốt.
- **Bấm 4 · Lưu ý:** SSL do chính tác giả đề xuất và đo đúng điều SCSA tối ưu, nên SCSA thắng ở SSL gần như chắc chắn. Nhìn thêm FID và CFSD. Dẫn: SSL là thước đo chính; xem nó đo cụ thể thế nào.

### Slide 35 · SSL: chấm style theo từng cặp vùng

**Số bước:** 5 · **Thời lượng:** 3 phút · **Nguồn:** minh hoạ: tính trên bốn ảnh của slide 8

**Nói:**

- **Ý tưởng:** SSL là thước đo chính của paper, nên nói kỹ một chút. Ý tưởng: không so cả bức, mà cắt kết quả và tranh theo bản đồ nhãn, rồi so từng cặp vùng cùng nhãn: trời với trời, vách núi với vách núi, rừng với rừng, dãy xa với dãy xa. Mỗi cặp so hai con số thống kê của đặc trưng: trung bình μ, tức tông, và độ lệch chuẩn σ, tức độ đậm nhạt của nét.
- **Bấm 1 · Công thức:** Viết thành công thức: cộng qua các vùng, cộng qua các lớp VGG, khoảng cách μ cộng khoảng cách σ. Đây chính là loss style của AdaIN mà ta đã gặp, chỉ khác là tính riêng trong từng vùng. Lưu ý: paper chỉ mô tả SSL bằng lời ở mục 4.3, không ghi lớp VGG nào và cộng thế nào; công thức trên bảng là mình viết lại từ mô tả đó.
- **Bấm 2 · Cả ảnh:** Vì sao phải theo vùng? Mình thử minh hoạ trên bốn ảnh của slide Bốn phương pháp, dùng màu thay cho đặc trưng VGG, nên đây không phải số của paper. Nếu so cả bức như loss style thường, SANet cộng SCSA lại tệ nhất, 6,7, còn Gatys tốt nhất, 1,6. Lý do: so cả ảnh chỉ hỏi tổng lượng màu có giống tranh không. Tô màu trời lên vách núi vẫn có thể giữ tổng lượng màu đúng. Paper nêu thêm một lý do: vùng to nhỏ khác nhau giữa ảnh và tranh làm lệch phép so toàn cục.
- **Bấm 3 · Từng vùng:** So từng vùng rồi cộng, thứ hạng đảo ngược: SCSA 21, ba cách kia 85 đến 95. Nhìn màu trong thanh: phần lớn lỗi của ba cách đầu nằm ở vách núi, màu vàng, và dãy xa, màu xanh dương, đúng những chỗ ta thấy tô nhầm.
- **Bấm 4 · Chốt:** Lỗi tô nhầm vùng chỉ lộ ra khi so theo từng vùng; đó là lý do tác giả đặt ra SSL. Mặt trái: SSL dùng chính bản đồ nhãn mà SCSA dùng, nên nó đo đúng điều SCSA tối ưu. Vì vậy khi đọc số, luôn nhìn kèm FID và CFSD. Dẫn: Hiểu SSL rồi; xem ảnh kết quả trước, số sau.

### Slide 36 · Kết quả thật trên ba họ mô hình

**Số bước:** 4 · **Thời lượng:** 3,5 phút · **Nguồn:** ảnh thật từ paper; mẫu 29 nhóm chạy lại (compare_style_transfer.ipynb)

**Nói:**

- **SANet:** Ba ví dụ lấy nguyên từ hình kết quả của paper. Mỗi hàng: ảnh nội dung, ảnh phong cách, mô hình gốc, mô hình cộng SCSA. Hàng đầu là cặp ảnh ta theo dõi cả buổi: vách núi từ màu trời sang màu núi.
- **Bấm 1 · StyTr2:** Ví dụ thác nước: bản gốc màu loang lổ, bản SCSA giữ dòng thác trắng và đá tối.
- **Bấm 2 · StyleID:** Ví dụ chân dung: áo, mặt, nền lấy nét từ đúng vùng tương ứng trong tranh.
- **Bấm 3 · Mẫu 29:** Để so cho công bằng, nhóm chạy lại cả ba họ mô hình trên đúng cặp ảnh của ta, bằng notebook so sánh. Hàng trên là mô hình gốc: SANet, StyTr2, StyleID đều tô vách núi màu mây. Hàng dưới là cắm SCSA vào từng mô hình, mỗi lần một: trời kem, vách núi xanh, dãy xa hồng, cả ba giống nhau. Mình chỉ mô tả những gì thấy trên ảnh; số tổng quát ở slide sau. Dẫn: Giờ đến số.

### Slide 37 · Lỗi style theo vùng giảm 29–47%

**Số bước:** 3 · **Thời lượng:** 3 phút · **Nguồn:** số từ Table 1

**Nói:**

- **Mô hình gốc:** Thước đo SSL, thấp là tốt. Cột xám là mô hình gốc: SANet 1,66; StyTr2 1,98; StyleID 1,75.
- **Bấm 1 · Cộng SCSA:** Cột đen là cộng SCSA: 0,88; 1,22; 1,24. Lỗi style theo vùng giảm 47, 38 và 29%. SANet cộng SCSA còn tốt hơn cả năm phương pháp semantic chuyên biệt.
- **Bấm 2 · Thước đo khác:** FID tốt hơn nhẹ ở cả ba. CFSD: riêng StyleID cộng SCSA giữ bố cục kém hơn, 0,092 lên 0,118; đó là cái giá. Với SANet và StyTr2, CFSD còn tốt hơn: 0,110 xuống 0,087 và 0,075 xuống 0,071. Người xem chọn bản SCSA 83, 84 và 78%. Số từ Table 1, trên 91 bộ do tác giả tự tuyển. Dẫn: So với các phương pháp semantic chuyên biệt thì sao?

### Slide 38 · So với năm phương pháp semantic chuyên biệt

**Số bước:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** số từ Table 1

**Nói:**

- **Tám phương pháp:** Không chỉ so với mô hình gốc: Table 1 còn có năm phương pháp làm riêng cho semantic style transfer: STROTSS, MAST, TR, DIA, GLStyleNet. Xếp theo SSL, thấp là tốt. Cột đen là mô hình cộng SCSA, cột xám là phương pháp chuyên biệt. SANet cộng SCSA đứng đầu, 0,88. StyTr2 và StyleID cộng SCSA ở giữa nhóm, sau GLStyleNet và STROTSS.
- **Bấm 1 · FID và CFSD:** Ở hai thước đo còn lại, StyTr2 cộng SCSA tốt nhất cả bảng: FID 12,40 và CFSD 0,071.
- **Bấm 2 · GLStyleNet:** GLStyleNet có SSL thứ hai, nhưng CFSD 0,399, gấp khoảng bốn lần các phương pháp khác: style đúng vùng nhưng bố cục bị vỡ. Vì vậy phải đọc nhiều thước đo cùng lúc.
- **Bấm 3 · STROTSS:** STROTSS tối ưu lại cho từng ảnh nên chậm; SANet cộng SCSA chỉ chạy một lượt qua mạng mà vẫn đứng đầu SSL. Lưu ý: phần chọn của người xem trong Table 1 đến từ hai thí nghiệm khác nhau, nên mình không so chéo số đó ở đây. Dẫn: Mỗi khối góp bao nhiêu? Bỏ từng khối ra thử.

### Slide 39 · Bỏ bớt một mảnh, lỗi tăng bao nhiêu?

**Số bước:** 5 · **Thời lượng:** 2,5 phút · **Nguồn:** số từ Fig. 6 và Appendix F

**Nói:**

- **Đủ cả ba:** Bỏ từng khối, trên StyleID, số từ Fig. 6. Đủ cả ba khối: 1,245, làm mốc.
- **Bấm 1 · Bỏ SSA:** 1,33: mất texture.
- **Bấm 2 · Bỏ S-AdaIN:** 1,76: tông của từng vùng kém chính xác.
- **Bấm 3 · Bỏ SCA:** 2,30, gần gấp đôi: lệch màu giữa các vùng.
- **Bấm 4 · Chốt:** SCA lo tông chung, SSA lo nét cọ; thiếu khối nào, SSL cũng tăng. Nhưng có đánh đổi: bỏ SSA hoặc S-AdaIN lại giữ bố cục (CFSD) tốt hơn chút, và trên SANet, bỏ S-AdaIN gần như không đổi SSL (0,876 so với 0,877). Dẫn: Gom lại thành điểm mạnh.

### Slide 40 · Điểm mạnh: đúng vùng mà không phải train

**Số bước:** 5 · **Thời lượng:** 2 phút · **Nguồn:** số từ Table 1, Fig. 6

**Nói:**

- **Không train:** Tổng hợp điểm mạnh. Một: không train, cắm là chạy. Không tham số mới, dùng lại trọng số gốc.
- **Bấm 1 · Ba họ mô hình:** Hai: tổng quát. Cùng một khối giúp cả CNN, Transformer và Diffusion; SSL giảm 29 đến 47%. Bên phải là kết quả của ba mô hình.
- **Bấm 2 · Hai nhánh:** Ba: hai nhánh bổ trợ và có nút chỉnh. α₁ chỉnh tông, α₂ chỉnh nét; ablation cho thấy bỏ khối nào thì lỗi theo vùng (SSL) cũng tăng.
- **Bấm 3 · Người xem:** Bốn: người xem đồng ý, chọn bản có SCSA trong 78 đến 84% số cặp.
- **Bấm 4 · Dễ giải thích:** Năm: dễ giải thích. Nhìn ma trận attention là biết mỗi điểm lấy style từ đâu, như ba ma trận ở chặng 3. Slide sau là mặt còn lại: hạn chế. Dẫn: Và những gì SCSA chưa làm được.

### Slide 41 · Những điều SCSA chưa giải quyết

**Số bước:** 3 · **Thời lượng:** 2,5 phút · **Nguồn:** tính minh hoạ trên ảnh mẫu

**Nói:**

- **Cần map nhãn:** Sáu điều chưa giải quyết. Một: phải tự có bản đồ nhãn, và nhãn hai bên phải khớp; tác giả tự nêu điều này.
- **Bấm 1 · Dùng lại mảnh:** Hai: SSA chỉ lấy một điểm nên một mảnh tranh có thể bị dùng lại nhiều lần. Lưới ở giữa là kết quả SSA trên lưới minh hoạ, mỗi ô một mảnh tranh; một mảnh bị dùng 19 lần (khung magenta). Ở độ phân giải thật, điều này có thể gây lặp texture; paper chưa đo.
- **Bấm 2 · Bốn điều thảo luận:** Chỉ 91 bộ tự tuyển. SSL do tác giả tự đặt. Chậm và tốn bộ nhớ hơn. Vùng của ảnh không có vùng cùng nhãn bên tranh thì cả hàng bị cấm, paper không nói xử lý thế nào. Thêm một cái giá thấy trong số liệu: StyleID cộng SCSA giữ bố cục kém hơn, CFSD 0,092 lên 0,118. Mỗi điều là một hướng phát triển, mình quay lại ở chặng cuối. Dẫn: Chặng 5: mang về gì.

## Chặng 5 · Kết luận (slide 42–46, ~8,5 phút)

> Khung giảng viên: *Key takeaways; future directions*

### Slide 42 · Chặng 5 · Mang về gì, đi tiếp đâu?

**Số bước:** 1 · **Thời lượng:** 0,5 phút

**Nói:**

- **Mở chặng:** Câu trả lời của chặng 4: lỗi theo vùng giảm 29 đến 47 phần trăm, không train lại; đổi lại cần bản đồ nhãn và chạy chậm hơn. Chặng 5: mang về gì, và đi tiếp đâu. Dẫn: Một câu cần nhớ.

### Slide 43 · Chỉ lấy style từ vùng cùng nhãn

**Số bước:** 3 · **Thời lượng:** 2 phút

**Nói:**

- **Một câu:** Mang về một câu: chỉ lấy style từ vùng cùng nhãn.
- **Bấm 1 · Trước và sau:** Đây là câu trả lời cho câu hỏi đầu buổi: SANet tô vách núi bằng màu vùng khác vì attention không biết nhãn vùng; SCSA cấm điều đó.
- **Bấm 2 · Bên trong:** SCA lấy tông chung của cả vùng, SSA giữ nét cọ của một điểm. Không train lại; lỗi style theo vùng giảm 29–47%. Nếu chỉ nhớ một hình: ba ma trận attention ở chặng 3. Dẫn: Từ các hạn chế, mở ra hướng đi tiếp.

### Slide 44 · Hướng phát triển: mỗi hạn chế một lối mở

**Số bước:** 6 · **Thời lượng:** 2,5 phút · **Nguồn:** proposal của nhóm

**Nói:**

- **Map tự động:** Hướng phát triển, mỗi hạn chế một lối mở. Một: bản đồ nhãn đang vẽ tay. Hướng: sinh map tự động bằng mô hình phân đoạn như Grounded-SAM, hoặc SAM 2 cộng CLIP, rồi ghép nhãn hai bên bằng embedding văn bản, ví dụ cỏ với cánh đồng.
- **Bấm 1 · Vùng không cặp:** Hai: vùng của ảnh không có cặp bên tranh. Hướng: phương án dự phòng, lùi về attention thường cho vùng đó, hoặc mượn vùng gần nghĩa nhất.
- **Bấm 2 · Chi phí:** Ba: tốn thời gian và bộ nhớ, vì vẫn tính bảng N nhân M rồi mới cấm. Hướng: tính riêng từng vùng, chi phí còn tổng Nᵢ nhân Mᵢ; SSA thực chất là tìm láng giềng gần nhất nên dùng được thư viện tìm kiếm nhanh.
- **Bấm 3 · Top-k:** Bốn: SSA top-1 cứng, dễ lặp texture. Hướng: top-k có nhiệt độ, giữ nét cọ mà mượt hơn ở biên vùng.
- **Bấm 4 · Đánh giá:** Năm: mới đánh giá trên 91 bộ với thước đo tự đặt. Hướng: benchmark lớn MS-COCO nhân WikiArt, đo bằng thước độc lập như ArtFID, LPIPS, CLIP.
- **Bấm 5 · Proposal:** Bốn hướng đầu chính là bốn module trong proposal của nhóm. Dẫn: Hướng thứ nhất đã có người làm: StyleGallery.

### Slide 45 · Bước tiếp: StyleGallery bỏ bản đồ nhãn

**Số bước:** 4 · **Thời lượng:** 2,5 phút · **Nguồn:** He et al., StyleGallery, CVPR 2026 (arXiv 2603.10354): abstract, mục 3.3–3.5, 4.1, 4.2 (Fig. 7 so với SCSA), 4.4, 5; hình là Fig. 1(b) của paper

**Nói:**

- **SCSA cần map:** Hướng thứ nhất đã có người làm. Nhắc lại: SCSA cần bộ bốn, ảnh, tranh và hai bản đồ nhãn do người dùng vẽ hoặc lấy từ mô hình phân đoạn ngoài. Không có map thì không chạy được; đây là hạn chế lớn nhất khi đem ra dùng thật.
- **Bấm 1 · StyleGallery:** StyleGallery, CVPR 2026, của He và cộng sự. Đầu vào chỉ còn ảnh và một hoặc nhiều tranh, không cần map. Chính paper ghi rõ ba hạn chế của các phương pháp trước, trong đó có việc phụ thuộc ràng buộc thêm như semantic mask, và gọi tên SCSA là phương pháp dựa trên mask. Hình bên phải là Fig. 1(b) của paper: ảnh được tự gom cụm, mỗi cụm ghép với cụm hợp nhất trong các tranh, rồi tối ưu ra kết quả.
- **Bấm 2 · Ba bước:** Một: tự chia vùng, gom cụm K-means trên đặc trưng của Stable Diffusion 1.5, sau đó gộp và tách cụm cho gọn. Hai: ghép vùng, so độ giống từng cặp cụm bằng thống kê đặc trưng, đặc trưng ngữ nghĩa DINOv2 và vị trí, với nhiều tranh cùng lúc. Ba: tô theo vùng, dùng một loss style theo từng cặp cụm và một loss giữ bố cục để dẫn quá trình lấy mẫu của diffusion. Không train gì cả, giống SCSA. Có thể nói: luật “chỉ lấy style từ vùng cùng nhãn” vẫn còn, chỉ là nhãn giờ do máy tự tìm.
- **Bấm 3 · Cái giá:** Đổi lại: khoảng 30 giây mỗi ảnh trên RTX 4090 vì phải tối ưu 150 bước, paper nói ghép thêm mô hình lấy mẫu nhanh thì còn khoảng 8 giây, 28 bước. Và chính tác giả ghi hạn chế: cụm sai thì ảnh bị tô vỡ từng phần; khi đó có thể đưa map tay hoặc SAM vào làm map ban đầu. Paper chỉ so với SCSA bằng hình (Fig. 7, dùng kết quả có sẵn trong repo SCSA), không có bảng số, nên mình không kết luận bên nào tốt hơn về số liệu. Dẫn: Hết phần trình bày.

### Slide 46 · SCSA

**Số bước:** 1 · **Thời lượng:** 1 phút · **Nguồn:** kết quả thật từ paper

**Nói:**

- **Kết thúc:** Cảm ơn mọi người đã lắng nghe, mình xin nhận câu hỏi.

## Nếu thiếu thời gian

Bản đầy đủ ~110 phút.

- **Bớt ~12 phút:** bỏ 7 (Mười năm), 14 (Softmax), 25 (S-AdaIN), 29 (Trộn hai nhánh).
- **Bớt thêm ~24 phút:** bỏ 12 (Lưới điểm), 13 (Attention), 15 (Universal Attention), 17 (Lỗi 1: sai vùng), 18 (Lỗi 2 và 3), 27 (Ba ma trận), 36 (Kết quả thật), 39 (Ablation). Khi bỏ slide softmax thì nói lướt ý “softmax không nhìn nhãn” ở slide công thức attention.
- **Không bỏ** (mục giảng viên yêu cầu): 6 (Vì sao quan trọng), 11 (Phát biểu bài toán), 16 (Công thức attention), 28 (Công thức SCA, SSA), 30 (Thuật toán), 32 (Huấn luyện và điểm mới), 38 (So với phương pháp khác), 40 (Điểm mạnh), 41 (Hạn chế), 43 (Tóm tắt), 44 (Hướng phát triển).

## Câu hỏi thường gặp

| Câu hỏi | Trả lời ngắn |
| --- | --- |
| Không có semantic map thì sao? | Không dùng được: map là đầu vào bắt buộc. Hướng mở: sinh map bằng mô hình phân đoạn rồi khớp nhãn hai bên. |
| Vì sao SCA hỏi bằng map mà không bằng ảnh? | Để mọi điểm trong vùng hỏi cùng một câu, nhận cùng một tông. Hỏi bằng ảnh thì chỉ sửa được lỗi sai vùng. |
| Top-1 có làm lặp texture không? | Có thể. Trên lưới minh hoạ, một mảnh tranh bị SSA dùng lại 19 lần. Paper không đo điều này. |
| Vì sao StyleID + SCSA giữ bố cục kém hơn? | Paper không giải thích sâu. Giả thuyết: hỏi bằng map làm mất chi tiết, phần pha feature ảnh chưa bù đủ. |
| Có phải train gì không? | Không. Luật cấm chỉ thay điểm số bằng âm vô cực, trọng số của backbone giữ nguyên. |
| Số phần trăm trong các slide nền tảng có phải của paper? | Không. Đó là phép tính minh hoạ trên màu của ảnh mẫu 29. Số của paper ở các slide SSL, so sánh, ablation, điểm mạnh. |
| SSL có công bằng không? | Nó đo đúng mục tiêu nhưng do tác giả đề xuất. Nên nhìn kèm FID và CFSD. |
| Ký hiệu hay gặp trong paper? | F_c, F_s là lưới điểm của ảnh và tranh; F gạch ngang là bản đã chuẩn hoá; α1, α2 là hai hệ số trộn; μ đọc “miu”, σ đọc “xích-ma”. |
| SCA khác UA ở đâu trong công thức? | Hai chỗ: Q, K lấy từ feature của bản đồ nhãn (F_csem, F_ssem) thay vì của ảnh, và thêm mặt nạ G₁ đặt −∞ cho cặp khác nhãn. |
| SCA khác attention gốc ở đâu trong công thức? | Hai chỗ: Q, K lấy từ bản đồ nhãn thay vì từ ảnh, và cộng mặt nạ M (paper gọi là G₁) đặt −∞ cho cặp khác nhãn. |
| Vì sao SSA thành “sao chép”? | Mặt nạ của SSA (G₂) chỉ chừa một ô mỗi hàng; softmax của một ô luôn là 100%, nên đầu ra là đúng giá trị của điểm tranh đó. |
| Độ phức tạp của SCSA? | Mỗi bảng N × M (lưới 64 × 64 → ~16,8 triệu ô), SCA và SSA mỗi nhánh một bảng, tính đủ rồi mới cấm: tốn hơn mô hình gốc. Tính riêng từng vùng là hướng phát triển. |
| Q, K, V là gì, nói ngắn? | Như tra cứu: Q là câu hỏi (điểm của ảnh), K là nhãn từng ngăn, V là đồ trong ngăn (điểm của tranh). |
| SCSA có hàm loss hay bước huấn luyện nào không? | Không. Không tham số mới, không loss mới; chỉ chạy lúc suy luận trên trọng số gốc của backbone. |
| So với các phương pháp semantic chuyên biệt thì sao? | SANet + SCSA tốt nhất về SSL (0,88); StyTr2 + SCSA tốt nhất về FID, CFSD; GLStyleNet SSL tốt nhưng CFSD 0,399 (vỡ bố cục). |

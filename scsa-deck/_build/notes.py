"""Speaker notes, the single source of truth (they override `notes=` in s_*.py).

NOTES[id] is a list of (label, text), one entry per step of the slide (= per fragment).
Step 0 is what the slide shows on its own when you arrive; every later step is one click, so
a slide with n fragments has n entries and n-1 "Bấm" cues. build.py turns each entry into one
line ("Bấm k · label: text") and checks the counts.
Numbers quoted here (35/63/1/1, 99, 36, 19, ...) come from assets/data/scsa-data.json and the
paper's Table 1 / Fig. 6; re-check them if that data is regenerated.
After editing, run `python3 _build/build.py` then `python3 _build/sync_script_md.py`.
"""

NOTES = {
"cover": [
 ("Mở đầu", "Chào mọi người. Hôm nay mình trình bày SCSA, paper CVPR 2025: dạy attention nhìn đúng vùng khi chuyển phong cách cho ảnh. Mình giả định mọi người chưa biết style transfer. Ba ảnh bên phải là thật, từ repo của tác giả: ảnh chụp Yosemite, một bức tranh núi, và kết quả tô ảnh theo tranh bằng SCSA. Cả buổi dùng đúng cặp ảnh này."),
],
"hook": [
 ("Hai kết quả", "Kết quả thật trong paper, cùng một đầu vào ở giữa. Trái là SANet, mô hình có sẵn. Phải là SANet cộng SCSA."),
 ("Vách núi", "Nhìn vách núi lớn. SANet tô nó bằng màu kem của trời. SCSA tô đúng màu xanh của núi."),
 ("Câu hỏi", "Vì sao bên trái tô nhầm? Cả buổi trả lời câu này. Giữ nó trong đầu."),
],
"minute": [
 ("Attention chọn style", "Cả paper trong một sơ đồ. Ảnh và tranh vào khối attention; khối này chọn mỗi điểm của ảnh lấy style từ đâu trong tranh. Nó chọn theo kiểu “trông giống”, nên tô nhầm vùng, như SANet vừa rồi."),
 ("Thêm nhãn vùng", "SCSA thêm bản đồ nhãn, mỗi màu một vùng. Attention chỉ lấy style từ vùng cùng nhãn, nên đúng vùng."),
 ("Hai cách nhìn", "Bên trong có hai cách. SCA nhìn cả vùng, lấy tông chung. SSA nhìn một điểm, lấy nét cọ, tức vệt sơn của tranh. Không train lại. Chưa cần hiểu hết, cả buổi đi từng cái."),
],
"roadmap": [
 ("Năm chặng", "Mỗi chặng là một câu hỏi. Bối cảnh: style transfer là gì. Nền tảng: attention chọn style thế nào. Vấn đề: vì sao tô nhầm vùng. SCSA: sửa bằng cách nào. Kết quả: tốt tới đâu."),
 ("Trọng tâm", "Chặng 4 là trọng tâm. Lạc thì hỏi, mình quay về đầu chặng."),
],
"ch1": [
 ("Mở chặng", "Chặng 1, bối cảnh. Câu hỏi: style transfer là gì?"),
],
"st": [
 ("Ảnh chụp", "Ảnh chụp cho bố cục: trời ở trên, vách núi ở giữa, rừng ở dưới."),
 ("Bức tranh", "Bức tranh cho lớp áo: màu, nét cọ, bề mặt."),
 ("Kết quả", "Bố cục cũ, áo mới. Để ý: trời mang màu kem của tranh, vách núi mang màu xanh của núi."),
 ("Arbitrary", "Một mô hình dùng cho mọi bức tranh, không train lại. Hỏi nhanh: vách núi bị tô màu trời có thành công không? Không: vẫn là áo của tranh, nhưng mặc sai chỗ."),
],
"history": [
 ("2016 · Gatys", "Chỉnh từng pixel cho tới khi ảnh vừa giống bố cục, vừa giống màu tranh. Đẹp nhưng chậm, mỗi ảnh vài phút."),
 ("2017 · AdaIN", "Một mạng cho mọi tranh, khớp tông cả ảnh. Nhanh nhưng thô. Sẽ gặp lại ở chặng 2."),
 ("2019–22 · SANet, StyTr2", "Attention: mỗi điểm của ảnh tự đi tìm style."),
 ("2024 · StyleID", "Attention bên trong Stable Diffusion."),
 ("2025 · SCSA", "Attention biết nhãn vùng."),
 ("Khung cam", "Ba mô hình ở giữa là ba mô hình SCSA cắm vào. SCSA không thay chúng."),
],
"maps": [
 ("Ảnh và tranh", "Ảnh chụp và bức tranh của ta."),
 ("Hai bản đồ nhãn", "Thêm hai bản đồ nhãn (semantic map). Mỗi màu là một vùng. Đây là file thật trong repo."),
 ("Màu là mã nhãn", "Đỏ là trời, vàng là vách núi, xanh lá là rừng, xanh dương là dãy xa. Màu chỉ là mã, không phải màu thật."),
 ("Nối cặp", "Nối đúng cặp: trời với trời, vách núi với vách núi."),
 ("Luật", "Mỗi vùng chỉ lấy style từ vùng cùng tên. Đầu vào giờ là bộ bốn: ảnh, map ảnh, tranh, map tranh. Ai vẽ map? Người dùng, hoặc mô hình phân đoạn. Paper không tự sinh map, đó là một hạn chế."),
],
"ch2": [
 ("Mở chặng", "Chặng 2, nền tảng. Câu hỏi: attention chọn style thế nào? Bốn khái niệm: lưới điểm, attention, softmax với mask, AdaIN; rồi gộp lại thành Universal Attention. Đừng bỏ chặng này: SCSA chỉ là thay đổi nhỏ trên những thứ này."),
],
"grid": [
 ("Ảnh 512×512", "Từ “điểm” dùng suốt phần sau. Đây là ảnh 512 nhân 512 pixel."),
 ("Lưới điểm", "Encoder cắt ảnh thành lưới. Ở đây 12×12 cho dễ nhìn; mô hình thật 64×64, tức 4.096 điểm."),
 ("Điểm là vector", "Mỗi điểm là một vector, ví dụ 512 số, mô tả mảng ảnh quanh nó: màu, cạnh, bề mặt. Không phải một pixel."),
 ("Decoder", "Decoder vẽ lưới ngược lại thành ảnh. SCSA chỉ sửa ở giữa, trên lưới điểm."),
],
"attn": [
 ("Query", "Attention giống tra từ điển, nhưng mềm. Một điểm vách núi của ảnh hỏi: “style nào hợp với tôi?”. Đây là query."),
 ("Key và value", "Nó so với các điểm của tranh. Mỗi điểm có key để so và value để lấy về. Mình chỉ vẽ 4 trong 4.096 điểm: trời, dãy xa, vách núi, rừng. Mỗi điểm là một vị trí trên lưới, không phải pixel. Đường càng dày càng giống."),
 ("Trọng số", "Độ giống đổi thành trọng số: 35, 63, 1 và 1 phần trăm."),
 ("Trộn", "Màu chảy về theo trọng số rồi trộn lại."),
 ("Lỗi", "Chú ý: điểm vách núi xám nhạt giống dãy xa và trời của tranh hơn vách núi của tranh, nên 99% màu lấy từ sai vùng. Đó là lỗi ta thấy ở SANet. Số tính minh hoạ trên màu của ảnh mẫu, không phải số của mô hình thật."),
],
"softmax": [
 ("Điểm số", "Vẫn bốn điểm đó. Điểm số giống nhau: dãy xa cao nhất, khoảng 4,6; trời khoảng 4; vách núi và rừng quanh 0,5."),
 ("Softmax", "Đổi điểm số thành phần trăm, cộng lại đủ 100: 35, 63, 1, 1. Điểm cao được phần lớn, nhưng không ai bị bỏ hẳn."),
 ("Cấm", "Luật: điểm vách núi chỉ lấy từ vách núi, ba điểm kia bị cấm. Cách cấm: đặt âm vô cực vào điểm số của chúng; e mũ âm vô cực bằng 0 nên ba cột về đúng 0, vách núi nhận 100%. Không sửa gì khác, nên SCSA cắm được vào mô hình đã train."),
 ("Chốt", "Toàn bộ SCSA chỉ là quyết định ô nào bị cấm."),
],
"adain": [
 ("Tông của ảnh", "AdaIN là phương pháp 2017; SCSA dùng lại. Tông của một ảnh tóm trong hai số: μ là màu trung bình, σ là độ tương phản (đọc “miu” và “xích-ma”). Ảnh chụp này xám ấm."),
 ("Tông của tranh", "Bức tranh có μ, σ riêng: kem xanh, tương phản thấp hơn."),
 ("Khoác tông", "Bỏ μ, σ của ảnh, khoác μ, σ của tranh. Ảnh bên phải là phép tính thật trên pixel: cả ảnh ngả về tông của tranh. Trong mô hình, phép này làm trên lưới điểm, không phải pixel."),
 ("Giới hạn", "Chỉ một cặp số cho cả ảnh, nên trời, vách núi, rừng bị kéo về cùng một tông. S-AdaIN ở chặng 4 sẽ sửa."),
],
"ua": [
 ("Hai lưới", "Paper gọi khối attention của SANet, StyTr2, StyleID là Universal Attention, viết tắt UA. Trái: 144 điểm của ảnh. Phải: 144 điểm của tranh."),
 ("Quét", "Khung magenta là câu hỏi đang xét, chạy qua vài điểm. Mỗi lần nối tới 8 điểm tranh giống nhất (số 8 mình chọn cho dễ nhìn). Đường đen là cùng vùng, magenta là sang vùng khác. Chữ ở giữa là phần trăm trọng số sang vùng khác, tính trên cả 144 điểm. Đoạn này chạy khoảng 8 giây, nói trong lúc đó."),
 ("Chốt", "Mỗi điểm nhìn tất cả 144 thẻ, không ai hỏi điểm đó thuộc vùng nào. Với lưới thật 64×64, bảng so có 16 triệu ô. Số tính minh hoạ."),
],
"ch3": [
 ("Mở chặng", "Chặng 3, vấn đề. Câu hỏi: vì sao tô nhầm vùng? Ta chạy attention trên chính ảnh Yosemite và đếm xem bao nhiêu style lấy sai chỗ."),
],
"err1": [
 ("Bức ghép UA", "Chạy UA cho cả 144 điểm của ảnh. Mỗi ô là màu trộn mà điểm đó lấy về."),
 ("Phủ magenta", "Phủ magenta lên ô lấy style từ vùng khác, càng đậm càng nhiều. Trung bình 36% trọng số sang vùng sai; 36 trên 144 điểm lấy phần lớn style từ vùng sai, dồn vào vách núi."),
 ("Kết quả thật", "So với kết quả thật của SANet: đúng chỗ đó, vách núi mang màu trời."),
 ("Lỗi 1", "Phép tính của mình dùng màu trung bình nên chỉ là minh hoạ, nhưng nó chỉ ra cùng một chỗ sai với mô hình thật. Lỗi 1: lấy style từ sai vùng."),
],
"err23": [
 ("Lỗi 2 · loang lổ", "Dải trời cắt từ hai kết quả thật của paper. Trên là SANet: trời lẫn vệt xanh của núi, vì mỗi điểm tự chọn style theo cấu trúc riêng. Dưới là SANet cộng SCSA: cả vùng trời một tông, đó là điều ta muốn."),
 ("Lỗi 3 · nhạt nhoà", "Bốn điểm tranh mà điểm vách núi lấy nhiều nhất đều sắc nét, nhưng trộn lại thành màu đục, mất nét cọ."),
 ("Hai lỗi kéo ngược", "Lỗi 2 muốn các điểm trong vùng giống nhau; lỗi 3 muốn mỗi điểm giữ nét riêng. Vì vậy SCSA cần hai cách nhìn."),
],
"fixmap": [
 ("Sai vùng", "Sửa bằng luật cấm theo nhãn, có sẵn trong cả SCA và SSA, nên lỗi 1 được sửa miễn phí."),
 ("Loang lổ", "Sửa bằng SCA: cả vùng dùng chung một tông."),
 ("Nhạt nhoà", "Sửa bằng SSA: chỉ lấy một điểm, giữ nguyên nét cọ."),
 ("Một gốc chung", "Cả ba lỗi chung một gốc: attention không biết nhãn vùng. Các slide sau phóng to cột phải."),
],
"ch4": [
 ("Mở chặng", "Chặng 4, SCSA, phần trọng tâm. Câu hỏi: sửa bằng cách nào? Đi từ ý tưởng, sơ đồ, rồi từng khối: SCA, S-AdaIN, SSA, phép trộn."),
],
"idea": [
 ("Câu cần nhớ", "Câu nhớ nhất của paper: chỉ nhìn trong vùng cùng nhãn. Đây là một điểm vách núi của ảnh."),
 ("SCA", "Cách nhìn thứ nhất. Nó nhìn tất cả điểm vách núi của tranh; vùng khác bị gạch chéo, tức bị cấm. Kết quả: tông chung của cả vùng."),
 ("SSA", "Cách nhìn thứ hai. Chỉ một đường nối, tới đúng một điểm vách núi giống nhất, lấy nguyên nét cọ (vệt sơn) của điểm đó."),
 ("Tên gọi", "S là Semantic, dùng nhãn vùng. C là Continuous, nhìn cả vùng, tức SCA. S là Sparse, thưa, một điểm, tức SSA. A là Attention."),
],
"pipe": [
 ("Đầu vào", "Bốn đầu vào: ảnh, map ảnh, tranh, map tranh. Encoder biến cả bốn thành lưới điểm."),
 ("SCA", "Nhánh trên: hỏi bằng map, lấy tông chung của cả vùng."),
 ("S-AdaIN và SSA", "Nhánh dưới hai bước: S-AdaIN đổi tông ảnh theo từng vùng, rồi SSA tìm một điểm giống nhất trong cùng vùng."),
 ("Trộn", "Trộn tông chung, nét cọ, và cộng bố cục của ảnh vào (đường đứt nét magenta)."),
 ("Decoder", "Decoder vẽ ra ảnh."),
 ("Chốt", "Encoder, decoder giữ nguyên; chỉ ba khối ở giữa là SCSA."),
],
"sca": [
 ("Câu hỏi từ map", "SCA khác UA ở hai chỗ. Chỗ một: câu hỏi không lấy từ ảnh mà từ bản đồ nhãn."),
 ("Cùng một câu", "Map là mảng màu phẳng, nên mọi điểm vách núi hỏi cùng một câu."),
 ("Luật G1", "Chỗ hai: khác nhãn thì cấm. Trọng số chia đều cho mọi điểm vách núi của tranh."),
 ("Bức ghép", "Mỗi điểm vách núi nhận cùng một màu: trung bình của vách núi trong tranh, màu xanh. Làm tương tự các vùng khác, ta được bức ghép bên phải, tính thật trên ảnh mẫu."),
 ("Ưu và nhược", "Liền mạch, đúng vùng, hết loang lổ. Cái giá: phẳng, mất nét cọ. Hỏi nhanh: giữ luật cấm mà hỏi bằng ảnh thì sửa được lỗi nào? Chỉ lỗi sai vùng."),
],
"sadain": [
 ("Ảnh gốc", "Nhớ AdaIN: hai số, màu trung bình và độ tương phản. Đây là ảnh gốc."),
 ("AdaIN cả ảnh", "Một cặp số cho mọi vùng, nên cả ảnh ngả một tông."),
 ("S-AdaIN", "Tính riêng cho từng vùng nhãn. Vách núi nhận tông xanh của vách núi trong tranh, dãy xa nhận tông hồng. Ba ảnh này là phép tính thật trên pixel."),
 ("Để làm gì", "Để SSA so “giống” trên cùng thang màu với tranh. Ảnh chụp có vách núi xám, tranh có vách núi xanh; so ngay thì bị lệch. Trong mô hình, phép này làm trên lưới điểm."),
],
"ssa": [
 ("Câu hỏi", "SSA hỏi bằng ảnh đã qua S-AdaIN. Đây là một điểm vách núi đang hỏi."),
 ("Luật G2 · cấm", "Khác nhãn thì cấm, chỉ còn vùng vách núi của tranh."),
 ("Giữ một điểm", "Trong vùng đó chỉ giữ đúng một điểm giống nhất (khung magenta); bốn khung đen là ứng viên tiếp theo, bị bỏ. Chỉ còn một điểm thì trọng số 100%, tức copy nguyên mảnh đó."),
 ("Bức ghép", "Mảnh bay sang đúng vị trí trong kết quả. Làm cho cả 144 điểm: mỗi ô là một mảnh tranh thật, giữ nguyên nét cọ."),
 ("Chốt", "Hết nhạt nhoà. Ý tưởng giống Style-Swap 2016, nhưng khoá trong vùng ngữ nghĩa và không cần train."),
],
"matrices": [
 ("UA", "Mỗi ma trận: hàng là điểm của ảnh (ba trời, ba vách núi), cột là điểm của tranh; ô càng đậm, trọng số càng lớn. UA dày đặc, mỗi hàng trải khắp nơi; ô magenta là trọng số tràn sang vùng khác. Lỗi 1 nằm ở đó."),
 ("SCA", "Luật G1 gạch bỏ hai khối chéo, phần còn lại đều nhau vì hỏi bằng map phẳng. Hết loang lổ."),
 ("SSA", "Mỗi hàng giữ đúng một ô, luôn trong khối đúng. Hết nhạt nhoà."),
 ("Chốt", "Nếu chỉ nhớ một hình của cả buổi, hãy nhớ hình này. Giá trị trong hình là minh hoạ."),
],
"mix": [
 ("SSA thuần", "Kết quả cuối là tông chung từ SCA, cộng nét cọ từ SSA, cộng bố cục của ảnh; hai hệ số là một nút chỉnh. Đây là nút ở SSA thuần: toàn mảnh tranh thật, sắc nét nhưng màu nhảy giữa các ô."),
 ("SCA thuần", "Kéo hết sang SCA: đều màu nhưng phẳng."),
 ("SANet dùng", "0,7 tông chung và 0,3 nét cọ. Bức ghép này tính trên lưới 12×12 nên còn thô."),
 ("Kết quả thật", "Bên phải là kết quả thật của SANet cộng SCSA trên cùng cặp ảnh, ở độ phân giải đầy đủ."),
 ("Chốt", "Kết quả = tông chung + nét cọ + bố cục. Mô hình khác dùng hệ số khác: StyTr2 là 1,2 và 0,5; StyleID là 0,8 và 0,2."),
],
"plug": [
 ("SANet", "Mỗi mô hình có một khối attention giữa encoder và decoder. Đây là SANet, một mạng CNN, tỉ lệ trộn 0,7 và 0,3."),
 ("SCSA thay khối", "SCSA thay đúng khối đó; encoder, decoder và trọng số gốc giữ nguyên."),
 ("StyTr2", "Một transformer, tỉ lệ 1,2 và 0,5."),
 ("StyleID", "Một mô hình diffusion, tỉ lệ 0,8 và 0,2. Hỏi thuần bằng map làm mất chi tiết nên tác giả pha thêm feature của ảnh (Appendix C)."),
 ("Chốt", "Không train lại, dùng ngay với mô hình có sẵn."),
],
"ch5": [
 ("Mở chặng", "Chặng 5, kết quả. Câu hỏi: tốt tới đâu? Ảnh thật, số thật từ paper, ablation, hạn chế, và cách chạy code."),
],
"results": [
 ("SANet", "Ba ví dụ lấy nguyên từ hình kết quả của paper. Mỗi hàng: ảnh nội dung, ảnh phong cách, mô hình gốc, mô hình cộng SCSA. Hàng đầu là cặp ảnh ta theo dõi cả buổi: vách núi từ màu trời sang màu núi."),
 ("StyTr2", "Ví dụ thác nước: bản gốc màu loang lổ, bản SCSA giữ dòng thác trắng và đá tối."),
 ("StyleID", "Ví dụ chân dung: áo, mặt, nền lấy nét từ đúng vùng tương ứng trong tranh. Mình chỉ mô tả những gì thấy trên ba ảnh; số tổng quát ở slide sau."),
],
"metrics": [
 ("SSL", "Bốn thước đo, mỗi lần bấm một cái. SSL (Semantic Style Loss): cắt kết quả và tranh theo nhãn, so style trời với trời, vách núi với vách núi. Thấp là tốt."),
 ("FID", "Cả tập kết quả có trông như tranh không, xét tổng thể. Thấp là tốt."),
 ("CFSD", "Kết quả còn giữ bố cục của ảnh gốc không. Thấp là tốt."),
 ("Người xem", "40 người, 1.200 phiếu, so từng cặp có và không có SCSA. Cao là tốt."),
 ("Lưu ý", "SSL do chính tác giả đề xuất và đo đúng điều SCSA tối ưu, nên SCSA thắng ở SSL gần như chắc chắn. Nhìn thêm FID và CFSD."),
],
"ssl": [
 ("Mô hình gốc", "Thước đo SSL, thấp là tốt. Cột xám là mô hình gốc: SANet 1,66; StyTr2 1,98; StyleID 1,75."),
 ("Cộng SCSA", "Cột đen là cộng SCSA: 0,88; 1,22; 1,24. Lỗi style theo vùng giảm 47, 38 và 29%. SANet cộng SCSA còn tốt hơn cả năm phương pháp semantic chuyên biệt."),
 ("Thước đo khác", "FID tốt hơn nhẹ ở cả ba. CFSD: riêng StyleID cộng SCSA giữ bố cục kém hơn, 0,092 lên 0,118; đó là cái giá. Người xem chọn SCSA 83, 84 và 78%. Số từ Table 1, trên 91 bộ do tác giả tự tuyển."),
],
"ablation": [
 ("Đủ cả ba", "Bỏ từng khối, trên StyleID. Đủ cả ba khối: 1,245, làm mốc."),
 ("Bỏ SSA", "1,33: mất texture."),
 ("Bỏ S-AdaIN", "1,76: kém chính xác, ít chi tiết."),
 ("Bỏ SCA", "2,30, gần gấp đôi: lệch màu giữa các vùng."),
 ("Chốt", "SCA lo tông chung, SSA lo nét cọ; thiếu cái nào cũng tệ hơn. Phản biện: trên SANet, bỏ S-AdaIN gần như không đổi SSL (0,876 so với 0,877); với mô hình yếu hơn không phải khối nào cũng cần. Số từ Fig. 6 và Appendix F."),
],
"limits": [
 ("Cần map nhãn", "Sáu điều chưa giải quyết. Một: phải tự có bản đồ nhãn, và nhãn hai bên phải khớp; tác giả tự nêu điều này."),
 ("Dùng lại mảnh", "Hai: SSA chỉ lấy một điểm nên một mảnh tranh có thể bị dùng lại nhiều lần. Trên lưới minh hoạ, một mảnh bị dùng 19 lần (khung magenta). Ở độ phân giải thật có thể gây lặp texture."),
 ("Bốn điều thảo luận", "Chỉ 91 bộ tự tuyển. SSL do tác giả tự đặt. Chậm và tốn bộ nhớ hơn. Vùng của ảnh không có vùng cùng nhãn bên tranh thì cả hàng bị cấm, paper không nói xử lý thế nào. Mỗi điều là một hướng mở rộng cho proposal."),
],
"code": [
 ("Bốn file", "Bốn file bên trái chính là bộ bốn ta dùng cả buổi, trong sem_data/29 của repo."),
 ("Bốn lệnh", "Clone repo; chạy sem.py tạo mặt nạ nhãn; vào SANet+SCSA; chạy SCSA.py với mẫu 29. Môi trường Python 3.8, PyTorch 2.4.1; tải trọng số gốc của SANet vào thư mục models. Muốn so với bản gốc thì chạy SANet.py cùng ảnh."),
 ("Lệnh đầy đủ", "Có thêm hai cờ sem_map_64 và sem_map_32, trỏ tới sem_precomputed_feats/29. StyleID dùng tên cờ khác, và sem.py có bảng màu cứng theo số thư mục."),
],
"summary": [
 ("Một câu", "Mang về một câu: chỉ lấy style từ vùng cùng nhãn."),
 ("Trước và sau", "Đây là câu trả lời cho câu hỏi đầu buổi: SANet tô vách núi bằng màu vùng khác vì attention không biết nhãn vùng; SCSA cấm điều đó."),
 ("Bên trong", "SCA lấy tông chung của cả vùng, SSA giữ nét cọ của một điểm. Không train lại; lỗi style theo vùng giảm 29–47%. Nếu chỉ nhớ một hình: ba ma trận ở slide 25. Mình xin nhận câu hỏi."),
],
}

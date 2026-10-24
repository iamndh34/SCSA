# SPEC — SCSA explained from zero (HyperFrames slideshow)

GOAL:    Người mới hiểu vì sao attention tô sai vùng và SCSA sửa thế nào, nhớ một câu: "chỉ lấy style từ vùng cùng nhãn".
OUTPUT:  HyperFrames slideshow, 1920 x 1080, 30 fps, trình chiếu bằng `hyperframes present`; không render MP4.
TIME:    35 slide, ~80 phút nói. Mỗi bước (fragment) 0.8–4 s hoạt hình, rồi giữ yên.

LOOK:    medium = "tường triển lãm và bản in": ảnh thật được in, dán lên tường, cắt thành mảnh, dán lại.
         ground #EDEFF1 phẳng, không hạt, không gradient. Bản in: viền trắng #FFFFFF 12 px, bóng 0 18 px 40 px rgba(20,24,28,.14).
         ink #16181C (chữ, đường cấu trúc), ink-2 #4B5260 (chú thích).
         accent #C2185B (magenta): một nghĩa duy nhất = "chỗ cần nhìn / chỗ sai", tối đa một từ mỗi tiêu đề.
         nhãn vùng (dữ liệu, chỉ dùng trên bản đồ và mã vùng): trời #E8574B, vách núi #E9B10F, rừng #3E9B4F, dãy xa #3F6FD8.
         vùng bị cấm: sọc chéo 45°, ink 30%, nét 6 px.
         type: Be Vietnam Pro (file trong assets/fonts). Tiêu đề 66 px / 800 / tracking -0.02em / tối đa 2 dòng, trái, x = 192, y = 108.
         dòng chốt 44 px / 600. Thân 40 px / 500. Nhãn trên vật 32 px / 600 với đường dẫn 3 px. Số lớn 140 px / 800.
         mono: JetBrains Mono 28 px, chỉ cho lệnh terminal.
OBJECTS: ảnh Yosemite (29.jpg) và tranh núi (29_paint.jpg) luôn là bản in có viền trắng; bản đồ nhãn là bản in phẳng 4 màu;
         "điểm" là mảnh vuông cắt từ chính bản in (background-position), không phải ô màu trừu tượng;
         attention là đường nối từ một mảnh của ảnh tới mảnh của tranh, độ dày = trọng số;
         kết quả là bức ghép từ mảnh (SSA) hoặc ô màu phẳng (SCA), tính thật trên ảnh mẫu (assets/data/scsa-data.json).
MOTION:  tới: expo.out 0.8 s (bản in đặt xuống: y 28 → 0, scale .985 → 1); di chuyển/camera: power2.inOut 0.7 s;
         đường nối: vẽ 0.5 s power2.inOut; tiêu đề: từng từ blur 6 px → 0, 0.13 s, cách 0.067 s (xen kẽ: cả dòng blur 8 px → 0, 0.18 s);
         stagger mảnh lưới 12 ms; không spring trên chữ; không lặp vô hạn; mọi chuyển động nằm trong timeline (seek được).
SHOTS:   mỗi slide một ý; mỗi bước một chuyển động chính; nhãn xuất hiện cùng vật nó gọi tên.
BANNED:  nền kem + serif; nhãn nhỏ in hoa kiểu "01 · BỐI CẢNH"; pill/chip; ba thẻ một hàng; ô callout có viền trái;
         mọi thứ mờ dần và trượt lên; vòng lặp thở/nhấp nháy; chú giải (legend) tách rời vật; số trang trong khung;
         ô màu trừu tượng thay cho ảnh khi có ảnh thật; số liệu không có nguồn (số minh hoạ ghi rõ "tính minh hoạ trên ảnh mẫu").
QA:      mỗi slide ở bước cuối: chữ ≥ 32 px, không đè nhau, nằm trong khung an toàn 192–1728 x 108–972;
         trình chiếu thật: bấm tới chạy hoạt hình, bấm lùi nhảy thẳng, không lỗi JS; `hyperframes check` sạch lỗi.

from lib import *

S = []

# ---------------- cover ----------------
sid = "cover"
letters = "".join(f'<span class="cover-l">{ch}</span>' for ch in "SCSA")
m = (f'<div id="cover-h" class="big" style="left:192px;top:300px;font-size:220px">{letters}</div>'
     f'<p id="cover-sub" class="ln" style="left:192px;top:520px;width:840px;font-size:52px;font-weight:700">{words("Dạy attention nhìn đúng vùng khi chuyển phong cách cho ảnh", "cover-w", ("đúng","vùng"))}</p>'
     f'{line("cover-paper", "Semantic Continuous-Sparse Attention for Arbitrary Semantic Style Transfer · CVPR 2025", 760, 30, width=780, weight=500, color=INK2)}'
     f'{line("cover-au", "Chunnan Shang, Hongwei Wang, Zhizhong Wang, Xiangming Meng · Zhejiang University", 850, 30, width=780, weight=500, color=INK2)}'
     + print_img("cover-p1", IMG + "29.jpg", 1010, 150, 330, rot=-2)
     + print_img("cover-p2", IMG + "29_paint.jpg", 1384, 196, 320, rot=2)
     + print_img("cover-p3", IMG + "ex1_sanet_scsa.png", 1170, 560, 360, rot=-1))
js = "\n".join([f'tl.fromTo(".cover-l",{{opacity:0.3,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:0.18,ease:"power2.out",stagger:0.1}},0.2);',
               WORDS("cover-w", 0.7), FADE("#cover-paper", 1.2, 0.4), FADE("#cover-au", 1.35, 0.4),
               PLACE("#cover-p1", 0.4), PLACE("#cover-p2", 0.7), PLACE("#cover-p3", 1.5)])
S.append(dict(id=sid, label="Bìa", dur=3.0, frags=[2.4], html=m, js=js, title="SCSA",
  notes="Chào mọi người. Hôm nay mình trình bày SCSA, một paper ở CVPR 2025. Mình giả định mọi người chưa biết style transfer. Ba bức ảnh bên phải là thật, lấy từ repo của tác giả: ảnh chụp thung lũng Yosemite, một bức tranh núi, và kết quả khi tô ảnh chụp theo phong cách bức tranh bằng SCSA. Cả buổi hôm nay mình sẽ dùng đúng cặp ảnh này để giải thích từng bước."))

# ---------------- hook ----------------
sid = "hook"
m = (title(sid, "Cùng ảnh, cùng tranh, hai kết quả", ("hai",))
     + print_img("hook-a", IMG + "ex1_sanet.png", 192, 250, 480)
     + print_img("hook-b", IMG + "ex1_sanet_scsa.png", 1212, 250, 480)
     + print_img("hook-c", IMG + "29.jpg", 768, 300, 168, mat=8)
     + print_img("hook-s", IMG + "29_paint.jpg", 972, 300, 168, mat=8)
     + label("hook-in", "cùng đầu vào", 708, 500, 504, align="center", color=INK2)
     + svg(leader("hook-ar1", [(900, 580), (730, 580)], INK2, 3, False) + '<path id="hook-ah1" d="M744 568 L724 580 L744 592Z" fill="#4B5260"/>'
           + leader("hook-ar2", [(1020, 580), (1190, 580)], INK2, 3, False) + '<path id="hook-ah2" d="M1176 568 L1196 580 L1176 592Z" fill="#4B5260"/>'
           + f'<ellipse id="hook-e1" cx="360" cy="560" rx="118" ry="168" fill="none" stroke="{ACC}" stroke-width="6"/>'
           + f'<ellipse id="hook-e2" cx="1380" cy="560" rx="118" ry="168" fill="none" stroke="{INK}" stroke-width="6" stroke-dasharray="14 10"/>')
     + label("hook-ca", "SANet", 192, 774, 504, 40, align="center", weight=800)
     + label("hook-cb", f'SANet + {acc("SCSA")}', 1212, 774, 504, 40, align="center", weight=800)
     + label("hook-na", "vách núi bị tô bằng màu trời", 192, 834, 504, align="center", color=ACC)
     + label("hook-nb", "vách núi mang màu núi", 1212, 834, 504, align="center")
     + line("hook-q", "Vì sao bên trái tô nhầm? Cả buổi hôm nay trả lời câu này.", 900, 44, align="center"))
js = "\n".join([WORDS(f"{sid}-tw", 0.1), PLACE("#hook-c", 0.3), PLACE("#hook-s", 0.45), FADE("#hook-in", 0.6),
                DRAW("#hook-ar1", 0.7, 0.4, 200), FADE("#hook-ah1", 1.0, 0.15), DRAW("#hook-ar2", 0.7, 0.4, 200), FADE("#hook-ah2", 1.0, 0.15),
                PLACE("#hook-a", 0.8), PLACE("#hook-b", 0.95), FADE("#hook-ca", 1.1), FADE("#hook-cb", 1.2),
                DRAW("#hook-e1", 1.6, 0.6, 950), FADE("#hook-na", 1.9), DRAW("#hook-e2", 2.2, 0.6, 950), FADE("#hook-nb", 2.5),
                WORDS("hook-qw", 3.0) if False else BLUR("#hook-q", 3.0, 0.2)])
S.append(dict(id=sid, label="Câu hỏi mở màn", dur=4.0, frags=[1.5, 2.9, 3.5], html=m, js=js, title="Cùng ảnh, cùng tranh, hai kết quả",
  notes="Hai bức này là kết quả thật trong paper, cùng một đầu vào ở giữa. Trái là SANet, một mô hình style transfer có sẵn. Phải là SANet cộng SCSA. Bấm: nhìn vách núi lớn bên trái. SANet tô nó bằng màu kem của bầu trời trong tranh. Bên phải, vách núi mang màu xanh của núi trong tranh, đúng như ta muốn. Bấm: vì sao bên trái tô nhầm? Cả buổi hôm nay trả lời câu này. Giữ câu hỏi này trong đầu."))

# ---------------- one minute ----------------
sid = "minute"
m = (title(sid, "SCSA trong một phút")
     + print_img("min-p1", IMG + "29.jpg", 192, 250, 260)
     + print_img("min-p2", IMG + "29_paint.jpg", 192, 600, 260)
     + print_img("min-m1", IMG + "29_sem.png", 420, 380, 120, mat=8)
     + print_img("min-m2", IMG + "29_paint_sem.png", 420, 730, 120, mat=8)
     + f'<div id="min-box" style="position:absolute;left:720px;top:470px;width:420px;height:170px;border:4px solid {INK};border-radius:20px;background:#F7F8F9"></div>'
     + label("min-bt1", "Attention", 720, 528, 420, 44, align="center", weight=800)
     + label("min-bt2", f'Attention + {acc("nhãn vùng")}', 720, 528, 420, 40, align="center", weight=800)
     + svg(leader("min-a1", [(488, 380), (600, 380), (716, 520)], INK, 3, False)
           + leader("min-a2", [(488, 730), (600, 730), (716, 590)], INK, 3, False)
           + leader("min-a3", [(548, 440), (640, 440), (716, 540)], ACC, 3, False)
           + leader("min-a4", [(548, 790), (640, 790), (716, 610)], ACC, 3, False)
           + leader("min-a5", [(1144, 555), (1262, 555)], INK, 3, False) + '<path id="min-ah" d="M1250 543 L1270 555 L1250 567Z" fill="#16181C"/>')
     + print_img("min-r", IMG + "ex1_sanet.png", 1274, 330, 420)
     + f'<div id="min-r2" class="print" style="left:1274px;top:330px;width:444px;height:444px;padding:12px;background:transparent;box-shadow:none"><img src="{IMG}ex1_sanet_scsa.png" alt="" style="width:420px;height:420px;object-fit:cover;display:block"></div>'
     + label("min-ra", f'chọn theo “trông giống” → {acc("tô nhầm vùng")}', 1274, 796, 460, 32)
     + label("min-rb", "chỉ lấy style từ vùng cùng nhãn → đúng vùng", 1274, 796, 460, 32)
     + label("min-sca", "SCA: nhìn cả vùng", 740, 668, 400, 32)
     + label("min-ssa", "SSA: nhìn một điểm", 740, 714, 400, 32)
     + line("min-end", "Không train lại: cắm thẳng vào mô hình có sẵn.", 900, 40, left=720, width=1008))
js = "\n".join([WORDS(f"{sid}-tw", 0.1), PLACE("#min-p1", 0.2), PLACE("#min-p2", 0.35), BLUR("#min-box", 0.7, 0.2), FADE("#min-bt1", 0.75, 0.2),
                DRAW("#min-a1", 0.9, 0.5, 400), DRAW("#min-a2", 0.95, 0.5, 400), PLACE("#min-r", 1.2), DRAW("#min-a5", 1.2, 0.3, 200), FADE("#min-ah", 1.45, 0.1), FADE("#min-ra", 1.6),
                HIDE("#min-r2"), HIDE("#min-bt2"), HIDE("#min-rb"),
                PLACE("#min-m1", 2.1), PLACE("#min-m2", 2.25), DRAW("#min-a3", 2.4, 0.5, 400), DRAW("#min-a4", 2.45, 0.5, 400),
                FADE("#min-bt1", 2.6, 0.15, 1, 0), FADE("#min-bt2", 2.7, 0.2),
                FADE("#min-r2", 2.8, 0.01), WIPE("#min-r2", 2.8, 0.9), FADE("#min-ra", 3.0, 0.15, 1, 0), FADE("#min-rb", 3.2, 0.25),
                BLUR("#min-sca", 3.8), BLUR("#min-ssa", 3.95), BLUR("#min-end", 4.2, 0.2)])
S.append(dict(id=sid, label="SCSA trong một phút", dur=5.0, frags=[2.0, 3.6, 4.6], html=m, js=js, title="SCSA trong một phút",
  notes="Cả paper trong một sơ đồ. Bấm: ảnh và tranh đi vào một khối gọi là attention, khối này quyết định mỗi điểm của ảnh lấy style từ đâu trong tranh. Nó chọn theo kiểu “trông giống”, nên tô nhầm vùng, như kết quả SANet ta vừa thấy. Bấm: SCSA thêm hai bản đồ nhãn, mỗi màu là một vùng: trời, vách núi, rừng, dãy xa. Attention giờ chỉ được lấy style từ vùng cùng nhãn, và kết quả đúng vùng. Bấm: bên trong là hai cách nhìn, SCA nhìn cả vùng để lấy tông chung, SSA nhìn một điểm để lấy nét cọ. Và không phải train lại gì cả. Chưa cần hiểu hết các từ này, cả buổi sẽ đi qua từng cái."))

# ---------------- roadmap + chapter cards ----------------
XS = [300, 630, 960, 1290, 1620]
CH = ["Bối cảnh", "Nền tảng", "Vấn đề", "SCSA", "Kết quả"]
QS = ["Style transfer là gì?", "Attention chọn style thế nào?", "Vì sao tô nhầm vùng?", "Sửa bằng cách nào?", "Tốt tới đâu?"]

def rail(sid, cur, show_q=True):
    m = svg(f'<path id="{sid}-rl" d="M{XS[0]} 440 L{XS[-1]} 440" stroke="#C9CDD3" stroke-width="6" stroke-linecap="round" fill="none"/>')
    for i, (x, n, q) in enumerate(zip(XS, CH, QS)):
        done = cur is not None and i < cur
        now = cur is not None and i == cur
        col = INK if (cur is None or now) else ("#7C838F" if done else "#A3A9B2")
        fill = INK if now else ("#7C838F" if done else GROUND)
        m += f'<div id="{sid}-d{i}" style="position:absolute;left:{x-22}px;top:418px;width:44px;height:44px;border-radius:50%;background:{fill};border:5px solid {col}"></div>'
        m += label(f"{sid}-n{i}", n, x - 160, 340, 320, 40, col, "center", 800)
        if show_q:
            m += label(f"{sid}-q{i}", q, x - 150, 488, 300, 30, INK2 if cur is None else col, "center", 500)
    return m

sid = "roadmap"
m = title(sid, "Năm chặng, từ tổng quát tới chi tiết") + rail(sid, None)
m += f'<div id="roadmap-ring" style="position:absolute;left:{XS[3]-40}px;top:400px;width:80px;height:80px;border-radius:50%;border:6px solid {ACC}"></div>'
m += line("roadmap-end", f'Mỗi chặng mở bằng một câu hỏi, rồi mới đi vào chi tiết. {acc("Chặng 4")} là trọng tâm.', 760, 40)
js = [WORDS(f"{sid}-tw", 0.1), DRAW("#roadmap-rl", 0.3, 0.8, 1400)]
for i in range(5):
    js += [T(f"#roadmap-d{i}", 0.5 + 0.15*i, '{opacity:0,scale:0.4}', '{opacity:1,scale:1}', 0.5, "back.out(1.4)"), BLUR(f"#roadmap-n{i}", 0.55 + 0.15*i), FADE(f"#roadmap-q{i}", 0.7 + 0.15*i, 0.3)]
js += [T("#roadmap-ring", 2.0, '{opacity:0,scale:1.6}', '{opacity:1,scale:1}', 0.5, "expo.out"), BLUR("#roadmap-end", 2.3, 0.2)]
S.append(dict(id=sid, label="Lộ trình", dur=3.2, frags=[1.7, 2.8], html=m, js="\n".join(js), title="Năm chặng, từ tổng quát tới chi tiết",
  notes="Năm chặng, mỗi chặng là một câu hỏi. Bối cảnh: style transfer là gì. Nền tảng: attention chọn style thế nào, phần này có năm slide: bốn khái niệm, mỗi cái một hoạt hình, rồi gộp lại thành Universal Attention. Vấn đề: vì sao tô nhầm vùng, ta sẽ thấy tận mắt trên chính bức ảnh Yosemite. SCSA: sửa bằng cách nào. Kết quả: tốt tới đâu, số liệu và hạn chế. Bấm: vòng tròn dừng ở chặng 4, SCSA, đây là trọng tâm. Lạc thì hỏi, mình quay về đầu chặng."))

CHAPTER_NOTES = [
  "Chặng 1, bối cảnh. Câu hỏi: style transfer là gì, và phiên bản “semantic” muốn thêm điều gì.",
  "Chặng 2, nền tảng. Câu hỏi: attention chọn style thế nào. Bốn khái niệm: lưới điểm, attention, softmax với mask, và AdaIN. Sau đó gộp lại thành Universal Attention, khối attention sẵn có của các mô hình. Đừng bỏ chặng này, vì cả phần SCSA chỉ là thay đổi nhỏ trên những thứ này.",
  "Chặng 3, vấn đề. Câu hỏi: vì sao tô nhầm vùng. Ta chạy attention trên chính bức ảnh Yosemite và đếm xem bao nhiêu style lấy sai chỗ.",
  "Chặng 4, SCSA, phần trọng tâm. Câu hỏi: sửa bằng cách nào. Đi từ ý tưởng, sơ đồ, rồi từng khối: SCA, S-AdaIN, SSA, phép trộn.",
  "Chặng 5, kết quả. Câu hỏi: tốt tới đâu. Ảnh thật, số thật từ paper, ablation, hạn chế, và cách chạy code.",
]

def chapter(k):
    sid = f"ch{k+1}"
    m = rail(sid, k, show_q=False)
    prev = max(k - 1, 0)
    m += f'<div id="{sid}-ring" style="position:absolute;left:{XS[prev]-40}px;top:400px;width:80px;height:80px;border-radius:50%;border:6px solid {INK}"></div>'
    m += label(f"{sid}-k", f"Chặng {k+1} · {CH[k]}", 192, 600, 1536, 40, INK2, weight=600)
    m += f'<h1 id="{sid}-qq" class="t" style="top:660px;font-size:96px;width:1536px">{words(QS[k], sid + "-qw")}</h1>'
    js = [FADE(f"#{sid}-rl", 0, 0.3)] + [FADE(f"#{sid}-d{i}", 0.05*i, 0.3) for i in range(5)] + [FADE(f"#{sid}-n{i}", 0.05*i, 0.3) for i in range(5)]
    js += [MOVE(f"#{sid}-ring", 0.3, 0, 0, XS[k] - XS[prev], 0, 0.7), BLUR(f"#{sid}-k", 0.8), WORDS(f"{sid}-qw", 0.95, 0.09)]
    return dict(id=sid, label=f"Chặng {k+1}: {CH[k]}", dur=2.0, frags=[1.6], html=m, js="\n".join(js), title=f"Chặng {k+1} · {QS[k]}", notes=CHAPTER_NOTES[k])

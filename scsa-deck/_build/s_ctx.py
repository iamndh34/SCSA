from lib import *

S = []

# ---------------- style transfer ----------------
sid = "st"
m = (title(sid, "Style transfer: giữ bố cục, thay lớp áo", ("lớp", "áo"))
     + print_img("st-a", IMG + "29.jpg", 192, 290, 400)
     + label("st-plus", "+", 616, 440, 104, 80, INK2, "center", 800)
     + print_img("st-b", IMG + "29_paint.jpg", 720, 290, 400)
     + label("st-eq", "=", 1144, 440, 108, 80, INK2, "center", 800)
     + print_img("st-c", IMG + "29.jpg", 1252, 290, 400)
     + f'<div id="st-c2" style="position:absolute;left:1264px;top:302px;width:400px;height:400px"><img src="{IMG}ex1_sanet_scsa.png" alt="" style="width:400px;height:400px;object-fit:cover;display:block"></div>'
     + label("st-la", "ảnh chụp cho <b>bố cục</b>: trời, vách núi, rừng", 192, 738, 424, 32, align="center", weight=500)
     + label("st-lb", "tranh cho <b>lớp áo</b>: màu, nét cọ", 720, 738, 424, 32, align="center", weight=500)
     + label("st-lc", "kết quả: bố cục cũ, áo mới", 1252, 738, 424, 32, align="center", weight=500)
     + line("st-end", f'<b>Arbitrary</b>: một mô hình dùng cho {acc("mọi")} bức tranh, không train lại.', 860, 44))
js = "\n".join([WORDS(f"{sid}-tw", 0.1), PLACE("#st-a", 0.3), BLUR("#st-la", 0.6),
                BLUR("#st-plus", 1.1), PLACE("#st-b", 1.15), BLUR("#st-lb", 1.45),
                BLUR("#st-eq", 2.0), PLACE("#st-c", 2.05), WIPE("#st-c2", 2.5, 1.0), BLUR("#st-lc", 3.3),
                BLUR("#st-end", 3.8, 0.2)])
S.append(dict(id=sid, label="Style transfer là gì", dur=4.6, frags=[0.9, 1.8, 3.6, 4.2], html=m, js=js, title="Style transfer: giữ bố cục, thay lớp áo",
  notes="Ảnh chụp cho bố cục: trời ở trên, vách núi ở giữa, rừng ở dưới. Bấm: bức tranh cho lớp áo: màu, nét cọ, bề mặt. Bấm: kết quả là bố cục cũ, áo mới. Nhìn lúc ảnh được tô lại: trời mang màu kem của trời trong tranh, vách núi mang màu xanh của núi trong tranh. Bấm: arbitrary nghĩa là một mô hình dùng cho mọi bức tranh, không phải train lại cho từng tranh. Hỏi nhanh: nếu vách núi bị tô màu trời thì có tính là thành công không? Vẫn là mặc áo của tranh, nhưng mặc sai chỗ."))

# ---------------- ten years ----------------
sid = "history"
CX = [345, 652, 960, 1267, 1574]
stops = [("2016", "Gatys", "Tối ưu từng ảnh. Đẹp, nhưng chậm."), ("2017", "AdaIN", "Khớp tông cả ảnh. Nhanh, nhưng thô."),
         ("2019–22", "SANet, StyTr2", "Attention: mỗi điểm tự đi tìm style."), ("2024", "StyleID", "Attention bên trong Stable Diffusion."),
         ("2025", "SCSA", "Attention biết nhãn vùng.")]
m = title(sid, "Mười năm style transfer, năm bước") + svg(f'<path id="history-rl" d="M240 470 L1680 470" stroke="#C9CDD3" stroke-width="6" stroke-linecap="round" fill="none"/>'
      + f'<rect id="history-br" x="800" y="352" width="628" height="360" rx="28" fill="none" stroke="{ACC}" stroke-width="5" stroke-dasharray="16 12"/>')
for i, (x, (y_, n, d)) in enumerate(zip(CX, stops)):
    last = i == 4
    m += f'<div id="history-d{i}" style="position:absolute;left:{x-18}px;top:452px;width:36px;height:36px;border-radius:50%;background:{ACC if last else INK}"></div>'
    m += label(f"history-y{i}", y_, x - 150, 378, 300, 44, ACC if last else INK, "center", 800)
    m += label(f"history-n{i}", n, x - 150, 510, 300, 36, INK, "center", 700)
    m += label(f"history-t{i}", d, x - 145, 560, 290, 32, INK2, "center", 500)
m += f'<div id="history-ring" style="position:absolute;left:{CX[0]-38}px;top:432px;width:76px;height:76px;border-radius:50%;border:6px solid {INK}"></div>'
m += line("history-end", f'SCSA là {acc("mảnh")} {acc("ghép")} cắm vào ba mô hình trong khung: SANet, StyTr2, StyleID.', 790, 40)
js = [WORDS(f"{sid}-tw", 0.1), DRAW("#history-rl", 0.3, 0.8, 1500), HIDE("#history-br")]
for i in range(5):
    t = 0.8 + i * 0.9
    if i: js.append(MOVE("#history-ring", t - 0.1, CX[i-1] - CX[0], 0, CX[i] - CX[0], 0, 0.6))
    else: js.append(T("#history-ring", t - 0.1, '{opacity:0,scale:1.5}', '{opacity:1,scale:1}', 0.5, "expo.out"))
    js += [T(f"#history-d{i}", t, '{scale:0}', '{scale:1}', 0.45, "back.out(1.6)"), BLUR(f"#history-y{i}", t + 0.1), BLUR(f"#history-n{i}", t + 0.2), FADE(f"#history-t{i}", t + 0.3, 0.3)]
js += [FADE("#history-br", 5.4, 0.01), DRAW("#history-br", 5.4, 0.7, 2000), BLUR("#history-end", 5.8, 0.2)]
S.append(dict(id=sid, label="Mười năm", dur=6.6, frags=[1.5, 2.4, 3.3, 4.2, 5.1, 6.2], html=m, js="\n".join(js), title="Mười năm style transfer, năm bước",
  notes="Bấm qua từng mốc. 2016, Gatys: chỉnh từng pixel cho tới khi ảnh vừa giống bố cục, vừa giống chữ ký màu của tranh; đẹp nhưng mỗi ảnh vài phút. 2017, AdaIN: một mạng cho mọi tranh, khớp tông của cả ảnh; nhanh nhưng thô, ta sẽ gặp lại nó ở chặng 2. 2019 đến 2022, SANet và StyTr2: attention, mỗi điểm của ảnh tự đi tìm điểm giống nó trong tranh. 2024, StyleID: attention nằm bên trong Stable Diffusion, không cần train. 2025, SCSA: attention biết nhãn vùng. Bấm cuối: khung cam bao ba mô hình ở giữa, đó là ba backbone SCSA cắm vào; SCSA không thay chúng."))

# ---------------- semantic maps ----------------
sid = "maps"
PX = [192, 582, 972, 1362]; PY, PS = 270, 340
def centroids(labels):
    out = []
    for l in range(4):
        cs = [divmod(i, G) for i, v in enumerate(labels) if v == l]
        out.append((sum(c for _, c in cs) / len(cs), sum(r for r, _ in cs) / len(cs)) if cs else None)
    return out
cc, sc = centroids(DATA["labelsC"]), centroids(DATA["labelsS"])
def pos(base_x, cr): c, r = cr; return base_x + 12 + (c + 0.5) * PS / G, PY + 12 + (r + 0.5) * PS / G
# hand nudges so names sit inside their regions
NUDGE_C = {0: (0, -40), 1: (-26, -34), 2: (-40, 30), 3: (24, 26)}
NUDGE_S = {0: (0, -30), 1: (0, 10), 2: (-30, 20), 3: (0, 0)}
m = (title(sid, "Semantic: mỗi ảnh có thêm một bản đồ nhãn", size=60)
     + print_img("maps-a", IMG + "29.jpg", PX[0], PY, PS) + print_img("maps-b", IMG + "29_sem.png", PX[1], PY, PS)
     + print_img("maps-c", IMG + "29_paint.jpg", PX[2], PY, PS) + print_img("maps-d", IMG + "29_paint_sem.png", PX[3], PY, PS))
for side, base, cents, nud in (("c", PX[1], cc, NUDGE_C), ("s", PX[3], sc, NUDGE_S)):
    for l in range(4):
        if not cents[l]: continue
        x, y = pos(base, cents[l]); x += nud[l][0]; y += nud[l][1]
        colr = "#FFFFFF" if l in (0, 2, 3) else INK
        shadow = "0 1px 3px rgba(0,0,0,.55)" if colr == "#FFFFFF" else "0 0 3px rgba(255,255,255,.8)"
        m += f'<div id="maps-{side}{l}" class="lb" style="left:{x-90:.0f}px;top:{y-20:.0f}px;width:180px;text-align:center;font-size:30px;font-weight:800;color:{colr};text-shadow:{shadow}">{REGN[l]}</div>'
arcs = ""
for l in range(4):
    x1, _ = pos(PX[1], cc[l]); x2, _ = pos(PX[3], sc[l]); y0 = PY + PS + 24
    depth = 70 + l * 34
    arcs += f'<path id="maps-arc{l}" d="M{x1:.0f} {y0} C {x1:.0f} {y0+depth}, {x2:.0f} {y0+depth}, {x2:.0f} {y0}" stroke="{REG[l]}" stroke-width="7" fill="none" stroke-linecap="round"/>'
m += svg(arcs)
m += label("maps-la", "ảnh chụp", PX[0], 222, PS + 24, 30, INK2, "left", 500) + label("maps-lc", "tranh", PX[2], 222, PS + 24, 30, INK2, "left", 500)
m += line("maps-end", f'Mỗi vùng chỉ được lấy style từ vùng {acc("cùng")} {acc("tên")} trong tranh.', 860, 44)
js = [WORDS(f"{sid}-tw", 0.1), PLACE("#maps-a", 0.3), PLACE("#maps-c", 0.45), FADE("#maps-la", 0.6), FADE("#maps-lc", 0.7),
      WIPE("#maps-b", 1.2, 0.9, frm="inset(0% 0% 100% 0%)"), WIPE("#maps-d", 1.35, 0.9, frm="inset(0% 0% 100% 0%)")]
for l in range(4):
    js += [BLUR(f"#maps-c{l}", 2.4 + 0.12*l), BLUR(f"#maps-s{l}", 2.45 + 0.12*l)]
for l in range(4):
    js.append(DRAW(f"#maps-arc{l}", 3.6 + 0.15*l, 0.7, 1400))
js.append(BLUR("#maps-end", 4.7, 0.2))
S.append(dict(id=sid, label="Bản đồ nhãn", dur=5.4, frags=[1.0, 2.2, 3.4, 4.5, 5.1], html=m, js="\n".join(js), title="Semantic: mỗi ảnh có thêm một bản đồ nhãn",
  notes="Bấm: thêm hai bản đồ nhãn, semantic map. Đây là file thật trong repo: 29_sem.png và 29_paint_sem.png. Mỗi màu là một vùng. Bấm: đỏ là trời, vàng là vách núi, xanh lá là rừng, xanh dương là dãy núi xa. Màu chỉ là mã nhãn, không phải màu thật. Bấm: yêu cầu là nối đúng cặp, trời với trời, vách núi với vách núi. Bấm: chốt, mỗi vùng chỉ được lấy style từ vùng cùng tên. Đầu vào giờ là bộ bốn: ảnh, map ảnh, tranh, map tranh. Ai vẽ map? Người dùng, tự vẽ hoặc dùng mô hình phân đoạn. Paper không tự sinh map, đây là một hạn chế ta sẽ nhắc lại."))

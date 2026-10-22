from lib import *
import s_base as B

S = []
LC, LS, UA = DATA["labelsC"], DATA["labelsS"], DATA["ua"]

# ---------------- error 1: wrong region, measured on the sample ----------------
sid = "err1"
CL, X1, Y1 = 36, 192, 300
wrong_mean = round(DATA["uaWrongMean"] * 100)
cliff = [i for i in range(G*G) if LC[i] == 1]
ccx = sum(cell_center(i, X1, Y1, CL)[0] for i in cliff) / len(cliff)
ccy = sum(cell_center(i, X1, Y1, CL)[1] for i in cliff) / len(cliff)
m = (title(sid, "Lỗi 1: lấy style từ sai vùng", ("sai",))
     + label("e1-l", "UA trên lưới 12 × 12 (minh hoạ)", X1, Y1 - 50, 520, 30, INK2, weight=500)
     + flat("e1-m", [rgb(u["rgb"]) for u in UA], X1, Y1, CL)
     + flat("e1-h", [f"rgba(194,24,91,{min(0.9, u['wrong']*0.95):.2f})" for u in UA], X1, Y1, CL)
     + f'<div id="e1-n" class="big" style="left:690px;top:300px;font-size:150px;color:{ACC}">{wrong_mean}%</div>'
     + label("e1-nc", "trọng số trung bình rơi sang vùng sai", 690, 470, 520, 34, INK, weight=600)
     + label("e1-n2", f'{DATA["uaWrongCells"]} / 144 điểm lấy phần lớn style từ vùng sai', 690, 600, 520, 34, INK, weight=600)
     + print_img("e1-r", IMG + "ex1_sanet.png", 1272, 288, 432)
     + svg(f'<ellipse id="e1-ell" cx="{1284+0.30*432:.0f}" cy="{300+0.60*432:.0f}" rx="105" ry="150" fill="none" stroke="{ACC}" stroke-width="6"/>'
           + leader("e1-ld", [(ccx, ccy), (ccx + 40, 790), (330, 790)], INK, 3, True))
     + label("e1-rl", "kết quả thật của SANet: vách núi cũng mang màu trời", 1272, 760, 456, 30, INK, weight=600)
     + label("e1-cl", "vách núi", 192, 772, 140, 30, INK, weight=700)
     + line("e1-end", f'Cùng một chỗ sai: phép tính đơn giản và mô hình thật đều tô vách núi bằng màu vùng khác.', 860, 40))
js = [WORDS(f"{sid}-tw", 0.1), FADE("#e1-l", 0.3),
      'tl.fromTo(".e1-m-c",{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.35,ease:"expo.out",stagger:0.006},0.4);',
      'tl.fromTo(".e1-h-c",{opacity:0},{opacity:1,duration:0.3,stagger:{each:0.004,from:"random"}},1.8);',
      T("#e1-n", 1.9, '{opacity:0,filter:"blur(8px)"}', '{opacity:1,filter:"blur(0px)"}', 0.25, "power2.out"), BLUR("#e1-nc", 2.1), BLUR("#e1-n2", 2.4),
      DRAW("#e1-ld", 2.3, 0.5, 800), FADE("#e1-ld-dot", 2.3, 0.2), BLUR("#e1-cl", 2.6),
      PLACE("#e1-r", 3.2), DRAW("#e1-ell", 3.7, 0.6, 900), BLUR("#e1-rl", 3.9), BLUR("#e1-end", 4.6, 0.2)]
S.append(dict(id=sid, label="Lỗi 1: sai vùng", dur=5.4, frags=[1.4, 3.0, 4.4, 5.0], html=m, js="\n".join(js), title="Lỗi 1: lấy style từ sai vùng",
  notes=f"Chạy UA cho cả 144 điểm của ảnh, ta được bức ghép bên trái: mỗi ô là màu trộn mà điểm đó lấy về. Bấm: phủ magenta lên những ô lấy style từ vùng khác, càng đậm càng nhiều. Trung bình {wrong_mean} phần trăm trọng số rơi sang vùng sai, và {DATA['uaWrongCells']} trên 144 điểm lấy phần lớn style từ vùng sai, dồn vào vách núi. Bấm: so với kết quả thật của SANet trong paper: đúng chỗ đó, vách núi mang màu trời. Bấm: phép tính của mình chỉ dùng màu trung bình của mảnh, nên chỉ là minh hoạ, nhưng nó chỉ ra cùng một chỗ sai với mô hình thật. Đây là lỗi 1: lấy style từ sai vùng."))

# ---------------- errors 2 and 3 ----------------
sid = "err23"
best = None
for r in range(G):
    for l in range(4):
        run = [r*G + c for c in range(G) if LC[r*G + c] == l]
        if len(run) < 8: continue
        for s0 in range(len(run) - 7):
            seg = run[s0:s0+8]
            if any(seg[i+1] - seg[i] != 1 for i in range(7)): continue
            cols = [UA[i]["rgb"] for i in seg]
            mu = [sum(c[j] for c in cols)/8 for j in range(3)]
            var = sum(sum((c[j]-mu[j])**2 for j in range(3)) for c in cols)
            if best is None or var > best[0]: best = (var, seg, l)
_, ROW, RL = best
q = B.QA
top4 = UA[q]["top"][:4]
def sky(id_, src, y):
    return (f'<div id="{id_}" class="print" style="left:192px;top:{y}px;width:732px;height:204px;padding:12px">'
            f'<div style="width:708px;height:180px;background-image:url({IMG}{src});background-size:708px 708px;background-position:0 -8px"></div></div>')
m = (title(sid, "Lỗi 2 và 3: loang lổ, nhạt nhoà")
     + label("e2-h", "Loang lổ", 192, 250, 600, 48, INK, weight=800)
     + sky("e2-a", "ex1_sanet.png", 320) + label("e2-al", 'SANet: trời lẫn vệt xanh của núi', 192, 530, 732, 30, INK, weight=600)
     + sky("e2-b", "ex1_sanet_scsa.png", 590) + label("e2-bl", "mong muốn: trời một tông (SANet + SCSA)", 192, 800, 732, 30, INK2, weight=500)
     + label("e3-h", "Nhạt nhoà", 1020, 250, 600, 48, INK, weight=800)
     + label("e3-d", "Trộn nhiều mảnh sắc nét ra một màu đục.", 1020, 315, 708, 32, INK2, weight=500))
conv = ""
for j, (k, w) in enumerate(top4):
    m += B.ptile(f"e3-k{j}", IMG + "29_paint.jpg", k, 1020 + j*130, 400, 110)
    conv += f'<path id="e3-c{j}" d="M{1075 + j*130} 516 L1305 600" stroke="{INK}" stroke-width="3" fill="none"/>'
m += svg(conv)
m += f'<div id="e3-r" style="position:absolute;left:1240px;top:610px;width:130px;height:130px;background:{rgb(UA[q]["rgb"])};box-shadow:0 0 0 6px {ACC}"></div>'
m += label("e3-rl", "trộn có trọng số → đục, mất nét cọ", 1020, 760, 708, 30, INK, "center", 600)
m += line("e23-end", f'Hai lỗi kéo {acc("ngược")} nhau: cần một tông chung, nhưng vẫn giữ nét riêng.', 880, 40)
js = [WORDS(f"{sid}-tw", 0.1), BLUR("#e2-h", 0.3), PLACE("#e2-a", 0.5), BLUR("#e2-al", 0.8), PLACE("#e2-b", 1.1), BLUR("#e2-bl", 1.4),
      BLUR("#e3-h", 2.0), FADE("#e3-d", 2.15)]
for j in range(4):
    js += [PLACE(f"#e3-k{j}", 2.3 + 0.08*j, 0.6), DRAW(f"#e3-c{j}", 3.0 + 0.06*j, 0.4, 400)]
js += [T("#e3-r", 3.4, '{opacity:0,scale:0.7}', '{opacity:1,scale:1}', 0.5, "expo.out"), BLUR("#e3-rl", 3.6), BLUR("#e23-end", 4.3, 0.2)]
S.append(dict(id=sid, label="Lỗi 2 và 3", dur=5.2, frags=[1.8, 4.1, 4.7], html=m, js="\n".join(js), title="Lỗi 2 và 3: loang lổ, nhạt nhoà",
  notes=f"Lỗi 2, loang lổ. Đây là dải trời cắt từ hai kết quả thật của paper. Trên là SANet: bầu trời lẫn vệt xanh của núi, mỗi chỗ một kiểu, vì mỗi điểm tự chọn style theo cấu trúc riêng của nó. Dưới là SANet cộng SCSA: cả vùng trời một tông, đó là điều ta muốn. Bấm: lỗi 3, nhạt nhoà. Bốn mảnh tranh mà điểm vách núi lấy nhiều nhất, sắc nét, trộn lại thành một màu đục, nét cọ mất. Bấm: hai lỗi kéo ngược nhau: lỗi 2 muốn các điểm trong vùng giống nhau hơn, lỗi 3 muốn mỗi điểm giữ nét riêng. Vì vậy SCSA cần hai cách nhìn, không phải một."))

# ---------------- three errors, three fixes ----------------
sid = "fixmap"
rows = [("Sai vùng", "Luật cấm theo nhãn", "cấm mọi điểm khác nhãn; có trong cả SCA và SSA"),
        ("Loang lổ", "SCA", "cả vùng dùng chung một tông"),
        ("Nhạt nhoà", "SSA", "chỉ lấy một điểm, giữ nguyên nét cọ")]
m = title(sid, "Ba lỗi, ba cách sửa")
paths = ""
for i, (a, b_, c) in enumerate(rows):
    y = 280 + i * 170
    m += label(f"fx-a{i}", a, 192, y, 520, 56, INK2, weight=800)
    m += label(f"fx-b{i}", b_, 900, y, 828, 56, INK, weight=800)
    m += label(f"fx-c{i}", c, 900, y + 72, 828, 32, INK2, weight=500)
    w = 40 + 31 * len(a)
    paths += f'<path id="fx-s{i}" d="M188 {y+36} L{196+w} {y+34}" stroke="{ACC}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    paths += f'<path id="fx-r{i}" d="M720 {y+36} L860 {y+36}" stroke="{INK}" stroke-width="4" fill="none"/><path id="fx-h{i}" d="M848 {y+24} L868 {y+36} L848 {y+48}Z" fill="{INK}"/>'
m += svg(paths)
m += line("fx-end", f'Một gốc chung: attention {acc("không")} biết nhãn vùng. SCSA thêm đúng mảnh đó.', 830, 44)
js = [WORDS(f"{sid}-tw", 0.1)]
for i in range(3):
    t = 0.4 + i * 1.0
    js += [BLUR(f"#fx-a{i}", t), DRAW(f"#fx-s{i}", t + 0.3, 0.35, 500), DRAW(f"#fx-r{i}", t + 0.45, 0.3, 200), FADE(f"#fx-h{i}", t + 0.7, 0.1), BLUR(f"#fx-b{i}", t + 0.6), FADE(f"#fx-c{i}", t + 0.75)]
js.append(BLUR("#fx-end", 3.6, 0.2))
S.append(dict(id=sid, label="Ba lỗi, ba cách sửa", dur=4.4, frags=[1.3, 2.3, 3.3, 4.0], html=m, js="\n".join(js), title="Ba lỗi, ba cách sửa",
  notes="Bản đồ nối sang phần SCSA. Bấm từng hàng. Sai vùng, sửa bằng luật cấm theo nhãn; luật này nằm sẵn trong cả SCA và SSA nên lỗi 1 được sửa miễn phí. Loang lổ, sửa bằng SCA: cả vùng dùng chung một tông. Nhạt nhoà, sửa bằng SSA: chỉ lấy một điểm, giữ nguyên nét. Bấm: cả ba lỗi chung một gốc, attention không biết nhãn vùng. Mọi slide sau chỉ phóng to cột phải."))

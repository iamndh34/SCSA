from lib import *
import s_base as B

S = []
LC, LS, UA, SSA, SCA = DATA["labelsC"], DATA["labelsS"], DATA["ua"], DATA["ssa"], DATA["sca"]
QA = B.QA

def hatch_cells(id_, x0, y0, cl, keep_label, pid):
    out = ""
    for k in range(G*G):
        if LS[k] == keep_label: continue
        r, c = divmod(k, G)
        out += f'<rect x="{x0 + c*cl}" y="{y0 + r*cl}" width="{cl}" height="{cl}" fill="url(#{pid})"/>'
    return f'<g id="{id_}">{out}</g>'

# ---------------- big idea ----------------
sid = "idea"
CL, GX, GY = 40, 1240, 370
pick = SSA[QA]
qx, qy = 1060 + 40, 580 + 40
fan = ""
for k in range(G*G):
    if LS[k] != 1: continue
    kx, ky = cell_center(k, GX, GY, CL)
    fan += f'<line class="idea-fl" x1="{qx+40}" y1="{qy}" x2="{kx}" y2="{ky}" stroke="{INK}" stroke-width="2.5" stroke-opacity="0.55"/>'
px_, py_ = cell_center(pick, GX, GY, CL)
m = (f'<h1 id="idea-big" class="t" style="top:200px;font-size:84px;width:1536px">{words("Chỉ nhìn trong vùng cùng nhãn.", "idea-w", ("cùng", "nhãn."))}</h1>'
     + tiles("idea-g", IMG + "29_paint.jpg", GX, GY, CL)
     + svg(hatch_def("ideah") + hatch_cells("idea-ban", GX, GY, CL, 1, "ideah") + f'<g id="idea-fan">{fan}</g>'
           + f'<line id="idea-beam" x1="{qx+40}" y1="{qy}" x2="{px_}" y2="{py_}" stroke="{ACC}" stroke-width="8" stroke-linecap="round"/>'
           + f'<rect id="idea-pick" x="{px_-CL/2-4}" y="{py_-CL/2-4}" width="{CL+8}" height="{CL+8}" fill="none" stroke="{ACC}" stroke-width="6"/>')
     + B.ptile("idea-q", IMG + "29.jpg", QA, 1060, 580, 80, f"box-shadow:0 0 0 6px {ACC}")
     + label("idea-ql", "1 điểm vách núi", 1000, 680, 200, 28, INK2, "center", 500)
     + label("idea-gl", "tranh", GX, GY - 48, 480, 30, INK2, weight=500)
     + label("idea-a", "SCA · nhìn cả vùng", 192, 420, 780, 48, INK, weight=800)
     + label("idea-a2", "lấy tông chung của mọi điểm cùng nhãn", 192, 482, 780, 32, INK2, weight=500)
     + label("idea-b", "SSA · nhìn một điểm", 192, 590, 780, 48, INK, weight=800)
     + label("idea-b2", "lấy nét cọ của đúng một điểm giống nhất", 192, 652, 780, 32, INK2, weight=500)
     + line("idea-name", "<b>S</b>emantic · <b>C</b>ontinuous · <b>S</b>parse · <b>A</b>ttention", 880, 44, weight=500, color=INK2))
js = [WORDS("idea-w", 0.2, 0.09), 'tl.fromTo(".idea-g-c",{opacity:0},{opacity:1,duration:0.3,stagger:0.004},0.4);', FADE("#idea-gl", 0.6),
      T("#idea-q", 0.7, '{opacity:0,scale:0.7}', '{opacity:1,scale:1}', 0.6, "expo.out"), FADE("#idea-ql", 0.8),
      HIDE("#idea-ban"), HIDE("#idea-fan"), HIDE("#idea-beam"), HIDE("#idea-pick"),
      FADE("#idea-ban", 1.4, 0.4), FADE("#idea-fan", 1.6, 0.01), DRAW(".idea-fl", 1.6, 0.6, 900), BLUR("#idea-a", 1.7), FADE("#idea-a2", 1.85),
      FADE("#idea-fan", 2.8, 0.4, 1, 0.12), FADE("#idea-beam", 2.9, 0.01), DRAW("#idea-beam", 2.9, 0.5, 900),
      T("#idea-pick", 3.3, '{opacity:0,scale:1.8,transformOrigin:"50% 50%"}', '{opacity:1,scale:1}', 0.4, "expo.out"), BLUR("#idea-b", 3.0), FADE("#idea-b2", 3.15),
      INK_IN("idea-nw", 4.0) if False else BLUR("#idea-name", 4.0, 0.2)]
S.append(dict(id=sid, label="Ý tưởng cốt lõi", dur=4.8, frags=[1.2, 2.6, 3.8, 4.5], html=m, js="\n".join(js), title="Chỉ nhìn trong vùng cùng nhãn",
  notes="Câu cần nhớ nhất của paper: chỉ nhìn trong vùng cùng nhãn. Bấm: cách nhìn thứ nhất, SCA. Điểm vách núi của ảnh nhìn tất cả điểm vách núi của tranh, các vùng khác bị gạch chéo, tức là bị cấm. Kết quả là tông chung của cả vùng. Bấm: cách nhìn thứ hai, SSA. Chỉ một đường nối, tới đúng một mảnh vách núi giống nhất, lấy nguyên nét cọ của mảnh đó. Bấm: giải nghĩa cái tên. S là Semantic, dùng nhãn vùng. C là Continuous, nhìn liên tục cả vùng, tức SCA. S là Sparse, thưa, chỉ một điểm, tức SSA. A là Attention."))

# ---------------- pipeline ----------------
sid = "pipe"
def box(id_, x, y, w, h, t1, t2="", dark=False, accent=False, fs=38):
    bg = INK if dark else "#FFFFFF"
    bd = ACC if accent else INK
    c1 = "#FFFFFF" if dark else INK
    c2 = "#C9CDD3" if dark else INK2
    s2 = f'<div style="font-size:30px;font-weight:500;color:{c2};line-height:1.2;margin-top:4px">{t2}</div>' if t2 else ""
    return (f'<div id="{id_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{bg};border:4px solid {bd};'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:8px 12px">'
            f'<div style="font-size:{fs}px;font-weight:800;color:{c1}">{t1}</div>{s2}</div>')
ins = ["29.jpg", "29_sem.png", "29_paint.jpg", "29_paint_sem.png"]
m = title(sid, "Toàn cảnh: SCSA nằm ở giữa", ("giữa",))
m += '<div id="pp-in">' + "".join(print_img(f"pp-i{j}", IMG + f, 192, 290 + j*104, 80, mat=8) for j, f in enumerate(ins)) + '</div>'
m += box("pp-enc", 330, 290, 150, 406, "Encoder", fs=28)
m += box("pp-sca", 530, 290, 400, 160, "SCA", "tông chung cả vùng", dark=True)
m += box("pp-sad", 530, 536, 190, 160, "S-AdaIN", "", fs=30)
m += box("pp-ssa", 740, 536, 190, 160, "SSA", "1 điểm", dark=True)
m += box("pp-mix", 990, 420, 250, 180, "Trộn", "tông + nét + bố cục", accent=True)
m += box("pp-dec", 1290, 430, 170, 160, "Decoder", fs=30)
m += print_img("pp-out", IMG + "ex1_sanet_scsa.png", 1500, 390, 220)
P = {"in": "M296 338 L330 338 M296 442 L330 442 M296 546 L330 546 M296 650 L330 650", "e1": "M480 370 L530 370", "e2": "M480 616 L530 616",
     "e3": "M720 616 L740 616", "m1": "M930 370 L960 370 L960 470 L990 470", "m2": "M930 616 L960 616 L960 550 L990 550",
     "res": "M405 696 L405 750 L1115 750 L1115 600", "d1": "M1240 510 L1290 510", "d2": "M1460 510 L1500 510"}
pp = ""
for k, d in P.items():
    pp += f'<path id="pp-p{k}" d="{d}" stroke="{ACC if k == "res" else INK}" stroke-width="4" fill="none"/>'
DOTS = [("e1", 480, 370, 530, 370), ("e3", 720, 616, 740, 616), ("d1", 1240, 510, 1290, 510), ("d2", 1460, 510, 1500, 510)]
for k, x1, y1, x2, y2 in DOTS:
    pp += f'<circle id="pp-dot{k}" cx="{x1}" cy="{y1}" r="9" fill="{ACC}"/>'
m += svg(pp)
m += label("pp-rl", "bố cục của ảnh được cộng vào", 650, 760, 460, 30, ACC, weight=600)
m += line("pp-end", f'Encoder, decoder giữ nguyên. Chỉ ba khối ở giữa là {acc("SCSA")}.', 860, 44)
js = [WORDS(f"{sid}-tw", 0.1), 'tl.fromTo("#pp-in .print",{opacity:0,y:20},{opacity:1,y:0,duration:0.6,ease:"expo.out",stagger:0.08},0.3);',
      DRAW("#pp-pin", 0.7, 0.3, 300), BLUR("#pp-enc", 0.8, 0.2),
      DRAW("#pp-pe1", 1.4, 0.3, 100), PLACE("#pp-sca", 1.5, 0.6),
      DRAW("#pp-pe2", 2.3, 0.3, 100), PLACE("#pp-sad", 2.4, 0.6), DRAW("#pp-pe3", 2.7, 0.2, 100), PLACE("#pp-ssa", 2.8, 0.6),
      DRAW("#pp-pm1", 3.4, 0.4, 300), DRAW("#pp-pm2", 3.4, 0.4, 300), PLACE("#pp-mix", 3.6, 0.6), DRAW("#pp-pres", 3.7, 0.6, 1000), 'tl.set("#pp-pres",{strokeDasharray:"12 9",strokeDashoffset:0},4.3);', BLUR("#pp-rl", 4.0),
      DRAW("#pp-pd1", 4.5, 0.2, 100), PLACE("#pp-dec", 4.6, 0.6), DRAW("#pp-pd2", 4.8, 0.2, 100), PLACE("#pp-out", 4.9, 0.7),
      BLUR("#pp-end", 5.6, 0.2)]
for k, x1, y1, x2, y2 in DOTS:
    t_on = {"e1": 1.5, "e3": 2.8, "d1": 4.6, "d2": 4.9}[k]
    js += [HIDE(f"#pp-dot{k}"), f'tl.fromTo("#pp-dot{k}",{{attr:{{cx:{x1}}},opacity:1}},{{attr:{{cx:{x2}}},duration:0.6,ease:"none",repeat:2}},{t_on});', f'tl.set("#pp-dot{k}",{{opacity:0}},{t_on + 1.8});']
S.append(dict(id=sid, label="Sơ đồ toàn cảnh", dur=6.4, frags=[1.2, 2.0, 3.2, 4.4, 5.4, 6.0], html=m, js="\n".join(js), title="Toàn cảnh: SCSA nằm ở giữa",
  notes="Bấm từng bước, từ trái sang phải. Bốn đầu vào: ảnh, map ảnh, tranh, map tranh. Encoder biến cả bốn thành lưới điểm, kể cả hai map. Bấm: nhánh trên, SCA: hỏi bằng map, lấy tông chung của cả vùng. Bấm: nhánh dưới hai bước: S-AdaIN đổi tông ảnh theo từng vùng để làm sạch câu hỏi, rồi SSA tìm một điểm giống nhất trong cùng vùng. Bấm: trộn tông chung, nét cọ, và cộng bố cục của ảnh vào, đường đứt nét magenta. Bấm: decoder vẽ ra ảnh. Bấm: encoder, decoder giữ nguyên, chỉ ba khối giữa là SCSA. Với StyleID, encoder là VAE cộng DDIM inversion."))

# ---------------- SCA ----------------
sid = "sca"
CL, XA, XB, XR, Y = 36, 192, 744, 1296, 330
cl_cells = [k for k in range(G*G) if LS[k] == 1]
src_cells = [i for i in range(G*G) if LC[i] == 1]
sx = XA + G*CL + 8
sy = sum(cell_center(i, XA, Y, CL)[1] for i in src_cells) / len(src_cells)
fan = "".join(f'<line class="sca-fl" x1="{sx}" y1="{sy:.0f}" x2="{cell_center(k, XB, Y, CL)[0]:.0f}" y2="{cell_center(k, XB, Y, CL)[1]:.0f}" stroke="{INK}" stroke-width="2" stroke-opacity="0.5"/>' for k in cl_cells)
m = (title(sid, "SCA: hỏi bằng bản đồ nhãn, lấy tông cả vùng", ("bản", "đồ", "nhãn,"))
     + label("sca-l1", "câu hỏi: ảnh → bản đồ nhãn", XA, Y - 52, 432, 30, INK2, weight=500)
     + label("sca-l2", "tranh: chỉ vùng cùng nhãn", XB, Y - 52, 432, 30, INK2, weight=500)
     + label("sca-l3", "kết quả SCA", XR, Y - 52, 432, 30, INK2, weight=500)
     + tiles("sca-a", IMG + "29.jpg", XA, Y, CL) + flat("sca-am", [REG[l] for l in LC], XA, Y, CL)
     + tiles("sca-b", IMG + "29_paint.jpg", XB, Y, CL)
     + svg(hatch_def("scah") + hatch_cells("sca-ban", XB, Y, CL, 1, "scah") + f'<g id="sca-fan">{fan}</g>'
           + f'<rect id="sca-ring" x="{XA-4}" y="{Y-4}" width="{G*CL+8}" height="{G*CL+8}" fill="none" stroke="{ACC}" stroke-width="0"/>')
     + flat("sca-r1", [rgb(SCA[i]) if LC[i] == 1 else None for i in range(G*G)], XR, Y, CL)
     + flat("sca-r2", [rgb(SCA[i]) if LC[i] != 1 else None for i in range(G*G)], XR, Y, CL)
     + label("sca-n1", "vách núi: cùng một câu hỏi", XA, Y + G*CL + 20, 520, 32, INK, weight=600)
     + label("sca-n2", f'vùng khác {acc("cấm")}, vách núi chia đều', XB, Y + G*CL + 20, 520, 32, INK, weight=600)
     + label("sca-n3", "mỗi vùng một tông", XR, Y + G*CL + 20, 432, 32, INK, weight=600)
     + line("sca-end", f'Liền mạch, đúng vùng. Cái giá: {acc("phẳng")}, mất nét cọ.', 880, 44))
js = [WORDS(f"{sid}-tw", 0.1), FADE("#sca-l1", 0.3), FADE("#sca-l2", 0.35), FADE("#sca-l3", 0.4),
      'tl.fromTo(".sca-a-c",{opacity:0},{opacity:1,duration:0.3,stagger:0.003},0.3);', 'tl.fromTo(".sca-b-c",{opacity:0},{opacity:1,duration:0.3,stagger:0.003},0.5);',
      'tl.fromTo(".sca-am-c",{opacity:0},{opacity:1,duration:0.4,stagger:{each:0.005,from:"start"}},1.3);', BLUR("#sca-n1", 1.9),
      HIDE("#sca-ban"), HIDE("#sca-fan"), FADE("#sca-ban", 2.6, 0.4), FADE("#sca-fan", 2.8, 0.01), DRAW(".sca-fl", 2.8, 0.6, 900), BLUR("#sca-n2", 3.0),
      'tl.fromTo(".sca-r1-c",{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.35,ease:"expo.out",stagger:0.02},3.9);',
      'tl.fromTo(".sca-r2-c",{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.35,ease:"expo.out",stagger:0.004},4.4);', BLUR("#sca-n3", 4.9),
      BLUR("#sca-end", 5.6, 0.2)]
S.append(dict(id=sid, label="SCA", dur=6.4, frags=[1.2, 2.4, 3.7, 5.3, 6.0], html=m, js="\n".join(js), title="SCA: hỏi bằng bản đồ nhãn",
  notes="SCA khác UA ở hai chỗ. Bấm: chỗ một, câu hỏi không lấy từ ảnh mà từ bản đồ nhãn. Map là mảng màu phẳng, nên mọi điểm vách núi hỏi cùng một câu. Bấm: chỗ hai, luật G1: khác nhãn thì cấm. Vì mọi điểm vách núi hỏi giống nhau, trọng số chia đều cho mọi điểm vách núi trong tranh. Nội dung lấy về vẫn từ tranh. Bấm: mỗi điểm vách núi nhận cùng một màu: trung bình của vách núi trong tranh, màu xanh. Làm tương tự cho các vùng khác, ta được bức ghép bên phải, tính thật trên ảnh mẫu. Bấm: liền mạch, đúng vùng, hết loang lổ. Cái giá: phẳng, mất nét cọ. Hỏi nhanh: nếu giữ luật cấm mà hỏi bằng ảnh thì sửa được lỗi nào? Chỉ lỗi sai vùng, loang lổ vẫn còn."))

# ---------------- S-AdaIN ----------------
sid = "sadain"
m = (title(sid, "S-AdaIN: đổi tông riêng từng vùng", ("riêng",))
     + print_img("sd-a", IMG + "29.jpg", 192, 270, 408) + print_img("sd-b", IMG + "29_adain.png", 756, 270, 408) + print_img("sd-c", IMG + "29_sadain.png", 1320, 270, 408)
     + label("sd-la", "ảnh gốc", 192, 712, 432, 30, INK, "center", 700)
     + label("sd-lb", "AdaIN cả ảnh: 1 tông", 756, 712, 432, 30, INK, "center", 700)
     + label("sd-lc", f'S-AdaIN: {acc("mỗi")} vùng 1 tông', 1320, 712, 432, 30, INK, "center", 700)
     + label("sd-nc", "vách núi xanh, dãy xa hồng: như trong tranh", 1320, 762, 432, 30, INK2, "center", 500)
     + line("sd-end", "Để làm gì? Để SSA so “giống” trên cùng một thang màu với tranh.", 880, 44))
js = [WORDS(f"{sid}-tw", 0.1), PLACE("#sd-a", 0.3), BLUR("#sd-la", 0.6),
      PLACE("#sd-b", 1.2), WIPE("#sd-b", 1.3, 0.9), BLUR("#sd-lb", 1.9),
      PLACE("#sd-c", 2.4), WIPE("#sd-c", 2.5, 1.1, frm="inset(0% 0% 100% 0%)"), BLUR("#sd-lc", 3.2), FADE("#sd-nc", 3.4),
      BLUR("#sd-end", 4.1, 0.2)]
S.append(dict(id=sid, label="S-AdaIN", dur=4.8, frags=[0.9, 2.2, 3.8, 4.4], html=m, js="\n".join(js), title="S-AdaIN: đổi tông riêng từng vùng",
  notes="Nhớ AdaIN ở chặng 2: hai con số, màu trung bình và độ tương phản. Bấm: AdaIN cả ảnh dùng một cặp số cho mọi vùng, nên cả ảnh ngả một tông. Bấm: S-AdaIN tính riêng cho từng vùng nhãn. Vách núi nhận tông của vách núi trong tranh, thành xanh; dãy xa nhận tông hồng của dãy xa trong tranh. Ba ảnh này là phép tính thật trên pixel của ảnh mẫu, dùng đúng hai bản đồ nhãn. Bấm: mục đích là làm sạch câu hỏi cho SSA. Ảnh chụp có vách núi xám, tranh có vách núi xanh; nếu so ngay thì “giống” bị lệch. Kéo về cùng thang màu trước rồi mới so. Trong mô hình, phép này làm trên lưới điểm, không phải trên pixel."))

# ---------------- SSA ----------------
sid = "ssa"
CL, XA, XB, XR, Y = 36, 192, 744, 1296, 330
pick = SSA[QA]
rank = sorted((k for k in range(G*G) if LS[k] == 1 and k != pick), key=lambda k: d2(DATA["rgbSad"][QA], DATA["rgbS"][k]))[:4]
qx, qy = cell_center(QA, XA, Y, CL)
pkx, pky = cell_center(pick, XB, Y, CL)
rx_, ry_ = cell_center(QA, XR, Y, CL)
def ssa_tile(i):
    k = SSA[i]; r, c = divmod(k, G)
    return f';background-image:url({IMG}29_paint.jpg);background-size:{G*CL}px {G*CL}px;background-position:-{c*CL}px -{r*CL}px'
m = (title(sid, "SSA: chỉ giữ một mảnh giống nhất", ("một",))
     + label("ssa-l1", "câu hỏi: ảnh đã qua S-AdaIN", XA, Y - 52, 432, 30, INK2, weight=500)
     + label("ssa-l2", "tranh", XB, Y - 52, 432, 30, INK2, weight=500)
     + label("ssa-l3", "kết quả SSA", XR, Y - 52, 432, 30, INK2, weight=500)
     + tiles("ssa-a", IMG + "29_sadain.png", XA, Y, CL) + tiles("ssa-b", IMG + "29_paint.jpg", XB, Y, CL)
     + "".join(f'<div class="ssa-r-c tile" style="left:{XR + (i % G)*CL}px;top:{Y + (i // G)*CL}px;width:{CL}px;height:{CL}px{ssa_tile(i)}"></div>' for i in range(G*G) if i != QA)
     + f'<div id="ssa-fly" class="tile" style="left:{pkx-CL/2}px;top:{pky-CL/2}px;width:{CL}px;height:{CL}px{ssa_tile(QA)};box-shadow:0 0 0 5px {ACC}"></div>'
     + svg(hatch_def("ssah") + hatch_cells("ssa-ban", XB, Y, CL, 1, "ssah")
           + f'<rect id="ssa-q" x="{qx-CL/2-3}" y="{qy-CL/2-3}" width="{CL+6}" height="{CL+6}" fill="none" stroke="{ACC}" stroke-width="6"/>'
           + "".join(f'<rect class="ssa-cand" x="{cell_center(k, XB, Y, CL)[0]-CL/2-2}" y="{cell_center(k, XB, Y, CL)[1]-CL/2-2}" width="{CL+4}" height="{CL+4}" fill="none" stroke="{INK}" stroke-width="4"/>' for k in rank)
           + f'<rect id="ssa-pk" x="{pkx-CL/2-4}" y="{pky-CL/2-4}" width="{CL+8}" height="{CL+8}" fill="none" stroke="{ACC}" stroke-width="7"/>'
           + f'<line id="ssa-ln" x1="{qx+CL/2}" y1="{qy}" x2="{pkx-CL/2}" y2="{pky}" stroke="{ACC}" stroke-width="6" stroke-linecap="round"/>')
     + label("ssa-n1", "một điểm vách núi hỏi", XA, Y + G*CL + 20, 432, 32, INK, weight=600)
     + label("ssa-n2", f'vùng khác {acc("cấm")}, giữ 1 mảnh', XB, Y + G*CL + 20, 520, 32, INK, weight=600)
     + label("ssa-n3", "mỗi ô là một mảnh tranh thật", XR, Y + G*CL + 20, 432, 32, INK, weight=600)
     + line("ssa-end", f'Copy {acc("nguyên")} một mảnh tranh: giữ nét cọ, hết nhạt nhoà.', 880, 44))
js = [WORDS(f"{sid}-tw", 0.1), FADE("#ssa-l1", 0.3), FADE("#ssa-l2", 0.35), FADE("#ssa-l3", 0.4),
      'tl.fromTo(".ssa-a-c",{opacity:0},{opacity:1,duration:0.3,stagger:0.003},0.3);', 'tl.fromTo(".ssa-b-c",{opacity:0},{opacity:1,duration:0.3,stagger:0.003},0.5);',
      HIDE("#ssa-q"), HIDE("#ssa-ban"), HIDE(".ssa-cand"), HIDE("#ssa-pk"), HIDE("#ssa-ln"), HIDE("#ssa-fly"), HIDE(".ssa-r-c"),
      T("#ssa-q", 1.0, '{opacity:0,scale:2,transformOrigin:"50% 50%"}', '{opacity:1,scale:1}', 0.5, "expo.out"), BLUR("#ssa-n1", 1.2),
      FADE("#ssa-ban", 2.0, 0.4),
      'tl.fromTo(".ssa-cand",{opacity:0},{opacity:1,duration:0.2,stagger:0.12},2.5);',
      T("#ssa-pk", 3.1, '{opacity:0,scale:1.8,transformOrigin:"50% 50%"}', '{opacity:1,scale:1}', 0.4, "expo.out"), FADE("#ssa-ln", 3.2, 0.01), DRAW("#ssa-ln", 3.2, 0.4, 700), BLUR("#ssa-n2", 3.3),
      FADE("#ssa-fly", 4.0, 0.01), MOVE("#ssa-fly", 4.0, 0, 0, rx_ - pkx, ry_ - pky, 0.9),
      'tl.fromTo(".ssa-r-c",{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.3,ease:"expo.out",stagger:0.005},4.9);', BLUR("#ssa-n3", 5.3),
      BLUR("#ssa-end", 5.9, 0.2)]
S.append(dict(id=sid, label="SSA", dur=6.6, frags=[1.6, 2.4, 3.8, 5.6, 6.3], html=m, js="\n".join(js), title="SSA: chỉ giữ một mảnh giống nhất",
  notes="SSA hỏi bằng ảnh đã qua S-AdaIN, nên so “giống” theo cấu trúc thật của ảnh. Bấm: một điểm vách núi hỏi. Bấm: luật G2, bước một: khác nhãn thì cấm, chỉ còn vùng vách núi của tranh. Bấm: bước hai: trong vùng vách núi, chỉ giữ đúng một mảnh giống nhất, khung magenta; bốn khung đen là các ứng viên tiếp theo, bị bỏ. Chỉ còn một điểm thì trọng số của nó là 100 phần trăm, tức là copy nguyên mảnh đó. Bấm: mảnh bay sang đúng vị trí trong kết quả. Làm cho cả 144 điểm, ta được bức ghép bên phải: mỗi ô là một mảnh tranh thật, giữ nguyên nét cọ. Bấm: hết nhạt nhoà. Ý tưởng giống Style-Swap năm 2016, nhưng khoá trong vùng ngữ nghĩa và không cần train."))

# ---------------- three matrices ----------------
sid = "matrices"
def matrix(prefix, x0, y0, kind):
    C = 52; s = ""
    s += f'<rect x="{x0}" y="{y0-20}" width="{3*C}" height="10" fill="{REG[0]}"/><rect x="{x0+3*C}" y="{y0-20}" width="{3*C}" height="10" fill="{REG[1]}"/>'
    s += f'<rect x="{x0-20}" y="{y0}" width="10" height="{3*C}" fill="{REG[0]}"/><rect x="{x0-20}" y="{y0+3*C}" width="10" height="{3*C}" fill="{REG[1]}"/>'
    ua = [[.30,.12,.08,.36,.08,.06],[.10,.28,.14,.08,.30,.10],[.08,.12,.34,.06,.10,.30],[.32,.06,.08,.30,.14,.10],[.06,.30,.10,.12,.30,.12],[.10,.06,.32,.08,.12,.32]]
    pick = [0, 1, 2, 0, 1, 2]
    for r in range(6):
        for c in range(6):
            same = (r < 3) == (c < 3); x, y = x0 + c*C, y0 + r*C
            if kind == "ua":
                v = ua[r][c]; col = INK if same else ACC
                s += f'<rect class="{prefix}" x="{x+3}" y="{y+3}" width="{C-6}" height="{C-6}" fill="{col}" fill-opacity="{min(1, 0.12 + 2.3*v):.2f}"/>'
            elif not same:
                s += f'<rect class="{prefix}" x="{x+3}" y="{y+3}" width="{C-6}" height="{C-6}" fill="url(#mxh)"/>'
            elif kind == "sca":
                s += f'<rect class="{prefix}" x="{x+3}" y="{y+3}" width="{C-6}" height="{C-6}" fill="{INK}" fill-opacity="0.5"/>'
            else:
                hit = (c % 3) == pick[r]
                s += f'<rect class="{prefix}" x="{x+3}" y="{y+3}" width="{C-6}" height="{C-6}" fill="{INK}" fill-opacity="{0.95 if hit else 0.06}"/>'
    return s
MX = [300, 804, 1308]; MY = 320
caps = [("Universal Attention", "dày đặc; ô magenta tràn sang vùng khác"), ("SCA · luật G1", "đều nhau trong khối đúng; khối gạch bị cấm"), ("SSA · luật G2", "mỗi hàng đúng một ô, luôn trong khối đúng")]
m = title(sid, "Ba ma trận attention, nhìn là thấy khác")
m += label("mx-ax", "hàng: điểm của ảnh (3 trời, 3 vách núi) · cột: điểm của tranh · ô đậm: trọng số lớn", 192, 230, 1536, 30, INK2, weight=500)
m += svg(hatch_def("mxh") + "".join(f'<g id="mx-g{i}">{matrix(f"mx-c{i}", MX[i], MY, k)}</g>' for i, k in enumerate(["ua", "sca", "ssa"])))
for i, (h, d) in enumerate(caps):
    m += label(f"mx-t{i}", h, MX[i] - 60, MY + 330, 432, 38, INK, "center", 800)
    m += label(f"mx-d{i}", d, MX[i] - 60, MY + 384, 432, 30, INK2, "center", 500)
m += line("mx-end", "Nếu chỉ nhớ một hình của cả buổi, hãy nhớ hình này.", 880, 44)
js = [WORDS(f"{sid}-tw", 0.1), FADE("#mx-ax", 0.3)]
for i in range(3):
    t = 0.5 + i * 1.2
    js += [f'tl.fromTo(".mx-c{i}",{{opacity:0,scale:0.4,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.4)",stagger:0.015}},{t});', BLUR(f"#mx-t{i}", t + 0.5), FADE(f"#mx-d{i}", t + 0.6)]
js.append(BLUR("#mx-end", 4.1, 0.2))
S.append(dict(id=sid, label="Ba ma trận", dur=4.8, frags=[1.4, 2.6, 3.8, 4.5], html=m, js="\n".join(js), title="Ba ma trận attention, nhìn là thấy khác",
  notes="Mỗi ma trận: hàng là điểm của ảnh, ba trời ba vách núi; cột là điểm của tranh. Ô càng đậm, trọng số càng lớn. Trái, UA: dày đặc, mỗi hàng trải khắp nơi, ô magenta là trọng số tràn sang vùng khác; lỗi 1 nằm ở đó. Bấm: giữa, SCA: luật G1 gạch bỏ hai khối chéo, phần còn lại đều nhau vì hỏi bằng map phẳng; hết loang lổ. Bấm: phải, SSA: mỗi hàng giữ đúng một ô, luôn trong khối đúng; hai hàng có thể chọn cùng một ô. Hết nhạt nhoà. Bấm: chốt, nếu chỉ nhớ một hình của cả buổi thì nhớ hình này. Giá trị trong hình là minh hoạ."))

# ---------------- mix with slider ----------------
sid = "mix"
CL, XM, YM = 40, 192, 360
def ssa40(i):
    k = SSA[i]; r, c = divmod(k, G)
    return f';background-image:url({IMG}29_paint.jpg);background-size:{G*CL}px {G*CL}px;background-position:-{c*CL}px -{r*CL}px'
TX0, TW = 300, 300
m = (title(sid, "Trộn hai nhánh: một nút chỉnh tông và nét", ("nút",))
     + label("mx2-l", "SSA", 192, 278, 90, 32, INK, weight=800) + label("mx2-r", "SCA", TX0 + TW + 28, 278, 100, 32, INK, weight=800)
     + f'<div id="mx2-tr" style="position:absolute;left:{TX0}px;top:296px;width:{TW}px;height:8px;background:{INK}"></div>'
     + f'<div id="mx2-k" style="position:absolute;left:{TX0-20}px;top:280px;width:40px;height:40px;border-radius:50%;background:{ACC};box-shadow:0 0 0 5px #fff"></div>'
     + "".join(f'<div class="mx2-p tile" style="left:{XM + (i % G)*CL}px;top:{YM + (i // G)*CL}px;width:{CL}px;height:{CL}px{ssa40(i)}"></div>' for i in range(G*G))
     + f'<div id="mx2-sca">' + flat("mx2-s", [rgb(SCA[i]) for i in range(G*G)], XM, YM, CL) + '</div>'
     + line("mx2-t0", "Chỉ SSA: sắc nét, nhưng màu nhảy giữa các ô.", 380, 40, left=760, width=480, weight=600)
     + line("mx2-t1", "Chỉ SCA: đều màu, nhưng phẳng.", 380, 40, left=760, width=480, weight=600)
     + line("mx2-t2", f'SANet dùng {acc("0,7")} tông chung + 0,3 nét cọ.', 380, 40, left=760, width=480, weight=600)
     + print_img("mx2-real", IMG + "ex1_sanet_scsa.png", 1300, 348, 404)
     + label("mx2-rl", "kết quả thật của SANet + SCSA", 1300, 790, 428, 30, INK2, "center", 500)
     + line("mx2-end", "Kết quả = tông chung + nét cọ + bố cục của ảnh.", 880, 44))
js = [WORDS(f"{sid}-tw", 0.1), FADE("#mx2-l", 0.3), FADE("#mx2-r", 0.3), GROW_X("#mx2-tr", 0.3, 0.5), FADE("#mx2-k", 0.5, 0.2),
      'tl.fromTo(".mx2-p",{opacity:0},{opacity:1,duration:0.3,stagger:0.003},0.4);', HIDE("#mx2-sca"), HIDE("#mx2-t1"), HIDE("#mx2-t2"),
      BLUR("#mx2-t0", 0.9),
      MOVE("#mx2-k", 1.6, 0, 0, TW, 0, 1.2, "power2.inOut"), FADE("#mx2-sca", 1.6, 1.2, 0, 1, "power2.inOut"), FADE("#mx2-t0", 1.6, 0.2, 1, 0), BLUR("#mx2-t1", 2.6),
      MOVE("#mx2-k", 3.4, TW, 0, TW*0.7, 0, 0.8, "power2.inOut"), FADE("#mx2-sca", 3.4, 0.8, 1, 0.7, "power2.inOut"), FADE("#mx2-t1", 3.4, 0.2, 1, 0), BLUR("#mx2-t2", 4.0),
      PLACE("#mx2-real", 4.8), FADE("#mx2-rl", 5.1), BLUR("#mx2-end", 5.6, 0.2)]
S.append(dict(id=sid, label="Trộn hai nhánh", dur=6.4, frags=[1.2, 3.0, 4.4, 5.4, 6.0], html=m, js="\n".join(js), title="Trộn hai nhánh: một nút chỉnh tông và nét",
  notes="Kết quả cuối là tông chung từ SCA cộng nét cọ từ SSA, cộng bố cục của ảnh. Hai hệ số là nút chỉnh. Bấm đầu: nút ở SSA thuần, bức ghép toàn mảnh tranh thật, sắc nét nhưng màu nhảy giữa các ô. Bấm: kéo hết sang SCA thuần, đều màu nhưng phẳng. Bấm: SANet dùng 0,7 tông chung và 0,3 nét cọ. Bức ghép này tính trên lưới 12 nhân 12 nên còn thô. Bấm: bên phải là kết quả thật của SANet cộng SCSA trên cùng cặp ảnh, ở độ phân giải đầy đủ. Các backbone khác dùng hệ số khác: StyTr2 1,2 và 0,5, StyleID 0,8 và 0,2."))

# ---------------- plug into three backbones ----------------
sid = "plug"
BB = [("SANet", "CNN", "0,7 / 0,3"), ("StyTr2", "Transformer", "1,2 / 0,5"), ("StyleID", "Diffusion", "0,8 / 0,2")]
m = title(sid, "Cắm vào ba họ mô hình, không train lại", ("không",))
for j, (n, f, a) in enumerate(BB):
    m += f'<div id="pl-n{j}" class="lb" style="left:192px;top:270px;width:900px;font-size:64px;font-weight:800">{n} <span style="color:{INK2};font-weight:500;font-size:44px">· {f}</span></div>'
    m += label(f"pl-a{j}", f"tỉ lệ trộn tông / nét: {a}", 192, 360, 900, 34, INK2, weight=500)
m += box("pl-enc", 300, 500, 240, 150, "Encoder")
m += f'<div id="pl-slot" style="position:absolute;left:660px;top:470px;width:340px;height:210px;border:4px dashed {INK2}"></div>'
m += f'<div id="pl-old" style="position:absolute;left:680px;top:490px;width:300px;height:170px;background:#C9CDD3;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:700">attention gốc</div>'
m += f'<div id="pl-new" style="position:absolute;left:680px;top:490px;width:300px;height:170px;background:{INK};color:#fff;display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:800">SCSA</div>'
m += box("pl-dec", 1120, 500, 240, 150, "Decoder")
m += svg(leader("pl-w1", [(540, 575), (656, 575)], INK, 4, False) + leader("pl-w2", [(1004, 575), (1116, 575)], INK, 4, False))
m += line("pl-end", f'Chỉ thay khối attention. Trọng số gốc giữ nguyên: {acc("không")} train lại.', 860, 44)
js = [WORDS(f"{sid}-tw", 0.1), BLUR("#pl-n0", 0.3), FADE("#pl-a0", 0.45), PLACE("#pl-enc", 0.4), PLACE("#pl-dec", 0.5), DRAW("#pl-a1", 0.7, 0.3, 200), DRAW("#pl-a2", 0.7, 0.3, 200),
      FADE("#pl-slot", 0.8), FADE("#pl-old", 0.9), HIDE("#pl-new"), HIDE("#pl-n1"), HIDE("#pl-n2"), HIDE("#pl-a1"), HIDE("#pl-a2")]
js = [j for j in js if j not in (HIDE("#pl-a1"), HIDE("#pl-a2"))] + [HIDE("#pl-a1"), HIDE("#pl-a2")]
js = [WORDS(f"{sid}-tw", 0.1), BLUR("#pl-n0", 0.3), FADE("#pl-a0", 0.45), PLACE("#pl-enc", 0.4), PLACE("#pl-dec", 0.5), DRAW("#pl-w1", 0.7, 0.3, 200), DRAW("#pl-w2", 0.7, 0.3, 200),
      FADE("#pl-slot", 0.8), FADE("#pl-old", 0.9), HIDE("#pl-new"), HIDE("#pl-n1"), HIDE("#pl-n2"), HIDE("#pl-a1"), HIDE("#pl-a2"),
      T("#pl-old", 1.5, '{y:0,opacity:1}', '{y:240,opacity:0}', 0.45, "power3.in"),
      T("#pl-new", 1.7, '{y:-260,opacity:0}', '{y:0,opacity:1}', 0.7, "expo.out")]
for j in (1, 2):
    t = 2.4 + (j - 1) * 0.8
    js += [T(f"#pl-n{j-1}", t, '{y:0,opacity:1}', '{y:-40,opacity:0}', 0.25, "power3.in"), FADE(f"#pl-a{j-1}", t, 0.2, 1, 0),
           T(f"#pl-n{j}", t + 0.15, '{y:40,opacity:0}', '{y:0,opacity:1}', 0.35, "expo.out"), FADE(f"#pl-a{j}", t + 0.25, 0.25)]
js.append(BLUR("#pl-end", 4.0, 0.2))
S.append(dict(id=sid, label="Cắm vào backbone", dur=4.8, frags=[1.2, 2.2, 3.0, 3.8, 4.5], html=m, js="\n".join(js), title="Cắm vào ba họ mô hình, không train lại",
  notes="Mỗi backbone có một khối attention nằm giữa encoder và decoder. Bấm: SCSA thay đúng khối đó, encoder, decoder và trọng số gốc giữ nguyên. Bấm: tên đổi sang StyTr2, một transformer, tỉ lệ trộn 1,2 và 0,5. Bấm: StyleID, một mô hình diffusion, 0,8 và 0,2. Với StyleID có thêm chi tiết: hỏi thuần bằng map làm mất chi tiết, nên tác giả pha thêm feature của ảnh; S-AdaIN chỉ dùng ở bước đầu. Chi tiết ở Appendix C của paper. Bấm: chốt ý, không train lại, dùng ngay với model có sẵn."))

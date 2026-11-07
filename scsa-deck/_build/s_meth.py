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
m += box("pp-enc", 330, 290, 150, 406, "Encoder", "của mô hình gốc", fs=28)
m += box("pp-sca", 530, 290, 400, 160, "SCA", "tông chung cả vùng", dark=True)
m += box("pp-sad", 530, 536, 190, 160, "S-AdaIN", "", fs=30)
m += box("pp-ssa", 740, 536, 190, 160, "SSA", "1 điểm", dark=True)
m += box("pp-mix", 990, 420, 250, 180, "Trộn", "tông + nét + bố cục", accent=True)
m += box("pp-dec", 1290, 430, 170, 170, "Decoder", "của mô hình gốc", fs=30)
m += print_img("pp-out", IMG + "ex1_sanet_scsa.png", 1500, 390, 220)
m += label("pp-ol", "SANet + SCSA", 1488, 640, 268, 30, INK, "center", 700)
PSUB = ["SANet (CNN): encoder VGG → SCSA → decoder CNN",
        "StyTr2 (Transformer): transformer encoder → SCSA trong transformer decoder → decoder CNN",
        "StyleID (Diffusion): DDIM inversion → SCSA trong U-Net → VAE decoder"]
for j, t_ in enumerate(PSUB):
    m += label(f"pp-sub{j}", t_, 192, 212, 1600, 32, INK2, weight=500)
P = {"in": "M296 338 L330 338 M296 442 L330 442 M296 546 L330 546 M296 650 L330 650", "e1": "M480 370 L530 370", "e2": "M480 616 L530 616",
     "e3": "M720 616 L740 616", "m1": "M930 370 L960 370 L960 470 L990 470", "m2": "M930 616 L960 616 L960 550 L990 550",
     "res": "M625 696 L625 750 L1115 750 L1115 600", "d1": "M1240 510 L1290 510", "d2": "M1460 510 L1500 510"}
pp = ""
for k, d in P.items():
    pp += f'<path id="pp-p{k}" d="{d}" stroke="{ACC if k == "res" else INK}" stroke-width="4" fill="none"/>'
DOTS = [("e1", 480, 370, 530, 370), ("e3", 720, 616, 740, 616), ("d1", 1240, 510, 1290, 510), ("d2", 1460, 510, 1500, 510)]
for k, x1, y1, x2, y2 in DOTS:
    pp += f'<circle id="pp-dot{k}" cx="{x1}" cy="{y1}" r="9" fill="{ACC}"/>'
m += svg(pp)
m += label("pp-rl", "bố cục của ảnh (sau S-AdaIN) được cộng vào", 650, 760, 560, 30, ACC, weight=600)
m += line("pp-end", f'Hai đầu là của mô hình gốc, giữ nguyên. Các khối ở giữa là {acc("SCSA")}.', 860, 44)
js = [WORDS(f"{sid}-tw", 0.1), FADE("#pp-sub0", 0.4), HIDE("#pp-sub1"), HIDE("#pp-sub2"), 'tl.fromTo("#pp-in .print",{opacity:0,y:20},{opacity:1,y:0,duration:0.6,ease:"expo.out",stagger:0.08},0.3);',
      DRAW("#pp-pin", 0.7, 0.3, 300), BLUR("#pp-enc", 0.8, 0.2),
      DRAW("#pp-pe1", 1.4, 0.3, 100), PLACE("#pp-sca", 1.5, 0.6),
      DRAW("#pp-pe2", 2.3, 0.3, 100), PLACE("#pp-sad", 2.4, 0.6), DRAW("#pp-pe3", 2.7, 0.2, 100), PLACE("#pp-ssa", 2.8, 0.6),
      DRAW("#pp-pm1", 3.4, 0.4, 300), DRAW("#pp-pm2", 3.4, 0.4, 300), PLACE("#pp-mix", 3.6, 0.6), DRAW("#pp-pres", 3.7, 0.6, 1000), 'tl.set("#pp-pres",{strokeDasharray:"12 9",strokeDashoffset:0},4.3);', BLUR("#pp-rl", 4.0),
      DRAW("#pp-pd1", 4.5, 0.2, 100), PLACE("#pp-dec", 4.6, 0.6), DRAW("#pp-pd2", 4.8, 0.2, 100), PLACE("#pp-out", 4.9, 0.7), FADE("#pp-ol", 5.2),
      FADE("#pp-sub0", 5.6, 0.25, 1, 0), BLUR("#pp-sub1", 5.8, 0.25),
      T("#pp-enc", 5.6, '{borderColor:"#16181C"}', '{borderColor:"#C2185B"}', 0.3, "power2.out"),
      T("#pp-dec", 5.6, '{borderColor:"#16181C"}', '{borderColor:"#C2185B"}', 0.3, "power2.out"),
      FADE("#pp-sub1", 6.4, 0.25, 1, 0), BLUR("#pp-sub2", 6.6, 0.25),
      BLUR("#pp-end", 7.3, 0.2)]
for k, x1, y1, x2, y2 in DOTS:
    t_on = {"e1": 1.5, "e3": 2.8, "d1": 4.6, "d2": 4.9}[k]
    js += [HIDE(f"#pp-dot{k}"), f'tl.fromTo("#pp-dot{k}",{{attr:{{cx:{x1}}},opacity:1}},{{attr:{{cx:{x2}}},duration:0.5,ease:"none"}},{t_on});', f'tl.set("#pp-dot{k}",{{opacity:0}},{t_on + 0.5});']
S.append(dict(id=sid, label="Sơ đồ toàn cảnh", dur=8.0, frags=[1.2, 2.0, 3.2, 4.4, 5.4, 6.2, 7.0, 7.7], html=m, js="\n".join(js), title="Toàn cảnh: SCSA nằm ở giữa",
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
NOL = ";box-shadow:none"  # no grid lines, so the brush texture stays visible under the mix
def ssa40(i):
    k = SSA[i]; r, c = divmod(k, G)
    return f';background-image:url({IMG}29_paint.jpg);background-size:{G*CL}px {G*CL}px;background-position:-{c*CL}px -{r*CL}px{NOL}'
TX0, TW = 300, 300
m = (title(sid, "Trộn hai nhánh: chỉnh tông và nét", ("Trộn",))
     + label("mz-l", "SSA", 192, 278, 90, 32, INK, weight=800) + label("mz-r", "SCA", TX0 + TW + 28, 278, 100, 32, INK, weight=800)
     + f'<div id="mz-tr" style="position:absolute;left:{TX0}px;top:296px;width:{TW}px;height:8px;background:{INK}"></div>'
     + f'<div id="mz-k" style="position:absolute;left:{TX0-20}px;top:280px;width:40px;height:40px;border-radius:50%;background:{ACC};box-shadow:0 0 0 5px #fff"></div>'
     + "".join(f'<div class="mz-p tile" style="left:{XM + (i % G)*CL}px;top:{YM + (i // G)*CL}px;width:{CL}px;height:{CL}px{ssa40(i)}"></div>' for i in range(G*G))
     + f'<div id="mz-tone" style="position:absolute;inset:0;mix-blend-mode:color">' + flat("mz-c", [rgb(SCA[i]) for i in range(G*G)], XM, YM, CL, extra_fn=lambda i: NOL) + '</div>'
     + f'<div id="mz-sca">' + flat("mz-s", [rgb(SCA[i]) for i in range(G*G)], XM, YM, CL, extra_fn=lambda i: NOL) + '</div>'
     + line("mz-t0", "Chỉ SSA: sắc nét, nhưng màu nhảy giữa các ô.", 380, 40, left=760, width=480, weight=600)
     + line("mz-t1", "Chỉ SCA: đều màu, nhưng phẳng.", 380, 40, left=760, width=480, weight=600)
     + line("mz-t2", f'SANet: {acc("0,7")} tông chung + {acc("0,3")} nét cọ → đều màu mà vẫn có nét.', 380, 40, left=760, width=480, weight=600)
     + print_img("mz-real", IMG + "ex1_sanet_scsa.png", 1300, 348, 404)
     + label("mz-rl", "kết quả thật", 1300, 790, 428, 30, INK2, "center", 500)
     + line("mz-end", f'Kết quả = {acc("α₁")}·SCA + {acc("α₂")}·SSA + bố cục của ảnh', 880, 44))
js = [WORDS(f"{sid}-tw", 0.1), FADE("#mz-l", 0.3), FADE("#mz-r", 0.3), GROW_X("#mz-tr", 0.3, 0.5), FADE("#mz-k", 0.5, 0.2),
      'tl.fromTo(".mz-p",{opacity:0},{opacity:1,duration:0.3,stagger:0.003},0.4);', HIDE("#mz-sca"), HIDE("#mz-tone"), HIDE("#mz-t1"), HIDE("#mz-t2"),
      BLUR("#mz-t0", 0.9),
      MOVE("#mz-k", 1.6, 0, 0, TW, 0, 1.2, "power2.inOut"), FADE("#mz-sca", 1.6, 1.2, 0, 1, "power2.inOut"), FADE("#mz-t0", 1.6, 0.2, 1, 0), BLUR("#mz-t1", 2.6),
      MOVE("#mz-k", 3.4, TW, 0, TW*0.7, 0, 0.8, "power2.inOut"), FADE("#mz-sca", 3.4, 0.8, 1, 0.35, "power2.inOut"), FADE("#mz-tone", 3.4, 0.01), FADE("#mz-t1", 3.4, 0.2, 1, 0), BLUR("#mz-t2", 4.0),
      PLACE("#mz-real", 4.8), FADE("#mz-rl", 5.1), BLUR("#mz-end", 5.6, 0.2)]
S.append(dict(id=sid, label="Trộn hai nhánh", dur=6.4, frags=[1.2, 3.0, 4.4, 5.4, 6.0], html=m, js="\n".join(js), title="Trộn hai nhánh: chỉnh tông và nét",
  notes="Thanh trượt giữa SSA thuần và SCA thuần; SANet đặt ở 0,7 / 0,3."))

# ---------------- plug into three backbones ----------------
sid = "plug"
# where SCSA goes in each backbone: README §4 / outline A.4.6 (paper Appendix C)
BB = [("SANet", "CNN", ("Encoder VGG", ""), "khối SANet", "thay khối attention SANet", ("Decoder", "CNN"), "0,7 / 0,3"),
      ("StyTr2", "Transformer", ("Transformer encoder", "ảnh, tranh"), "attention ảnh–tranh", "thay attention ảnh–tranh ở lớp chẵn của decoder", ("Decoder", "CNN"), "1,2 / 0,5"),
      ("StyleID", "Diffusion", ("DDIM inversion", "ảnh, tranh → nhiễu"), "self-attention của U-Net", "thay self-attention của U‑Net (K, V từ tranh)", ("VAE decoder", "Stable Diffusion"), "0,8 / 0,2")]
PCX, PW = [192, 720, 1248], 480
m = title(sid, "Cắm vào ba họ mô hình, không train lại", ("không",))
wires = ""
for j, (n, fam, b1, old, new_, b3, a) in enumerate(BB):
    x = PCX[j]
    m += f'<div id="pl-n{j}" class="lb" style="left:{x}px;top:236px;width:{PW}px;font-size:48px;font-weight:800">{n} <span style="color:{INK2};font-weight:500;font-size:34px">· {fam}</span></div>'
    m += box(f"pl-e{j}", x, 316, PW, 104, b1[0], b1[1], fs=32)
    m += f'<div id="pl-o{j}" style="position:absolute;left:{x}px;top:452px;width:{PW}px;height:176px;background:#C9CDD3;border:4px dashed {INK2};display:flex;align-items:center;justify-content:center;text-align:center;padding:12px;font-size:34px;font-weight:700;color:{INK}">{old}</div>'
    m += (f'<div id="pl-s{j}" style="position:absolute;left:{x}px;top:452px;width:{PW}px;height:176px;background:{INK};color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:10px 18px">'
          f'<div style="font-size:44px;font-weight:800;color:#fff">SCSA</div><div style="font-size:30px;font-weight:500;color:#C9CDD3;line-height:1.2;margin-top:4px">{new_}</div></div>')
    m += box(f"pl-d{j}", x, 660, PW, 104, b3[0], b3[1], fs=32)
    m += label(f"pl-a{j}", f"trộn tông / nét: {a}", x, 784, PW, 30, INK2, "center", 500)
    cx = x + PW // 2
    wires += f'<path id="pl-w{j}a" d="M{cx} 420 L{cx} 452" stroke="{INK}" stroke-width="4"/><path id="pl-w{j}b" d="M{cx} 628 L{cx} 660" stroke="{INK}" stroke-width="4"/>'
m += svg(wires)
m += line("pl-end", f'Mỗi lần cắm vào một mô hình, chỉ thay khối attention: {acc("không")} train lại.', 860, 44)
def col(j, t, swap_at):
    out = [BLUR(f"#pl-n{j}", t), PLACE(f"#pl-e{j}", t + 0.1, 0.6), FADE(f"#pl-w{j}a", t + 0.3, 0.2), FADE(f"#pl-o{j}", t + 0.35, 0.3),
           FADE(f"#pl-w{j}b", t + 0.45, 0.2), PLACE(f"#pl-d{j}", t + 0.5, 0.6), FADE(f"#pl-a{j}", t + 0.7), HIDE(f"#pl-s{j}"),
           T(f"#pl-o{j}", swap_at, '{y:0,opacity:1}', '{y:60,opacity:0}', 0.35, "power3.in"),
           T(f"#pl-s{j}", swap_at + 0.2, '{y:-80,opacity:0}', '{y:0,opacity:1}', 0.6, "expo.out")]
    return out
js = [WORDS(f"{sid}-tw", 0.1)] + col(0, 0.3, 1.4) + col(1, 2.4, 3.1) + col(2, 4.1, 4.8) + [BLUR("#pl-end", 5.8, 0.2)]
S.append(dict(id=sid, label="Cắm vào backbone", dur=6.6, frags=[1.2, 2.25, 4.0, 5.7, 6.2], html=m, js="\n".join(js), title="Cắm vào ba họ mô hình, không train lại",
  notes="Mỗi backbone có một khối attention nằm giữa encoder và decoder. Bấm: SCSA thay đúng khối đó, encoder, decoder và trọng số gốc giữ nguyên. Bấm: tên đổi sang StyTr2, một transformer, tỉ lệ trộn 1,2 và 0,5. Bấm: StyleID, một mô hình diffusion, 0,8 và 0,2. Với StyleID có thêm chi tiết: hỏi thuần bằng map làm mất chi tiết, nên tác giả pha thêm feature của ảnh; S-AdaIN chỉ dùng ở bước đầu. Chi tiết ở Appendix C của paper. Bấm: chốt ý, không train lại, dùng ngay với model có sẵn."))

# ---------------- training process and what is new ----------------
sid = "train"
TR = [("Backbone: train sẵn, giữ nguyên", "SANet, StyTr2: MS-COCO × WikiArt · StyleID: Stable Diffusion có sẵn"),
      (f'SCSA: {acc("0")} tham số mới', "không loss mới, không bước train nào"),
      ("Lúc chạy: ba việc", "tạo mặt nạ nhãn (K-Means) → thay khối attention → trộn α₁, α₂")]
NEW = [("SCA", "hỏi bằng bản đồ nhãn, cả vùng chung một tông"),
       ("SSA", "top-1 trong cùng vùng, giữ nguyên nét cọ"),
              ("Cắm được", "một khối cho CNN, Transformer, Diffusion"),
       ("SSL", "thước đo style theo từng vùng")]
m = title(sid, "Huấn luyện thế nào, và điểm mới ở đâu")
m += label("tr-h", "Huấn luyện", 192, 262, 700, 48, INK, weight=800)
for i, (h, d) in enumerate(TR):
    y = 340 + i * 150
    m += label(f"tr-a{i}", h, 192, y, 700, 38, INK, weight=700)
    m += label(f"tr-b{i}", d, 192, y + 52, 700, 32, INK2, weight=500)
m += svg(f'<path id="tr-div" d="M960 270 L960 800" stroke="#C9CDD3" stroke-width="4" fill="none"/>')
m += label("tr-nh", "Điểm mới", 1028, 262, 700, 48, INK, weight=800)
for j, (h, d) in enumerate(NEW):
    m += label(f"tr-n{j}", f'<b>{h}</b> · {d}', 1028, 340 + j * 94, 700, 34, INK, weight=500)
m += line("tr-end", f'Cái mới nằm ở {acc("luật")} {acc("cấm")} theo nhãn, không nằm ở trọng số.', 870, 44)
js = [WORDS(f"{sid}-tw", 0.1), BLUR("#tr-h", 0.3)]
for i in range(3):
    t = 0.5 + 0.45 * i
    js += [BLUR(f"#tr-a{i}", t), FADE(f"#tr-b{i}", t + 0.15)]
js += [DRAW("#tr-div", 2.2, 0.5, 600), BLUR("#tr-nh", 2.3)]
for j in range(len(NEW)):
    js.append(BLUR(f"#tr-n{j}", 2.5 + 0.25 * j))
js.append(BLUR("#tr-end", 4.3, 0.2))
S.append(dict(id=sid, label="Huấn luyện và điểm mới", dur=5.0, frags=[2.0, 4.0, 4.6], html=m, js="\n".join(js), title="Huấn luyện thế nào, và điểm mới ở đâu",
  notes="Huấn luyện và điểm mới."))

# ---------------- one formula, plus a mask ----------------
sid = "maskf"
MROW = ["−∞" if B.KL[j] != 1 else "0" for j in range(4)]
OUTP = ["0%" if B.KL[j] != 1 else "100%" for j in range(4)]
CLIFF = B.RGBS[B.KEYS[B.KL.index(1)]]
m = title(sid, "SCA, SSA: cùng công thức, thêm mặt nạ M")
m += eq("mk-f", f'softmax( Q K<sup style="font-size:0.6em">T</sup> <span id="mk-fm">+ M</span> ) · V', 222, size=68, width=1300)
m += label("mk-fn", f'M = 0: được lấy · M = {acc("−∞")}: bị cấm (e<sup>−∞</sup> = 0, nên ô cấm nhận 0%)', 192, 318, 1536, 34, INK2, weight=500)
m += B.ex_head("mk", 420)
m += B.ex_row("mk-r1", f'Q K<sup>T</sup> · độ giống', [vn(v_) for v_ in B.SHOW], 590)
m += B.ex_row("mk-r2", f'{acc("+ M")} · khác nhãn thì cấm', MROW, 652, [ACC if x_ != "0" else INK for x_ in MROW])
m += B.ex_row("mk-r3", "softmax · chia đủ 100%", OUTP, 714)
m += f'<div id="mk-out" style="position:absolute;left:{B.EXC[2]}px;top:774px;width:140px;height:44px;background:{rgb(CLIFF)}"></div>'
m += label("mk-outl", "→ lấy đúng màu vách núi", B.EXC[3] + 160, 778, 420, 30, INK, weight=600)
m += label("mk-sca", f'<b>SCA</b> · Q, K hỏi bằng {acc("bản đồ nhãn")}; M cấm ô khác nhãn → cả vùng một tông', 192, 846, 1536, 32, INK, weight=500)
m += label("mk-ssa", f'<b>SSA</b> · Q hỏi bằng ảnh; M cấm thêm, chỉ chừa {acc("1 ô")} giống nhất cùng nhãn → giữ nét cọ', 192, 896, 1536, 32, INK, weight=500)
js = [WORDS(f"{sid}-tw", 0.1), BLUR("#mk-f", 0.3, 0.25), FADE("#mk-fn", 0.6)]
js += B.ex_head_js("mk", 1.2) + B.ex_js("mk-r1", 1.6)
js += [T("#mk-fm", 2.6, f'{{color:"{INK}"}}', f'{{color:"{ACC}"}}', 0.25, "power2.out")] + B.ex_js("mk-r2", 2.6)
js += B.ex_js("mk-r3", 3.6) + [WIPE("#mk-out", 4.0, 0.5), BLUR("#mk-outl", 4.4)]
js += [BLUR("#mk-sca", 5.0), BLUR("#mk-ssa", 5.4)]
S.append(dict(id=sid, label="Công thức SCA, SSA", dur=6.2, frags=[1.0, 2.5, 3.5, 4.8, 5.8], html=m, js="\n".join(js), title="SCA, SSA: cùng công thức, thêm mặt nạ M",
  notes="Công thức mặt nạ."))

# ---------------- the whole algorithm ----------------
sid = "algo"
STEPS = [("Vào", "ảnh, map ảnh, tranh, map tranh · hai hệ số α₁, α₂"),
         ("1", "Encoder: ảnh, tranh và hai map → lưới điểm"),
         ("2", "K-Means trên hai map → mặt nạ nhãn"),
         ("3", "SCA, mặt nạ cùng nhãn → tông chung"),
         ("4", "S-AdaIN: đổi tông ảnh riêng từng vùng"),
         ("5", "SSA, mặt nạ top-1 cùng nhãn → nét cọ"),
         ("6", f'Trộn: F = α₁·SCA + α₂·SSA + {v("F","c")}'),
         ("Ra", "Decoder: lưới điểm → ảnh kết quả")]
GROUPS = [(0, 1, 2), (3, 4, 5), (6, 7)]
m = title(sid, "Thuật toán SCSA: một lượt chạy, không train")
m += f'<div id="al-panel" style="position:absolute;left:192px;top:250px;width:1100px;height:560px;background:#FFFFFF;box-shadow:0 18px 40px rgba(20,24,28,.10)"></div>'
m += f'<div id="al-hl" style="position:absolute;left:192px;top:276px;width:1100px;height:58px;background:rgba(194,24,91,0.10)"></div>'
for i, (k, s_) in enumerate(STEPS):
    y = 280 + i * 64
    m += label(f"al-k{i}", k, 216, y, 80, 34, ACC if k in ("Vào", "Ra") else INK2, "right", 800)
    m += f'<div id="al-s{i}" class="lb" style="left:320px;top:{y}px;width:950px;font-size:34px;font-weight:600;white-space:nowrap">{s_}</div>'
m += label("al-ch", "Chi phí mỗi lớp attention", 1360, 262, 368, 34, INK, weight=800)
m += f'<div id="al-big" class="big" style="left:1360px;top:370px;font-size:110px">4.096²</div>'
m += label("al-cn", "≈ 16,8 triệu ô mỗi bảng; SCA, SSA mỗi nhánh một bảng", 1360, 500, 368, 32, INK, weight=500)
m += label("al-cg", "bước 2 làm sẵn một lần (sem.py)", 1360, 680, 368, 32, INK2, weight=500)
m += line("al-end", f'Bước 2–6 là phần SCSA; encoder, decoder {acc("giữ")} nguyên.', 880, 44)
js = [WORDS(f"{sid}-tw", 0.1), PLACE("#al-panel", 0.2), HIDE("#al-hl")]
t0 = [0.5, 2.0, 3.6]
for g, idx in enumerate(GROUPS):
    for j, i in enumerate(idx):
        js += [BLUR(f"#al-k{i}", t0[g] + 0.25 * j), WIPE(f"#al-s{i}", t0[g] + 0.25 * j, 0.5)]
    first, last = idx[0], idx[-1]
    p0, p1 = (GROUPS[g - 1][0], GROUPS[g - 1][-1]) if g else (first, first)
    js.append(T("#al-hl", t0[g], f'{{y:{p0 * 64},height:{(p1 - p0) * 64 + 58},opacity:{1 if g else 0}}}', f'{{y:{first * 64},height:{(last - first) * 64 + 58},opacity:1}}', 0.5, "power2.inOut"))
js += [BLUR("#al-ch", 4.6), BLUR("#al-big", 4.75), FADE("#al-cn", 4.9), FADE("#al-cg", 5.0), BLUR("#al-end", 5.6, 0.2)]
S.append(dict(id=sid, label="Thuật toán", dur=6.4, frags=[1.6, 3.2, 4.5, 5.4, 6.0], html=m, js="\n".join(js), title="Thuật toán SCSA: một lượt chạy, không train",
  notes="Thuật toán."))

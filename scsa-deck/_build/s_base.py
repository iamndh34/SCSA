from lib import *
import math

S = []
LC, LS, UA = DATA["labelsC"], DATA["labelsS"], DATA["ua"]
RGBC, RGBS, RGBAD = DATA["rgbC"], DATA["rgbS"], DATA["rgbAd"]

# shared worked example: the cliff point that leans hardest on the wrong region
QA = max((i for i in range(G*G) if LC[i] == 1), key=lambda i: UA[i]["wrong"])
def rep(l):
    cand = [k for k in range(G*G) if LS[k] == l]
    mu = DATA["regMean"][l]
    return min(cand, key=lambda k: sum((a-b)**2 for a, b in zip(RGBS[k], mu)))
KEYS = [rep(0), rep(3), rep(1), rep(2)]          # trời, dãy xa, vách núi, rừng
KL = [0, 3, 1, 2]
_d = [d2(RGBAD[QA], RGBS[k]) for k in KEYS]
_T = sorted(_d)[1]
LOGIT = [-v / _T for v in _d]
_z = sum(math.exp(v) for v in LOGIT)
W = [math.exp(v) / _z for v in LOGIT]
PCT = [round(w * 100) for w in W]; PCT[PCT.index(max(PCT))] += 100 - sum(PCT)
SHOW = [v - min(LOGIT) + 0.5 for v in LOGIT]
MIX = [round(sum(w * RGBS[k][j] for w, k in zip(W, KEYS))) for j in range(3)]

def ptile(id_, src, i, x, y, size, extra=""):
    r, c = divmod(i, G)
    return (f'<div id="{id_}" class="tile" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;background-image:url({src});'
            f'background-size:{size*G}px {size*G}px;background-position:-{c*size}px -{r*size}px;{extra}"></div>')

# ---------------- grid ----------------
sid = "grid"
C0, X0, Y0, GAP = 34, 204, 262, 5
LIFT = QA
m = (title(sid, "Ảnh được cắt thành lưới điểm")
     + print_img("grid-p", IMG + "29.jpg", 192, 250, 408)
     + tiles("grid-t", IMG + "29.jpg", X0, Y0, C0)
     + label("grid-l1", "ảnh 512 × 512 pixel", 192, 690, 520, 32, INK2, weight=500)
     + label("grid-l2", "12 × 12 = 144 điểm · mô hình thật: 64 × 64 = 4.096", 192, 750, 720, 32, INK, weight=600))
bars = [int(30 + (RGBC[LIFT][k % 3] * (k + 3) * 37) % 110) for k in range(18)]
m += f'<div id="grid-vec" style="position:absolute;left:1000px;top:250px;width:560px;height:150px;display:flex;align-items:flex-end;gap:10px">'
m += "".join(f'<div class="grid-bar" style="width:20px;height:{h}px;background:{INK}"></div>' for h in bars) + '</div>'
m += label("grid-vl", "1 điểm vách núi = 1 vector, ví dụ 512 số: mô tả mảng ảnh quanh nó", 820, 420, 900, 32)
m += label("grid-dec", "decoder vẽ lưới thành ảnh", 820, 540, 440, 32, INK2, weight=500)
m += svg(leader("grid-ar", [(800, 600), (1270, 600)], INK, 3, False) + '<path id="grid-ah" d="M1258 588 L1278 600 L1258 612Z" fill="#16181C"/>')
m += print_img("grid-out", IMG + "29.jpg", 1300, 520, 400)
m += line("grid-end", f'SCSA chỉ sửa {acc("lưới")} {acc("điểm")} ở giữa.', 860, 40, width=1060)
js = [WORDS(f"{sid}-tw", 0.1), PLACE("#grid-p", 0.3), FADE("#grid-l1", 0.6), HIDE(".grid-t-c")]
js += [FADE(".grid-t-c", 1.2, 0.01), FADE("#grid-p", 1.25, 0.3, 1, 0), FADE("#grid-l1", 1.25, 0.2, 1, 0)]
js.append(f'tl.fromTo(".grid-t-c",{{x:0,y:0}},{{x:function(i){{return (i%{G})*{GAP};}},y:function(i){{return Math.floor(i/{G})*{GAP};}},duration:0.8,ease:"power2.inOut",stagger:{{each:0.004,from:"start"}}}},1.3);')
js.append(BLUR("#grid-l2", 1.9))
r, c = divmod(LIFT, G)
sx, sy = X0 + c*(C0+GAP), Y0 + r*(C0+GAP)
dx, dy = 820 - sx, 250 - sy
js.append(f'tl.fromTo("#grid-t-{LIFT}",{{x:{c*GAP},y:{r*GAP},scale:1,transformOrigin:"0% 0%",boxShadow:"0 0 0 rgba(0,0,0,0)"}},{{x:{c*GAP+dx},y:{r*GAP+dy},scale:{150/C0:.3f},boxShadow:"0 14px 30px rgba(20,24,28,0.25)",duration:0.8,ease:"expo.out"}},2.6);')
js += [GROW_Y(".grid-bar", 3.0, 0.4).replace("duration:0.4", "duration:0.4,stagger:0.02"), BLUR("#grid-vl", 3.2)]
js += [BLUR("#grid-dec", 3.8), DRAW("#grid-ar", 3.9, 0.4, 500), FADE("#grid-ah", 4.25, 0.1), PLACE("#grid-out", 4.1), BLUR("#grid-end", 4.6, 0.2)]
S.append(dict(id=sid, label="Lưới điểm", dur=5.4, frags=[1.0, 2.4, 3.6, 5.0], html=m, js="\n".join(js), title="Ảnh được cắt thành lưới điểm",
  notes="Từ “điểm” dùng suốt phần sau. Bấm: encoder cắt ảnh thành lưới. Ở đây mình cắt 12 nhân 12 cho dễ nhìn; mô hình thật dùng 64 nhân 64, tức 4.096 điểm. Bấm: mỗi điểm không chỉ là một màu, mà là một vector, ví dụ 512 số, mô tả mảng ảnh quanh nó: màu, cạnh, bề mặt. Hai điểm trông giống nhau thì vector gần nhau. Bấm: decoder vẽ lưới ngược lại thành ảnh. Style transfer kiểu attention sửa lưới ở giữa, và SCSA cũng chỉ sửa ở đó."))

# ---------------- attention ----------------
sid = "attn"
KY = [270, 410, 550, 690]; KS = 120
m = (title(sid, "Attention: hỏi, so, cân, trộn")
     + label("attn-ql", "một điểm vách núi hỏi:", 192, 340, 420, 32, INK2, weight=500)
     + ptile("attn-q", IMG + "29.jpg", QA, 230, 400, 180, f"box-shadow:0 0 0 7px {ACC}")
     + label("attn-qb", "“style nào hợp với tôi?”", 192, 610, 460, 34, INK, weight=600))
lines = ""
for j, (k, y, w) in enumerate(zip(KEYS, KY, W)):
    lines += f'<line id="attn-ln{j}" x1="417" y1="490" x2="852" y2="{y + KS/2}" stroke="{INK}" stroke-width="{2 + 22*w:.1f}" stroke-linecap="round" stroke-opacity="{0.35 + 0.65*w/max(W):.2f}"/>'
m += svg(lines)
for j, (k, y, w, l) in enumerate(zip(KEYS, KY, W, KL)):
    m += ptile(f"attn-k{j}", IMG + "29_paint.jpg", k, 860, y, KS)
    m += f'<div id="attn-sw{j}" style="position:absolute;left:1000px;top:{y+16}px;width:22px;height:22px;background:{REG[l]}"></div>'
    m += label(f"attn-kn{j}", REGN[l], 1032, y + 6, 150, 30, INK, weight=600)
    m += f'<div id="attn-b{j}" style="position:absolute;left:1000px;top:{y+60}px;width:{max(4, int(w*420))}px;height:34px;background:{INK}"></div>'
    m += label(f"attn-v{j}", f"{PCT[j]}%", 1012 + max(4, int(w*420)), y + 54, 120, 34, INK, weight=800)
    m += f'<div id="attn-pt{j}" style="position:absolute;left:{860+KS/2-18}px;top:{y+KS/2-18}px;width:36px;height:36px;background:{rgb(RGBS[k])};box-shadow:0 0 0 3px #fff"></div>'
m += label("attn-kl", "4 điểm trong tranh", 860, 822, 400, 32, INK2, weight=500)
m += f'<div id="attn-r" style="position:absolute;left:1520px;top:400px;width:190px;height:190px;background:#DADDE1;box-shadow:0 0 0 7px {ACC}"></div>'
m += label("attn-rl", "kết quả = trộn theo trọng số", 1480, 610, 260, 32, INK, "center")
_ord = sorted(range(4), key=lambda j: -W[j]); WRONGP = sum(PCT[j] for j in range(4) if KL[j] != 1)
m += line("attn-end", f'Vách núi giống {REGN[KL[_ord[0]]]} và {REGN[KL[_ord[1]]]} hơn vách núi: {acc(str(WRONGP) + "%")} màu lấy sai vùng.', 860, 44)
js = [WORDS(f"{sid}-tw", 0.1), BLUR("#attn-ql", 0.3), T("#attn-q", 0.4, '{opacity:0,scale:0.8}', '{opacity:1,scale:1}', 0.7, "expo.out"), BLUR("#attn-qb", 0.8)]
for j in range(4):
    js += [PLACE(f"#attn-k{j}", 1.4 + 0.1*j, 0.6), DRAW(f"#attn-ln{j}", 1.6 + 0.1*j, 0.5, 600), FADE(f"#attn-sw{j}", 1.6 + 0.1*j, 0.2), BLUR(f"#attn-kn{j}", 1.65 + 0.1*j)]
js.append(FADE("#attn-kl", 2.0))
for j in range(4):
    js += [GROW_X(f"#attn-b{j}", 2.6 + 0.12*j, 0.6), BLUR(f"#attn-v{j}", 2.9 + 0.12*j)]
js += [T("#attn-r", 3.6, '{opacity:0,scale:0.8}', '{opacity:1,scale:1}', 0.6, "expo.out"), FADE("#attn-rl", 3.7)]
for j, y in enumerate(KY):
    js += [HIDE(f"#attn-pt{j}"), FADE(f"#attn-pt{j}", 3.8 + 0.12*j, 0.1), MOVE(f"#attn-pt{j}", 3.8 + 0.12*j, 0, 0, 1615 - (860 + KS/2), 495 - (y + KS/2), 0.7),
           FADE(f"#attn-pt{j}", 4.5 + 0.12*j, 0.15, 1, 0)]
js += [f'tl.fromTo("#attn-r",{{backgroundColor:"#DADDE1"}},{{backgroundColor:"{rgb(MIX)}",duration:0.5,ease:"power1.inOut",immediateRender:false}},4.6);', BLUR("#attn-end", 5.3, 0.2)]
S.append(dict(id=sid, label="Attention", dur=6.0, frags=[1.2, 2.4, 3.4, 5.1, 5.7], html=m, js="\n".join(js), title="Attention: hỏi, so, cân, trộn",
  notes=f"Attention giống tra từ điển, nhưng mềm. Bấm: một điểm trên vách núi của ảnh đặt câu hỏi, gọi là query. Bấm: nó so với các điểm trong tranh; mỗi điểm có thẻ để so, gọi là key, và nội dung để lấy về, gọi là value. Ở đây là bốn mảnh thật của bức tranh: trời, dãy xa, vách núi, rừng. Đường càng dày càng giống. Bấm: độ giống đổi thành trọng số {PCT[0]}, {PCT[1]}, {PCT[2]} và {PCT[3]} phần trăm. Bấm: màu chảy về theo trọng số và trộn lại. Bấm: chú ý, mảnh vách núi xám nhạt trong ảnh trông giống {REGN[KL[_ord[0]]]} và {REGN[KL[_ord[1]]]} của tranh hơn chính vách núi trong tranh, nên {WRONGP} phần trăm màu của nó lấy từ sai vùng. Đó chính là lỗi ta thấy ở kết quả SANet. Số phần trăm tính minh hoạ trên màu của ảnh mẫu, không phải số của mô hình thật."))

# ---------------- softmax + mask ----------------
sid = "softmax"
BX = [250, 420, 590, 760]; BASE, HMAX = 700, 340
smax = max(SHOW)
H1 = [HMAX * v / smax for v in SHOW]
H2 = [HMAX * p / 100 for p in PCT]
KEEP = KL.index(1)
H3 = [HMAX if j == KEEP else 0 for j in range(4)]
m = title(sid, "Chia trọng số, và cách “cấm” một ô", ("cấm",))
m += label("sm-ct", "điểm số của 4 mảnh", 230, 240, 640, 32, INK2, weight=500)
for j, (x, l, k) in enumerate(zip(BX, KL, KEYS)):
    m += f'<div id="sm-b{j}" style="position:absolute;left:{x}px;top:{BASE-HMAX}px;width:110px;height:{HMAX}px;background:{REG[l]};transform-origin:50% 100%"></div>'
    for tag, val, top in (("s", vn(SHOW[j]), H1[j]), ("w", f"{PCT[j]}%", H2[j]), ("v", f"{100 if j == KEEP else 0}%", H3[j])):
        m += label(f"sm-{tag}{j}", val, x - 25, BASE - top - 52, 160, 38, ACC if tag != "s" else INK, "center", 800)
    m += ptile(f"sm-t{j}", IMG + "29_paint.jpg", k, x + 20, BASE + 16, 70)
    m += label(f"sm-n{j}", REGN[l], x - 25, BASE + 94, 160, 28, INK, "center", 600)
m += f'<div style="position:absolute;left:230px;top:{BASE}px;width:660px;height:5px;background:{INK}"></div>'
m += svg(hatch_def("smh") + "".join(f'<rect id="sm-h{j}" x="{BX[j]-6}" y="{BASE-HMAX-20}" width="122" height="{HMAX+20}" fill="url(#smh)"/>' for j in range(4) if j != KEEP))
m += label("sm-x", f'khác nhãn vách núi: {acc("cấm")}', 230, 240, 660, 32, INK, weight=700)
m += label("sm-sbl", "chia 100% trọng số", 1000, 330, 728, 32, INK2, weight=500)
seg = "".join(f'<div id="sm-g{j}" style="height:110px;width:{728*PCT[j]/100:.0f}px;background:{REG[KL[j]]}"></div>' for j in range(4))
m += f'<div id="sm-sb" style="position:absolute;left:1000px;top:380px;width:728px;height:110px;display:flex;overflow:hidden;background:#fff">{seg}</div>'
m += line("sm-e1", "Softmax: điểm cao được phần lớn, cộng lại đúng 100%.", 540, 40, left=1000, width=728, weight=500)
m += line("sm-e2", f'Đặt {acc("−∞")} vào ô bị cấm: ô đó nhận đúng 0%, phần còn lại tự chia lại.', 540, 40, left=1000, width=728, weight=500)
m += line("sm-end", f'SCSA chỉ làm một việc: quyết định {acc("ô")} {acc("nào")} {acc("bị")} {acc("cấm")}.', 760, 44, left=1000, width=728)
js = [WORDS(f"{sid}-tw", 0.1), FADE("#sm-ct", 0.3)]
for j in range(4):
    js += [GROW_Y(f"#sm-b{j}", 0.4 + 0.12*j, 0.7, 0, H1[j]/HMAX), PLACE(f"#sm-t{j}", 0.4 + 0.12*j, 0.6), FADE(f"#sm-n{j}", 0.5 + 0.12*j), BLUR(f"#sm-s{j}", 0.8 + 0.12*j)]
    js += [HIDE(f"#sm-w{j}"), HIDE(f"#sm-v{j}")]
js += [HIDE("#sm-x"), HIDE("#sm-e2")] + [HIDE(f"#sm-h{j}") for j in range(4) if j != KEEP]
for j in range(4):
    js += [FADE(f"#sm-s{j}", 1.6, 0.2, 1, 0), T(f"#sm-b{j}", 1.7, f'{{scaleY:{H1[j]/HMAX:.4f}}}', f'{{scaleY:{H2[j]/HMAX:.4f}}}', 0.8, "power2.inOut"), BLUR(f"#sm-w{j}", 2.4)]
js += [WIPE("#sm-sb", 1.8, 0.9), FADE("#sm-sbl", 1.8), BLUR("#sm-e1", 2.4, 0.2)]
for j in range(4):
    if j != KEEP: js.append(FADE(f"#sm-h{j}", 3.0, 0.3))
js += [FADE("#sm-ct", 2.9, 0.15, 1, 0), BLUR("#sm-x", 3.0), FADE("#sm-e1", 3.2, 0.2, 1, 0), BLUR("#sm-e2", 3.4, 0.2)]
for j in range(4):
    js += [FADE(f"#sm-w{j}", 3.3, 0.2, 1, 0), T(f"#sm-b{j}", 3.4, f'{{scaleY:{H2[j]/HMAX:.4f}}}', f'{{scaleY:{max(H3[j],0.001)/HMAX:.4f}}}', 0.8, "power2.inOut"), BLUR(f"#sm-v{j}", 4.1),
           T(f"#sm-g{j}", 3.5, f'{{width:{728*PCT[j]/100:.0f}}}', f'{{width:{728 if j == KEEP else 0}}}', 0.8, "power2.inOut")]
js.append(BLUR("#sm-end", 4.7, 0.2))
S.append(dict(id=sid, label="Softmax và luật cấm", dur=5.6, frags=[1.4, 2.8, 4.4, 5.2], html=m, js="\n".join(js), title="Chia trọng số, và cách “cấm” một ô",
  notes=f"Vẫn bốn mảnh vừa rồi. Bấm: đây là điểm số giống nhau của từng mảnh, cột trời cao nhất. Bấm: softmax biến điểm số thành phần trăm, cộng lại đủ 100: {PCT[0]}, {PCT[1]}, {PCT[2]}, {PCT[3]}. Điểm cao được phần lớn, nhưng không ai bị bỏ hẳn. Bấm: giờ ta ra luật: điểm vách núi chỉ được lấy từ vách núi. Ba mảnh kia bị cấm. Cách cấm là đặt âm vô cực vào điểm số của chúng; e mũ âm vô cực bằng 0, nên ba cột rơi về đúng 0 và cột vách núi nhận 100 phần trăm. Không phải sửa gì khác trong mô hình, đó là lý do SCSA cắm được vào mô hình đã train. Bấm: toàn bộ SCSA chỉ là quyết định ô nào bị cấm."))

# ---------------- AdaIN ----------------
sid = "adain"
def stats(cells):
    mu = [sum(c[j] for c in cells) / len(cells) for j in range(3)]
    lum = [0.299*c[0] + 0.587*c[1] + 0.114*c[2] for c in cells]
    ml = sum(lum) / len(lum); sd = (sum((v - ml) ** 2 for v in lum) / len(lum)) ** 0.5
    return [round(v) for v in mu], sd
muC, sdC = stats(RGBC); muS, sdS = stats(RGBS)
m = (title(sid, "AdaIN: đổi tông bằng hai con số", ("hai",))
     + print_img("ad-a", IMG + "29.jpg", 192, 270, 380)
     + print_img("ad-s", IMG + "29_paint.jpg", 680, 470, 150, mat=8)
     + print_img("ad-r", IMG + "29_adain.png", 1324, 270, 380))
for tag, mu, sd, y, nm in (("c", muC, sdC, 290, "tông của ảnh"), ("s", muS, sdS, 490, "tông của tranh")):
    m += label(f"ad-{tag}n", nm, 870, y - 6, 400, 32, INK, weight=700)
    m += f'<div id="ad-{tag}mu" style="position:absolute;left:870px;top:{y+40}px;width:90px;height:90px;background:{rgb(mu)};box-shadow:0 0 0 3px #fff"></div>'
    m += label(f"ad-{tag}ml", "μ màu trung bình", 975, y + 44, 300, 28, INK2, weight=500)
    m += f'<div id="ad-{tag}sd" style="position:absolute;left:975px;top:{y+92}px;width:{min(260, sd*3.2):.0f}px;height:22px;background:{INK}"></div>'
    m += label(f"ad-{tag}sl", "σ độ tương phản", 975, y + 120, 260, 28, INK2, weight=500)
m += svg(leader("ad-ar", [(1250, 470), (1312, 470)], INK, 4, False) + '<path id="ad-ah" d="M1302 456 L1322 470 L1302 484Z" fill="#16181C"/>')
m += label("ad-rl", "cả ảnh khoác một tông của tranh", 1324, 690, 404, 32, INK, "center")
m += line("ad-step", "Bỏ μ, σ của ảnh, khoác μ, σ của tranh.", 690, 32, left=192, width=500, weight=500, color=INK2)
m += line("ad-end", f'Một cặp số cho cả ảnh: mọi vùng bị kéo về {acc("cùng")} một tông.', 860, 44)
js = [WORDS(f"{sid}-tw", 0.1), PLACE("#ad-a", 0.3)]
js += [BLUR("#ad-cn", 0.6), T("#ad-cmu", 0.7, '{opacity:0,scale:0.6}', '{opacity:1,scale:1}', 0.5, "expo.out"), FADE("#ad-cml", 0.8), GROW_X("#ad-csd", 0.8), FADE("#ad-csl", 1.0)]
js += [PLACE("#ad-s", 1.4), BLUR("#ad-sn", 1.5), T("#ad-smu", 1.6, '{opacity:0,scale:0.6}', '{opacity:1,scale:1}', 0.5, "expo.out"), FADE("#ad-sml", 1.7), GROW_X("#ad-ssd", 1.7), FADE("#ad-ssl", 1.9)]
js += [DRAW("#ad-ar", 2.4, 0.3, 100), FADE("#ad-ah", 2.65, 0.1), PLACE("#ad-r", 2.5), WIPE("#ad-r", 2.6, 0.9), BLUR("#ad-rl", 3.2), FADE("#ad-step", 3.2)]
js += [BLUR("#ad-end", 3.9, 0.2)]
S.append(dict(id=sid, label="AdaIN", dur=4.8, frags=[1.2, 2.2, 3.6, 4.4], html=m, js="\n".join(js), title="AdaIN: đổi tông bằng hai con số",
  notes="AdaIN là phương pháp 2017 trong slide lịch sử, SCSA dùng lại nó. Bấm: tông của một ảnh tóm trong hai con số. μ là màu trung bình: ảnh chụp này xám ấm. σ là độ tương phản: sáng tối chênh nhau bao nhiêu. Bấm: bức tranh có μ, σ riêng: màu kem xanh, tương phản thấp hơn. Bấm: AdaIN bỏ μ, σ của ảnh rồi khoác μ, σ của tranh. Ảnh bên phải là phép tính thật trên pixel của ảnh mẫu: cả ảnh ngả về tông của tranh. Trong mô hình, phép này làm trên lưới điểm, không phải trên pixel; bước “bỏ μ, σ” chính là ký hiệu F gạch ngang trong paper. Bấm: giới hạn là chỉ một cặp số cho cả ảnh, nên trời, vách núi, rừng bị kéo về cùng một tông. S-AdaIN ở chặng 4 sẽ sửa điều này."))

# ---------------- universal attention sweep ----------------
sid = "ua"
CL, XC, XS_, YG = 36, 192, 1296, 320
order = []
for l, n in ((1, 3), (0, 2), (2, 2), (3, 1)):
    cand = sorted((i for i in range(G*G) if LC[i] == l), key=lambda i: -UA[i]["wrong"])
    pick = cand[:: max(1, len(cand)//(n+1))][:n]
    order += pick
order.sort()
m = (title(sid, "Universal Attention: ai cũng nhìn tất cả", ("tất", "cả"))
     + label("ua-l1", "ảnh chụp: 144 câu hỏi", XC, YG - 52, 432, 32, INK2, weight=500)
     + label("ua-l2", "tranh: 144 thẻ", XS_, YG - 52, 432, 32, INK2, weight=500)
     + tiles("ua-c", IMG + "29.jpg", XC, YG, CL) + tiles("ua-s", IMG + "29_paint.jpg", XS_, YG, CL))
ln = "".join(f'<line id="ua-ln{j}" x1="0" y1="0" x2="0" y2="0" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>' for j in range(8))
m += svg(ln + f'<rect id="ua-q" x="{XC}" y="{YG}" width="{CL}" height="{CL}" fill="none" stroke="{ACC}" stroke-width="6"/>'
         + "".join(f'<rect id="ua-k{j}" x="0" y="0" width="{CL}" height="{CL}" fill="none" stroke="{INK}" stroke-width="4"/>' for j in range(8)))
for s_, q in enumerate(order):
    pw = round(UA[q]["wrong"] * 100)
    m += label(f"ua-r{s_}", f'<span style="color:{REG[LC[q]]}">■</span> {REGN[LC[q]]}: {acc(str(pw) + "%")} trọng số sang vùng khác', 192, 774, 1536, 36, INK, "center", 700)
m += line("ua-end", f'Mỗi điểm nhìn tất cả 144 thẻ. {acc("Không")} ai hỏi điểm đó thuộc vùng nào.', 868, 44)
js = [WORDS(f"{sid}-tw", 0.1), FADE("#ua-l1", 0.3), FADE("#ua-l2", 0.3),
      'tl.fromTo(".ua-c-c",{opacity:0},{opacity:1,duration:0.3,stagger:0.004},0.3);', 'tl.fromTo(".ua-s-c",{opacity:0},{opacity:1,duration:0.3,stagger:0.004},0.5);',
      HIDE("#ua-q")] + [HIDE(f"#ua-ln{j}") for j in range(8)] + [HIDE(f"#ua-k{j}") for j in range(8)] + [HIDE(f"#ua-r{s}") for s in range(len(order))]
t0, step = 1.6, 1.0
for s_, q in enumerate(order):
    t = t0 + s_ * step
    qx, qy = cell_center(q, XC, YG, CL)
    js.append(f'tl.set("#ua-q",{{attr:{{x:{qx-CL/2},y:{qy-CL/2}}},opacity:1}},{t});')
    top = UA[q]["top"][:8]
    wmax = top[0][1]
    for j, (k, w) in enumerate(top):
        kx, ky = cell_center(k, XS_, YG, CL)
        wrong = LS[k] != LC[q]
        col = ACC if wrong else INK
        js.append(f'tl.set("#ua-ln{j}",{{attr:{{x1:{qx+CL/2},y1:{qy},x2:{kx-CL/2},y2:{ky},stroke:"{col}","stroke-width":{2+14*w/wmax:.1f}}},opacity:{0.35+0.65*w/wmax:.2f}}},{t});')
        js.append(f'tl.set("#ua-k{j}",{{attr:{{x:{kx-CL/2},y:{ky-CL/2},stroke:"{col}"}},opacity:1}},{t});')
    js.append(f'tl.fromTo(".ua-lnd",{{opacity:0}},{{opacity:1,duration:0.01}},{t});'.replace('.ua-lnd', f'#ua-r{s_}'))
    if s_: js.append(f'tl.set("#ua-r{s_-1}",{{opacity:0}},{t});')
tend = t0 + len(order) * step
js.append(BLUR("#ua-end", tend + 0.6, 0.2))
S.append(dict(id=sid, label="Universal Attention", dur=round(tend + 1.4, 1), frags=[1.4, round(tend + 0.2, 2), round(tend + 1.0, 2)], html=m, js="\n".join(js), title="Universal Attention: ai cũng nhìn tất cả",
  notes="Paper gọi khối attention trong SANet, StyTr2, StyleID là Universal Attention, viết tắt UA. Trái là 144 điểm của ảnh, phải là 144 điểm của tranh, đều là mảnh thật. Bấm: khung magenta là câu hỏi đang xét; nó chạy qua vài điểm của vách núi, trời, rừng, dãy xa. Mỗi lần, các đường nối tới 8 mảnh tranh giống nó nhất. Đường đen là cùng vùng, đường magenta là sang vùng khác. Dòng chữ giữa đọc phần trăm trọng số rơi sang vùng khác. Bấm: chốt ý, mỗi điểm nhìn tất cả 144 thẻ, không ai hỏi điểm đó thuộc vùng nào. Với lưới 64 nhân 64 thật, bảng so khớp có 16 triệu ô. Số tính minh hoạ trên màu của ảnh mẫu."))

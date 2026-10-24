from lib import *
import s_base as B

S = []
SSA = DATA["ssa"]

# ---------------- real results ----------------
sid = "results"
EX = [("ex1", "SANet", "vách núi: màu trời → màu núi, trời đúng màu trời"),
      ("ex2", "StyTr2", "dòng thác trắng, liền mạch; đá giữ màu tối của đá"),
      ("ex3", "StyleID", "áo, mặt, nền lấy nét từ đúng vùng trong tranh")]
XS = [192, 580, 968, 1356]
m = title(sid, "Kết quả thật trên ba họ mô hình")
for e, (ex, bb, note) in enumerate(EX):
    g = f'<div id="rs-g{e}" style="position:absolute;left:0;top:0;width:1920px;height:1080px">'
    for j, (suf, cap) in enumerate((("content", "ảnh nội dung"), ("style", "ảnh phong cách"), (bb.lower(), bb), (bb.lower() + "_scsa", f'{bb} + {acc("SCSA")}'))):
        g += print_img(f"rs-p{e}{j}", IMG + f"{ex}_{suf}.png", XS[j], 290, 348)
        g += label(f"rs-c{e}{j}", cap, XS[j], 684, 372, 32, INK if j >= 2 else INK2, "center", 700 if j >= 2 else 500)
    g += line(f"rs-n{e}", note, 760, 40, weight=600) + '</div>'
    m += g
m += line("rs-src", "Ảnh: Fig. 2 trong repo của tác giả (github.com/scn-00/SCSA).", 880, 30, weight=500, color=INK2)
js = [WORDS(f"{sid}-tw", 0.1), HIDE("#rs-g1"), HIDE("#rs-g2")]
js += [f'tl.fromTo("#rs-g0 .print",{{opacity:0,y:28}},{{opacity:1,y:0,duration:0.8,ease:"expo.out",stagger:0.1}},0.3);', BLUR("#rs-n0", 0.9), FADE("#rs-src", 1.0)]
for e in (1, 2):
    t = 1.4 + (e - 1) * 1.4
    js += [T(f"#rs-g{e-1}", t, '{x:0,opacity:1,filter:"blur(0px)"}', '{x:-160,opacity:0,filter:"blur(6px)"}', 0.3, "power3.in"),
           T(f"#rs-g{e}", t + 0.2, '{x:200,opacity:0,filter:"blur(6px)"}', '{x:0,opacity:1,filter:"blur(0px)"}', 0.7, "expo.out")]
S.append(dict(id=sid, label="Kết quả thật", dur=4.6, frags=[1.2, 2.6, 4.0], html=m, js="\n".join(js), title="Kết quả thật trên ba họ mô hình",
  notes="Ba ví dụ lấy nguyên từ hình kết quả của paper. Mỗi hàng: ảnh nội dung, ảnh phong cách, backbone gốc, và backbone cộng SCSA. SANet: đúng cặp ảnh ta theo dõi cả buổi; vách núi chuyển từ màu trời sang màu núi. Bấm: StyTr2, ví dụ thác nước: bản gốc lấy màu loang lổ, bản SCSA giữ dòng thác trắng và đá tối. Bấm: StyleID, ví dụ chân dung: áo, mặt và nền lấy nét từ đúng vùng tương ứng trong tranh. Lưu ý: mình chỉ mô tả những gì thấy được trên ba ảnh này; con số tổng quát ở slide sau."))

# ---------------- four metrics ----------------
sid = "metrics"
MT = [("SSL", "↓ thấp là tốt", "So style từng vùng: trời với trời, vách núi với vách núi.", "ssl"),
      ("FID", "↓ thấp là tốt", "Cả tập kết quả có “trông như tranh” không, xét tổng thể.", "fid"),
      ("CFSD", "↓ thấp là tốt", "Kết quả còn giữ bố cục của ảnh gốc không.", "cfsd"),
      ("Người xem", "↑ cao là tốt", "40 người so từng cặp có và không có SCSA, tổng 1.200 phiếu.", "vote")]
m = title(sid, "Bốn thước đo, đọc trước khi xem số")
for j, (h, a, s, kind) in enumerate(MT):
    g = f'<div id="mt-g{j}" style="position:absolute;left:0;top:0;width:1920px;height:1080px">'
    g += f'<div class="big" style="left:192px;top:300px;font-size:120px">{h}</div>'
    g += label(f"mt-a{j}", a, 192, 440, 600, 40, INK2, weight=600)
    g += line(f"mt-s{j}", s, 520, 44, width=880)
    if kind == "ssl":
        g += print_img(f"mt-x{j}a", IMG + "ex1_sanet_scsa.png", 1150, 300, 240) + print_img(f"mt-x{j}b", IMG + "29_paint.jpg", 1460, 300, 240)
        g += label(f"mt-x{j}l", "kết quả ↔ tranh, từng vùng", 1150, 580, 574, 32, INK, "center")
    elif kind == "fid":
        for i, ex in enumerate(("ex1", "ex2", "ex3")):
            g += print_img(f"mt-f{i}", IMG + f"{ex}_{['sanet','stytr2','styleid'][i]}_scsa.png", 1150 + i*196, 300, 160, mat=8)
            g += print_img(f"mt-h{i}", IMG + f"{ex}_style.png", 1150 + i*196, 500, 160, mat=8)
        g += label(f"mt-x{j}l", "cả tập kết quả ↔ cả tập tranh", 1150, 700, 574, 32, INK, "center")
    elif kind == "cfsd":
        g += print_img(f"mt-x{j}a", IMG + "29.jpg", 1150, 300, 240) + print_img(f"mt-x{j}b", IMG + "ex1_sanet_scsa.png", 1460, 300, 240)
        g += label(f"mt-x{j}l", "bố cục ảnh gốc ↔ bố cục kết quả", 1150, 580, 574, 32, INK, "center")
    else:
        g += f'<div class="big" style="left:1150px;top:320px;font-size:110px;color:{INK}">1.200</div>' + label("mt-vl", "phiếu bầu", 1150, 450, 574, 40, INK2, weight=600)
    m += g + '</div>'
m += line("mt-end", f'SSL do {acc("chính")} tác giả đề xuất: nhìn thêm FID và CFSD để thấy cái giá.', 860, 44)
js = [WORDS(f"{sid}-tw", 0.1)] + [HIDE(f"#mt-g{j}") for j in (1, 2, 3)]
js += [T("#mt-g0", 0.3, '{opacity:0,filter:"blur(8px)"}', '{opacity:1,filter:"blur(0px)"}', 0.25, "power2.out")]
for j in (1, 2, 3):
    t = 0.9 + (j - 1) * 0.8
    js += [T(f"#mt-g{j-1}", t, '{opacity:1,filter:"blur(0px)"}', '{opacity:0,filter:"blur(8px)"}', 0.18, "power2.in"),
           T(f"#mt-g{j}", t + 0.15, '{opacity:0,filter:"blur(8px)"}', '{opacity:1,filter:"blur(0px)"}', 0.25, "power2.out")]
js.append(BLUR("#mt-end", 3.4, 0.2))
S.append(dict(id=sid, label="Bốn thước đo", dur=4.2, frags=[0.7, 1.5, 2.3, 3.1, 3.8], html=m, js="\n".join(js), title="Bốn thước đo, đọc trước khi xem số",
  notes="Mỗi lần bấm một thước đo. SSL, Semantic Style Loss: cắt kết quả và tranh theo nhãn, so style trời với trời, vách núi với vách núi, bằng chữ ký màu kiểu Gatys. Thấp là tốt. Bấm: FID: cả tập kết quả có trông như tranh không, xét tổng thể, không quan tâm đúng vùng. Bấm: CFSD: kết quả còn giữ bố cục của ảnh gốc không. Bấm: người xem: 40 người, 1.200 phiếu, so từng cặp có và không có SCSA. Bấm: lưu ý quan trọng, SSL do chính tác giả đề xuất và đo đúng điều SCSA tối ưu, nên SCSA thắng ở SSL gần như chắc chắn. Nhìn thêm FID và CFSD."))

# ---------------- SSL chart ----------------
sid = "ssl"
GR = [("SANet", 1.6583, 0.8762, "−47%"), ("StyTr2", 1.9826, 1.2228, "−38%"), ("StyleID", 1.7538, 1.2447, "−29%")]
BASE, SC = 780, 190
m = title(sid, "Lỗi style theo vùng giảm 29–47%")
m += label("sl-leg", f'SSL, thấp là tốt · <span style="color:#9AA1AC">■</span> mô hình gốc · <span style="color:{INK}">■</span> + SCSA', 192, 230, 900, 30, INK2, weight=500)
m += f'<div style="position:absolute;left:220px;top:{BASE}px;width:880px;height:5px;background:{INK}"></div>'
for i, (n, a, b_, p) in enumerate(GR):
    x = 260 + i*290; ha, hb = a*SC, b_*SC
    m += f'<div id="sl-a{i}" style="position:absolute;left:{x}px;top:{BASE-ha:.0f}px;width:100px;height:{ha:.0f}px;background:#9AA1AC"></div>'
    m += label(f"sl-av{i}", vn(a, 2), x - 20, BASE - ha - 48, 140, 34, INK2, "center", 700)
    m += f'<div id="sl-b{i}" style="position:absolute;left:{x+110}px;top:{BASE-hb:.0f}px;width:100px;height:{hb:.0f}px;background:{INK}"></div>'
    m += label(f"sl-bv{i}", vn(b_, 2), x + 90, BASE - hb - 48, 140, 34, INK, "center", 800)
    m += label(f"sl-n{i}", n, x - 20, BASE + 16, 250, 36, INK, "center", 800)
    m += label(f"sl-p{i}", p, x + 90, BASE - hb - 100, 140, 40, ACC, "center", 800)
for j, (h, s) in enumerate((("FID", "tốt hơn nhẹ ở cả ba mô hình"), ("CFSD", f'StyleID + SCSA giữ bố cục {acc("kém")} hơn: 0,092 → 0,118'), ("Người xem", "chọn bản SCSA: 83% · 84% · 78%"))):
    m += label(f"sl-k{j}", h, 1180, 300 + j*170, 548, 40, INK, weight=800)
    m += label(f"sl-ks{j}", s, 1180, 352 + j*170, 548, 34, INK, weight=500)
m += line("sl-src", "Số liệu: Table 1 của paper, 91 bộ bốn do tác giả tuyển.", 880, 30, weight=500, color=INK2)
js = [WORDS(f"{sid}-tw", 0.1), FADE("#sl-leg", 0.3)]
for i in range(3):
    js += [GROW_Y(f"#sl-a{i}", 0.4 + 0.15*i, 0.7), FADE(f"#sl-av{i}", 0.9 + 0.15*i), FADE(f"#sl-n{i}", 0.4 + 0.15*i)]
for i in range(3):
    js += [GROW_Y(f"#sl-b{i}", 1.6 + 0.2*i, 0.8), FADE(f"#sl-bv{i}", 2.2 + 0.2*i), BLUR(f"#sl-p{i}", 2.3 + 0.2*i)]
for j in range(3):
    js += [BLUR(f"#sl-k{j}", 3.2 + 0.3*j), FADE(f"#sl-ks{j}", 3.3 + 0.3*j)]
js.append(FADE("#sl-src", 3.2))
S.append(dict(id=sid, label="Số liệu SSL", dur=4.8, frags=[1.4, 3.0, 4.4], html=m, js="\n".join(js), title="Lỗi style theo vùng giảm 29–47%",
  notes="Cột xám là mô hình gốc, cột đen là có SCSA, thước đo SSL. Bấm: SANet từ 1,66 xuống 0,88, giảm 47 phần trăm. StyTr2 từ 1,98 xuống 1,22, giảm 38. StyleID từ 1,75 xuống 1,24, giảm 29. Bấm: các thước đo khác. FID tốt hơn nhẹ ở cả ba, tức style tổng thể không tệ đi. CFSD: riêng StyleID cộng SCSA giữ bố cục kém hơn, 0,092 lên 0,118; đây là cái giá. Người xem chọn bản SCSA 83, 84, 78 phần trăm. SANet cộng SCSA còn có SSL tốt hơn năm phương pháp semantic chuyên biệt. Số lấy từ Table 1, đánh giá trên 91 bộ bốn tác giả tự tuyển."))

# ---------------- ablation ----------------
sid = "ablation"
AB = [("Đủ cả ba", 1.245, "mốc để so", INK), ("Bỏ SSA", 1.330, "mất texture", INK2), ("Bỏ S-AdaIN", 1.756, "kém chính xác, ít chi tiết", INK2), ("Bỏ SCA", 2.298, "lệch màu giữa các vùng", ACC)]
m = title(sid, "Bỏ bớt một mảnh, lỗi tăng bao nhiêu?")
m += label("ab-sub", "trên StyleID · SSL, thấp là tốt", 192, 230, 900, 30, INK2, weight=500)
for i, (n, v, d, c) in enumerate(AB):
    y = 300 + i * 120; w = v * 320
    m += label(f"ab-n{i}", n, 192, y + 14, 300, 40, INK, weight=800)
    m += f'<div id="ab-b{i}" style="position:absolute;left:500px;top:{y}px;width:{w:.0f}px;height:80px;background:{c}"></div>'
    m += label(f"ab-v{i}", f'<b style="font-size:44px">{vn(v, 3)}</b> · {d}', 520 + w, y + 14, 560, 32, INK, weight=500)
m += line("ab-end", f'SCA lo tông chung, SSA lo nét cọ. {acc("Thiếu")} cái nào cũng tệ hơn.', 840, 44)
js = [WORDS(f"{sid}-tw", 0.1), FADE("#ab-sub", 0.2)]
for i in range(4):
    t = 0.3 + 0.8*i
    js += [BLUR(f"#ab-n{i}", t), GROW_X(f"#ab-b{i}", t, 0.6), FADE(f"#ab-v{i}", t + 0.4)]
js.append(BLUR("#ab-end", 3.6, 0.2))
S.append(dict(id=sid, label="Ablation", dur=4.6, frags=[1.0, 1.8, 2.6, 3.4, 4.2], html=m, js="\n".join(js), title="Bỏ bớt một mảnh, lỗi tăng bao nhiêu?",
  notes="Thí nghiệm bỏ từng khối, trên StyleID là nơi thấy rõ nhất. Bấm từng thanh. Đủ cả ba: 1,245. Bỏ SSA: 1,33, màu đúng nhưng mất texture. Bỏ S-AdaIN: 1,76, kém chính xác, ít chi tiết. Bỏ SCA: 2,30, gần gấp đôi, lệch màu giữa các vùng. Bấm: SCA lo tông chung, SSA lo nét cọ. Điểm nên phản biện: trên SANet, bỏ S-AdaIN gần như không đổi SSL, 0,876 so với 0,877, và bỏ SCA hoặc S-AdaIN lại cho FID tốt hơn. Với backbone yếu, không phải mảnh nào cũng cần. Số từ Fig. 6 và Appendix F."))

# ---------------- limits ----------------
sid = "limits"
from collections import Counter
top_k, top_n = Counter(SSA).most_common(1)[0]
CL, XM, YM = 30, 600, 300
def t30(i):
    k = SSA[i]; r, c = divmod(k, G)
    return f';background-image:url({IMG}29_paint.jpg);background-size:{G*CL}px {G*CL}px;background-position:-{c*CL}px -{r*CL}px'
m = title(sid, "Những điều SCSA chưa giải quyết")
m += print_img("lm-map", IMG + "29_sem.png", 192, 288, 336)
m += label("lm-ml", "phải tự có bản đồ nhãn, nhãn hai bên phải khớp", 192, 660, 380, 32, INK, weight=600)
m += "".join(f'<div class="lm-t tile" style="left:{XM + (i % G)*CL}px;top:{YM + (i // G)*CL}px;width:{CL}px;height:{CL}px{t30(i)}"></div>' for i in range(G*G))
m += svg("".join(f'<rect class="lm-rep" x="{XM + (i % G)*CL + 2}" y="{YM + (i // G)*CL + 2}" width="{CL-4}" height="{CL-4}" fill="none" stroke="{ACC}" stroke-width="4"/>' for i in range(G*G) if SSA[i] == top_k))
m += label("lm-rl", f'một mảnh tranh bị SSA dùng lại {acc(str(top_n) + " lần")}', 600, 660, 420, 32, INK, weight=600)
for j, s in enumerate(("Chỉ 91 bộ dữ liệu tự tuyển, chưa có benchmark lớn.", "SSL, thước đo chính, do tác giả tự đặt.", "Chậm và tốn bộ nhớ hơn mô hình gốc.", "Vùng không có cặp bên tranh thì sao?")):
    m += line(f"lm-s{j}", s, 300 + j*120, 38, left=1100, width=628, weight=600)
js = [WORDS(f"{sid}-tw", 0.1), PLACE("#lm-map", 0.3), BLUR("#lm-ml", 0.6),
      'tl.fromTo(".lm-t",{opacity:0},{opacity:1,duration:0.3,stagger:0.004},1.2);', HIDE(".lm-rep"),
      'tl.fromTo(".lm-rep",{opacity:0,scale:1.6,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:0.3,ease:"expo.out",stagger:0.05},1.9);', BLUR("#lm-rl", 2.4)]
for j in range(4): js.append(BLUR(f"#lm-s{j}", 3.2 + 0.25*j, 0.2))
S.append(dict(id=sid, label="Hạn chế", dur=4.6, frags=[1.0, 3.0, 4.2], html=m, js="\n".join(js), title="Những điều SCSA chưa giải quyết",
  notes=f"Hai hạn chế nhìn được ngay trên ví dụ của ta. Bản đồ nhãn phải do người dùng cung cấp, và nhãn hai bên phải khớp nhau; tác giả tự nêu điều này. Bấm: SSA chỉ lấy một điểm, nên một mảnh tranh có thể bị dùng lại nhiều lần: trên lưới minh hoạ, một mảnh bị dùng {top_n} lần, khung magenta. Ở độ phân giải thật, điều này có thể gây lặp texture. Bấm: thêm các điểm để thảo luận: chỉ 91 bộ dữ liệu tự tuyển; SSL do tác giả tự đặt; tốn thời gian và bộ nhớ hơn; và nếu một vùng của ảnh không có vùng cùng nhãn bên tranh thì cả hàng attention bị cấm, paper không nói xử lý thế nào. Mỗi điểm là một hướng mở rộng cho proposal."))

# ---------------- code ----------------
sid = "code"
FILES = [("29.jpg", "ảnh"), ("29_paint.jpg", "tranh"), ("29_sem.png", "map ảnh"), ("29_paint_sem.png", "map tranh")]
TERM = ["$ git clone https://github.com/scn-00/SCSA", "$ cd SCSA && python sem.py", "$ cd SANet+SCSA", "$ python SCSA.py \\",
        "    --content ../sem_data/29/29.jpg \\", "    --style ../sem_data/29/29_paint.jpg \\", "    --content_sem ../sem_data/29/29_sem.png \\", "    --style_sem ../sem_data/29/29_paint_sem.png ..."]
m = title(sid, "Chạy code gốc trên đúng ví dụ này")
m += label("cd-l", "sem_data/29/ · một bộ bốn", 192, 250, 620, 32, INK2, weight=500)
for j, (f, n) in enumerate(FILES):
    x, y = 192 + (j % 2) * 300, 300 + (j // 2) * 270
    m += print_img(f"cd-f{j}", IMG + f, x, y, 150, mat=8)
    m += label(f"cd-fn{j}", f'<span class="mono" style="font-size:28px">{f}</span> · {n}', x, y + 174, 300, 28, INK, weight=600)
lines_ = "".join(f'<div id="cd-t{i}" class="mono" style="white-space:pre;font-size:28px;line-height:1.6;color:{"#F2B8CF" if t.startswith("$") else "#E3E6EA"}">{t}</div>' for i, t in enumerate(TERM))
m += f'<div id="cd-term" style="position:absolute;left:820px;top:290px;width:908px;height:500px;background:{INK};padding:40px 36px">{lines_}</div>'
m += line("cd-end", "Lệnh đầy đủ có thêm hai cờ sem_map; StyleID dùng tên cờ khác. Xem README.", 880, 32, weight=500, color=INK2)
js = [WORDS(f"{sid}-tw", 0.1), FADE("#cd-l", 0.2)] + [PLACE(f"#cd-f{j}", 0.3 + 0.1*j, 0.6) for j in range(4)] + [FADE(f"#cd-fn{j}", 0.5 + 0.1*j) for j in range(4)]
js.append(PLACE("#cd-term", 1.2))
for i in range(len(TERM)):
    js.append(f'tl.fromTo("#cd-t{i}",{{clipPath:"inset(0% 100% 0% 0%)"}},{{clipPath:"inset(0% 0% 0% 0%)",duration:0.35,ease:"steps(20)"}},{1.6 + 0.3*i});')
js.append(FADE("#cd-end", 4.2))
S.append(dict(id=sid, label="Chạy code", dur=5.0, frags=[1.0, 4.0, 4.6], html=m, js="\n".join(js), title="Chạy code gốc trên đúng ví dụ này",
  notes="Bốn file bên trái chính là bộ bốn ta dùng cả buổi, nằm trong sem_data/29 của repo. Bấm: bốn bước. Clone repo, môi trường Python 3.8, PyTorch 2.4.1. Chạy sem.py để tạo mặt nạ nhãn từ semantic map; nó gom màu bằng K-Means. Tải trọng số gốc của SANet vào thư mục models. Vào SANet+SCSA và chạy SCSA.py với mẫu 29. Muốn so với bản gốc thì chạy SANet.py cùng ảnh. Bấm: lệnh đầy đủ có thêm hai cờ sem_map_64 và sem_map_32 trỏ tới sem_precomputed_feats/29. StyleID dùng tên cờ khác, và sem.py có bảng màu cứng theo số thư mục."))

# ---------------- summary ----------------
sid = "summary"
m = (f'<h1 id="sum-big" class="t" style="top:150px;font-size:88px;width:1536px">{words("Chỉ lấy style từ vùng cùng nhãn.", "sum-w", ("cùng", "nhãn."))}</h1>'
     + print_img("sum-a", IMG + "ex1_sanet.png", 192, 360, 340) + print_img("sum-b", IMG + "ex1_sanet_scsa.png", 600, 360, 340)
     + label("sum-ca", "trước", 192, 728, 364, 32, INK2, "center", 600) + label("sum-cb", "sau", 600, 728, 364, 32, INK, "center", 700)
     + line("sum-1", "SCA lấy tông chung của cả vùng.", 380, 40, left=1040, width=688)
     + line("sum-2", "SSA giữ nét cọ của một điểm.", 460, 40, left=1040, width=688)
     + line("sum-3", "Không train lại; lỗi theo vùng giảm 29–47%.", 540, 40, left=1040, width=688)
     + line("sum-l", "arxiv.org/abs/2503.04119 · github.com/scn-00/SCSA", 860, 30, weight=500, color=INK2))
js = [WORDS("sum-w", 0.2, 0.09), PLACE("#sum-a", 1.1), PLACE("#sum-b", 1.25), FADE("#sum-ca", 1.4), FADE("#sum-cb", 1.5),
      BLUR("#sum-1", 2.2), BLUR("#sum-2", 2.5), BLUR("#sum-3", 2.8), FADE("#sum-l", 3.0)]
S.append(dict(id=sid, label="Tóm tắt", dur=3.8, frags=[0.9, 2.0, 3.4], html=m, js="\n".join(js), title="Chỉ lấy style từ vùng cùng nhãn",
  notes="Một câu mang về: chỉ lấy style từ vùng cùng nhãn. Bấm: đây là câu trả lời cho câu hỏi đầu buổi. SANet tô vách núi bằng màu vùng khác vì attention không biết nhãn vùng; SCSA cấm điều đó. Bấm: bên trong là hai cách nhìn: SCA lấy tông chung của cả vùng, SSA giữ nét cọ của một điểm. Không phải train lại, và lỗi style theo vùng giảm 29 đến 47 phần trăm. Nếu chỉ nhớ một hình: ba ma trận. Mình nhận câu hỏi."))

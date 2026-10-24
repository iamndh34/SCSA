"""Export the deck as one standalone HTML presentation (no server, works offline).
Run from the project root: python3 _build/export_html.py <out_dir>
Images go to <out_dir>/assets/img, GSAP to <out_dir>/lib/gsap.min.js (copy them alongside)."""
import base64, json, math, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build                                   # rebuilds the HyperFrames project and exposes SL
from lib import ROOT, GROUND

OUT = pathlib.Path(sys.argv[1]).resolve()
fonts = ""
for n, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800)]:
    b64 = base64.b64encode((ROOT / f"assets/fonts/BeVietnamPro-{n}.ttf").read_bytes()).decode()
    fonts += f"@font-face{{font-family:'Be Vietnam Pro';src:url(data:font/ttf;base64,{b64}) format('truetype');font-weight:{w};font-display:block}}\n"
b64 = base64.b64encode((ROOT / "assets/fonts/JetBrainsMono.ttf").read_bytes()).decode()
fonts += f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/ttf;base64,{b64}) format('truetype');font-weight:100 800;font-display:block}}\n"
deck_css = (ROOT / "assets/deck.css").read_text()

sections, inits, meta = [], [], []
for i, s in enumerate(build.SL):
    sections.append(f'<section class="slide" id="slide-{s["id"]}"><div class="sc">{s["html"]}</div></section>')
    js = build.fix_immediate(s["js"])
    inits.append(f'INIT.push(function () {{\nconst tl = gsap.timeline({{ paused: true }});\n{js}\nTL["{s["id"]}"] = tl;\n}});')
    meta.append({"id": s["id"], "title": s["title"], "frags": s["frags"], "notes": s["notes"]})

html = f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SCSA giải thích từ đầu</title>
<style>
{fonts}
{deck_css}
html, body {{ margin:0; height:100%; background:{GROUND}; overflow:hidden; }}
body {{ font-family:'Be Vietnam Pro', sans-serif; }}
#stage {{ position:absolute; left:50%; top:50%; width:1920px; height:1080px; transform-origin:50% 50%; overflow:hidden; background:{GROUND}; }}
.slide {{ position:absolute; inset:0; visibility:hidden; }}
.slide.on {{ visibility:visible; }}
#hud {{ position:fixed; right:18px; bottom:14px; font:600 14px 'Be Vietnam Pro', sans-serif; color:#4B5260; background:rgba(255,255,255,.75);
        padding:6px 12px; border-radius:6px; opacity:0; transition:opacity .3s; user-select:none; }}
body:hover #hud, #hud.show {{ opacity:1; }}
#help {{ position:fixed; left:50%; top:50%; transform:translate(-50%,-50%); background:#fff; color:#16181C; padding:28px 36px; border-radius:10px;
         box-shadow:0 20px 60px rgba(0,0,0,.25); font:500 18px/1.7 'Be Vietnam Pro', sans-serif; display:none; z-index:10; }}
#help b {{ display:inline-block; min-width:150px; }}
</style>
<script src="lib/gsap.min.js"></script>
</head>
<body>
<div id="stage">
{chr(10).join(sections)}
</div>
<div id="hud"></div>
<div id="help">
<div style="font-weight:800;font-size:22px;margin-bottom:10px">Phím tắt</div>
<b>→ / Space / click</b>bước tiếp theo (chạy hoạt hình)<br>
<b>←</b>lùi một bước<br>
<b>Home / End</b>slide đầu / cuối<br>
<b>F</b>toàn màn hình<br>
<b>P</b>mở cửa sổ ghi chú người trình bày<br>
<b>H hoặc ?</b>bật / tắt bảng này
</div>
<script>
window.__timelines = window.__timelines || {{}};
const TL = window.__timelines, INIT = [];
const META = {json.dumps(meta, ensure_ascii=False).replace("</", "<\\/")};
{chr(10).join(inits)}
</script>
<script>
(function () {{
  INIT.forEach(function (f) {{ f(); }});
  const slides = Array.from(document.querySelectorAll(".slide"));
  const N = META.length;
  let cur = -1, frag = 0, anim = null, notesWin = null, t0 = Date.now();
  const tl = i => TL[META[i].id];
  const F = i => META[i].frags;
  function fit() {{
    const s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    document.getElementById("stage").style.transform = "translate(-50%,-50%) scale(" + s + ")";
  }}
  function kill() {{ if (anim) {{ anim.kill(); anim = null; }} }}
  function playTo(i, t) {{
    kill(); const T = tl(i); const d = t - T.time();
    if (d <= 0) {{ T.time(t); return; }}
    anim = gsap.to(T, {{ time: t, duration: d, ease: "none", onComplete: function () {{ anim = null; }} }});
  }}
  function enter(i, f, animate) {{
    kill();
    slides.forEach(function (s, k) {{ s.classList.toggle("on", k === i); }});
    cur = i; frag = f;
    const T = tl(i);
    if (animate) {{ T.time(0.001, true); T.time(0, true); playTo(i, F(i)[f]); }}
    else T.time(F(i)[f], true);
    update();
  }}
  function next() {{
    if (frag < F(cur).length - 1) {{ frag++; playTo(cur, F(cur)[frag]); update(); }}
    else if (cur < N - 1) enter(cur + 1, 0, true);
  }}
  function prev() {{
    if (frag > 0) {{ frag--; kill(); tl(cur).time(F(cur)[frag], true); update(); }}
    else if (cur > 0) enter(cur - 1, F(cur - 1).length - 1, false);
  }}
  function update() {{
    document.getElementById("hud").textContent = (cur + 1) + " / " + N + " · bước " + (frag + 1) + "/" + F(cur).length;
    try {{ history.replaceState(null, "", "#" + (cur + 1)); }} catch (e) {{}}
    renderNotes();
  }}
  function esc(t) {{ return String(t).replace(/[&<>]/g, function (c) {{ return {{"&":"&amp;","<":"&lt;",">":"&gt;"}}[c]; }}); }}
  function renderNotes() {{
    if (!notesWin || notesWin.closed) return;
    const m = META[cur], nx = META[cur + 1];
    const el = notesWin.document.getElementById("n");
    if (!el) return;
    el.innerHTML = '<div class="top"><span>Slide ' + (cur + 1) + ' / ' + N + '</span><span>Bước ' + (frag + 1) + ' / ' + m.frags.length + '</span><span id="clock"></span></div>'
      + '<h1>' + esc(m.title) + '</h1>' + m.notes.split("\\n").map(function (ln, i) {{ return '<p class="' + (i === frag ? "cur" : "dim") + '">' + esc(ln) + '</p>'; }}).join("")
      + '<div class="next">Tiếp theo: ' + (nx ? esc(nx.title) : "hết") + '</div>';
  }}
  function openNotes() {{
    notesWin = window.open("", "scsa-notes", "width=900,height=720");
    if (!notesWin) return;
    notesWin.document.open();
    notesWin.document.write('<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Ghi chú · SCSA</title><style>'
      + 'body{{font-family:-apple-system,Segoe UI,sans-serif;background:#16181C;color:#E9ECEF;margin:0;padding:28px 34px}}'
      + '.top{{display:flex;gap:28px;color:#9AA1AC;font-size:18px}} h1{{font-size:30px;margin:14px 0}} p{{font-size:24px;line-height:1.5;margin:10px 0;padding-left:14px;border-left:4px solid transparent}} p.dim{{color:#7C838E}} p.cur{{color:#fff;border-left-color:#E0568A}}'
      + '.next{{margin-top:24px;color:#F2B8CF;font-size:20px}} .hint{{color:#6B7280;font-size:15px;margin-top:30px}}</style></head>'
      + '<body><div id="n"></div><div class="hint">Phím → ← dùng được ở cả cửa sổ này.</div></body></html>');
    notesWin.document.close();
    notesWin.document.addEventListener("keydown", onKey);
    renderNotes();
  }}
  setInterval(function () {{
    if (!notesWin || notesWin.closed) return;
    const c = notesWin.document.getElementById("clock"); if (!c) return;
    const s = Math.floor((Date.now() - t0) / 1000); c.textContent = "⏱ " + Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
  }}, 1000);
  function onKey(e) {{
    const k = e.key;
    if (k === "ArrowRight" || k === " " || k === "PageDown" || k === "Enter") {{ e.preventDefault(); next(); }}
    else if (k === "ArrowLeft" || k === "PageUp" || k === "Backspace") {{ e.preventDefault(); prev(); }}
    else if (k === "Home") enter(0, 0, true);
    else if (k === "End") enter(N - 1, F(N - 1).length - 1, false);
    else if (k === "f" || k === "F") {{ if (!document.fullscreenElement) document.documentElement.requestFullscreen().catch(function () {{}}); else document.exitFullscreen(); }}
    else if (k === "p" || k === "P") openNotes();
    else if (k === "h" || k === "H" || k === "?") {{ const h = document.getElementById("help"); h.style.display = h.style.display === "block" ? "none" : "block"; }}
  }}
  document.addEventListener("keydown", onKey);
  document.addEventListener("click", function (e) {{ if (e.target.closest("#help")) return; next(); }});
  window.addEventListener("resize", fit);
  fit();
  const start = Math.max(1, Math.min(N, parseInt((location.hash || "#1").slice(1), 10) || 1)) - 1;
  function go() {{ enter(start, 0, true); const h = document.getElementById("hud"); h.classList.add("show"); setTimeout(function () {{ h.classList.remove("show"); }}, 2500); }}
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(go); else go();
}})();
</script>
</body>
</html>
'''
(OUT / "SCSA_trinh_chieu.html").write_text(html, encoding="utf-8")
print("wrote", OUT / "SCSA_trinh_chieu.html", round(len(html) / 1e6, 2), "MB")

"""Assemble the SCSA deck (v2). Run from the project root: python3 _build2/build.py"""
import json, math, re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lib import ROOT, scene, FONTFACE, INK, GROUND, ACC
import s_open, s_ctx, s_base, s_prob, s_meth, s_res

by = {s["id"]: s for mod in (s_open, s_ctx, s_base, s_prob, s_meth, s_res) for s in mod.S}
for k in range(5):
    c = s_open.chapter(k); by[c["id"]] = c
ORDER = ["cover", "hook", "roadmap",
         "ch1", "st", "apps", "history", "gens",
         "ch2", "maps", "task", "grid", "attn", "softmax", "ua", "uaf", "err1", "err23", "fixmap", "minute",
         "ch3", "pipe", "sca", "adain", "sadain", "ssa", "matrices", "maskf", "mix", "algo", "plug", "train",
         "ch4", "metrics", "results", "ssl", "compare", "ablation", "strengths", "limits",
         "ch5", "summary", "future", "next", "end"]
SL = [by[i] for i in ORDER]
from settle import settle
for s_ in SL:  # never pause a step while its motion is still running
    s_["frags"], _iss = settle(s_)
    for f, f2, leak in _iss:
        print(f"settle: {s_['id']} step at {f}s still moving until {f2}s; next-step tweens start inside: {leak}")
from notes import NOTES, BRIDGE
assert set(NOTES) == set(ORDER), set(NOTES) ^ set(ORDER)
for s_ in SL:
    steps = list(NOTES[s_["id"]])
    if s_["id"] in BRIDGE:
        lab_, txt_ = steps[-1]
        steps[-1] = (lab_, f"{txt_} Dẫn: {BRIDGE[s_['id']]}")
    assert len(steps) == len(s_["frags"]), (s_["id"], len(steps), len(s_["frags"]))
    s_["notes"] = "\n".join((f"Bấm {k} · " if k else "") + f"{lab}: {txt}" for k, (lab, txt) in enumerate(steps))

FT = re.compile(r'tl\.fromTo\("([^"]+)",\{(.*?)\},\{(.*)\},([\d.]+)\);$')
def keys(frm):
    return {k.strip() for k in re.findall(r'(?:^|,)\s*([A-Za-z]+)\s*:', frm)}
def fix_immediate(js):
    seen, out = {}, []
    for ln in js.split("\n"):
        m = FT.match(ln.strip())
        if m:
            sel, frm, to, t = m.groups()
            ks = keys(frm)
            prev = seen.setdefault(sel, set())
            if prev & ks and "immediateRender" not in to:
                ln = f'tl.fromTo("{sel}",{{{frm}}},{{{to},immediateRender:false}},{t});'
            prev |= ks
        out.append(ln)
    return "\n".join(out)

comp = ROOT / "compositions"
for f in comp.glob("*.html"): f.unlink()
start, hosts, island = 0.0, [], []
for s in SL:
    dur = math.ceil(s["dur"] * 2) / 2
    assert all(0 < f < dur for f in s["frags"]), (s["id"], s["frags"], dur)
    (comp / f'{s["id"]}.html').write_text(scene(s["id"], s["html"], fix_immediate(s["js"])), encoding="utf-8")
    hosts.append(f'<div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{start:g}" data-duration="{dur:g}" data-label="{s["label"]}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
    island.append({"sceneId": s["id"], "fragments": [round(start + f, 2) for f in s["frags"]], "notes": s["notes"]})
    start = round(start + dur, 2)
isl = json.dumps({"slides": island}, ensure_ascii=False, indent=1).replace("</", "<\\/")
variables = json.dumps([
    {"id": "color-ground", "type": "color", "label": "Nền", "default": GROUND},
    {"id": "color-ink", "type": "color", "label": "Chữ", "default": INK},
    {"id": "color-accent", "type": "color", "label": "Màu nhấn", "default": ACC}], ensure_ascii=False)
index = f'''<!doctype html>
<html lang="vi" data-composition-variables='{variables}'>
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>SCSA giải thích từ đầu</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="assets/deck-motion.js"></script>
<link rel="stylesheet" href="assets/deck.css" />
<style>
{FONTFACE}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1920px; height:1080px; overflow:hidden; background:{GROUND}; }}
</style>
</head>
<body>
<script type="application/hyperframes-slideshow+json">
{isl}
</script>
<div id="root" data-composition-id="main" data-start="0" data-duration="{start:g}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = gsap.timeline({{ paused: true }});
</script>
</body>
</html>
'''
(ROOT / "index.html").write_text(index, encoding="utf-8")
(HERE / "slides.json").write_text(json.dumps([{"n": i + 1, "id": s["id"], "label": s["label"], "title": s["title"], "notes": s["notes"], "frags": len(s["frags"])} for i, s in enumerate(SL)], ensure_ascii=False, indent=1), encoding="utf-8")
print("slides", len(SL), "total", start)

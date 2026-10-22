"""Shared helpers for the SCSA deck generator (deck v2)."""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "assets/data/scsa-data.json").read_text())
G = DATA["G"]

INK, INK2, GROUND, ACC = "#16181C", "#4B5260", "#EDEFF1", "#C2185B"
REG = ["#E8574B", "#E9B10F", "#3E9B4F", "#3F6FD8"]
REGN = ["trời", "vách núi", "rừng", "dãy xa"]
IMG = "assets/img/"

FONTFACE = "\n".join(
    f"@font-face {{ font-family:'Be Vietnam Pro'; src:url('assets/fonts/BeVietnamPro-{n}.ttf') format('truetype'); font-weight:{w}; font-display:block; }}"
    for n, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800)]
) + "\n@font-face { font-family:'JetBrains Mono'; src:url('assets/fonts/JetBrainsMono.ttf') format('truetype'); font-weight:100 800; font-display:block; }"

def rgb(c): return f"rgb({c[0]},{c[1]},{c[2]})"
def vn(x, d=1):
    s = f"{x:.{d}f}"
    return s.replace(".", ",")

# ---------------- JS tween helpers (one line each, parsed by build.fix_immediate) ----------------
def T(sel, t, frm, to, d, ease):
    return f'tl.fromTo("{sel}",{frm},{{{to[1:-1]},duration:{d},ease:"{ease}"}},{t});'
def PLACE(sel, t, d=0.8):  # a print laid on the wall
    return T(sel, t, '{opacity:0,y:28,scale:0.985}', '{opacity:1,y:0,scale:1}', d, "expo.out")
def BLUR(sel, t, d=0.18):  # whole element blurs in
    return T(sel, t, '{opacity:0,filter:"blur(8px)"}', '{opacity:1,filter:"blur(0px)"}', d, "power2.out")
def WORDS(cls, t, gap=0.067):  # per-word blur in
    return f'tl.fromTo(".{cls}",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:0.13,ease:"power2.out",stagger:{gap}}},{t});'
def INK_IN(cls, t, gap=0.08):  # per-word from light grey to ink
    return f'tl.fromTo(".{cls}",{{color:"#B9BEC6"}},{{color:"{INK}",duration:0.25,ease:"power1.out",stagger:{gap}}},{t});'
def FADE(sel, t, d=0.35, a=0, b=1, ease="power2.out"):
    return T(sel, t, f'{{opacity:{a}}}', f'{{opacity:{b}}}', d, ease)
def DRAW(sel, t, d=0.5, L=2000, ease="power2.inOut"):
    return T(sel, t, f'{{strokeDasharray:{L},strokeDashoffset:{L}}}', '{strokeDashoffset:0}', d, ease)
def GROW_X(sel, t, d=0.6, a=0, b=1, ease="expo.out"):
    return T(sel, t, f'{{scaleX:{a},transformOrigin:"0% 50%"}}', f'{{scaleX:{b}}}', d, ease)
def GROW_Y(sel, t, d=0.6, a=0, b=1, ease="expo.out"):
    return T(sel, t, f'{{scaleY:{a},transformOrigin:"50% 100%"}}', f'{{scaleY:{b}}}', d, ease)
def WIPE(sel, t, d=0.9, ease="power2.inOut", frm="inset(0% 100% 0% 0%)"):
    return T(sel, t, f'{{clipPath:"{frm}"}}', '{clipPath:"inset(0% 0% 0% 0%)"}', d, ease)
def MOVE(sel, t, fx, fy, tx, ty, d=0.7, ease="power2.inOut"):
    return T(sel, t, f'{{x:{fx},y:{fy}}}', f'{{x:{tx},y:{ty}}}', d, ease)
def HIDE(sel):  # start hidden; a later tween reveals it
    return f'tl.set("{sel}",{{opacity:0}},0);'

# ---------------- markup helpers ----------------
def words(text, cls, accent=()):
    out = []
    for w in text.split(" "):
        hit = any(w.strip(".,:;“”\"!?").lower() == a.lower() for a in accent)
        style = f' style="color:{ACC}"' if hit else ""
        out.append(f'<span class="{cls}"{style}>{w}</span>')
    return " ".join(out)

def title(sid, text, accent=(), top=108, size=66, width=1536):
    return (f'<h1 id="{sid}-title" class="t" style="top:{top}px;font-size:{size}px;width:{width}px">'
            f'{words(text, sid + "-tw", accent)}</h1>')

def line(id_, html, top, size=44, left=192, width=1536, weight=600, color=INK, align="left"):
    return (f'<p id="{id_}" class="ln" style="left:{left}px;top:{top}px;width:{width}px;font-size:{size}px;'
            f'font-weight:{weight};color:{color};text-align:{align}">{html}</p>')

def acc(t): return f'<span style="color:{ACC}">{t}</span>'

def label(id_, text, x, y, w=360, size=32, color=INK, align="left", weight=600):
    return (f'<div id="{id_}" class="lb" style="left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;'
            f'color:{color};text-align:{align};font-weight:{weight}">{text}</div>')

def leader(id_, pts, color=INK, w=3, dot=True):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    s = f'<path id="{id_}" d="{d}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
    if dot:
        x, y = pts[-1]
        s += f'<circle id="{id_}-dot" cx="{x}" cy="{y}" r="7" fill="{color}"/>'
    return s

def svg(inner, id_=None):
    i = f' id="{id_}"' if id_ else ""
    return f'<svg{i} class="ov" width="1920" height="1080" viewBox="0 0 1920 1080">{inner}</svg>'

def print_img(id_, src, x, y, w, h=None, mat=12, rot=0, fit="cover", extra=""):
    h = h or w
    r = f"rotate:{rot}deg;" if rot else ""
    return (f'<div id="{id_}" class="print" style="left:{x}px;top:{y}px;width:{w + 2*mat}px;height:{h + 2*mat}px;padding:{mat}px;{r}{extra}">'
            f'<img src="{src}" alt="" style="width:{w}px;height:{h}px;object-fit:{fit};display:block"></div>')

def tile_style(src_size, r, c, cell):
    return f"background-image:url({IMG}29_paint.jpg);background-size:{src_size}px {src_size}px;background-position:-{c*cell}px -{r*cell}px"

def tiles(prefix, src, x, y, cell, gap=0, cls=None, idx=None, extra_fn=None):
    """A G x G grid of real image tiles cut from `src` (positioned absolutely)."""
    cls = cls or prefix + "-c"
    S = cell * G
    out = []
    for i in range(G * G):
        if idx is not None and i not in idx: continue
        r, c = divmod(i, G)
        e = extra_fn(i) if extra_fn else ""
        out.append(f'<div id="{prefix}-{i}" class="{cls} tile" style="left:{x + c*(cell+gap)}px;top:{y + r*(cell+gap)}px;width:{cell}px;height:{cell}px;'
                   f'background-image:url({src});background-size:{S}px {S}px;background-position:-{c*cell}px -{r*cell}px{e}"></div>')
    return "".join(out)

def flat(prefix, colors, x, y, cell, cls=None, gap=0, extra_fn=None):
    cls = cls or prefix + "-c"
    out = []
    for i, col in enumerate(colors):
        if col is None: continue
        r, c = divmod(i, G)
        e = extra_fn(i) if extra_fn else ""
        out.append(f'<div id="{prefix}-{i}" class="{cls} tile" style="left:{x + c*(cell+gap)}px;top:{y + r*(cell+gap)}px;width:{cell}px;height:{cell}px;background:{col}{e}"></div>')
    return "".join(out)

def cell_center(i, x, y, cell, gap=0):
    r, c = divmod(i, G)
    return x + c*(cell+gap) + cell/2, y + r*(cell+gap) + cell/2

def hatch_def(pid):
    return (f'<defs><pattern id="{pid}" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="16" height="16" fill="{GROUND}" fill-opacity="0.72"/><rect width="6" height="16" fill="{INK}" fill-opacity="0.30"/></pattern></defs>')

# ---------------- colour maths for illustrative rankings ----------------
def lab(c):
    def f(v):
        v /= 255
        return ((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92
    R, Gg, B = (f(v) for v in c)
    X = (R*0.4124 + Gg*0.3576 + B*0.1805) / 0.95047
    Y = R*0.2126 + Gg*0.7152 + B*0.0722
    Z = (R*0.0193 + Gg*0.1192 + B*0.9505) / 1.08883
    h = lambda t: t ** (1/3) if t > 0.008856 else 7.787*t + 16/116
    X, Y, Z = h(X), h(Y), h(Z)
    return (116*Y - 16, 500*(X - Y), 200*(Y - Z))
def d2(a, b): return sum((p - q) ** 2 for p, q in zip(lab(a), lab(b)))

def scene(sid, markup, js, bg=GROUND):
    return f'''<template>
<style>
{FONTFACE}
#root {{ position:absolute; inset:0; background:{bg}; }}
</style>
<div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
<div class="sc">
{markup}
</div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["{sid}"] = tl;
if (window.hfPlayForward) window.hfPlayForward(tl);
</script>
</template>
'''

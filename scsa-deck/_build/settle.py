"""Move each fragment (pause point) to after every tween that started before it has finished,
so presenting never freezes a slide mid-motion. Reports tweens that would leak into the step."""
import re

TW = re.compile(r'tl\.(?:fromTo|to|from)\("([^"]+)",.*?,([\d.]+)\);$')

def intervals(js, html):
    out = []
    for ln in js.split("\n"):
        m = TW.match(ln.strip())
        if not m: continue
        sel, t0 = m.group(1), float(m.group(2))
        ds = re.findall(r'duration:([\d.]+)', ln); d = float(ds[-1]) if ds else 0.5
        rep = re.search(r'repeat:(\d+)', ln)
        if rep: d *= 1 + int(rep.group(1))
        st = re.search(r'stagger:\{?(?:each:)?([\d.]+)', ln)
        if st:
            if sel.startswith('.'):
                n = len(re.findall(r'class="[^"]*\b' + re.escape(sel[1:]) + r'\b', html))
            else:
                n = len(re.findall(r'class="print"', html.split(f'id="{sel.split()[0][1:]}"', 1)[-1][:20000])) if ' ' in sel else 1
            d += float(st.group(1)) * max(0, n - 1)
        ease = (re.findall(r'ease:"([^"]+)"', ln) or ["power1.out"])[-1]
        # time fraction at which the tween is visually done (>= ~97% of its change)
        vis = {"expo.out": 0.6, "power3.out": 0.75, "power2.out": 0.83, "power1.out": 0.9, "back.out(1.6)": 0.85,
               "power2.inOut": 0.9, "power3.inOut": 0.88, "expo.inOut": 0.8}.get(ease, 1.0)
        dd = float(ds[-1]) if ds else 0.5
        out.append((sel, t0, t0 + (d - dd) + dd * vis))
    return out

def settle(s, slack=0.05, verbose=False):
    iv = intervals(s["js"], s["html"])
    new, issues = [], []
    for k, f in enumerate(s["frags"]):
        end = max([t1 for _, t0, t1 in iv if t0 < f] + [f - slack])
        f2 = round(max(f, end + slack), 2)
        nxt = s["frags"][k + 1] if k + 1 < len(s["frags"]) else None
        leak = [(sel, t0) for sel, t0, _ in iv if f <= t0 < f2]
        if leak or (nxt is not None and f2 >= nxt):
            issues.append((f, f2, leak))
            f2 = f  # keep authored value; needs a manual fix
        new.append(f2)
    return new, issues

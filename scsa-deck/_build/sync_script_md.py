"""Copy each slide's speaker notes (slides.json) into the "**Nói:**" block of the markdown script.
Each note line becomes one bullet: "- **label:** text" (step 0) or "- **Bấm k · label:** text".
Run from anywhere after build.py: python3 _build/sync_script_md.py"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
MD = HERE.parent.parent / "03_Script_HyperFrames_SCSA.md"
slides = json.loads((HERE / "slides.json").read_text(encoding="utf-8"))

def bullets(notes):
    out = []
    for ln in notes.split("\n"):
        head, text = ln.split(": ", 1)
        out.append(f"- **{head}:** {text}")
    return out

lines = MD.read_text(encoding="utf-8").split("\n")
res, it, n, i = [], iter(slides), 0, 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("**Nói:**"):
        res.append("**Nói:**")
        res.append("")
        res.extend(bullets(next(it)["notes"]))
        n += 1
        i += 1
        while i < len(lines) and (lines[i].startswith("- ") or (lines[i] == "" and i + 1 < len(lines) and lines[i + 1].startswith("- "))):
            i += 1
        continue
    res.append(ln)
    i += 1
assert n == len(slides), (n, len(slides))
MD.write_text("\n".join(res), encoding="utf-8")
print("synced", n, "slides ->", MD.name)

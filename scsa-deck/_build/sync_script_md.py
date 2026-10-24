"""Copy each slide's speaker notes (slides.json) into the "**Nói:**" lines of the markdown script.
Run from anywhere after build.py: python3 _build/sync_script_md.py"""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
MD = HERE.parent.parent / "03_Script_HyperFrames_SCSA.md"
slides = json.loads((HERE / "slides.json").read_text(encoding="utf-8"))
lines = MD.read_text(encoding="utf-8").split("\n")
it = iter(slides)
n = 0
for i, ln in enumerate(lines):
    if ln.startswith("**Nói:** "):
        lines[i] = "**Nói:** " + next(it)["notes"].strip()
        n += 1
assert n == len(slides), (n, len(slides))
MD.write_text("\n".join(lines), encoding="utf-8")
print("synced", n, "slides ->", MD.name)

"""Compile every figure source in this folder (except slides-style.tex) and save it as a 300-dpi PNG
in proposal-defense/figures/. LaTeX auxiliary files go to a temporary folder, not the repo.

Run from the repo root:
    conda run -n thesis-engagenet python -I proposal-defense/figures/src/build_tex.py [name ...]
"""
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
names = sys.argv[1:] or [p.stem for p in sorted(SRC.glob("*.tex")) if p.stem != "slides-style"]

failed = []
with tempfile.TemporaryDirectory() as tmp:
    for name in names:
        r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={tmp}", f"{name}.tex"],
                           cwd=SRC, capture_output=True, text=True)
        pdf = Path(tmp) / f"{name}.pdf"
        if r.returncode != 0 or not pdf.exists():
            log = (Path(tmp) / f"{name}.log")
            tail = log.read_text(encoding="latin-1")[-1500:] if log.exists() else r.stdout[-1500:]
            print(f"FAILED {name}\n{tail}")
            failed.append(name)
            continue
        overfull = (Path(tmp) / f"{name}.log").read_text(encoding="latin-1").count("Overfull")
        subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", str(pdf), str(OUT / name)], check=True)
        print(f"ok {name}.png" + (f"  ({overfull} overfull boxes)" if overfull else ""))
sys.exit(1 if failed else 0)

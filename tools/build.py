#!/usr/bin/env python3
"""Arma index.html (archivo único, listo para GitHub Pages) inyectando el maestro de estándares."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src/index.template.html").read_text(encoding="utf-8")
std = json.loads((root / "data/estandares.json").read_text(encoding="utf-8"))
out = tpl.replace("__SEED_STD__", json.dumps(std, ensure_ascii=False, separators=(",", ":")))
(root / "index.html").write_text(out, encoding="utf-8")
print("index.html", len(out)//1024, "KB,", len(std), "estándares")

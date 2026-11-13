#!/usr/bin/env python3
"""Arma index.html (archivo único, listo para GitHub Pages) inyectando el maestro de estándares."""
import json, pathlib, base64
root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src/index.template.html").read_text(encoding="utf-8")
std = json.loads((root / "data/estandares.json").read_text(encoding="utf-8"))
def uri(f): return "data:image/png;base64," + base64.b64encode((root / "assets" / f).read_bytes()).decode()
tpl = (tpl.replace("__ICONO__", uri("icono-planillas.png")).replace("__LOGO_ESC__", uri("logo-escorial.png"))
          .replace("__LOGO_SPE__", uri("logo-spe.png")).replace("__FAVICON__", uri("favicon.png")))
out = tpl.replace("__SEED_STD__", json.dumps(std, ensure_ascii=False, separators=(",", ":")))
(root / "index.html").write_text(out, encoding="utf-8")
print("index.html", len(out)//1024, "KB,", len(std), "estándares")

#!/usr/bin/env python3
"""Arma index.html (archivo único, listo para GitHub Pages) inyectando el maestro de estándares."""
import json, pathlib, base64
root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src/index.template.html").read_text(encoding="utf-8")
std = json.loads((root / "data/estandares.json").read_text(encoding="utf-8"))
for r in std: r["modelo"] = (r.get("modelo") or "").upper()
def uri(f): return "data:image/png;base64," + base64.b64encode((root / "assets" / f).read_bytes()).decode()
tpl = (tpl.replace("__ICONO__", uri("icono-planillas.png")).replace("__LOGO_ESC_AZ__", uri("logo-escorial-azul.png"))
          .replace("__LOGO_SPE__", uri("logo-spe.png")).replace("__FAVICON__", uri("favicon.png")))
API_URL = "https://br-gentle-term-bbwokq5o-plancontrol.compute.c-15.us-east-1.aws.neon.tech"
base = tpl.replace("__SEED_STD__", json.dumps(std, ensure_ascii=False, separators=(",", ":")))
# index.html = versión con base compartida (GitHub Pages); demo.html = versión local con datos de demostración
(root / "index.html").write_text(base.replace("__API_URL__", API_URL), encoding="utf-8")
(root / "demo.html").write_text(base.replace("__API_URL__", ""), encoding="utf-8")
print("index.html + demo.html", len(base)//1024, "KB,", len(std), "estándares")

#!/usr/bin/env python3
"""Genera data/seed.json a partir de las dos planillas de estándares.
Uso: python3 tools/make_seed.py Prensas_UET5.xlsx control_golpes.xlsm data/seed.json
Clave de fusión: (modelo, código, cód. operación, máquina normalizada).
A = hoja "Estandares" de Prensas_UET5 | B = hoja "Estandar" de control_golpes.
"""
import sys, json, datetime, warnings, openpyxl
warnings.filterwarnings("ignore")

def norm(m): return str(m).strip().upper().replace(' ', '') if m else ''
def s(x): return str(x).strip() if x is not None else ''

pa, pb, out = sys.argv[1:4]
A = {}
for r in openpyxl.load_workbook(pa, data_only=True)["Estandares"].iter_rows(min_row=3, values_only=True):
    if r[1] and isinstance(r[5], (int, float)):
        A[(s(r[0]), s(r[1]), s(r[3]), norm(r[4]))] = dict(
            comp=s(r[2]), std=round(r[5], 2),
            fecha=r[7].date().isoformat() if isinstance(r[7], datetime.datetime) else None)
B = {}
for r in openpyxl.load_workbook(pb, data_only=True)["Estandar"].iter_rows(min_row=3, values_only=True):
    if r[1] and isinstance(r[7], (int, float)):
        B[(s(r[0]), s(r[1]), s(r[3]), norm(r[5]))] = dict(
            comp=s(r[2]), opn=s(r[4]), ppu=r[6], std=round(r[7], 2))

rows = []
for k in sorted(set(A) | set(B), key=lambda k: (k[3], k[1], k[2], k[0])):
    a, b = A.get(k), B.get(k)
    row = dict(modelo=k[0], codigo=k[1], op=k[2], maq=k[3],
               comp=(a or b)['comp'], opn=(b or {}).get('opn', ''), ppu=(b or {}).get('ppu'),
               fecha=(a or {}).get('fecha'), validado=False, stdAlt=None)
    if a and b:
        row['std'] = a['std']
        if abs(a['std'] - b['std']) > 0.5:
            row.update(estado='conflicto', src='AB', stdAlt=b['std'])
        else:
            row.update(estado='ok', src='AB')
    elif a:
        row.update(std=a['std'], estado='unica', src='A')
    else:
        row.update(std=b['std'], estado='unica', src='B')
    rows.append(row)
for i, r in enumerate(rows, 1): r['id'] = f"S{i:03d}"
json.dump(rows, open(out, 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(rows), "estándares |", dict(Counter(r['estado'] for r in rows)), "|", dict(Counter(r['maq'] for r in rows)))

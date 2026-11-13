# PlanillasdeControl · UET 5 · Escorial

App unificada que reemplaza tres planillas de la UET 5 (línea de prensas): `Seguimiento_de_perdidas_OA`, `control_golpes` y `Prensas_UET5`.

**Una sola carga por turno y máquina → tres salidas**: golpes vs. estándar, OA / pérdidas, e informe diario para el gerente industrial.

## Estado: v1 (demo funcional)
- Archivo único `index.html` (se publica tal cual en GitHub Pages). Guarda en el navegador (`localStorage`); la base compartida llega con el repo [PlanillasdeControlAPI](../PlanillasdeControlAPI).
- **Carga de cierre**: fecha, turno, supervisor (legajo + nombre), 11 máquinas, tramos de producción (el STD sale del maestro) y paradas con catálogo de causas.
- **Informe diario**: KPIs con semáforo (metas OA 90 / Rend. 95 / Calidad 98), golpes reales vs. teóricos, OA por máquina, tendencia con bandas, radar, donut y Pareto de causas; imprimible.
- **Ingeniería · Maestro**: estándares editables (96, fusión de las dos planillas, con conflictos marcados y botones "Usar B / Mantener A"), máquinas y catálogo de causas.
- Los datos que trae al abrir por primera vez son **de demostración (simulados)**; se borran desde el banner.

## Definiciones de cálculo
- Carga = minutos netos del turno (485). Máquinas *No programada* o *Fuera de servicio* no entran en la carga.
- Disponibilidad = minutos de producción / carga. Rendimiento = golpes reales / golpes teóricos (minutos × STD / 60). **OA = Disponibilidad × Rendimiento** (sin calidad). OEE = OA × Calidad.
- El estándar se guarda en cada tramo al cargarlo: cambiar el maestro no reescribe el historial.

## Maestro de estándares
`data/estandares.json` se generó con `tools/make_seed.py` a partir de `Prensas_UET5.xlsx` (A) y `control_golpes.xlsm` (B), con clave modelo + código + operación + máquina: 96 filas (36 coinciden, 13 con STD distinto, 47 en una sola planilla).

## Desarrollo
```
python3 tools/make_seed.py Prensas_UET5.xlsx control_golpes.xlsm data/estandares.json   # opcional
python3 tools/build.py                                                                  # src/index.template.html -> index.html
```
Editar siempre `src/index.template.html`, no `index.html`.

Desarrollado por Mgter. Diego Ortiz — Líder de Mejora Continua | Consultor ISO

---
description: Evalúa si se cumple el criterio de avance de una fase
argument-hint: F0 | F1 | F2 | F3 | F4 | F5
---

Evaluá la compuerta de la fase $ARGUMENTS según `gestion/GUIA.md`, sección 4.

1. Listá cada criterio de la compuerta.
2. Para los verificables con código, correlos (`scripts/check_ids.py`, búsqueda de marcadores `[[` en `tesis/`, existencia de archivos en `evidencia/`).
3. Para el resto, delegá: `auditor-coherencia` (coherencia), `verificador-citas` (citas de los capítulos involucrados) y `revisor-tribunal` (argumentación). Si Tomás lo indica, pedile al revisor que trabaje con Opus (o hacé la revisión en el chat de claude.ai).
4. Escribí `gestion/revisiones/compuerta-$ARGUMENTS-AAAA-MM-DD.md` con una tabla criterio | cumple (sí / no / parcial) | evidencia | qué falta.
5. Recomendá: pasa / pasa con condiciones / no pasa. **La decisión final es de Tomás**; no cambies la fase en el tablero.

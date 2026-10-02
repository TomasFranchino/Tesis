---
description: Ejecuta una tarea del tablero delegándola al subagente correspondiente
argument-hint: T-xxx [instrucciones adicionales]
---

Ejecutá la tarea $ARGUMENTS del tablero siguiendo el protocolo del orquestador de `CLAUDE.md`:

1. Confirmá que no estás en `main`. En local, usá la rama `sesion/<fecha de hoy>` (creala desde `main` si no existe); en una sesión en la nube, usá la rama que creó la sesión.
2. Leé la fila de la tarea en `gestion/TABLERO.md`. Si depende de algo no terminado o requiere una decisión no tomada, detenete y explicalo.
3. Armá el brief para el subagente: objetivo, archivos de entrada con ruta exacta, archivo de salida, criterio de cierre, extensión máxima, y la instrucción de devolver un resumen de ≤ 250 palabras.
4. Delegá al subagente indicado en la tarea.
5. Al volver: revisá `git diff`, corré `python scripts/check_ids.py` si se tocaron `insumos/` o `tesis/`, y hacé un commit `[T-xxx][agente] …`.
6. Actualizá la fila en el tablero a `en revisión` y agregá las tareas nuevas que haya propuesto el subagente, en estado `propuesta`.
7. Mostrale a Tomás: qué cambió (archivos y resumen del diff), marcadores `[[…]]` nuevos y qué tiene que revisar o decidir.

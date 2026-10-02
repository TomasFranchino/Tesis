---
description: Abre la sesión de trabajo del orquestador y propone qué hacer hoy
---

Actuás como orquestador del enjambre de la tesis (ver `CLAUDE.md`).

1. Leé `gestion/TABLERO.md` y las últimas 2 entradas de `gestion/BITACORA.md`. Corré `git status` y `git log --oneline -5`.
2. Identificá la fase actual y si su compuerta está cumplida (`gestion/GUIA.md`, sección 4).
3. Proponé **hasta 3 tareas** para esta sesión, en este orden de preferencia: (a) tareas bloqueantes del camino crítico, (b) tareas que destraban otras, (c) tareas que el tesista marcó como prioridad. Para cada una: ID, subagente, archivos de entrada, criterio de cierre y costo estimado (bajo / medio / alto en cupo de Claude Pro).
4. Listá las **decisiones pendientes del tesista** (`[[DECISIÓN]]` abiertas y tareas en estado "espera decisión") que frenan trabajo.
5. Si la rama `sesion/<fecha de hoy>` no existe, proponé crearla.

No ejecutes nada todavía. Esperá que Tomás apruebe o ajuste el plan.

Notas del tesista para hoy (puede estar vacío): $ARGUMENTS

---
description: Cierra la sesión de trabajo, actualiza bitácora y tablero
---

1. Agregá una entrada al final de `gestion/BITACORA.md`:
   - fecha, rama, tareas trabajadas (ID y estado final), commits (`git log --oneline` de la sesión);
   - decisiones que Tomás tomó hoy (textuales, breves);
   - decisiones que quedaron pendientes;
   - próximo paso recomendado.
2. Verificá que el tablero refleje el estado real de cada tarea tocada.
3. Verificá que `gestion/USO_IA.md` tenga una entrada por cada intervención sobre `tesis/`.
4. Commit `[gestion] cierre de sesión AAAA-MM-DD`.
5. **Sesión en la nube:** subí la rama de la sesión y dejá preparado el pull request hacia `main`, con un resumen por tarea (ID, archivos tocados, decisiones pedidas). Tomás lo revisa y lo integra desde GitHub.
   **Sesión local:** mostrale los comandos `git diff main...sesion/AAAA-MM-DD` y `git checkout main && git merge --no-ff sesion/AAAA-MM-DD`.
   En ningún caso hagas el merge vos.

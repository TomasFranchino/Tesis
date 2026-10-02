# Guía del enjambre de la tesis

1. Arquitectura · 2. Instalación · 3. Uso de Claude Pro y los créditos · 4. Fases y compuertas · 5. Prompts de arranque · 6. Prism y MCP

---

## 1. Arquitectura

### 1.1. Principio de diseño

El enjambre corre dentro de **Claude Code**, incluido en Claude Pro, y puede ejecutarse en dos lugares con la misma configuración: **sesiones en la nube** (claude.ai/code, app de escritorio o móvil, o `claude --cloud`; trabajan sobre un repositorio de GitHub y siguen corriendo con la computadora apagada) o **Claude Code local** sobre tu clon del repositorio. La sesión principal es el **orquestador**; los especialistas son **subagentes** (archivos en `.claude/agents/`), cada uno con su propia ventana de contexto, sus herramientas y su modelo. Los agentes no conversan entre sí: **se coordinan a través del repositorio**. El tablero dice qué hay que hacer, los informes en `gestion/revisiones/` dicen qué se encontró, y Git guarda cada cambio como un commit revisable.

```
                            Tomás (autor: decide, aprueba, integra a main)
                                  ▲  decisiones        │ /planificar /ejecutar /compuerta
                                  │  y revisión        ▼
                      ┌──────────────────────────────────────────────┐
                      │ ORQUESTADOR (sesión principal de Claude Code)│
                      │ lee TABLERO + BITÁCORA · arma briefs cerrados│
                      │ commit por tarea · nunca merge ni push       │
                      └──┬───────┬────────┬────────┬────────┬───────┬┘
          ┌──────────────┘       │        │        │        │       └──────────────┐
          ▼                      ▼        ▼        ▼        ▼                      ▼
   auditor-coherencia   investigador  verificador redactor  revisor-     corrector   analista-
   (Sonnet, solo lee)    -fuentes     -citas     (Sonnet)  tribunal     -estilo     evidencia
          │              (Sonnet+web) (Haiku)       │      (Sonnet/Opus) (Haiku)    (Sonnet+Bash)
          ▼                  ▼            ▼         ▼          ▼            ▼            ▼
   revisiones/          fichas/ + .bib revisiones/ tesis/  revisiones/   tesis/     evidencia/
                                                                                     resultados/
   ─────────────────────────────── repositorio Git ───────────────────────────────────────────
   Herramientas sin LLM (costo cero): check_ids.py · reorganizar_repo.py · compilar.sh
   Dónde corre: sesiones en la nube (crédito de USD 100 hasta el 04/11) o Claude Code local (cupo Pro)
   Externa opcional:                  Prism / GPT como revisor de otra familia de modelos
```

### 1.2. Roles

| Agente | Responsabilidad | Escribe en | Modelo |
|--------|-----------------|-----------|--------|
| Orquestador | Prioriza, delega, integra, mantiene tablero y bitácora | `gestion/` | El de la sesión (Sonnet por defecto) |
| `auditor-coherencia` | Contradicciones entre archivos, promesas sin respaldo, huecos | `gestion/revisiones/` | Sonnet |
| `investigador-fuentes` | Encuentra y verifica fuentes; fichas; registro de búsquedas | `bibliografia/` | Sonnet |
| `verificador-citas` | Coteja cada afirmación contra las fichas | `gestion/revisiones/` | Haiku |
| `redactor` | Convierte insumos y decisiones en prosa de la memoria | `tesis/` | Sonnet, esfuerzo alto |
| `revisor-tribunal` | Critica argumentación, metodología y validez | `gestion/revisiones/` | Sonnet; Opus en compuertas |
| `corrector-estilo` | Ortografía, registro, terminología | `tesis/` | Haiku |
| `analista-evidencia` | Scripts de análisis y tablas de resultados reproducibles | `evidencia/`, `scripts/analisis/` | Sonnet |

La separación entre quien escribe (redactor) y quien critica (revisor, verificador, auditor) es deliberada: un agente que revisa su propio texto tiende a aprobarlo.

### 1.3. Flujo de una tarea

1. `/planificar` → el orquestador propone hasta 3 tareas; Tomás aprueba.
2. `/ejecutar T-xxx` → brief cerrado al subagente → cambio → `check_ids.py` → commit `[T-xxx][agente]` → tarea "en revisión".
3. Tomás revisa el diff (en la nube, como pull request en GitHub; en local, en VS Code o con `git diff main...sesion/fecha`), responde los `[[DECISIÓN]]` y marca "hecha".
4. `/cerrar-sesion` → bitácora, tablero y registro de uso de IA actualizados.
5. Al cerrar una fase: `/compuerta Fx` y, si Tomás aprueba, merge a `main` (lo hace Tomás).

Evitar duplicación: una tarea tiene un solo dueño en el tablero; el orquestador no delega una tarea "en curso" o "en revisión"; los informes quedan fechados y el auditor los lee antes de repetir un análisis.

---

## 2. Instalación paso a paso

**Requisitos:** Git, una cuenta de GitHub vinculada a Claude, Python 3.10+ y, para compilar la memoria en tu equipo, Pandoc. Node.js 18+ solo si además vas a usar Claude Code local.

1. **Subir el repositorio a GitHub como privado.** El crédito de USD 100 solo se aplica a sesiones en la nube, y esas sesiones trabajan sobre un repositorio de GitHub. Creá un repositorio **privado** (contiene trabajo inédito y, más adelante, datos del corpus) y subí tu repo local: `git remote add origin <url>` y `git push -u origin main`.
2. **Copiar el kit en la raíz del repositorio:** `CLAUDE.md`, `.claude/`, `gestion/`, `scripts/`, `bibliografia/`, `.gitignore` y `LEEME_ENJAMBRE.md`. Commit `[setup] kit del enjambre` y push.
3. **Reorganizar** en tu equipo (es un cambio delicado, conviene verlo): `python scripts/reorganizar_repo.py` muestra el plan; si está bien, `python scripts/reorganizar_repo.py --aplicar`, commit `[T-001]` y push.
4. **Primer control sin costo:** `python scripts/check_ids.py --salida gestion/revisiones/ids.md`. Debe mostrar las colisiones A1–A5 y SP1–SP4 sin definir (tareas T-002 y T-003).
5. **Abrir la primera sesión en la nube** desde claude.ai/code (o la pestaña Code de la app), eligiendo el repositorio. La sesión lee `CLAUDE.md` y `.claude/` desde el repo. Primer mensaje: `Listá los subagentes y comandos que tenés disponibles en este repositorio.` Tienen que aparecer los 7 subagentes y los 4 comandos.
6. **Revisar el resultado como pull request** en GitHub: la sesión trabaja en su propia rama y vos integrás a `main`.
7. **Claude Code local (opcional):** instalalo según <https://code.claude.com/docs>, entrá con tu cuenta de Claude y verificá que la variable `ANTHROPIC_API_KEY` **no** esté definida en tu sistema; si lo está, Claude Code factura a la API en lugar de usar tu plan. Después de cada sesión en la nube: `git pull`.
8. **Modelos:** si tu plan no permite elegir Opus para un subagente, dejá `revisor-tribunal` en Sonnet y hacé las revisiones de compuerta con Opus en el chat de claude.ai (por ejemplo, en el Proyecto de la tesis, subiendo los capítulos).

---

## 3. Uso de Claude Pro y del crédito de USD 100

### 3.1. Cómo funciona el crédito

- Se aplica **solo a sesiones de Claude Code en la nube**, no a Claude Code local, ni al chat, ni a Proyectos.
- Las sesiones en la nube lo gastan **primero y de forma automática**; cuando se agota o vence, pasan a consumir el cupo normal de Pro, sin cargos extra.
- **Vence el 04/11/2026** (05/11, 4:59 h de Argentina). Lo que no se use se pierde.

Esto da vuelta la estrategia: el crédito es un recurso que vence en cinco semanas, mientras que el cupo de Pro se renueva. **Hasta el 4 de noviembre, todo el trabajo agéntico pesado va a la nube**, y el cupo de Pro queda para el chat y para tareas cortas en local.

### 3.2. Cuánto rinde

El crédito se descuenta según los tokens que consume cada sesión, y una sesión agéntica reenvía su contexto en cada turno. No hay forma confiable de estimar el costo por sesión sin medirlo, así que la regla es **calibrar en la primera semana**: anotá en la bitácora el saldo antes y después de las 3 primeras sesiones y calculá el costo promedio por tipo de tarea. Con ese dato, ajustá el plan semanal (3.4).

Lo que más estira el crédito:

- **Modelo según la tarea:** Haiku para verificar citas y estilo, Sonnet para investigar, redactar y programar, Opus solo para compuertas. Opus cuesta aproximadamente el doble que Sonnet por token, y Haiku la mitad.
- **Sesiones largas y autónomas, con brief cerrado.** La nube conviene para tareas que corren solas mucho tiempo (verificar las 10 correcciones del estado del arte, auditar todo el repositorio, implementar el motor de reglas con su suite de pruebas). Las conversaciones de ida y vuelta para pulir un párrafo rinden mejor en el chat.
- **Una sesión por bloque de tareas relacionadas**, no una por tarea: el costo de cargar el contexto inicial se paga una vez.
- **Lo verificable con código, con código:** `check_ids.py` antes de cualquier auditoría.
- **`archivo/` bloqueado** para lectura: no contamina ni consume.

### 3.3. Reparto recomendado: priorizar el camino crítico

El cuello de botella de la tesis es la evidencia, no el texto. N2 (motor de reglas) y N3 (emulador) son ideales para un agente: están especificados en requisitos y ADR, son deterministas y tienen una suite de aceptación concreta (E01–E12). Por eso, si el prototipo está en un repositorio de GitHub, conviene que reciba la mayor parte del crédito.

| Destino | Proporción | Qué incluye |
|---------|:----------:|-------------|
| Prototipo (otro repositorio) | ~50 % | Esquema JSON del flujo, esqueleto del monolito modular, N2 + N3 con E01–E12 y pruebas basadas en propiedades, scripts de captura con Playwright |
| Tesis: F0 y F1 | ~25 % | Reorganización, identificadores, verificación de fuentes, reformulación de SP2 (LLM local), mapeo de patrones, antecedentes nacionales |
| Tesis: F2 (borradores de capítulos 1–3) | ~15 % | Redacción y verificación de citas |
| Reserva final | ~10 % | Últimos días antes del vencimiento: tribunal con Opus sobre todo lo escrito, verificación de citas completa |

El código generado con ayuda de agentes también se registra en `gestion/USO_IA.md`: la declaración de uso de IA de la memoria debe cubrir el prototipo, no solo el texto.

### 3.4. Plan hasta el vencimiento

| Semana | Tesis (este repositorio) | Prototipo |
|--------|--------------------------|-----------|
| 2–8 oct | F0 completa; calibrar costo por sesión | Subir a GitHub; esquema JSON (T-030) |
| 9–15 oct | F1: T-011 (SP2 con LLM local), T-019 (ADR-07), T-012 (patrones), T-015 (antecedentes) | Esqueleto del monolito; N2 con E01–E12 |
| 16–22 oct | Esqueleto de `tesis/`; capítulo 2 | N3 y pruebas basadas en propiedades |
| 23–29 oct | Capítulos 1 y 3 | Integración N2–N3; scripts de captura |
| 30 oct–4 nov | Compuerta F1/F2 con Opus; verificación de citas completa | Lo que quede del crédito |

Desde el 5 de noviembre las sesiones en la nube y las locales comparten el cupo de Pro. Ahí conviene volver a sesiones más cortas.

### 3.5. Hábitos que rinden el cupo de Pro

- Sesiones de hasta 3 tareas; `/clear` entre tareas no relacionadas.
- Briefs con rutas exactas: un subagente que "explora el repositorio" gasta diez veces más.
- `CLAUDE.md` corto; nada de pegar documentos enteros en él.
- Usar el chat de claude.ai para discutir decisiones (B1, B3) antes de pedirle a un agente que las aplique.

---

## 4. Fases y compuertas

Las fases 2 y 3 corren **en paralelo**: mientras el enjambre redacta los capítulos 1 a 3, vos avanzás corpus y prototipo.

| Fase | Objetivo | Compuerta (todo debe cumplirse) |
|------|----------|---------------------------------|
| **F0 Saneamiento** (~1 semana) | Repositorio ordenado y fuentes verificadas | Repositorio reorganizado · `check_ids.py` sin referencias rotas ni colisiones · correcciones de *Estado del arte* §7 aplicadas · `referencias.bib` con ficha para cada fuente ya citada · cada archivo de `insumos/` con cabecera de estado y versión |
| **F1 Decisiones abiertas** (~1–2 semanas; coincide con la Entrega 2) | Que no quede nada estructural por decidir | B1, B2 y B3 del diagnóstico resueltos y registrados · subconjunto de 7 patrones mapeado a las taxonomías · SP2 reformulada con LLM local (Ollama) y ADR-07 recalculado · índice de la memoria validado con el profesor · `revisor-tribunal` (Opus) sobre `insumos/` sin BLOQUEANTES |
| **F2 Capítulos 1–3 y anexos metodológicos** | Mitad teórica y metodológica entregable | Capítulos 1–3 en `tesis/` · verificador: 0 SIN CITA y 0 SIN RESPALDO · tribunal sin BLOQUEANTES · solo quedan marcadores `[[RESULTADO PENDIENTE]]` · justificación y contribución reescritas por Tomás con su voz · guía de etiquetado lista |
| **F3 Evidencia** (camino crítico) | Resultados reales y reproducibles | Corpus capturado y versionado · kappa calculado sobre ≥ 30 % · suite E01–E12 al 100 % · V1 ejecutado sobre el conjunto de prueba · V3, V4 y V5 ejecutados · todo resultado en `evidencia/resultados/` con metadatos · un comando reproduce el análisis |
| **F4 Capítulos 4–6** | Mitad empírica entregable | Toda cifra con `<!-- fuente: evidencia/… -->` · la discusión responde SP1–SP4 y la pregunta principal de forma explícita · limitaciones y amenazas a la validez actualizadas con lo ocurrido · tribunal sin BLOQUEANTES |
| **F5 Versión final** | Documento listo para entregar | `compilar.sh` sin marcadores `[[` · resumen y *abstract* · formato de la facultad · revisión completa con Opus y, opcionalmente, con un modelo de otra familia · declaración de uso de IA desde `USO_IA.md` · lectura completa de Tomás de principio a fin |

**Métrica de progreso** (la reporta `/planificar`): tareas hechas por fase, marcadores `[[…]]` abiertos en `tesis/` por tipo, y estado de cada criterio de la compuerta actual. Es más honesto que un porcentaje por capítulo.

---

## 5. Prompts de arranque

Primera sesión en la nube (F0):

```
/planificar Empezamos F0. T-001 ya está hecha en local. Prioridad: T-003, T-004 y T-006.
Anotá en la bitácora el saldo del crédito al empezar: USD <saldo>.
```

```
/ejecutar T-004
```

Invocación directa de un subagente, sin pasar por el tablero:

```
Usá el subagente investigador-fuentes. Verificá una por una las 10 correcciones de
insumos/Estado del arte comparativo.md §7. Para cada una: abrí la fuente primaria,
creá la ficha y decime si la corrección propuesta es correcta, está incompleta o es errónea.
No edites 1.1 todavía.
```

```
Usá el subagente revisor-tribunal sobre insumos/Contribucion y alcance.md e
insumos/Definicion de problema.md. Enfocate en si el mecanismo (rechazar cobros)
resuelve los daños que enumera el problema, considerando contratos con permanencia.
```

Sesión larga y autónoma (ideal para la nube):

```
Ejecutá en orden T-006 y T-007 con investigador-fuentes, y después T-012.
Al terminar cada tarea, commit. Al final, /cerrar-sesion y dejá el pull request listo.
No me consultes salvo que aparezca una decisión de las marcadas en CLAUDE.md.
```

---

## 6. Prism y MCP

**Qué aporta Prism acá.** Prism es el espacio de escritura científica de OpenAI, basado en LaTeX y con GPT integrado. Para esta tesis tiene dos usos razonables: (1) **revisor de otra familia de modelos** en las compuertas F2 y F5, porque un modelo distinto tiene puntos ciegos distintos; (2) **maquetación**, solo si la facultad acepta un PDF desde LaTeX (`pandoc` convierte la memoria a `.tex`). No conviene que redacte ni que escriba en el repositorio: la fuente de verdad son los `.md` y dos editores con escritura sobre el mismo texto generan conflictos.

**Cómo conectarlo.** No pude confirmar documentación pública de un servidor MCP de Prism. Si el tuyo expone una URL MCP, se agrega al proyecto con:

```
claude mcp add --transport http prism <URL-del-servidor> --scope project
```

Eso crea `.mcp.json` en la raíz. Luego conviene que solo `revisor-tribunal` lo use (campo `mcpServers` del subagente) y que sus respuestas se guarden como `gestion/revisiones/prism-*.md`. Si la conexión funciona en sentido inverso (desde Prism/ChatGPT hacia tus archivos), el flujo es manual: exportás el capítulo compilado, pedís la revisión allá y guardás el resultado en `gestion/revisiones/`.

**Otros MCP.** Claude Code ya trae búsqueda y lectura web, suficientes para el investigador. Un MCP de gestor bibliográfico (por ejemplo, Zotero) vale la pena solo si ya usás ese gestor.

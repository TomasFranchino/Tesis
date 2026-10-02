# Bitácora

Una entrada por sesión (la escribe `/cerrar-sesion`). Las decisiones de Tomás se registran acá con fecha: son la memoria del proyecto.

---

## 2026-09-30 — Diagnóstico inicial

- Diagnóstico completo en `gestion/DIAGNOSTICO.md`.
- `check_ids.py`: colisión A1–A5 (aportes vs. antecedentes) y SP1–SP4 usadas sin definir.
- Instalado el kit del enjambre. Fase actual: F0.
- Recursos: Claude Pro + crédito de USD 100 para sesiones de Claude Code en la nube (vence el 04/11/2026). Sin acceso a API por clave.
- **Decisiones pendientes de Tomás:** nomenclatura para resolver A1–A5 (T-002); postura sobre rechazo de cobro vs. obligación contractual (T-010); fecha de entrega; formato y norma de citación.
- **Próximo paso:** T-001, T-003, T-004.

---

## 2026-10-02 — Decisiones de Tomás (sesión de aplicación de decisiones)

Registradas antes de aplicarlas. Referencias B1 y B2: `gestion/DIAGNOSTICO.md` §3.1.

- **B1 (T-010) — se aplican las tres opciones del diagnóstico:**
  - (a) Alcance limitado a **suscripciones digitales pagadas con tarjeta y sin permanencia mínima**, incluidas las **pruebas gratuitas**.
  - (b) La **definición del problema se limita a los daños que el mecanismo previene**; el resto pasa a contexto y limitaciones.
  - (c) **Alerta previa a la contratación** cuando se detecta permanencia o costos ocultos.
- **B2 (T-011) — Jev (TypeSafe AI) queda excluido.** SP2 compara un **LLM local (Ollama)** contra la **línea base heurística**.
- **Formato de entrega:** Word (.docx).
- **Norma de citación:** IEEE.
- **Fecha final de entrega:** no hay.
- **Reglamento de la facultad sobre uso de IA:** no se conoce ninguno.
- **Código (prototipo):** todavía no hay.

---

## 2026-10-02 — Cierre: aplicación de decisiones B1 y B2

- **Rama:** `claude/focused-keller-417zss` (sesión en la nube).
- **Tareas trabajadas (estado final):**
  - T-001 reorganización del repositorio → en revisión.
  - T-010 B1 aplicado en `insumos/` → en revisión.
  - T-011 (reformulada: "Retirar Jev y reformular SP2") → en revisión.
  - T-019 (nueva: "Recalcular ADR-07 sin Jev") → en revisión. Tabla 7.5: S1 4,00 · S2 4,05 · **S3 4,40** · S4 4,35. **Ganador sin cambio (S3)**, pero la ventaja sobre S4 bajó de 0,20 a 0,05: con K2(S4) = 5 ganaría S4. La tabla 7.6 (sensibilidad) quedó como `[[RESULTADO PENDIENTE]]` (T-016).
  - T-028 (nueva: bloque de condiciones de contratación en el esquema A1) → pendiente.
  - Otros: CLAUDE.md con norma IEEE; `scripts/compilar.sh` usa `bibliografia/ieee.csl` (estilo oficial del repositorio CSL, CC BY-SA 3.0, agregado al repo); GUIA sin menciones a Jev.
- **Commits:** `3d132e8` T-001 · `491ada6` decisiones y norma IEEE · `afbfc15` tablero · `177769c` T-010 redactor · `af4316b` T-011/T-019 redactor · `d35389a` auditoría · cierre.
- **Verificaciones:** `check_ids.py` sin hallazgos nuevos (siguen SP1–SP4 sin definir → T-003 y colisión A1–A5 → T-002). Sin menciones a Jev/TypeSafe/"decisión estructurada" en contenido fuera de `archivo/` (solo en registros de `gestion/`).
- **Decisiones de Tomás hoy:** B1 (a)(b)(c); B2 (Jev excluido, SP2 = LLM local con Ollama vs. línea base heurística); entrega en Word; citas IEEE; sin fecha final; sin reglamento de IA conocido; sin código. Detalle en la entrada anterior.
- **Decisiones pendientes (nuevas):**
  - **BLOQUEANTE (auditoría):** RF-28 (alerta previa) analiza flujos de **alta**, pero el corpus, A1/A3 y OE2 son de flujos de **cancelación**. ¿Se amplía el corpus a flujos de alta, o la alerta queda fuera de la validación empírica?
  - Objetivo general y OE1–OE3 (`Objetivos.md`) no reflejan el alcance acotado ni la alerta previa: ¿se actualizan?
  - Prioridad de RF-28 (M o S; recomendación del redactor: M).
  - Modelo y tamaño del LLM local; hardware de ejecución; umbral de latencia con LLM local; repeticiones de la evaluación.
  - ADR-07: puntaje de K2 para S4 (Kotlin), que define el ganador; descarte de C# (motivo anterior caducó).
  - 1.1 Antecedentes: frases sobre DAZN y Telecentro (A eliminar / B reformular con la alerta previa; recomendación B).
  - Definición de problema: ubicación del costo de oportunidad y del impacto emocional (hoy en "contexto y limitaciones").
  - Aclarar el alcance de "sin código" (se registró como "todavía no hay prototipo").
- **Próximo paso recomendado:** Tomás revisa el PR y responde los pendientes; luego T-003 (etiquetar SP1–SP4), T-016 (recalcular sensibilidad del ADR-07, con fichas de Ollama por T-006) y T-028.

---

## 2026-10-02 — Segunda parte: decisiones sobre los pendientes del PR #1

El PR #1 fue integrado por Tomás. Esta parte se trabajó sobre la misma rama mediante la API de GitHub, sin comandos locales (indicación de Tomás).

- **Decisiones de Tomás (textuales, resumidas):**
  - **Bloqueante de RF-28:** "El patrón de *sneaking* (permanencia oculta) siempre debe quedar registrado por obligación legal en el correo de confirmación de la suscripción. Al hacer que el módulo de IA analice ese correo inicial, se mantiene el alcance técnico dentro de lo factible (parseo de emails con el LLM local) y se cierra el ciclo del producto: se detecta la trampa contractual en el alta y se previene el cobro abusivo en la baja mediante la tarjeta virtual."
  - **`Objetivos.md`:** se autoriza su actualización.
  - **"Sin código":** el prototipo todavía no existe; Tomás está abierto a que se proponga arrancarlo cuando sea necesario.
- **Aplicado** (commit `b03c629`): Objetivos v2.0 (vigente), Contribución v0.4, Requisitos v1.2 (RF-28 sobre el correo de confirmación; RNF-04 cubre los correos), Plan v1.2 (corpus de correos, §2.5 validación de la alerta, amenaza de pocos positivos). Tablero: T-028 reformulada, T-029 nueva, T-031 y T-033 ajustadas.
- **Observaciones del orquestador, dejadas como marcadores en los insumos:**
  - La obligación legal invocada no tiene ficha: `[[CITA PENDIENTE]]` en Contribución §5.2 → T-029. Si la norma no existe o no alcanza a todos los servicios, el argumento cambia.
  - El correo de confirmación llega **después** del alta, por lo que la alerta deja de ser "previa a la contratación" (B1 c): `[[DECISIÓN]]` en Contribución §5.2 (A: alerta temprana vinculada al derecho de revocación; B: conservar también el análisis del flujo de alta). Recomendación: A. En los insumos se usó el nombre neutro "alerta de permanencia o costos ocultos".
  - Forma de ingreso del correo: `[[DECISIÓN]]` en Contribución §5.1 (A: importación manual; B: IMAP/Gmail API). Recomendación: A.
  - Umbral de la alerta y correos adicionales con permanencia documentada: `[[DECISIÓN]]` en Plan §2.5 y §9.
- **Propuesta sobre el prototipo:** arrancarlo al cerrar T-028 y T-030 (esquema A1), porque el esquema define la estructura de datos de todos los módulos. Se registró en T-033.
- **No verificado en esta parte:** `check_ids.py` no se ejecutó (sin comandos locales). No se introdujeron identificadores nuevos de las familias que audita; queda para la próxima sesión local. `Arquitectura.md` (ADR-02, trazabilidad de RNF-04) no menciona todavía los correos de confirmación: ajuste menor pendiente.
- **Decisiones pendientes:** momento de la alerta; forma de ingreso del correo; prioridad de RF-28; umbral de la alerta; modelo, tamaño y hardware del LLM local; K2 de S4 en ADR-07; descarte de C#; frases sobre DAZN y Telecentro en 1.1; ubicación del impacto emocional en la Definición de problema.
- **Próximo paso recomendado:** T-029 (verificar la norma) antes de cualquier redacción del capítulo 1 que use el argumento; luego T-028, T-003 y T-016.

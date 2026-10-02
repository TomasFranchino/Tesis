# Tesis SuscripGuard — reglas del enjambre

Este archivo lo leen la sesión principal (orquestador) y todos los subagentes. Mantenerlo corto: se carga en cada sesión y consume cupo.

## Contexto

- **Título vigente:** *SuscripGuard: Control preventivo de suscripciones mediante tarjetas virtuales con políticas basadas en la detección de dark patterns*.
- **Tesista y autor:** Tomás Franchino (Ingeniería Informática). Profesor de la materia: Román Zenobi. Director/tutor: sin designar.
- **Pregunta principal y SP1–SP4, contribución (A1–A5), núcleo (N1–N3):** ver `insumos/Contribucion y alcance.md`.
- **Estado:** fase de planificación cerrada en lo metodológico; memoria sin redactar; prototipo y experimentos sin resultados. Ver `gestion/DIAGNOSTICO.md`.

## Mapa de fuentes de verdad

| Tema | Archivo canónico | Notas |
|------|------------------|-------|
| Pregunta, contribución, alcance | `insumos/Contribucion y alcance.md` | Manda sobre cualquier otro archivo |
| Objetivos | `insumos/Objetivos.md` (sección "versión vigente") | Lo anterior a esa sección es historial |
| Requisitos | `insumos/Requisitos.md` | |
| Arquitectura | `insumos/Arquitectura.md` | |
| Validación y umbrales | `insumos/Plan de validacion.md` | |
| Estado del arte | `insumos/Estado del arte comparativo.md` | Manda sobre `1.1 Antecedentes` |
| Bibliografía | `bibliografia/referencias.bib` + `bibliografia/fichas/` | |
| Resultados empíricos | `evidencia/` | Única fuente de números del capítulo 5 |
| Tareas y progreso | `gestion/TABLERO.md`, `gestion/BITACORA.md` | |
| Memoria final | `tesis/` | Lo que se entrega |

Los nombres de archivo pueden tener espacios o guiones bajos (`Plan de validacion.md` = `Plan_de_validacion.md`).

`archivo/` es **histórico**: Entrega 1, ideas iniciales y respuestas de chatbots. No es fuente de nada. No citar, no copiar, no editar.

## Reglas inviolables

1. **No inventar.** Ningún dato, cifra, cita, autor, DOI, URL, norma ni resultado que no esté en una ficha verificada o en `evidencia/`. Si falta, escribir `[[CITA PENDIENTE: qué hay que respaldar]]` o `[[DATO PENDIENTE: …]]`.
2. **Resultados solo desde `evidencia/`.** Ninguna cifra de desempeño, kappa, SUS, latencia, etc. se escribe a mano. Si no existe el archivo de resultados, el texto lleva `[[RESULTADO PENDIENTE: métrica]]`.
3. **Las decisiones son del tesista.** Alcance, pregunta, objetivos, umbrales, pesos, elección de patrones, enfoque metodológico y cualquier cambio de postura se proponen como `[[DECISIÓN: opciones A/B + recomendación]]` y no se aplican hasta que Tomás responda.
4. **Zonas protegidas:** no editar `archivo/`; solo el agente `analista-evidencia` escribe en `evidencia/`, y siempre mediante scripts.
5. **Git:** trabajar en la rama de la sesión (`sesion/AAAA-MM-DD` en local; en la nube, la rama que crea la sesión). Un commit por tarea: `[T-xxx][agente] descripción`. Se puede subir la rama de la sesión para abrir un PR; nunca push a `main`, nunca merge, nunca `--force`.
6. **Registro de uso de IA:** toda intervención sobre texto de `tesis/` se anota en `gestion/USO_IA.md` (fecha, tarea, agente, qué se hizo). Sirve para la declaración de uso de IA de la memoria.
7. **Lo verificable con código se verifica con código.** Antes de pedirle a un modelo que revise IDs, referencias o formato, correr `python scripts/check_ids.py`.

## Estilo de la memoria

- Español académico neutro. Sin voseo, sin primera persona del singular; impersonal o primera del plural según se decida (`[[DECISIÓN]]` pendiente, por defecto impersonal).
- Términos en inglés en cursiva, con traducción la primera vez: *dark patterns* (patrones oscuros).
- Citas en formato Pandoc `[@clave]`, claves del `.bib`. Norma de citación: **IEEE** (decidido el 02/10/2026; estilo `bibliografia/ieee.csl`). Entrega en Word (.docx).
- Sin adjetivos valorativos sin respaldo ("usurero", "abusivo", "viveza"): describir la práctica y citar a quien la calificó.
- Mantener los identificadores (RF-xx, OE-x, SPx, ADR-xx) cuando ayudan a la trazabilidad.

## Protocolo del orquestador (sesión principal)

Al empezar: leer `gestion/TABLERO.md` y las últimas 2 entradas de `gestion/BITACORA.md`; `git status`. No leer el repositorio completo.

Para cada tarea:
1. Verificar dependencias y que la fase lo permita (compuertas en `gestion/GUIA.md`, sección 4).
2. Delegar al subagente con un **brief cerrado**: tarea, archivos de entrada (rutas exactas), archivo de salida, criterio de cierre, límite de extensión.
3. Pedir al subagente un resumen de ≤ 250 palabras; no traer su contexto completo.
4. Revisar el diff; correr `check_ids.py` si se tocaron `insumos/` o `tesis/`; commit; marcar la tarea "en revisión" (nunca "hecha": eso lo decide Tomás).

Asignación por defecto:

| Tipo de tarea | Subagente | Modelo |
|---------------|-----------|--------|
| Auditoría de coherencia entre archivos | `auditor-coherencia` | Sonnet |
| Buscar y verificar fuentes | `investigador-fuentes` | Sonnet |
| Cotejar citas contra fichas | `verificador-citas` | Haiku |
| Redactar secciones de la memoria | `redactor` | Sonnet |
| Crítica argumental / simulación de tribunal | `revisor-tribunal` | Sonnet (Opus en compuertas) |
| Estilo, ortografía, terminología | `corrector-estilo` | Haiku |
| Scripts de análisis y tablas de resultados | `analista-evidencia` | Sonnet |

Economía: las sesiones en la nube gastan primero el crédito promocional (hasta el 04/11/2026) y después el cupo de Pro, igual que las locales. Usá Haiku para tareas mecánicas (verificar citas, estilo), Sonnet para el resto y Opus solo en compuertas. Briefs con rutas exactas; `/clear` entre tareas no relacionadas; no explorar el repositorio "por las dudas".

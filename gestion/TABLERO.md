# Tablero de tareas

Estados: `propuesta` · `pendiente` · `en curso` · `en revisión` · `espera decisión` · `hecha` (solo Tomás) · `descartada`.
Fase actual: **F0 — Saneamiento**. Referencias B1–B3 e I1–I10: `gestion/DIAGNOSTICO.md`.

## F0 — Saneamiento

| ID | Tarea | Agente | Depende de | Estado | Criterio de cierre |
|----|-------|--------|-----------|--------|--------------------|
| T-001 | Reorganizar el repositorio (`scripts/reorganizar_repo.py`) | orquestador | — | pendiente | Carpetas creadas; históricos en `archivo/`; commit |
| T-002 | Resolver colisión A1–A5 aportes vs. antecedentes (I1) | redactor | T-001, decisión de nomenclatura | espera decisión | `check_ids.py` sin colisiones |
| T-003 | Etiquetar subpreguntas SP1–SP4 en Contribución §2 (I2) | redactor | T-001 | pendiente | `check_ids.py` sin referencias rotas |
| T-004 | Verificar con fuente primaria las 10 correcciones de Estado del arte §7 (I3) | investigador-fuentes | T-001 | pendiente | Ficha por corrección; veredicto por cada una |
| T-005 | Aplicar las correcciones verificadas a 1.1 Antecedentes | redactor | T-004 | pendiente | 1.1 sin datos marcados como erróneos |
| T-006 | Fichas y `.bib` para todas las fuentes ya citadas en `insumos/` | investigador-fuentes | T-001 | pendiente | Cada URL de Estado del arte §8 con ficha |
| T-007 | Reemplazar fuentes secundarias de normativa por primarias (I9) | investigador-fuentes | T-006 | pendiente | Disp. 954/2025, 3/2026 y FTC citadas desde fuente oficial |
| T-008 | Cabecera de estado y versión en cada archivo de `insumos/` | auditor-coherencia | T-001 | pendiente | Todos con "Estado: … vX.Y (fecha)" |
| T-009 | Glosario inicial (`gestion/GLOSARIO.md`) | corrector-estilo | T-001 | pendiente | ≥ 25 términos con forma preferida |

## F1 — Decisiones abiertas

| ID | Tarea | Agente | Depende de | Estado | Criterio de cierre |
|----|-------|--------|-----------|--------|--------------------|
| T-010 | Rechazo del cobro vs. obligación contractual (B1): análisis de opciones de alcance | revisor-tribunal → Tomás | F0 | pendiente | Decisión registrada en BITÁCORA y aplicada en Contribución §4 y §5.5 |
| T-011 | Verificar Jev / TypeSafe AI: documentación, SDK, tipos de pregunta ("Choice", "Noul"), límites, términos para publicar (B2) | investigador-fuentes | F0 | pendiente | Ficha por afirmación; ADR-07 K2 recalculado si cambia algo |
| T-012 | Mapear los 7 patrones a Gray 2018, Mathur 2019 y Nembaware y Sousa 2025 | investigador-fuentes | T-006 | pendiente | Tabla de mapeo con justificación de inclusión/exclusión |
| T-013 | Definición operativa de niveles de riesgo para el anotador (B3) | redactor → Tomás | T-012 | espera decisión | Criterio independiente de la fórmula del sistema |
| T-014 | Corregir la comparación de umbrales binario vs. por tipo (I4) | redactor | T-006 | pendiente | Umbrales contrastados con métricas del mismo tipo |
| T-015 | Antecedentes nacionales y locales (I7) | investigador-fuentes | F0 | pendiente | Registro de búsqueda en ≥ 4 repositorios; fichas o resultado negativo documentado |
| T-016 | Script del análisis de sensibilidad del ADR-07 (I8) | analista-evidencia | — | pendiente | Script reproduce los porcentajes de la tabla 7.6 |
| T-017 | Consultas al profesor: índice ajustado, umbrales, pesos ADR-07, enfoque del marco teórico, segundo anotador | Tomás | — | pendiente | Respuestas registradas en BITÁCORA |
| T-018 | Revisión de tribunal (Opus) sobre `insumos/` completos | revisor-tribunal | T-010 a T-014 | pendiente | Sin BLOQUEANTES |

## F2 — Capítulos 1–3 (en paralelo con F3)

| ID | Tarea | Agente | Depende de | Estado | Criterio de cierre |
|----|-------|--------|-----------|--------|--------------------|
| T-020 | Esqueleto de `tesis/` con el índice validado | redactor | T-017 | pendiente | Un archivo por capítulo con títulos |
| T-021 | Reescribir la definición del problema con fuentes (I6) | redactor | T-010, T-005 | pendiente | Sin lenguaje valorativo; cada daño citado o eliminado |
| T-022 | Justificación desde cero (I6) | redactor → Tomás | T-021 | pendiente | Borrador + reescritura de Tomás |
| T-023 | Capítulo 1 completo | redactor | T-021, T-022 | pendiente | Compuerta F2 para el capítulo |
| T-024 | Marco teórico 2.1–2.5 (I5) | investigador-fuentes + redactor | T-017 | pendiente | Compuerta F2 para el capítulo |
| T-025 | Estado del arte y brecha (2.6) | redactor | T-012, T-014, T-015 | pendiente | Compuerta F2 para el capítulo |
| T-026 | Capítulo 3 Metodología | redactor | T-017 | pendiente | Compuerta F2 para el capítulo |
| T-027 | Guía de etiquetado (anexo) | redactor → Tomás | T-012, T-013 | pendiente | Definición operativa y ejemplos ± por patrón |

## F3 — Evidencia (camino crítico; trabajo principal de Tomás)

| ID | Tarea | Agente | Depende de | Estado | Criterio de cierre |
|----|-------|--------|-----------|--------|--------------------|
| T-030 | Esquema JSON del flujo de cancelación (A1) versionado | Tomás (+ Claude Code en el repo del prototipo) | T-012 | pendiente | Esquema publicado y validado con 2 flujos |
| T-031 | Captura del corpus (15–20 servicios) | Tomás | T-030 | pendiente | Flujos en `evidencia/datos/corpus/` con fecha |
| T-032 | Anotación, segundo anotador y kappa | Tomás + analista-evidencia | T-027, T-031 | pendiente | κ por patrón calculado por script |
| T-033 | Prototipo N1–N3 y soporte | Tomás (repo del prototipo) | T-030 | pendiente | Criterios V2/V3 ejecutables |
| T-034 | Evaluación V1 a V5 y análisis | Tomás + analista-evidencia | T-032, T-033 | pendiente | Resultados en `evidencia/resultados/` con metadatos |

## F4 y F5

Se detallan al cerrar F2. Resumen: capítulos 4–6 desde `evidencia/`; preliminares; compilación; revisión final; declaración de uso de IA.

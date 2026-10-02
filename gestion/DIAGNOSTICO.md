# Diagnóstico del estado de la tesis — 30/09/2026

Base: 16 archivos `.md` (≈ 20 300 palabras) y `Entrega 1 Tesis.docx`, más una corrida de `scripts/check_ids.py`.

## 1. Lectura general

El proyecto está **metodológicamente maduro y documentalmente inmaduro**. Los documentos del 29/09 (contribución, objetivos, requisitos, arquitectura, plan de validación, estado del arte) tienen un nivel alto: trazabilidad entre subpreguntas, objetivos, requisitos y métricas, decisiones justificadas con ADR y análisis multicriterio, criterios de aceptación y amenazas a la validez. Eso es lo más difícil de una tesis y ya está hecho en borrador.

Lo que falta es de otra naturaleza:

- **La memoria no existe como texto.** Hay documentos de trabajo, no capítulos. Ningún archivo es todavía prosa entregable.
- **No hay evidencia empírica.** Corpus, prototipo, evaluación del clasificador, suite de escenarios y estudio de usabilidad están planificados pero sin resultados. Los capítulos 4 y 5 (≈ 40–50 % de la memoria) dependen de ese trabajo.
- **Conviven tres generaciones de contenido:** notas y respuestas de chatbot (Ideas, Idea seleccionada, parte de 1.1), la Entrega 1 (título, objetivos y stack ya reemplazados) y los documentos del 29/09. Sin separarlas, cualquier agente va a mezclarlas.

Consecuencia para el enjambre: **el camino crítico hacia la versión final no es la redacción sino la evidencia.** El enjambre puede dejar listos los capítulos 1 a 3 y todos los anexos metodológicos, pero no puede ni debe producir el capítulo 5.

## 2. Madurez por capítulo (índice de `Estructura del trabajo final.md`)

| Capítulo | Material disponible | Madurez | Qué falta |
|----------|--------------------|:-------:|-----------|
| Preliminares (resumen, índice) | — | 0 % | Se escriben al final |
| 1. Introducción | Contribución y alcance, Objetivos (vigente), Definición de problema (notas), Justificación (vacía) | ~40 % | Redacción; justificación desde cero; problema reescrito con fuentes |
| 2. Marco teórico | Estado del arte comparativo (v0.1, bueno); 1.1 (notas con datos a corregir) | ~30 % | 2.1 Bases teóricas y 2.3 Conceptos: inexistentes. Antecedentes nacionales/locales |
| 3. Metodología | Arquitectura (v0.2), Plan de validación (v1.0) | ~45 % | Enfoque metodológico, fases y cronograma, guía de etiquetado, aspectos éticos |
| 4. Desarrollo | Requisitos (v1.0) | ~15 % | Modelo de datos, C4/UML, esquema JSON del flujo, implementación |
| 5. Resultados | Plan de validación define qué medir | 0 % | Todo: depende de los experimentos |
| 6. Conclusiones | — | 0 % | Depende del capítulo 5 |

## 3. Hallazgos

### 3.1. Bloqueantes (un tribunal los detectaría)

**B1. Bloquear el cobro no extingue el contrato.** La tesis sostiene, en 1.1 y en la Entrega 1, que ante prácticas como las de Telecentro o DAZN el usuario "simplemente elimina la tarjeta" y evita los cobros abusivos. Pero rechazar un cobro no rescinde el contrato: en servicios con permanencia (el caso DAZN, con compromiso anual) o facturados por otros medios, el proveedor puede generar deuda, intereses y gestiones de cobranza, que son exactamente los daños que enumera *Definición de problema* (deudas infladas, acoso cobratorio, perfil crediticio). Tal como está, la solución podría agravar el problema que la motiva. Hace falta: (a) acotar en el alcance el tipo de servicio donde el mecanismo es efectivo (pruebas gratuitas, suscripciones digitales mensuales pagadas con tarjeta y sin permanencia); (b) sacar de la definición del problema los daños que el sistema no ataca o explicitar que no los ataca; (c) aprovechar que el patrón 6 (*sneaking*, permanencia oculta) puede alertar **antes** de contratar, que es un argumento a favor de la contribución. Es una decisión del tesista.

**B2. La comparación entre clasificadores (SP2) depende de un servicio en acceso anticipado sin verificar.** Jev (TypeSafe AI) figura como lanzado en septiembre de 2026, propietario y sin validación independiente. Los documentos ya lo reconocen como riesgo, pero hay afirmaciones que dependen de su documentación y no tienen fuente en el repositorio: los SDK oficiales para Python y TypeScript (ADR-07, criterio K2, que pesa 15 puntos en la elección del stack), la integración con Spring AI, los tipos de pregunta "*Choice* o *Noul*" (Contribución 5.2: el segundo término parece un error de tipeo o un término a confirmar) y los términos de uso para publicar resultados. Si alguno no se confirma, cambia el puntaje del ADR-07 y quizás la decisión.

**B3. El índice de riesgo carece de definición operativa.** El Plan de validación exige "exactitud del nivel de riesgo ≥ 0,80" contra el nivel asignado por el anotador, pero no existe un criterio para que el anotador asigne bajo/medio/alto independiente de la fórmula del sistema. Sin esa definición en la guía de etiquetado, la métrica es circular o subjetiva.

### 3.2. Importantes

**I1. Colisión de identificadores A1–A5.** En *Contribución y alcance* A1–A5 son los **aportes**; en *Estado del arte* A1–A5 son **antecedentes** (Gray 2018, Mathur 2019…). Detectado por `check_ids.py`. Renombrar una de las dos series (sugerencia: antecedentes → AT1–AT5 y BT1–BT5, o aportes → C1–C5).

**I2. Subpreguntas sin identificador.** SP1–SP4 se usan en Objetivos, Plan de validación y Arquitectura, pero en *Contribución* §2 las subpreguntas están numeradas 1–4 sin la etiqueta SP. Corrección trivial.

**I3. Correcciones de datos no aplicadas.** *Estado del arte* §7 lista 10 correcciones sobre 1.1 (cifras sin fuente, "multa" de Amazon que fue un acuerdo, regla *Click-to-Cancel* desactualizada, Mint cerrado, denominación incorrecta de la Disposición 954/2025, enlace ACM no identificado). Siguen pendientes.

**I4. Umbrales contextualizados con métricas no comparables.** *Estado del arte* §2.2 dice que los trabajos reportan F1 entre 0,62 y 0,93, pero 0,93 (AutoBot) es clasificación **binaria** y 0,62 (AppRay) es **macro F1 por tipo**. El umbral de la tesis es por patrón y por par paso–patrón. Hay que comparar contra las métricas por tipo, no contra el rango completo.

**I5. Marco teórico inexistente.** No hay 2.1 ni 2.3. La pregunta al profesor sobre enfoque (economía del comportamiento vs. HCI/ingeniería de software) no tiene respuesta registrada. Temas mínimos: modelo de suscripción y regulación (AR/UE/EE. UU.); *dark patterns* (definiciones y taxonomías); emisión de tarjetas y ciclo de autorización; clasificación automática (reglas, LLM, modelos de decisión estructurada); evaluación (métricas, acuerdo entre anotadores, SUS).

**I6. Justificación vacía y problema en formato de notas.** *Justificación de tesis.md* tiene 15 palabras. *Definición de problema.md* es una lista con lenguaje valorativo ("usureros", "asfixia", "viveza corporativa") y afirmaciones psicológicas sin fuente. Hay buenas fuentes ya relevadas para reconstruirlo (ICPEN 2024, C+R Research 2022, Nembaware y Sousa 2025, casos documentados).

**I7. Antecedentes nacionales y locales ausentes.** Tu propia guía (1.1, punto 2) los pide. El estado del arte los declara pendientes.

**I8. Reproducibilidad del ADR-07.** El análisis de sensibilidad (100 000 combinaciones de pesos) no tiene script en el repositorio. Sin él, no es verificable; con él, es un anexo fuerte.

**I9. Fuentes secundarias para normativa.** La Disposición 954/2025 y la regla *Click-to-Cancel* se citan a través de estudios jurídicos. Reemplazar por Boletín Oficial / InfoLEG y Federal Register / comunicados de la FTC.

**I10. Estructura de la memoria sin lugar para lo más fuerte del trabajo.** El índice sugerido no tiene secciones para pregunta de investigación, contribución, alcance y limitaciones, aspectos éticos (hay un estudio con personas) ni amenazas a la validez. Ver propuesta en §5.

### 3.3. Menores

- *Entregable quincenal…md* dice "[Nombre del Profesor / Tutor]"; el `.docx` dice Román Zenobi. Ambos son históricos: van a `archivo/`.
- La Entrega 1 marca el capítulo 1 como 100 % completo; hoy no lo está. Conviene no repetir ese tipo de porcentajes en la Entrega 2.
- *Ideas.md* e *Idea seleccionada.md* contienen texto literal de chatbot ("¿Quieres que ahora te prepare…?"). Si algún fragmento llegara a la memoria sería un problema de integridad.
- El cronograma de 5 meses de la idea original (agosto → diciembre/enero) no fue actualizado con el alcance nuevo.

## 4. Lo que está sólido (no romper)

- La reformulación de la contribución como **integración** (detección que informa una acción preventiva) y la brecha formulada en *Estado del arte* §6.
- La trazabilidad OE ↔ SP ↔ componentes ↔ requisitos ↔ métricas.
- Los ADR justificados desde requisitos, en especial ADR-01 (monolito modular), ADR-03 (validar el vencimiento en el momento del cobro) y ADR-05.
- El plan de validación: conjunto de prueba reservado, segundo anotador con protocolo ciego, asimetría de costos FP/FN, distinción entre criterios de aceptación y resultados experimentales, descarte razonado de NPS.

## 5. Índice ajustado propuesto (a validar con el profesor)

- **Preliminares:** portada, resumen/abstract, índice, listas de figuras y tablas, siglas.
- **1. Introducción:** 1.1 Contexto · 1.2 Problema · 1.3 Pregunta y subpreguntas · 1.4 Objetivos · 1.5 Contribución · 1.6 Alcance y limitaciones · 1.7 Justificación · 1.8 Organización del documento.
- **2. Marco teórico y estado del arte:** 2.1 Suscripciones y regulación · 2.2 *Dark patterns* · 2.3 Tarjetas virtuales y autorización de pagos · 2.4 Detección y clasificación automática · 2.5 Métodos de evaluación · 2.6 Estado del arte comparativo y brecha.
- **3. Metodología:** 3.1 Enfoque (candidato: *design science research*) · 3.2 Fases · 3.3 Corpus y guía de etiquetado · 3.4 Plan de validación · 3.5 Aspectos éticos.
- **4. Diseño e implementación:** 4.1 Requisitos · 4.2 Arquitectura y decisiones · 4.3 Esquema del flujo, modelo de datos y máquina de estados · 4.4 Implementación de N1, N2 y N3 · 4.5 Prototipo integrado.
- **5. Resultados y discusión:** V1 a V6 · discusión por subpregunta · amenazas a la validez.
- **6. Conclusiones:** respuesta a la pregunta · aportes · limitaciones · trabajo futuro.
- **Anexos:** esquema JSON, guía de etiquetado, resumen del corpus, escenarios E01–E12, protocolo y consentimiento de usabilidad, análisis de sensibilidad del ADR-07, declaración de uso de IA.

## 6. Preguntas abiertas para el tesista

1. Fecha de entrega final y fecha de la Entrega 2.
2. ¿Existe ya código del prototipo? ¿En este repositorio o en otro?
3. Formato de entrega exigido (Word, PDF, LaTeX) y norma de citación.
4. ¿Hay reglamento de la facultad sobre uso de IA en el trabajo final?
5. ¿El texto de la devolución de la Entrega 1 está en algún archivo? Los documentos citan sus puntos 1 a 6; tenerlo en `guias/` permite verificar que se respondieron todos.

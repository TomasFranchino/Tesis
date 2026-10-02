# Plan de validación — SuscripGuard

> **Estado:** v1.0 — revisado y aprobado por el tesista (29/09/2026). Responde al punto 5 de la devolución de la Entrega 1: cada componente importante se asocia con métricas concretas, un instrumento de medición y un criterio de aceptación.
> Base: subpreguntas SP1–SP4 (*Contribucion y alcance.md*, sección 2), requisitos (*Requisitos.md* v1.0) y objetivo OE6.
> Los umbrales son **propuestos** y se ajustarán con el profesor de la materia (Román Zenobi), con el director/tutor una vez designado, y con los valores reportados en el estado del arte.

---

## 1. Enfoque

La validación se organiza en cinco bloques, uno por componente o atributo de calidad, y un escenario integral final:

| Bloque | Qué valida | Subpregunta | Tipo de evaluación |
|--------|------------|:-----------:|--------------------|
| V1 | Detección de *dark patterns* (N1) | SP1, SP2 | Experimental, sobre corpus etiquetado |
| V2 | Motor de reglas y políticas (N2) | SP3 | Pruebas basadas en escenarios |
| V3 | Emulador de tarjetas (N3) y rendimiento | SP3 | Pruebas funcionales y de carga |
| V4 | Seguridad y privacidad | — (RNF) | Análisis estático/dinámico e inspección |
| V5 | Usabilidad | SP4 | Prueba con usuarios (SUS) |
| V6 | Escenario integral | Pregunta principal | Demostración reproducible de extremo a extremo |

Se distingue entre **criterios de aceptación** (el prototipo debe cumplirlos) y **resultados experimentales** (se reportan cualquiera sea su valor). La comparación entre clasificadores es un resultado, no un criterio de aprobación: que el modelo de decisión estructurada supere o no a la línea base es, en sí mismo, un hallazgo.

---

## 2. V1 — Detección de *dark patterns*

### 2.1. Corpus

- **Tamaño:** 15 a 20 servicios por suscripción, priorizando servicios con uso en Argentina y casos documentados.
- **Unidad de análisis:** el par *(paso del flujo, patrón)*. Adicionalmente se evalúa el nivel *(flujo, patrón)* y el índice de riesgo por servicio.
- **Guía de etiquetado:** definición operativa de cada uno de los 7 patrones, con ejemplos positivos y negativos, elaborada a partir de las taxonomías del estado del arte.
- **Acuerdo entre anotadores:** un segundo anotador etiqueta de forma independiente al menos el 30 % del corpus. Segundo anotador propuesto: **Román Zenobi** (profesor de la materia Trabajo Final, no involucrado en el diseño del sistema), sujeto a su aceptación; alternativa: un compañero de carrera o docente del área.
- **Protocolo de anotación ciega:** el segundo anotador recibe solo la guía de etiquetado y los flujos en formato legible; no accede a las etiquetas del tesista ni a las salidas del sistema. Antes de la anotación se hace una sesión de calibración con 1 flujo del conjunto de diseño, que se excluye del cálculo de kappa. Los desacuerdos se discuten **después** de calcular kappa y se resuelven para formar la verdad de referencia final.
- **Esfuerzo estimado del segundo anotador:** 5–6 flujos × 5–8 pasos × 7 patrones ≈ 200–300 juicios, del orden de 2 a 3 horas. Se calcula el coeficiente kappa de Cohen por patrón. **Criterio:** κ ≥ 0,61 (acuerdo sustancial); los patrones por debajo de ese valor se redefinen o se excluyen del análisis.
- **Partición:** para evitar sobreajuste (las heurísticas y las preguntas al clasificador se diseñan mirando datos), el corpus se divide en un **conjunto de diseño** (≈ 30 %, 5–6 servicios) y un **conjunto de prueba** (≈ 70 %) que no se consulta hasta la evaluación final.

### 2.2. Métricas

| Métrica | Nivel | Uso |
|---------|-------|-----|
| Precisión, *recall* y F1 por patrón | Paso–patrón | Desempeño de cada patrón |
| F1 macro | Paso–patrón | Resumen global comparable entre clasificadores |
| Tasa de falsos positivos | Paso–patrón | Respuesta directa al punto 5 de la devolución |
| Curva precisión–*recall* por umbral | Paso–patrón | Aprovecha las probabilidades del clasificador para elegir el umbral de operación |
| Exactitud y kappa ponderado del nivel de riesgo | Servicio | Concordancia entre el índice calculado y el asignado por el anotador |
| Latencia p50 / p95 y costo por flujo | Flujo | Comparación operativa entre clasificadores |

### 2.3. Criterios de aceptación (propuestos)

El costo de los errores es asimétrico. Un **falso positivo** produce una política más restrictiva de lo necesario, pero el usuario la revisa y puede modificarla antes de aplicarla (RF-12). Un **falso negativo** deja una política laxa sobre un servicio riesgoso. Por eso se prioriza el *recall*:

- *Recall* macro ≥ 0,75 y precisión macro ≥ 0,70 en el conjunto de prueba, para al menos una de las implementaciones del clasificador.
- Exactitud del nivel de riesgo por servicio ≥ 0,80.
- Latencia por flujo < 30 s (RNF-09).

### 2.4. Comparación entre clasificadores (SP2)

- Implementaciones: **(a)** modelo de decisión estructurada (Jev), **(b)** línea base heurística y, opcionalmente, **(c)** LLM local.
- Ambas se evalúan sobre las mismas instancias del conjunto de prueba.
- Se reportan las diferencias de F1 con intervalos de confianza por *bootstrap* y la prueba de McNemar sobre las predicciones pareadas.
- Se registra la versión del modelo y la fecha de cada ejecución, porque el servicio externo puede cambiar.

---

## 3. V2 — Motor de reglas y políticas

### 3.1. Escenarios de prueba (mínimos)

| Id | Escenario | Resultado esperado |
|----|-----------|--------------------|
| E01 | Cobro dentro de la política vigente | Autorizado |
| E02 | Cobro posterior a la fecha de vencimiento | Rechazado — motivo: vencimiento |
| E03 | Cobro al finalizar el período de prueba (vencimiento relativo) | Rechazado |
| E04 | Cobro por monto superior al tope | Rechazado — motivo: tope |
| E05 | Cobro que excede la cantidad máxima de cobros | Rechazado — motivo: cantidad |
| E06 | Cobro sobre tarjeta congelada o bloqueada manualmente | Rechazado |
| E07 | Cobro sobre tarjeta destruida | Rechazado |
| E08 | Reinicio del sistema antes de un vencimiento programado | El vencimiento se aplica igual (RNF-07) |
| E09 | Modificación de la política por el usuario antes de un cobro | Se aplica la política nueva |
| E10 | Dos cobros simultáneos que, juntos, superan el límite | Se autoriza como máximo uno |
| E11 | Servicio con riesgo alto / medio / bajo | Se propone la política definida para cada nivel |
| E12 | Alerta previa a la renovación | Se emite con la anticipación configurada |

### 3.2. Métricas y criterios

- **Cumplimiento de reglas:** 100 % de escenarios aprobados (RNF-02).
- **Cobros autorizados indebidamente:** 0.
- **Puntualidad:** desvío del vencimiento < 1 minuto (RNF-07).
- **Determinismo:** cada escenario se ejecuta repetidas veces con resultado idéntico. Se complementa con pruebas basadas en propiedades (generación aleatoria de políticas y cobros, contrastados con un oráculo independiente).
- **Trazabilidad:** el 100 % de las decisiones queda registrado en la auditoría con las reglas evaluadas (RF-16, RNF-03).

---

## 4. V3 — Emulador de tarjetas y rendimiento

- **Máquina de estados:** se prueban todas las transiciones válidas y se verifica que las inválidas sean rechazadas (p. ej. reactivar una tarjeta destruida).
- **Rendimiento de autorización:** prueba de carga con una herramienta específica (p. ej. k6 o Locust), con carga acorde a un prototipo (decenas de solicitudes concurrentes). **Criterio:** p95 < 1 s (RNF-08).
- **Independencia:** la autorización se mide con el clasificador externo desconectado, para verificar que no depende de él.

---

## 5. V4 — Seguridad y privacidad

| Requisito | Instrumento | Criterio |
|-----------|-------------|----------|
| RNF-04 Privacidad | Registro e inspección del tráfico saliente durante la ejecución completa de las pruebas de extremo a extremo | 0 solicitudes externas con datos del usuario; al clasificador solo llegan flujos del corpus |
| RNF-05 Datos de tarjeta | Búsqueda automatizada de números de tarjeta (patrón + verificación de Luhn) en base de datos, logs y respuestas de la API | 0 hallazgos en claro |
| RNF-06 Seguridad de la aplicación | Escaneo dinámico (p. ej. OWASP ZAP) y revisión manual guiada por OWASP Top 10 | 0 hallazgos de severidad alta o crítica sin mitigar |

---

## 6. V5 — Usabilidad

- **Participantes:** 10 a 15 personas adultas con al menos dos suscripciones activas y sin formación en informática como requisito.
- **Tareas:** (1) registrar una suscripción con período de prueba; (2) consultar el informe de riesgo del servicio; (3) aceptar o ajustar la política propuesta; (4) identificar por qué se rechazó un cobro.
- **Instrumentos y métricas:**
  - Cuestionario **SUS**. **Criterio:** puntaje medio ≥ 68 (RNF-11).
  - Tasa de finalización de tareas. **Criterio:** ≥ 80 %.
  - Tiempo por tarea (se reporta, sin umbral).
  - Pregunta de comprensión: el participante explica con sus palabras por qué su tarjeta tiene esa política. Mide si la explicación del riesgo es entendible (RNF-03).
- **Se descarta NPS**: mide intención de recomendación, no usabilidad, y con una muestra de este tamaño no aporta información confiable.
- **Aspectos éticos:** consentimiento informado, datos ficticios (los participantes no usan tarjetas ni cuentas reales) y resultados anonimizados.

---

## 7. V6 — Escenario integral

Demostración reproducible que recorre la contribución completa:

1. Se analiza un flujo del corpus con riesgo alto (p. ej. un servicio cuyo flujo exige canal telefónico o chat de retención).
2. El sistema genera el informe de riesgo con evidencia.
3. El usuario registra una suscripción con 7 días de prueba y acepta la política propuesta (tarjeta de un solo uso con vencimiento al fin de la prueba).
4. El comercio simulado intenta el primer cobro al finalizar la prueba.
5. El cobro es rechazado y el usuario ve el motivo y la regla aplicada.

**Criterio:** el escenario se completa sin intervención manual fuera de las acciones del usuario, y cada paso queda registrado en la auditoría.

---

## 8. Matriz resumen

| Componente | Subpregunta | Requisitos | Métrica | Instrumento | Umbral propuesto |
|------------|:-----------:|------------|---------|-------------|------------------|
| N1 Detección | SP1 | RF-03–07, RF-09 | *Recall* / precisión macro | Corpus etiquetado (conjunto de prueba) | ≥ 0,75 / ≥ 0,70 |
| N1 Detección | SP1 | RF-07 | Exactitud del nivel de riesgo | Corpus etiquetado | ≥ 0,80 |
| N1 Detección | SP2 | RF-05 | ΔF1 entre clasificadores | *Bootstrap* + McNemar | Se reporta |
| N1 Detección | SP2 | RNF-09 | Latencia p95 y costo por flujo | Registro de ejecución | < 30 s |
| Corpus | SP1 | RF-08 | Kappa de Cohen | Doble anotación ≥ 30 % | ≥ 0,61 |
| N2 Motor | SP3 | RF-11–16, RNF-02 | % de escenarios aprobados | Suite E01–E12 + pruebas por propiedades | 100 % |
| N2 Motor | SP3 | RNF-07 | Desvío del vencimiento | Pruebas temporales | < 1 min |
| N3 Emulador | SP3 | RF-17–20, RNF-08 | Latencia de autorización p95 | Prueba de carga | < 1 s |
| Seguridad | — | RNF-04–06 | Hallazgos | Tráfico saliente, búsqueda de PAN, OWASP ZAP | 0 / 0 / 0 altos |
| Plataforma | SP4 | RNF-11 | SUS y finalización de tareas | Prueba con usuarios | ≥ 68 y ≥ 80 % |

---

## 9. Amenazas a la validez

| Amenaza | Mitigación |
|---------|------------|
| Corpus pequeño y tomado en una fecha: los resultados no se generalizan a todos los servicios ni a cambios posteriores. | Se declara como limitación; se registra la fecha de captura; se reportan intervalos de confianza. |
| Sesgo del anotador (el tesista diseña el sistema y etiqueta el corpus). | Segundo anotador independiente y cálculo de kappa. |
| Sobreajuste de heurísticas y preguntas al corpus. | Conjunto de prueba reservado y no consultado durante el diseño. |
| Cambios del servicio externo de clasificación (acceso anticipado). | Registro de versión y fecha; línea base propia que permite completar la evaluación sin él. |
| El emulador no reproduce todas las condiciones de una red de pagos real. | Se declara el alcance simulado; adaptador para un *sandbox* real como demostración opcional. |
| Muestra de usabilidad reducida y no representativa. | Se reporta como estudio exploratorio; perfil de participantes documentado. |

---

## 10. Pendientes

- Consultar a Román Zenobi si acepta ser segundo anotador (y tener una alternativa).
- Consultar con Román Zenobi los umbrales propuestos.
- Redactar la guía de etiquetado.
- Buscar en el estado del arte las métricas reportadas por trabajos de detección automática de *dark patterns*, para contextualizar los umbrales de V1.

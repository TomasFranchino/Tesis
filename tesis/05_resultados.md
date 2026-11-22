<!-- NOTA PARA TOMÁS: este capítulo tiene la estructura definitiva, pero no contiene ningún resultado: el prototipo no existe y los experimentos no se ejecutaron. Cada celda con [[RESULTADO PENDIENTE]] se completa solo con cifras de evidencia/resultados/ (con un comentario HTML "fuente: evidencia/…" al lado). Los umbrales son los propuestos en el Plan de validación; siguen pendientes de acuerdo con el profesor (Román Zenobi) y, cuando se designe, con el director. Las respuestas a las preguntas de investigación y la interpretación de los hallazgos conviene que las escribas con tu voz cuando haya datos. -->

# Análisis de resultados y validación

Este capítulo presenta los resultados de la validación del prototipo SuscripGuard y los contrasta con los criterios fijados en el diseño de la validación descrito en el Capítulo 3. La validación se organiza en seis bloques (V1 a V6): detección de *dark patterns* (patrones oscuros), motor de reglas y políticas, emulador de tarjetas y rendimiento, seguridad y privacidad, usabilidad y escenario integral. En cada uno se informa qué se mide, en qué forma se reporta y contra qué criterio se compara. A la fecha de este borrador, la validación no se ejecutó: las tablas definen la estructura de reporte y sus celdas se completarán con los datos que produzcan los experimentos.

Se distinguen dos tipos de resultado. Los **criterios de aceptación** son umbrales que el prototipo debe cumplir; los de este capítulo son los propuestos en el Plan de validación y se ajustarán con el profesor de la materia y con los valores reportados en el estado del arte. Los **resultados experimentales**, en cambio, se informan cualquiera sea su valor, sin umbral de aprobación; el caso principal es la comparación entre clasificadores, cuyo resultado es un hallazgo en sí mismo.

## Pruebas de funcionamiento

Esta sección muestra los resultados de los tres bloques que verifican el comportamiento del sistema: el motor de reglas (V2), el emulador de tarjetas con su rendimiento de autorización (V3) y los requisitos de seguridad y privacidad (V4). Los tres dependen de criterios binarios o de umbrales fijos, de modo que el reporte consiste en indicar si cada criterio se cumplió y con qué evidencia.

### Motor de reglas y políticas (V2)

El bloque V2 valida el motor de reglas determinista (N2, uno de los tres componentes que constituyen el núcleo de la contribución) mediante doce escenarios de prueba, E01 a E12, que cubren cobros dentro y fuera de política, estados de la tarjeta, reinicio del sistema, modificación de la política, concurrencia, propuesta de política por nivel de riesgo y alerta previa a la renovación. Los escenarios y el resultado esperado de cada uno figuran en el Anexo A. Para cada escenario se informan la cantidad de ejecuciones, el resultado obtenido y si coincide con el esperado; además, se informa la cantidad de casos generados en las pruebas basadas en propiedades (generación aleatoria de políticas y cobros contrastada con un oráculo independiente). Los resultados agregados se presentan en la tabla siguiente.

| Métrica | Criterio propuesto | Resultado |
|---------|--------------------|-----------|
| Escenarios aprobados (RNF-02, requisito de correctitud) | 100 % (12 de 12) | [[RESULTADO PENDIENTE: escenarios aprobados, V2]] |
| Cobros autorizados indebidamente | 0 | [[RESULTADO PENDIENTE: cobros indebidos, V2]] |
| Desvío del vencimiento (RNF-07, requisito de puntualidad) | < 1 minuto | [[RESULTADO PENDIENTE: desvío máximo, V2]] |
| Determinismo: ejecuciones con resultado idéntico | 100 % | [[RESULTADO PENDIENTE: determinismo, V2]] |
| Decisiones registradas en la auditoría con las reglas evaluadas (RF-16, RNF-03) | 100 % | [[RESULTADO PENDIENTE: trazabilidad, V2]] |

: Resultados de V2 contra los criterios propuestos.

### Emulador de tarjetas y rendimiento de autorización (V3)

El bloque V3 valida el emulador de tarjetas virtuales (N3) en dos aspectos. El primero es la máquina de estados del ciclo de vida de la tarjeta: se informa si todas las transiciones válidas se aceptaron y si las inválidas, como reactivar una tarjeta destruida, se rechazaron. El segundo es el rendimiento de la autorización bajo una prueba de carga con decenas de solicitudes concurrentes, acorde a un prototipo; se informa la latencia p95 junto con la herramienta y el nivel de carga utilizados. `[[DATO PENDIENTE: herramienta de prueba de carga y nivel de carga concurrente]]` Se informa también la latencia de autorización con el clasificador basado en un modelo de lenguaje local (LLM local) detenido, para verificar que la autorización no depende de él.

| Prueba | Criterio propuesto | Resultado |
|--------|--------------------|-----------|
| Transiciones válidas aceptadas | Todas | [[RESULTADO PENDIENTE: transiciones válidas, V3]] |
| Transiciones inválidas rechazadas | Todas | [[RESULTADO PENDIENTE: transiciones inválidas, V3]] |
| Latencia de autorización p95 (RNF-08) | < 1 s | [[RESULTADO PENDIENTE: p95 de autorización, V3]] |
| Autorización con el LLM local detenido | Se autoriza dentro del criterio de p95 < 1 s sin el LLM local | [[RESULTADO PENDIENTE: independencia del clasificador, V3]] |

: Resultados de V3 contra los criterios propuestos.

### Seguridad y privacidad (V4)

El bloque V4 verifica tres requisitos no funcionales: la privacidad (RNF-04), la protección de los datos de tarjeta (RNF-05) y la seguridad de la aplicación (RNF-06). Cada uno se evalúa con un instrumento distinto y se informa el número de hallazgos.

| Requisito | Instrumento | Criterio propuesto | Resultado |
|-----------|-------------|--------------------|-----------|
| RNF-04 Privacidad | Inspección del tráfico saliente durante las pruebas de extremo a extremo, incluido el análisis de correos de confirmación | 0 solicitudes externas con datos del usuario | [[RESULTADO PENDIENTE: solicitudes externas, V4]] |
| RNF-05 Datos de tarjeta | Búsqueda automatizada de números de tarjeta (patrón y verificación de Luhn) en base de datos, registros y respuestas de la API | 0 hallazgos en claro | [[RESULTADO PENDIENTE: hallazgos de números de tarjeta, V4]] |
| RNF-06 Seguridad de la aplicación | Escaneo dinámico (p. ej. OWASP ZAP) y revisión manual guiada por OWASP Top 10 | 0 hallazgos de severidad alta o crítica sin mitigar | [[RESULTADO PENDIENTE: hallazgos por severidad, V4]] |

: Resultados de V4 contra los criterios propuestos.

Con los resultados de funcionamiento se conoce si el sistema se comporta según lo especificado. La sección siguiente aborda el otro componente del núcleo, la detección, cuyo desempeño no es binario y se expresa con métricas de clasificación.

## Evaluación de rendimiento y métricas

Esta sección presenta los resultados del bloque V1, que evalúa el módulo de detección (N1), y de la validación de la alerta de permanencia o costos ocultos (RF-28). Los resultados se calculan sobre el conjunto de prueba del corpus, que se reserva sin consultar hasta la evaluación final; el conjunto de diseño (aproximadamente el 30 % del corpus) se usa solo para elaborar las heurísticas y las preguntas al clasificador. Se informan el tamaño efectivo del corpus y la fecha de captura de los flujos. `[[DATO PENDIENTE: cantidad de servicios, flujos y correos de confirmación efectivamente capturados, y fecha de captura]]`

### Acuerdo entre anotadores

Antes de evaluar a los clasificadores se verifica la calidad de la verdad de referencia. Un segundo anotador etiqueta de forma independiente al menos el 30 % del corpus siguiendo la guía de etiquetado (Anexo B), sin acceso a las etiquetas del tesista ni a las salidas del sistema; el anotador propuesto es el profesor de la materia, sujeto a su aceptación. `[[DATO PENDIENTE: segundo anotador confirmado]]` Se calcula el coeficiente kappa de Cohen por patrón y se contrasta con el criterio propuesto de κ ≥ 0,61, que se interpreta como acuerdo sustancial `[[CITA PENDIENTE: escala de interpretación del coeficiente kappa]]`. Los patrones que no alcancen ese valor se redefinen o se excluyen del análisis, y la exclusión se informa explícitamente.

| Patrón | Juicios comparados | κ de Cohen | ¿Cumple κ ≥ 0,61? |
|--------|--------------------|------------|-------------------|
| Asimetría alta/baja (*roach motel*) | [[DATO PENDIENTE: n]] | [[RESULTADO PENDIENTE: κ, V1]] | [[RESULTADO PENDIENTE]] |
| Obstrucción | [[DATO PENDIENTE: n]] | [[RESULTADO PENDIENTE: κ, V1]] | [[RESULTADO PENDIENTE]] |
| *Confirmshaming* (culpabilización en la opción de baja) | [[DATO PENDIENTE: n]] | [[RESULTADO PENDIENTE: κ, V1]] | [[RESULTADO PENDIENTE]] |
| Interferencia visual | [[DATO PENDIENTE: n]] | [[RESULTADO PENDIENTE: κ, V1]] | [[RESULTADO PENDIENTE]] |
| Interacción forzada (*nagging*) | [[DATO PENDIENTE: n]] | [[RESULTADO PENDIENTE: κ, V1]] | [[RESULTADO PENDIENTE]] |
| Costos o permanencia ocultos (*sneaking*) | [[DATO PENDIENTE: n]] | [[RESULTADO PENDIENTE: κ, V1]] | [[RESULTADO PENDIENTE]] |
| Preselección de opciones desfavorables | [[DATO PENDIENTE: n]] | [[RESULTADO PENDIENTE: κ, V1]] | [[RESULTADO PENDIENTE]] |

: Acuerdo entre anotadores por patrón.

### Detección por patrón y nivel de riesgo

La unidad de análisis es el par (paso del flujo, patrón). Para cada patrón se informan precisión, exhaustividad (*recall*), F1 y tasa de falsos positivos, además del F1 macro como resumen global. La tabla se presenta por separado para el clasificador LLM local y para la línea base heurística. Como complemento se grafica la curva precisión–*recall* por umbral, que sirve para elegir el umbral de operación a partir de las probabilidades del clasificador. El criterio propuesto prioriza la exhaustividad porque el costo de los errores es asimétrico: un falso positivo produce una política más restrictiva de lo necesario, que el usuario puede revisar y modificar antes de aplicarla (RF-12), mientras que un falso negativo deja una política laxa sobre un servicio riesgoso. El criterio es *recall* macro ≥ 0,75 y precisión macro ≥ 0,70 sobre el conjunto de prueba, para al menos una de las dos implementaciones. `[[CITA PENDIENTE: métricas reportadas por trabajos de detección automática de dark patterns, para contextualizar estos umbrales]]`

| Patrón | Precisión | *Recall* | F1 | Tasa de falsos positivos |
|--------|-----------|----------|----|--------------------------|
| Asimetría alta/baja (*roach motel*) | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Obstrucción | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| *Confirmshaming* | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Interferencia visual | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Interacción forzada (*nagging*) | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Costos o permanencia ocultos (*sneaking*) | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Preselección de opciones desfavorables | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Macro (promedio entre patrones) | [[RESULTADO PENDIENTE: precisión macro, V1]] | [[RESULTADO PENDIENTE: recall macro, V1]] | [[RESULTADO PENDIENTE: F1 macro, V1]] | [[RESULTADO PENDIENTE: falsos positivos macro, V1]] |

: Desempeño de detección por patrón, conjunto de prueba. Se reproduce para cada clasificador.

A nivel de servicio se informa la exactitud y el kappa ponderado del nivel de riesgo (bajo, medio, alto) calculado por el sistema frente al asignado por el anotador. La latencia p50 y p95 y el uso de recursos por flujo se informan para cada clasificador junto con el hardware de ejecución, porque la latencia del LLM local depende del equipo y no de la red. `[[DATO PENDIENTE: hardware donde corre el LLM local]]` El umbral de latencia propuesto es de 30 s por flujo (RNF-09); su aplicación al LLM local está sujeta a una decisión abierta que se resuelve una vez conocidos el modelo y el equipo. `[[DECISIÓN: umbral de latencia para el LLM local — A) mantener 30 s en el hardware declarado; B) fijar otro umbral según el modelo y el equipo; recomendación del Plan de validación: B si el modelo no cumple 30 s]]`

| Métrica | Criterio propuesto | LLM local | Línea base heurística |
|---------|--------------------|-----------|-----------------------|
| Exactitud del nivel de riesgo | ≥ 0,80 | [[RESULTADO PENDIENTE: exactitud, V1]] | [[RESULTADO PENDIENTE: exactitud, V1]] |
| Kappa ponderado del nivel de riesgo | Se reporta | [[RESULTADO PENDIENTE: kappa ponderado, V1]] | [[RESULTADO PENDIENTE: kappa ponderado, V1]] |
| Latencia p50 / p95 por flujo | < 30 s (sujeto a la decisión anterior) | [[RESULTADO PENDIENTE: latencia, V1]] | [[RESULTADO PENDIENTE: latencia, V1]] |
| Uso de recursos por flujo | Se reporta | [[RESULTADO PENDIENTE: recursos, V1]] | [[RESULTADO PENDIENTE: recursos, V1]] |

: Nivel de riesgo y latencia por clasificador.

### Alerta de permanencia o costos ocultos

La alerta de permanencia o costos ocultos (RF-28) se valida sobre los correos de confirmación del alta del corpus, con la misma partición entre conjuntos de diseño y de prueba que los flujos del servicio correspondiente. Se informan precisión, *recall* y F1 de la extracción de cada campo (permanencia mínima, penalidad por baja anticipada, renovación automática y precio tras la prueba) y precisión y *recall* de la alerta por servicio. Los correos que no informan una condición se etiquetan como "no informado", categoría distinta de "ausente", para que la falta de información no se cuente como acierto. Dado que el alcance prioriza servicios sin permanencia, es probable que el corpus tenga pocos casos positivos; por eso se informan los conteos absolutos junto con las métricas. `[[DECISIÓN: agregar correos de servicios con permanencia documentada solo para evaluar la alerta — recomendación del Plan de validación: sí, si el corpus base tiene menos de 5 casos positivos]]` El criterio de aceptación está pendiente de acuerdo con el profesor. `[[DECISIÓN: umbral de aceptación de la alerta — se recomienda priorizar el recall por el mismo argumento del costo asimétrico]]` Se registran las mismas condiciones de ejecución del LLM local que en V1.

| Campo o nivel | Casos positivos | Precisión | *Recall* | F1 |
|---------------|-----------------|-----------|----------|----|
| Permanencia mínima | [[RESULTADO PENDIENTE: n, V1]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Penalidad por baja anticipada | [[RESULTADO PENDIENTE: n, V1]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Renovación automática | [[RESULTADO PENDIENTE: n, V1]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Precio tras la prueba | [[RESULTADO PENDIENTE: n, V1]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] |
| Alerta por servicio | [[RESULTADO PENDIENTE: n, V1]] | [[RESULTADO PENDIENTE]] | [[RESULTADO PENDIENTE]] | No aplica |

: Validación de la alerta de permanencia o costos ocultos, conjunto de prueba.

Con las métricas de cada clasificador por separado se puede pasar a compararlos entre sí, que es lo que aborda la sección siguiente junto con la usabilidad y el escenario integral.

## Análisis comparativo

Esta sección contrasta los dos clasificadores sobre las mismas instancias, presenta los resultados de la prueba con usuarios y del escenario integral, y sintetiza lo anterior en una respuesta a cada pregunta de investigación.

### Clasificador LLM local frente a línea base heurística

La comparación responde a la segunda subpregunta (SP2). Ambas implementaciones se evalúan sobre las mismas instancias del conjunto de prueba. Se informan la diferencia de F1 con intervalos de confianza por *bootstrap* (remuestreo con reemplazo) `[[CITA PENDIENTE: método bootstrap para intervalos de confianza de métricas de clasificación]]` y la prueba de McNemar sobre las predicciones pareadas `[[CITA PENDIENTE: prueba de McNemar para comparar clasificadores]]`. No hay umbral de aprobación: que el LLM local supere o no a la línea base es un resultado. Dado que la salida de un modelo de lenguaje puede variar entre ejecuciones, versiones y equipos, se registran en cada ejecución el modelo, su versión o etiqueta, la cuantización, la temperatura, la semilla, el hardware y la fecha, y se repite la evaluación para estimar la variación. `[[DECISIÓN: modelo y tamaño del LLM local — opciones a confirmar]]` `[[DECISIÓN: número de repeticiones de la evaluación del LLM local]]` La línea base heurística, por ser determinista, sirve de referencia.

| Comparación | Estadístico | Resultado |
|-------------|-------------|-----------|
| Diferencia de F1 macro (LLM local − heurística) | Diferencia e intervalo de confianza por *bootstrap* | [[RESULTADO PENDIENTE: ΔF1 e intervalo, V1]] |
| Predicciones pareadas | Prueba de McNemar (estadístico y valor p) | [[RESULTADO PENDIENTE: McNemar, V1]] |
| Diferencia de tasa de falsos positivos | Diferencia por patrón | [[RESULTADO PENDIENTE: diferencia de falsos positivos, V1]] |
| Diferencia de latencia p50 / p95 | Diferencia con hardware declarado | [[RESULTADO PENDIENTE: diferencia de latencia, V1]] |
| Variación entre repeticiones del LLM local | Dispersión de F1 macro | [[RESULTADO PENDIENTE: variación entre repeticiones, V1]] |

: Comparación entre clasificadores (SP2).

### Usabilidad (V5)

El bloque V5 evalúa la usabilidad con 10 a 15 personas adultas con al menos dos suscripciones activas, con datos ficticios y consentimiento informado. Las cuatro tareas son registrar una suscripción con período de prueba, consultar el informe de riesgo, aceptar o ajustar la política propuesta e identificar por qué se rechazó un cobro. Dada la muestra, el estudio se informa como exploratorio y se documenta el perfil de los participantes. `[[DATO PENDIENTE: perfil y cantidad de participantes]]`

| Métrica | Criterio propuesto | Resultado |
|---------|--------------------|-----------|
| Puntaje medio del cuestionario SUS (*System Usability Scale*, RNF-11) | ≥ 68 `[[CITA PENDIENTE: SUS y valor de referencia 68]]` | [[RESULTADO PENDIENTE: SUS medio, V5]] |
| Tasa de finalización de tareas | ≥ 80 % | [[RESULTADO PENDIENTE: finalización, V5]] |
| Tiempo por tarea | Se reporta, sin umbral | [[RESULTADO PENDIENTE: tiempos, V5]] |
| Comprensión de la política (explicación con las propias palabras, RNF-03) | Se reporta | [[RESULTADO PENDIENTE: comprensión, V5]] |

: Resultados de la prueba de usabilidad.

### Escenario integral (V6)

El bloque V6 es una demostración reproducible de extremo a extremo: se analiza un flujo del corpus con riesgo alto, el sistema genera el informe de riesgo con evidencia, el usuario registra una suscripción con 7 días de prueba y acepta la política propuesta (tarjeta de un solo uso con vencimiento al fin de la prueba), el comercio simulado intenta el primer cobro al finalizar la prueba y el cobro es rechazado con el motivo y la regla aplicada visibles. El criterio propuesto es que el escenario se complete sin intervención manual fuera de las acciones del usuario y que cada paso quede registrado en la auditoría. [[RESULTADO PENDIENTE: completitud del escenario integral y registro de auditoría por paso, V6]]

### Respuesta a las preguntas de investigación

Las respuestas siguientes se redactarán cuando existan los resultados; cada una remite al bloque que la sustenta y se limita a lo que los datos permitan afirmar dentro del alcance acotado del trabajo.

**SP1: precisión de detección de un subconjunto de *dark patterns*.** La respuesta se apoya en V1: el *recall* y la precisión macro frente a los criterios propuestos, el acuerdo entre anotadores y la exactitud del nivel de riesgo. [[RESULTADO PENDIENTE: respuesta a SP1 a partir de V1]]

**SP2: diferencia entre el clasificador LLM local y la línea base heurística.** La respuesta se apoya en la diferencia de F1, la prueba de McNemar, los falsos positivos y la latencia con el hardware declarado. [[RESULTADO PENDIENTE: respuesta a SP2 a partir de V1]]

**SP3: cumplimiento verificable de las políticas por el motor de reglas.** La respuesta se apoya en V2 y V3: escenarios aprobados, cobros autorizados indebidamente, puntualidad, determinismo y trazabilidad. [[RESULTADO PENDIENTE: respuesta a SP3 a partir de V2 y V3]]

**SP4: usabilidad de la solución.** La respuesta se apoya en V5: SUS, finalización de tareas y comprensión de la política, con la salvedad del carácter exploratorio de la muestra. [[RESULTADO PENDIENTE: respuesta a SP4 a partir de V5]]

**Pregunta principal: prevención de cobros recurrentes no deseados.** La respuesta integra los resultados anteriores y el escenario integral V6, y se circunscribe a las suscripciones digitales pagadas con tarjeta y sin permanencia mínima, sobre un emulador de tarjetas y un corpus capturado en una fecha determinada. [[RESULTADO PENDIENTE: respuesta a la pregunta principal a partir de V1 a V6]]

Estas respuestas, junto con las limitaciones del alcance y de la validez, son el insumo del capítulo siguiente.

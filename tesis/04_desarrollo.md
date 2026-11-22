# Desarrollo e implementación

Este capítulo muestra qué debe hacer SuscripGuard, cómo se diseña en detalle y qué se documentará sobre su implementación. Se organiza en tres secciones: los requerimientos del sistema, el diseño detallado de los elementos centrales (esquema del flujo, detección, política de tarjeta y puertos) y la implementación del prototipo. Los requisitos y el diseño están definidos y se exponen en presente; los criterios de aceptación y las decisiones de arquitectura son propuestos. El prototipo todavía no se construyó, por lo que la última sección describe lo que se documentará y no resultados.

## Requerimientos del sistema

Esta sección presenta los actores, los requisitos funcionales por módulo, lo que queda fuera del alcance, los requisitos no funcionales y la trazabilidad con los objetivos específicos. Los requisitos se definieron antes que la arquitectura, y cada decisión tecnológica del capítulo anterior se justifica con los requisitos que las motivan. La prioridad se indica según el esquema MoSCoW: M (*must*, imprescindible), S (*should*, importante), C (*could*, deseable) y W (*won't*, fuera de alcance en esta versión) `[[CITA PENDIENTE: método de priorización MoSCoW]]`.

### Actores

| Actor | Descripción |
|-------|-------------|
| Usuario | Persona que registra sus suscripciones, consulta el riesgo de cada servicio y gestiona sus tarjetas virtuales. |
| Curador del corpus | Rol administrativo (en el prototipo, el tesista) que captura, importa y etiqueta flujos de cancelación. |
| Comercio simulado | Sistema externo simulado que genera solicitudes de cobro sobre las tarjetas virtuales. |
| LLM local (Ollama) | Proceso local, ejecutado en la misma máquina que el prototipo, que corre el modelo de lenguaje y es invocado a través de una interfaz propia. No es un servicio externo de terceros. |
| Planificador (tiempo) | Disparador de las reglas temporales (vencimientos y alertas). |

### Requisitos funcionales

Los requisitos funcionales se agrupan según los componentes definidos en el alcance: los tres del núcleo (N1, N2 y N3), el soporte y el complementario. En cada tabla, la columna OE indica el objetivo específico al que contribuye el requisito.

**N1, detección de *dark patterns* (patrones oscuros).**

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-01 | Importar un flujo de cancelación en formato JSON y validarlo contra el esquema de representación definido. | M | OE1, OE3 |
| RF-02 | Registrar los metadatos de cada captura (servicio, fecha, versión del esquema, curador). | M | OE2 |
| RF-03 | Detectar los patrones estructurales mediante reglas heurísticas explícitas. | M | OE3 |
| RF-04 | Clasificar los patrones semánticos mediante la implementación de clasificador configurada: clasificador basado en un modelo de lenguaje local (LLM local, ejecutado con Ollama) o línea base heurística. | M | OE3 |
| RF-05 | Permitir cambiar la implementación del clasificador por configuración, sin modificar el resto del módulo. | M | OE3 |
| RF-06 | Generar, por servicio, un informe con los patrones detectados, el paso donde ocurren, la evidencia asociada y la confianza de cada detección. | M | OE3 |
| RF-07 | Calcular un índice de riesgo de cancelación (bajo, medio o alto) mediante una fórmula documentada y parametrizable. | M | OE3 |
| RF-08 | Permitir registrar etiquetas manuales (verdad de referencia) por paso y patrón. | M | OE2 |
| RF-09 | Ejecutar la evaluación por lotes sobre el corpus y calcular precisión, *recall* (exhaustividad), F1 y tasa de falsos positivos por patrón y por clasificador. | S | OE6 |
| RF-10 | Asistir la captura de flujos mediante scripts de navegación que exporten el JSON para su anotación manual posterior. | S | OE2 |
| RF-28 | Analizar con el LLM local el correo de confirmación del alta de una suscripción, extraer las condiciones de contratación (permanencia mínima, penalidad por baja anticipada, renovación automática, precio tras la prueba) con salida validada contra un esquema y emitir una alerta cuando detecte permanencia mínima o costos ocultos, indicando el fragmento del correo que la respalda. | `[[DECISIÓN: prioridad M o S. Recomendación: M, porque la decisión de incorporar la alerta al mecanismo preventivo la integra al núcleo; S si se prefiere no comprometer el núcleo y dejarla sujeta al tiempo disponible]]` | OE3 |

El requisito RF-28 se numera a continuación de RF-27 para conservar los identificadores existentes, pero pertenece a N1. Su momento de emisión también es una decisión abierta: el diseño original la planteaba como alerta previa a la contratación, pero el correo de confirmación llega después del alta `[[DECISIÓN: momento de la alerta. Opciones: A) redefinirla como alerta temprana posterior al alta, vinculada con el derecho de revocación de la contratación a distancia (requiere cita de la norma y del plazo); B) conservar además el análisis del flujo de alta para emitir una alerta realmente previa, lo que amplía el corpus. Recomendación: A, porque mantiene el corpus y el alcance técnico definidos]]`. Del mismo modo, la forma de ingreso del correo está sin resolver `[[DECISIÓN: forma de ingreso del correo. Opciones: A) importación manual por el usuario (archivo .eml o texto pegado); B) lectura del buzón por IMAP o Gmail API. Recomendación: A, porque no requiere acceso al buzón y acota el tratamiento de datos personales a un solo correo]]`. La obligación legal de informar las condiciones de contratación en el correo de confirmación, que sustenta el enfoque, también está pendiente `[[CITA PENDIENTE: norma que obliga a informar la permanencia mínima y los cargos en el correo o comprobante de confirmación de la suscripción, y derecho de revocación de la contratación a distancia; jurisdicción y alcance (verificación legal pendiente, T-029)]]`.

**N2, motor de reglas y políticas.**

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-11 | Proponer una política de tarjeta a partir de los datos de la suscripción y del índice de riesgo del servicio. | M | OE4 |
| RF-12 | Permitir al usuario aceptar, modificar o rechazar la política propuesta antes de su aplicación. | M | OE4 |
| RF-13 | Soportar, como mínimo, las reglas: vencimiento en fecha fija, vencimiento relativo al fin del período de prueba, tope de monto por cobro, cantidad máxima de cobros y bloqueo manual. | M | OE4 |
| RF-14 | Ejecutar automáticamente las reglas temporales (vencer o destruir la tarjeta en la fecha programada). | M | OE4 |
| RF-15 | Emitir alertas al usuario con una anticipación configurable a la renovación o al vencimiento. | S | OE4 |
| RF-16 | Registrar cada decisión del motor (entrada, reglas evaluadas, resultado y fecha) para su auditoría. | M | OE4, OE6 |

**N3, emulador de tarjetas virtuales.**

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-17 | Emitir una tarjeta virtual simulada asociada a una única suscripción. | M | OE4 |
| RF-18 | Procesar solicitudes de cobro simuladas y autorizarlas o rechazarlas según las políticas vigentes, indicando el motivo del rechazo. | M | OE4 |
| RF-19 | Gestionar los estados de la tarjeta (activa, congelada, vencida, destruida) y sus transiciones válidas. | M | OE4 |
| RF-20 | Incluir un comercio simulado capaz de ejecutar escenarios de cobro predefinidos (cobros en fecha, posteriores al vencimiento, superiores al tope, repetidos). | M | OE4, OE6 |
| RF-21 | Integrar un proveedor real en modo *sandbox* (entorno de pruebas) a través de la interfaz de adaptador. | C | OE4 |

**Soporte y complementario.**

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-22 | Permitir el registro e inicio de sesión de usuarios. | M | OE5 |
| RF-23 | Permitir al usuario registrar manualmente una suscripción (servicio, precio, frecuencia, fin del período de prueba, fecha de renovación). | M | OE5 |
| RF-24 | Mostrar un panel con las suscripciones, la tarjeta asociada, el nivel de riesgo del servicio y el gasto mensual estimado. | M | OE5 |
| RF-25 | Permitir al usuario consultar el informe de riesgo de un servicio con la evidencia de cada patrón detectado. | M | OE5 |
| RF-26 | Mostrar el historial de cobros autorizados y rechazados por tarjeta. | S | OE5 |
| RF-27 | Sugerir suscripciones a partir de correos electrónicos, procesando solo metadatos o mediante un modelo local (complementario). | C | — |

### Fuera de alcance

Quedan fuera de esta versión la emisión de tarjetas reales, el análisis de extractos bancarios, la extensión de navegador, el análisis en vivo de sitios arbitrarios, el análisis de imágenes, la cancelación automática en nombre del usuario, la generación de cartas de cancelación, la solución SSI y el monitoreo con Grafana y Prometheus. Los motivos se detallan en la definición del alcance, porque ninguno de estos elementos responde a una subpregunta de investigación. Tampoco se cubren los servicios con permanencia mínima, porque bloquear la tarjeta no extingue la obligación contractual: el mecanismo solo alerta sobre la permanencia cuando la detecta en el correo de confirmación del alta.

### Requisitos no funcionales

La tabla condensa los atributos de calidad con su criterio de aceptación propuesto. Los criterios son propuestos y se validarán con el profesor de la materia y, cuando se designe, con el director o tutor; los umbrales definitivos corresponden al diseño de la validación del capítulo anterior.

| Id | Atributo | Criterio de aceptación (propuesto) | Prioridad |
|----|----------|-------------------------------------|:---------:|
| RNF-01 | Modificabilidad: el clasificador es intercambiable | Cambiar de implementación solo requiere configuración; ambas implementaciones pasan la misma suite de pruebas. | M |
| RNF-02 | Correctitud: las reglas de tarjetas son deterministas | Misma entrada, misma decisión; 100 % de cumplimiento en la suite de escenarios. | M |
| RNF-03 | Trazabilidad: toda detección y toda decisión son explicables | Cada patrón detectado referencia paso y evidencia; cada decisión del motor, las reglas aplicadas. | M |
| RNF-04 | Privacidad: ningún dato personal o financiero del usuario se envía a servicios externos | El LLM local corre en la misma máquina, por lo que ni el contenido de los flujos ni el de los correos de confirmación sale de ella; verificable mediante inspección del tráfico saliente. | M |
| RNF-05 | Seguridad de datos de tarjeta: sin números en claro | Almacenamiento tokenizado o cifrado; ausencia de números completos en registros. PCI-DSS como guía, no como certificación. | M |
| RNF-06 | Seguridad de la aplicación: protección del acceso a los datos de cada usuario | Sin hallazgos de severidad alta o crítica en el análisis con referencia a OWASP Top 10. | M |
| RNF-07 | Puntualidad: las reglas temporales se ejecutan en tiempo | Vencimiento aplicado con un desvío menor a 1 minuto; 0 cobros autorizados posteriores al vencimiento. | M |
| RNF-08 | Rendimiento de la autorización | p95 < 1 s, a contrastar con las ventanas de autorización en tiempo real de los proveedores de emisión. | S |
| RNF-09 | Rendimiento de la detección | < 30 s por flujo, con latencia medida por clasificador; la del LLM local depende del hardware (umbral definitivo en revisión). | C |
| RNF-10 | Reproducibilidad | Corpus, etiquetas y configuración versionados; la evaluación se reejecuta con un único comando. | M |
| RNF-11 | Usabilidad | Puntaje SUS ≥ 68. | S |
| RNF-12 | Portabilidad | Instalación documentada y levantada con un único comando. | S |
| RNF-13 | Extensibilidad: nuevos patrones sin modificar el motor de reglas | Agregar un patrón solo afecta al catálogo de patrones y a la fórmula de riesgo. | S |
| RNF-14 | Disponibilidad y escala | No se exige alta disponibilidad ni escalado horizontal; prototipo monousuario o de pocos usuarios concurrentes. | — |

Dos pendientes afectan a esta tabla. El umbral de latencia de RNF-09 depende del modelo y del hardware del LLM local, que no están decididos `[[DECISIÓN: modelo y tamaño del LLM local; opciones a confirmar]]` `[[DATO PENDIENTE: hardware donde corre el LLM local]]`. Además, el umbral de RNF-08 debe contrastarse con la ventana de autorización de los proveedores de emisión `[[CITA PENDIENTE: ventana de autorización en tiempo real de proveedores de emisión de tarjetas]]`.

### Trazabilidad de los objetivos específicos

La tabla asocia cada objetivo específico, cuyo enunciado completo se presenta en el Capítulo 1, con los requisitos que lo cubren.

| Objetivo | Tema | Requisitos funcionales | Requisitos no funcionales |
|----------|------|------------------------|---------------------------|
| OE1 | Caracterizar patrones y esquema | RF-01 | RNF-13 |
| OE2 | Corpus etiquetado | RF-02, RF-08, RF-10 | RNF-10 |
| OE3 | Módulo de detección y alerta | RF-03 a RF-07, RF-28 | RNF-01, RNF-03, RNF-04, RNF-09 |
| OE4 | Motor de reglas y emulador | RF-11 a RF-21 | RNF-02, RNF-03, RNF-05, RNF-07, RNF-08 |
| OE5 | Integración en prototipo web | RF-22 a RF-26 | RNF-06, RNF-11, RNF-12 |
| OE6 | Evaluación | RF-09, RF-16, RF-20 | RNF-02, RNF-07, RNF-10, RNF-11 |

El requisito RF-27, de carácter complementario, no se asocia a ningún objetivo. Fijados los requisitos, la sección siguiente describe cómo se diseñan los elementos centrales que los satisfacen.

## Diseño detallado

Esta sección muestra el diseño de los elementos que articulan el sistema: el esquema de representación del flujo, el proceso de detección y el informe de riesgo, la política de tarjeta, los puertos del clasificador y del emisor, y lo que falta definir del modelo de datos. Todo el diseño se encuentra en estado propuesto.

### Esquema de representación estructurada del flujo de cancelación

El esquema de representación (aporte A1) es el contrato central del sistema: permite analizar automáticamente los flujos de cancelación sin depender de capturas de pantalla, a partir de texto y atributos del DOM. Un flujo se captura de forma semiautomática, mediante scripts de navegación y anotación manual (RF-10), en una fecha registrada, y se exporta como JSON. La representación tiene dos niveles.

El **nivel flujo** contiene el servicio, la fecha de captura, la cantidad de pasos de alta y de baja, el canal final requerido para la baja (web, chat, teléfono o correo) y si requiere inicio de sesión. El **nivel paso** contiene la URL o el canal, los textos visibles, los elementos interactivos con su rol (acción principal, acción secundaria o enlace), los atributos de prominencia derivados del DOM y de las hojas de estilo (tamaño relativo, contraste y posición) y el tipo de acción ofrecida (cancelar, oferta de retención, redirección o información). Los flujos que terminan en canales no digitales, como el teléfono, se registran como tales, pero su contenido no se analiza.

El esquema se complementa con un **bloque de condiciones de contratación** extraídas del correo de confirmación del alta: permanencia mínima, penalidad por baja anticipada, renovación automática y precio tras la prueba. Cada condición admite el valor "no informado", que se distingue de "ausente" para no confundir la falta de información con la inexistencia de la condición. La especificación de los campos y sus tipos todavía no está cerrada `[[DATO PENDIENTE: especificación del bloque de condiciones de contratación (campos, tipos y valor "no informado") en el esquema A1 (T-028, T-030)]]`. Una vez cerrada, el esquema se publica versionado como esquema JSON derivado de los esquemas compartidos (ADR-07) y se valida con dos flujos antes de iniciar la captura del corpus.

### Proceso de detección e informe de riesgo

El módulo de detección (N1) recibe el flujo estructurado y produce un informe de riesgo en cinco pasos:

1. **Extracción de rasgos:** normalización de textos y cálculo de atributos derivados, como la asimetría entre alta y baja, la diferencia de prominencia entre las acciones de cancelar y de retener y la cantidad de ofertas de retención.
2. **Detección heurística** de los patrones estructurales, que se resuelven con reglas explícitas (por ejemplo, una baja que exige canal telefónico se registra como obstrucción).
3. **Clasificación** de los patrones semánticos mediante el puerto *Clasificador*, independiente del modelo, con dos implementaciones: el clasificador basado en un LLM local, cuya salida se valida contra un esquema, y la línea base heurística.
4. **Agregación** de los resultados en un índice de riesgo mediante una fórmula documentada y ponderada por patrón.
5. **Alerta de permanencia o costos ocultos:** el LLM local analiza el correo de confirmación del alta, extrae las condiciones de contratación con salida validada contra un esquema y, si detecta permanencia o costos ocultos, el sistema emite una alerta al usuario. El correo se procesa solo con el LLM local (RNF-04).

El subconjunto provisional de patrones abarca siete: asimetría alta/baja (*roach motel*), obstrucción, *confirmshaming*, interferencia visual, interacción forzada o *nagging*, costos o permanencia ocultos (*sneaking*) y preselección de opciones desfavorables (*preselection*). Su confirmación contra el estado del arte está pendiente y puede afectar a RF-03 y RF-04.

El **informe de riesgo** por servicio contiene la lista de patrones detectados, con el paso donde ocurren, la evidencia (elemento o texto) y la probabilidad o confianza asociada; el índice de riesgo de cancelación (niveles bajo, medio y alto); la alerta de permanencia o costos ocultos, si corresponde, con el fragmento del correo que la respalda; y la fecha de captura del flujo analizado. El índice de riesgo es la entrada que consume el motor de reglas (N2). El módulo tiene límites explícitos: no analiza imágenes ni sitios en vivo, no emite dictámenes legales (señala patrones, no incumplimientos normativos) y su resultado es válido para la fecha de captura. La alerta depende de lo que informe el correo: si una condición no figura en él, no se detecta y su ausencia se registra como tal. La fórmula del índice, sus ponderaciones y los umbrales entre niveles no están definidos todavía `[[DATO PENDIENTE: fórmula del índice de riesgo, ponderación por patrón y umbrales entre los niveles bajo, medio y alto]]`.

### Política de tarjeta y estados

Una política de tarjeta es la configuración que el motor de reglas (N2) propone a partir de los datos de la suscripción (servicio, precio, período de prueba y fecha de renovación) y del índice de riesgo del servicio (RF-11). El usuario la acepta, modifica o rechaza antes de su aplicación (RF-12). El motor soporta, como mínimo, cinco tipos de regla (RF-13): vencimiento en fecha fija, vencimiento relativo al fin del período de prueba, tope de monto por cobro, cantidad máxima de cobros y bloqueo manual.

Las políticas se almacenan como datos y se evalúan mediante funciones puras (ADR-03); no intervienen modelos probabilísticos. Cada evaluación devuelve la lista de reglas aplicadas, que se registra en la auditoría (RF-16). La autorización de un cobro verifica el vencimiento en el momento del cobro, de modo que ningún cobro posterior al vencimiento se autoriza aunque el planificador se retrase, y no invoca al clasificador ni a servicios externos (RNF-08). Cada tarjeta se asocia a una única suscripción (RF-17).

Sobre la política propuesta para cada nivel de riesgo, el diseño actual solo ofrece un ejemplo, tomado del escenario integral descrito en el Capítulo 3: para un servicio de riesgo alto con siete días de prueba, una tarjeta de un solo uso con vencimiento al fin de la prueba. La correspondencia completa entre niveles de riesgo y políticas no está definida `[[DATO PENDIENTE: política propuesta para cada nivel de riesgo (bajo, medio y alto), incluidos los valores por defecto de cada regla]]`.

La tarjeta tiene cuatro estados (RF-19): activa, congelada, vencida y destruida. Solo se conoce con certeza una transición inválida, reactivar una tarjeta destruida, que la validación del emulador debe rechazar. Tampoco está definida la relación entre la regla de bloqueo manual y el estado "congelada" `[[DATO PENDIENTE: diagrama de estados de la tarjeta con las transiciones válidas y la relación entre la regla de bloqueo manual y el estado congelada]]`.

### Puertos del clasificador y del emisor

El diseño aísla dos componentes variables detrás de puertos propios (ADR-02). El puerto *Clasificador* pertenece a N1; su entrada es un paso del flujo y un patrón, y su salida es una etiqueta, una confianza y la evidencia. Tiene dos adaptadores: el heurístico y el del LLM local (Ollama). El adaptador del LLM local invoca un proceso de la misma máquina, fija y registra la versión del modelo, la temperatura y la semilla, y valida la respuesta contra el esquema esperado antes de entregarla al puerto. El puerto *Emisor* pertenece a N3 y tiene dos adaptadores: el simulado, que es el emisor principal, y uno opcional que se conecta al *sandbox* de un proveedor real (RF-21). Las entradas y salidas del puerto *Emisor* no están especificadas `[[DATO PENDIENTE: operaciones, entradas y salidas del puerto Emisor]]`.

El análisis del correo de confirmación (RF-28) también usa el LLM local, pero el puerto *Clasificador*, definido sobre pasos de flujo y patrones, no lo contempla. Su ubicación entre los módulos y puertos es una decisión abierta, ya tratada en el capítulo anterior.

### Modelo de datos y diagrama de componentes

La arquitectura prevé una base relacional para usuarios, suscripciones, políticas, tarjetas, cobros y auditoría (ADR-04), y una bóveda con cifrado y tokens para el número de tarjeta simulado (ADR-06). El modelo entidad–relación, con sus entidades, atributos y relaciones, y el diagrama formal de componentes (UML o C4) no se elaboraron todavía `[[DATO PENDIENTE: modelo entidad–relación y diagrama de componentes formal]]`. La vista lógica del capítulo anterior es la referencia provisional.

## Implementación del prototipo

Esta sección anticipa lo que se documentará sobre la construcción del prototipo, que todavía no existe: no hay código, ni repositorio con módulos construidos, ni resultados. El prototipo se desarrollará en un repositorio propio, que se propone iniciar al cerrar el esquema del flujo, y la memoria registrará en este lugar su implementación a medida que avance.

Se documentarán los siguientes aspectos:

- **Estructura del repositorio y despliegue:** organización del código en módulos según la vista lógica (identidad y acceso, suscripciones, detección, motor de políticas, emulador de tarjetas, bóveda, auditoría, notificaciones y planificador), paquete de esquemas compartidos, comercio simulado como proceso aparte y levantado del entorno con Docker Compose.
- **Módulos del núcleo y de soporte:** implementación de N1, N2 y N3 y de las funciones de soporte, con el mapeo explícito entre los requisitos RF y RNF y los componentes que los satisfacen.
- **Scripts de captura:** scripts de navegación que exportan los flujos al formato del esquema para su anotación manual (RF-10), y procedimiento de anonimización de los correos de confirmación.
- **Adaptadores:** el adaptador heurístico y el del LLM local del puerto *Clasificador*, con el registro de modelo, versión, temperatura y semilla, y los adaptadores simulado y opcional *sandbox* del puerto *Emisor*.
- **Pruebas:** pruebas de arquitectura de los límites entre módulos, la suite de escenarios del motor y del emulador y las pruebas basadas en propiedades, en correspondencia con el diseño de la validación.
- **Reproducibilidad:** el comando único de ejecución de la evaluación y el versionado del corpus (RNF-10, RNF-12).

`[[RESULTADO PENDIENTE: implementación del prototipo N1–N3 y soporte (T-033): estructura final del repositorio, módulos construidos, adaptadores y estado de las pruebas]]`

Esta sección se completará con el prototipo construido; sus resultados de evaluación se presentan en el capítulo siguiente.

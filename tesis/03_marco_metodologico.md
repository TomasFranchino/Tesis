# Marco metodológico

Este capítulo describe cómo se concibe, se diseña y se valida SuscripGuard. Presenta el enfoque de la investigación, el proceso de selección de las tecnologías, la arquitectura propuesta con las decisiones que la sustentan, la secuencia prevista de implementación y el diseño de la validación. El capítulo se redacta en un estado intermedio del trabajo: la planificación metodológica está cerrada, pero el prototipo, el corpus y los experimentos todavía no existen. Por ese motivo, lo ya definido (requisitos, arquitectura propuesta, plan de validación) se expone en presente y lo que falta construir o medir, en futuro. Las decisiones de arquitectura se encuentran en estado **propuesto**, pendientes de revisión, y los umbrales de aceptación son **propuestos**: se ajustarán con el profesor de la materia, con el director o tutor una vez designado y con los valores reportados en el estado del arte.

## Enfoque y tipo de investigación

Esta sección ubica el trabajo desde el punto de vista metodológico y enumera los principios que ya están definidos. El encuadre formal (tipo de investigación y enfoque) no está fijado en la documentación de trabajo, por lo que queda como decisión abierta.

[[DECISIÓN: encuadre metodológico de la investigación (tipo y enfoque), a definir con el profesor de la materia en las consultas pendientes (T-017); los insumos no proponen opciones]]

Lo que sí está definido es la estructura de la validación. La pregunta principal indaga si es posible prevenir cobros recurrentes no deseados mediante tarjetas virtuales cuyas políticas de uso se configuran automáticamente a partir de la detección de *dark patterns* (patrones oscuros) en los flujos de cancelación de cada servicio. Esa pregunta se descompone en cuatro subpreguntas: la precisión de la detección de un subconjunto de patrones (SP1), la diferencia de desempeño entre un clasificador basado en un modelo de lenguaje local (LLM local, ejecutado con Ollama) y una línea base heurística (SP2), el cumplimiento verificable de las políticas por parte del motor de reglas (SP3) y la usabilidad de la solución para el usuario final (SP4).

Cada componente del núcleo de la contribución (N1, detección de *dark patterns*; N2, motor de reglas y políticas; N3, emulador de tarjetas virtuales) se valida con métricas propias, y no mediante una evaluación global única. La razón es que los tres componentes son de naturaleza distinta: N1 es probabilístico y se mide contra una verdad de referencia, mientras que N2 y N3 deben cumplir sus reglas sin excepciones y se verifican con escenarios y propiedades.

El plan de validación distingue dos categorías de resultado. Los **criterios de aceptación** son condiciones que el prototipo debe cumplir (por ejemplo, el cumplimiento del 100 % de los escenarios de reglas). Los **resultados experimentales** se reportan cualquiera sea su valor; la comparación entre el clasificador LLM local y la línea base heurística pertenece a esta categoría: que el primero supere o no a la segunda es, en sí mismo, un hallazgo y no una condición de aprobación.

La evaluación combina cuatro tipos de procedimiento, cada uno asociado a un bloque de validación:

- evaluación experimental sobre un corpus etiquetado (detección de *dark patterns* y alerta de permanencia o costos ocultos);
- pruebas basadas en escenarios y en propiedades (motor de reglas y emulador de tarjetas);
- inspección de seguridad y privacidad (análisis del tráfico saliente, búsqueda de números de tarjeta, escaneo dinámico y revisión manual);
- un estudio exploratorio de usabilidad con usuarios.

Dos principios metodológicos gobiernan el diseño técnico. El primero es que la arquitectura se deriva de los requisitos y no de las tecnologías disponibles: cada decisión se justifica con los requisitos concretos que la motivan, y la trazabilidad entre requisitos y decisiones se mantiene de forma explícita. El segundo es que la experiencia previa del tesista con determinadas tecnologías se excluye como criterio de selección tecnológica; la elección debe surgir de las necesidades del problema, y el análisis multicriterio de la sección siguiente se construye con ese criterio.

Definido este marco general, la sección siguiente detalla la selección de tecnologías, que es la decisión más sensible desde el punto de vista metodológico.

## Tecnologías y herramientas

Esta sección muestra cómo se seleccionó el lenguaje del sistema mediante un análisis multicriterio ponderado, qué resultados arroja, qué parte de ese análisis permanece sin respaldo y cuál es el stack tecnológico resultante. El backend y el frontend no se eligen por separado: la cantidad de lenguajes y la forma en que los componentes comparten sus contratos de datos dependen de la combinación. Por ello se evalúan combinaciones completas de stack.

### Cargas de trabajo y criterios descartados

El sistema combina dos cargas de trabajo con exigencias distintas. La primera es el dominio transaccional de pagos (N2 y N3): reglas que deben cumplirse al 100 % (RNF-02, requisito no funcional de correctitud), estados de tarjeta con transiciones válidas (RF-19), importes monetarios y autorizaciones concurrentes (escenario E10). En esta carga pesa que el compilador detecte errores: tipado estático, tipos suma con verificación de exhaustividad (que ningún estado ni tipo de regla quede sin tratar) y aritmética monetaria segura. La segunda es el procesamiento de flujos y la clasificación (N1): validar flujos contra un esquema (RF-01), invocar al clasificador (RF-04, RF-05) y producir informes con evidencia (RF-06). En esta carga pesan la integración con el clasificador y las herramientas de validación de esquemas.

Además, el esquema de representación del flujo de cancelación (aporte A1) atraviesa todo el sistema: lo producen los scripts de captura (RF-10), lo validan la importación y el detector (RF-01, RF-03 y RF-04), lo muestra la interfaz (RF-25) y lo consume la evaluación (RF-09). Que ese contrato tenga una única definición reduce una fuente concreta de errores.

Algunos criterios se descartaron por no discriminar entre las opciones:

| Criterio | Motivo del descarte |
|----------|---------------------|
| Rendimiento | El requisito de latencia de autorización (RNF-08, p95 < 1 s) lo cumple cualquier lenguaje de uso general `[[CITA PENDIENTE: respaldo de que lenguajes de uso general como Python, TypeScript y Kotlin cumplen holgadamente una latencia p95 < 1 s en una autorización de reglas simples]]`; la latencia de la detección (RNF-09) la domina la inferencia del modelo local, que depende del hardware y no del lenguaje del sistema. |
| Bibliotecas estadísticas | La evaluación se desacopla del sistema: este exporta las predicciones (JSON o CSV) y el análisis (métricas, *bootstrap*, McNemar, kappa) se realiza con scripts aparte en Python, con bibliotecas establecidas (SciPy, statsmodels, scikit-learn), sea cual sea el lenguaje del sistema. |
| Popularidad o mercado laboral | No responde a ningún requisito del sistema. |
| Experiencia previa del tesista | Excluida por decisión metodológica. |

### Preselección y combinaciones evaluadas

La preselección parte de los lenguajes de uso general candidatos y justifica los que pasan a la evaluación y los que se descartan.

| Opción | Resultado | Motivo |
|--------|-----------|--------|
| Python, TypeScript, Kotlin | Pasan a la evaluación | Cubren ambas cargas de trabajo. Python y TypeScript cuentan con biblioteca cliente de Ollama `[[CITA PENDIENTE: bibliotecas cliente oficiales de Ollama para Python y JavaScript/TypeScript]]`. Kotlin ofrece el sistema de tipos más estricto de los candidatos para el dominio de pagos y tiene integración con Ollama mediante Spring AI `[[CITA PENDIENTE: soporte de Ollama en Spring AI]]`. |
| Java | Representado por Kotlin | Misma plataforma; Kotlin agrega clases selladas con exhaustividad y seguridad frente a nulos. |
| C# (.NET) | Descartado | Perfil similar a Kotlin (véase la decisión abierta a continuación). |
| Go | Descartado | Sin tipos suma ni verificación de exhaustividad. |
| Rust | Descartado | Máxima seguridad de tipos, pero el costo de desarrollo no se compensa: ningún requisito de rendimiento o memoria lo justifica. |

El descarte de C# tiene una decisión abierta: el motivo inicial, vinculado a la integración con el clasificador, debe revisarse porque el clasificador se ejecuta localmente y se consume a través de una API local. `[[DECISIÓN: motivo del descarte de C#. Opciones: A) mantener el descarte solo por perfil similar a Kotlin, representado por la plataforma JVM y sin aportar un candidato distinto; B) incluir C# como quinta combinación y evaluarla. Recomendación: A, previa verificación de si existe cliente de Ollama para .NET]]` `[[CITA PENDIENTE: existencia y madurez de clientes de Ollama para .NET]]` Para Go, la ausencia de tipos suma y de verificación de exhaustividad basta para sostener el descarte. Las afirmaciones sobre las capacidades de tipado de estos lenguajes requieren respaldo `[[CITA PENDIENTE: documentación de los sistemas de tipos de Kotlin (clases selladas, nulabilidad), TypeScript (uniones discriminadas, modo estricto), Go y Rust (tipos suma)]]`.

Para el frontend, el navegador impone TypeScript (JavaScript con tipado estático) salvo que la interfaz se genere en el servidor. Por eso se evalúa también una variante con renderizado en el servidor mediante plantillas y htmx, que evita un segundo lenguaje. Las combinaciones evaluadas son cuatro:

- **S1:** Python (FastAPI) y TypeScript con React como aplicación de página única (SPA, *single-page application*).
- **S2:** Python (FastAPI) y plantillas en el servidor con htmx.
- **S3:** TypeScript de punta a punta: Node.js en el backend y TypeScript con React (SPA).
- **S4:** Kotlin (Spring Boot) y TypeScript con React (SPA).

### Criterios y pesos

Los siete criterios se derivan de los requisitos y se ponderan sobre una base de 100 puntos.

| Id | Criterio | Requisitos de origen | Peso |
|----|----------|----------------------|:----:|
| K1 | Correctitud del dominio de pagos: tipado estático verificado por el compilador, tipos suma con exhaustividad, aritmética monetaria segura, soporte de transacciones. | RNF-02, RNF-03, RF-13, RF-19, E10 | 25 |
| K2 | Integración con LLM local y validación de esquemas: biblioteca cliente de Ollama en el lenguaje del backend, salida estructurada con esquema JSON, validación de esquemas JSON y generación del esquema a partir del código. | RF-01, RF-04, RF-05 | 15 |
| K3 | Coherencia de contratos: un único esquema de flujo, informe y política compartido entre captura, detector, API e interfaz; cantidad de lenguajes del sistema. | RF-01, RF-06, RF-10, RF-25 | 15 |
| K4 | Verificabilidad: pruebas basadas en propiedades, pruebas de integración contra una base real y de extremo a extremo. | V2, V3, RNF-02 | 15 |
| K5 | Calidad de la interfaz: disponibilidad de componentes accesibles y maduros. | RNF-11, V5 | 10 |
| K6 | Seguridad y madurez web: autenticación, criptografía (AES-GCM), protecciones por defecto frente a OWASP Top 10. | RNF-05, RNF-06 | 10 |
| K7 | Costo intrínseco de desarrollo: verbosidad, configuración y ciclo de compilación y prueba para un equipo de una persona en un plazo acotado, independiente de quién programe. | Contexto del Trabajo Final | 10 |

K1 recibe el mayor peso porque N2 y N3 son la parte del núcleo que debe cumplirse sin excepciones, y un error en ellos significa un cobro indebido. Los pesos están pendientes de revisión con el profesor de la materia.

### Evaluación y resultado

Cada combinación se puntúa de 1 a 5 en cada criterio. La tabla siguiente muestra los puntajes y el puntaje ponderado resultante.

| Criterio (peso) | S1 Python + React | S2 Python + htmx | S3 TypeScript + React | S4 Kotlin + React |
|-----------------|:----:|:----:|:----:|:----:|
| K1 (25) | 3 | 3 | 4 | **5** |
| K2 (15) | **5** | **5** | **5** | 4 |
| K3 (15) | 3 | 4 | **5** | 3 |
| K4 (15) | **5** | **5** | 4 | **5** |
| K5 (10) | **5** | 3 | **5** | **5** |
| K6 (10) | 4 | 4 | 4 | **5** |
| K7 (10) | 4 | **5** | 4 | 3 |
| **Puntaje ponderado** | 4,00 | 4,05 | **4,40** | 4,35 |

S3 queda primera, pero su ventaja sobre S4 es de solo 0,05 puntos. Un 5 en K2 para S4, en lugar de 4, la haría ganar (4,50 contra 4,40). El puntaje de K2 de S4 es, por lo tanto, el dato más sensible de la tabla y necesita respaldo en fuentes (véanse los marcadores del fundamento siguiente).

El fundamento de los puntajes se resume por criterio:

- **K1.** Kotlin obtiene 5 por las clases selladas con `when` exhaustivo verificado por el compilador, la seguridad frente a nulos y `BigDecimal`. TypeScript obtiene 4: las uniones discriminadas con verificación de exhaustividad en modo estricto cubren el requisito, pero presenta dos debilidades conocidas con mitigación estándar (los tipos desaparecen en tiempo de ejecución, por lo que se valida en los bordes con esquemas, y `number` es de coma flotante, por lo que los importes se representan en enteros de unidades mínimas). Python obtiene 3: la verificación de tipos (mypy) es opcional y externa al lenguaje, y el programa corre aunque los tipos sean incorrectos. `[[CITA PENDIENTE: documentación de clases selladas y `when` exhaustivo en Kotlin; uniones discriminadas y modo estricto en TypeScript; carácter opcional de mypy en Python]]`
- **K2.** Python y TypeScript obtienen 5 porque combinan cliente, salida estructurada y validación en la misma herramienta: Ollama ofrece bibliotecas cliente para Python y JavaScript `[[CITA PENDIENTE: bibliotecas cliente oficiales de Ollama (Python, JavaScript)]]` y admite salida estructurada restringida a un esquema JSON `[[CITA PENDIENTE: salida estructurada con esquema JSON en Ollama]]`; Pydantic (Python) y Zod (TypeScript) validan el esquema y lo generan a partir del código `[[CITA PENDIENTE: generación de esquema JSON desde Pydantic y desde Zod]]`. Kotlin obtiene 4: depende de la integración de Spring AI con Ollama o de un cliente HTTP propio `[[CITA PENDIENTE: soporte de Ollama y de salida estructurada en Spring AI]]`, y la validación y generación de esquemas existen en la plataforma, pero requieren bibliotecas adicionales `[[CITA PENDIENTE: bibliotecas de esquema JSON para Kotlin/JVM]]`. Se descuenta solo un punto porque Ollama expone una API local que puede consumirse con un cliente HTTP simple o mediante la integración del framework.
- **K3.** S3 obtiene 5: un único paquete de tipos y esquemas compartido por captura, detector, API e interfaz, y Playwright, la herramienta de captura, tiene a TypeScript como lenguaje principal `[[CITA PENDIENTE: lenguajes soportados por Playwright y condición de TypeScript como lenguaje principal]]`. S2 obtiene 4: un solo lenguaje, pero la interfaz queda en plantillas sin tipado. S1 y S4 obtienen 3: dos lenguajes, con un contrato que se sincroniza generando tipos desde OpenAPI, paso que puede desincronizarse.
- **K4.** Python (Hypothesis) y la JVM (Testcontainers, jqwik, Kotest) tienen las herramientas más maduras; TypeScript cuenta con fast-check y Testcontainers para Node, algo menos maduras `[[CITA PENDIENTE: madurez comparada de herramientas de pruebas basadas en propiedades y de contenedores de prueba por ecosistema]]`.
- **K5.** React dispone de bibliotecas de componentes accesibles maduras (por ejemplo, React Aria y Radix); con htmx la accesibilidad depende de HTML escrito a mano `[[CITA PENDIENTE: bibliotecas de componentes accesibles para React]]`.
- **K6.** Spring Security es la opción más completa; las demás cubren los requisitos con bibliotecas establecidas `[[CITA PENDIENTE: capacidades de seguridad de Spring Security y alternativas en Node.js y Python]]`.
- **K7.** S2 tiene la menor configuración (un solo lenguaje, sin compilación del frontend); Kotlin con Spring tiene el ciclo de configuración y compilación más pesado.

### Análisis de sensibilidad

El análisis de sensibilidad evalúa si el ganador se mantiene al variar los pesos. Las pruebas disponibles en la documentación de trabajo (variaciones de cada peso, combinaciones aleatorias de pesos y búsqueda del punto de inversión) se calcularon con una definición anterior de K2 y no son aplicables a la tabla vigente. En consecuencia, no se reproducen sus resultados. Con S4 a solo 0,05 puntos de S3, la conclusión de robustez de la versión anterior (que la decisión solo cambia si se prioriza la seguridad de tipos del dominio de pagos muy por encima de todo lo demás, y que en ese caso la alternativa es S4 y no Python) queda en suspenso.

`[[RESULTADO PENDIENTE: análisis de sensibilidad del ADR-07 recalculado con K2 vigente (script del análisis de sensibilidad, T-016), incluida la confirmación o corrección de la conclusión de robustez]]`

### Decisión propuesta y mitigaciones

Se propone la combinación **S3**, TypeScript de punta a punta, con la siguiente composición:

- **Backend:** TypeScript sobre Node.js (versión de soporte de largo plazo, LTS), con NestJS como framework. Sus módulos e inyección de dependencias coinciden con el monolito modular (ADR-01) y con los puertos y adaptadores (ADR-02) `[[CITA PENDIENTE: modelo de módulos e inyección de dependencias de NestJS]]`.
- **Frontend:** TypeScript con React, como SPA compilada con Vite, y una biblioteca de componentes accesibles.
- **Esquemas compartidos:** un paquete común con los esquemas en Zod (flujo, informe de riesgo, política, cobro), del que se derivan los tipos de TypeScript y el esquema JSON publicado como parte del aporte A1.
- **Captura de flujos:** Playwright con TypeScript.
- **Análisis estadístico:** scripts en Python, fuera del sistema, sobre las predicciones exportadas.

Como la decisión acepta una menor garantía del compilador que Kotlin en el dominio de pagos, se establecen mitigaciones obligatorias de las debilidades de K1:

- modo `strict` del compilador y prohibición de `any` mediante reglas de lint;
- importes siempre en enteros de unidades mínimas, con un tipo diferenciado (`Money`) que impide mezclarlos con números comunes;
- validación con Zod en todo borde de entrada: API, importación de flujos y respuestas del clasificador;
- estados de tarjeta y tipos de regla como uniones discriminadas con verificación exhaustiva;
- acceso a datos mediante un constructor de consultas SQL que permita bloqueo explícito de filas (por ejemplo, Kysely o Drizzle) para resolver E10.

Entre las consecuencias favorables figuran un único lenguaje en el sistema, un contrato único para el esquema del flujo (a la vez aporte de la tesis y eje de todos los módulos) y una herramienta de captura en su lenguaje principal. Entre las desfavorables, la menor garantía del compilador, que se compensa con las mitigaciones anteriores y con la suite de escenarios y las pruebas basadas en propiedades de V2, y la presencia de un segundo lenguaje (Python) para el análisis estadístico, fuera del sistema.

### Stack tecnológico propuesto

La tabla resume el stack resultante y la decisión que justifica cada componente. Los detalles de cada decisión se desarrollan en la sección siguiente.

| Componente | Tecnología propuesta | Decisión que la justifica |
|------------|----------------------|---------------------------|
| Estilo arquitectónico | Monolito modular | ADR-01 |
| Backend | TypeScript sobre Node.js (LTS) con NestJS | ADR-07 (S3), ADR-01 |
| Frontend | TypeScript con React, SPA compilada con Vite, biblioteca de componentes accesibles (a elegir) | ADR-07, ADR-08 |
| Esquemas y contratos | Paquete común de esquemas en Zod | ADR-07 |
| Clasificador | Puerto *Clasificador* con adaptador heurístico y adaptador LLM local (Ollama; modelo y tamaño por decidir) | ADR-02 |
| Emisor de tarjetas | Puerto *Emisor* con adaptador simulado y adaptador *sandbox* opcional | ADR-02 |
| Motor de reglas | Evaluador propio con políticas como datos y funciones puras | ADR-03 |
| Base de datos | PostgreSQL; constructor de consultas SQL con bloqueo de filas (Kysely o Drizzle, a elegir) | ADR-04, ADR-07 |
| Corpus | JSON y etiquetas versionados en el repositorio | ADR-04 |
| Planificación de tareas | Proceso de barrido periódico (≤ 30 s) sobre la base | ADR-05 |
| Datos de tarjeta | Módulo Bóveda con cifrado autenticado y tokens | ADR-06 |
| Captura de flujos | Playwright con TypeScript | ADR-07 |
| Análisis estadístico | Scripts en Python (SciPy, statsmodels, scikit-learn), fuera del sistema | ADR-07 |
| Despliegue | Docker Compose | ADR-09 |

## Diseño de la solución y arquitectura del sistema

Esta sección presenta la arquitectura propuesta: los factores que la condicionan, su vista lógica y cada decisión de diseño con las alternativas consideradas. Todas las decisiones se registran como registros de decisión de arquitectura (ADR, *architecture decision records*) abreviados, con estado propuesto, y cada una se vincula con los requisitos que la justifican.

### Factores que condicionan la arquitectura

La tabla siguiente relaciona cada factor con su origen y con la consecuencia que impone al diseño.

| Factor | Origen | Consecuencia |
|--------|--------|--------------|
| Clasificador intercambiable: comparación entre un LLM local (Ollama) y una línea base heurística | RNF-01, RF-05, SP2 | Aislar el clasificador detrás de una interfaz propia. |
| Reglas deterministas, trazables y con control de concurrencia (E10) | RNF-02, RNF-03 | Evaluación de reglas en código propio, sobre datos con consistencia transaccional. |
| Autorización independiente de servicios externos, p95 < 1 s | RNF-08 | La ruta de autorización no invoca al clasificador ni a la red externa. |
| Vencimientos puntuales que sobreviven a reinicios | RNF-07 | Planificación persistida, no en memoria. |
| Privacidad: los datos del usuario no salen del sistema | RNF-04 | Frontera explícita entre el módulo de detección (datos públicos) y el resto. |
| Datos de tarjeta nunca en claro | RNF-05 | Almacenamiento separado y cifrado. |
| Reproducibilidad de la evaluación | RNF-10 | Corpus como artefacto versionado, fuera de la base operativa. |
| Sin exigencia de alta disponibilidad ni escalado; un solo desarrollador; plazo acotado `[[DATO PENDIENTE: confirmar el plazo de desarrollo; los insumos lo estiman en unos cinco meses y aún no hay fecha final de entrega]]` | RNF-14, contexto del Trabajo Final | No hay motivo para desplegar componentes por separado. |

### Vista lógica

La vista lógica propuesta organiza el sistema como un monolito modular con tres actores externos al proceso principal: el comercio simulado, el LLM local y el corpus versionado. El diagrama muestra los módulos y sus dependencias.

```
                         ┌──────────────────────── SuscripGuard (monolito modular) ───────────────────────┐
  Usuario ──► Frontend ──┤  API                                                                            │
                         │   │                                                                             │
                         │   ├─► Identidad y acceso                                                        │
                         │   ├─► Suscripciones ──────────────► Motor de políticas (N2) ──► Auditoría       │
                         │   │                                   ▲            │                             │
                         │   │                         índice de riesgo       │ política                    │
                         │   │                                   │            ▼                             │
                         │   ├─► Detección de dark patterns (N1) ┘   Emulador de tarjetas (N3) ◄── Bóveda  │
                         │   │        │ puerto «Clasificador»           │ puerto «Emisor»        (cifrado) │
                         │   │        ├─ adaptador heurístico           ├─ adaptador simulado              │
                         │   │        └─ adaptador LLM local ────────┐  └─ adaptador sandbox (opcional)    │
                         │   │                                       │                                     │
                         │   └─► Notificaciones ◄── Planificador (barrido periódico sobre la base)        │
                         └──────────────────────────────────────────┼───────────────────────────────────────┘
                                                                    │ interfaz propia (misma máquina)
  Comercio simulado (proceso aparte) ──► endpoint de autorización   ▼
                                                            Ollama (LLM local, proceso en la misma máquina)
  Corpus versionado (JSON + etiquetas, repositorio) ──► importación (RF-01) y evaluación por lotes (RF-09)
```

El módulo de detección (N1) alimenta con el índice de riesgo al motor de políticas (N2), que propone y aplica la política sobre el emulador de tarjetas (N3). La bóveda protege los datos de tarjeta, la auditoría recibe cada decisión del motor y el planificador materializa los vencimientos y dispara las alertas a través del módulo de notificaciones. El diagrama todavía no refleja dónde se ubica el análisis del correo de confirmación del alta (RF-28); ese punto figura entre los pendientes de la sección.

### Monolito modular (ADR-01)

Se considera la elección del estilo arquitectónico a partir de tres alternativas: microservicios, monolito modular y monolito sin límites internos. Los requisitos piden modificabilidad (clasificador intercambiable, patrones extensibles; RNF-01, RNF-13) y consistencia estricta en la autorización de cobros (RNF-02), pero no piden escalado independiente, alta disponibilidad ni despliegues separados (RNF-14).

| Dimensión | A. Microservicios | B. Monolito modular | C. Monolito sin límites internos |
|-----------|-------------------|---------------------|----------------------------------|
| Complejidad operativa | Alta (red, descubrimiento, despliegues múltiples) | Baja | Baja |
| Consistencia en la autorización (E10) | Difícil: el estado de tarjeta, política y cobros quedaría repartido y requeriría transacciones distribuidas o compensaciones | Simple: una transacción local | Simple |
| Modificabilidad (RNF-01, RNF-13) | Alta | Alta, mediante interfaces entre módulos | Baja |
| Escalado independiente | Sí | No | No |
| Esfuerzo para un desarrollador en un plazo acotado | Alto | Medio | Bajo al inicio, alto al mantener |
| Evidencia para la tesis | Pruebas complicadas por la red | Pruebas de integración directas | Difícil aislar componentes para evaluarlos |

`[[CITA PENDIENTE: respaldo de la comparación entre microservicios y monolito modular en consistencia transaccional y complejidad operativa]]` Se propone la opción B: una única aplicación desplegable dividida en módulos con responsabilidades y dependencias explícitas, que se comunican por interfaces internas y no por red. La única ventaja propia de los microservicios, el escalado y el despliegue independientes, no responde a ningún requisito. Hay dos excepciones: el comercio simulado corre como proceso aparte porque representa un actor externo, de modo que la autorización se prueba a través de su interfaz real, y el LLM local corre como proceso aparte pero en la misma máquina, invocado a través del adaptador del puerto *Clasificador*; no es un servicio remoto. El riesgo de acoplamiento entre módulos se mitiga con dependencias solo a través de las interfaces públicas de cada módulo, verificadas con pruebas de arquitectura. La decisión se revisaría si apareciera un requisito de escalado o disponibilidad.

### Puertos y adaptadores para el clasificador y el emisor (ADR-02)

El módulo N1 define un puerto *Clasificador* (entrada: paso del flujo y patrón; salida: etiqueta, confianza y evidencia) con dos adaptadores: heurístico y LLM local (Ollama). El módulo N3 define un puerto *Emisor* con dos adaptadores: simulado y *sandbox* (entorno de pruebas) de un proveedor real, este último opcional. Se descartan dos alternativas. Invocar al LLM local directamente desde la lógica de negocio es más simple al comienzo, pero acopla el módulo a un entorno de ejecución y a un modelo concretos e impide la comparación que exige SP2. Delegar la clasificación en un servicio remoto de terceros enviaría el contenido de los flujos fuera de la máquina y haría depender los resultados de la disponibilidad y de los cambios del proveedor; queda fuera del diseño por una decisión previa del tesista de procesar localmente.

Como consecuencia, la comparación entre clasificadores (V1) se reduce a ejecutar la misma evaluación con distinta configuración. El adaptador del LLM local invoca un proceso que corre en la misma máquina, por lo que el contenido de los flujos analizados no sale de ella, lo que facilita verificar RNF-04. Como la salida de un modelo de lenguaje puede variar entre ejecuciones, el adaptador debe fijar y registrar la versión del modelo, la temperatura y la semilla (a definir) y validar la respuesta contra el esquema esperado antes de entregarla al puerto `[[CITA PENDIENTE: respaldo de que fijar temperatura y semilla reduce la variabilidad de la salida en el entorno de ejecución elegido]]`.

### Motor de reglas propio y declarativo (ADR-03)

Se consideran tres opciones: un motor de reglas genérico (por ejemplo, Drools o bibliotecas de reglas en JSON), reglas escritas directamente en los controladores, o un evaluador propio con políticas almacenadas como datos y evaluadas por funciones puras. Se propone la tercera. Los tipos de regla son solo cinco (RF-13); un motor genérico agrega un lenguaje y una dependencia que no se aprovechan, y las reglas en los controladores impiden probarlas de forma aislada.

Las funciones puras permiten pruebas basadas en propiedades y determinismo verificable (V2). Cada evaluación devuelve la lista de reglas aplicadas, que se guarda en la auditoría (RNF-03). La autorización valida el vencimiento en el momento del cobro: aunque el planificador se atrase, no se autoriza ningún cobro posterior al vencimiento.

### Persistencia relacional y corpus versionado (ADR-04)

Se propone una base de datos relacional con transacciones ACID y bloqueo por fila (PostgreSQL) para usuarios, suscripciones, políticas, tarjetas, cobros y auditoría `[[CITA PENDIENTE: propiedades transaccionales y bloqueo por fila de PostgreSQL]]`. El corpus (flujos JSON, etiquetas y guía) se versiona en el repositorio y se importa a la base, pero la fuente de verdad es el repositorio. Una base documental resulta menos adecuada para verificar límites con cobros concurrentes; SQLite es viable para un prototipo, pero con concurrencia de escritura limitada, que es lo que prueba E10 `[[CITA PENDIENTE: limitaciones de concurrencia de escritura de SQLite]]`. Con esta decisión, E10 se resuelve con una transacción que bloquea la tarjeta durante la autorización, y la evaluación es reproducible desde una versión etiquetada del corpus.

### Planificación por barrido periódico (ADR-05)

Para los vencimientos puntuales y las alertas se consideran tres opciones: un planificador en memoria, que pierde las tareas al reiniciar e incumpliría el escenario E08; una cola de tareas con *broker* (Celery y Redis) o un motor de flujos de trabajo (Temporal); o un proceso que cada 30 segundos o menos consulta en la base las tarjetas a vencer y las alertas pendientes y las procesa de forma idempotente. Se propone la tercera: el estado de las tareas pendientes ya está en la base, por lo que sobrevive a reinicios sin infraestructura adicional, y con ese intervalo se cumple el desvío menor a un minuto exigido por RNF-07. Las alternativas con *broker* resuelven problemas de volumen y de flujos largos que el prototipo no tiene. La corrección de los cobros no depende del planificador (ADR-03): este solo materializa el cambio de estado y dispara las alertas.

### Bóveda para datos de tarjeta (ADR-06)

Un módulo *Bóveda* guarda el número de tarjeta simulado cifrado con cifrado autenticado (por ejemplo, AES-GCM) y entrega al resto del sistema un token. La clave se toma de la configuración del entorno, nunca de la base; la interfaz solo muestra el número enmascarado, salvo en la emisión, y los registros del sistema contienen únicamente el token `[[CITA PENDIENTE: respaldo de AES-GCM como cifrado autenticado y de las prácticas de tokenización de PCI-DSS usadas como guía]]`. Un gestor de secretos externo (por ejemplo, HashiCorp Vault) excede las necesidades del prototipo, y guardar el número en claro incumpliría RNF-05. Con esta decisión, la verificación de V4 (búsqueda de números con el algoritmo de Luhn en base, registros y API) tiene un único punto de control. PCI-DSS se usa como guía y no como certificación.

### Frontend como SPA (ADR-08)

Se consideran una SPA en React compilada con Vite, un meta-framework con renderizado en servidor (Next.js) y plantillas en el servidor con htmx (esta última evaluada como S2). Se propone la SPA: ningún requisito exige renderizado en servidor, optimización para buscadores ni rutas en el borde, y Next.js agregaría un segundo servidor de aplicación sin cubrir ninguna necesidad, dado que el backend debe existir por separado porque aloja el planificador (ADR-05) y el dominio transaccional. La SPA se sirve como archivos estáticos y consume la API tipada con los esquemas compartidos. Entre React, Vue y Svelte, que son técnicamente adecuadas, se elige React por la madurez de sus bibliotecas de componentes accesibles, que incide de forma directa en RNF-11 y en la prueba de usabilidad (V5).

### Despliegue en contenedores (ADR-09)

Se propone Docker Compose con tres servicios: aplicación, base de datos y comercio simulado. Se levanta con un único comando, lo que asegura que la evaluación se pueda reproducir en otro equipo, incluido el del tribunal (RNF-12, RNF-10). Queda pendiente decidir si Ollama corre dentro de este despliegue o en el equipo anfitrión.

### Revisión de la propuesta tecnológica preliminar

El diseño parte de una propuesta tecnológica preliminar que se revisó a la luz de los requisitos. La tabla indica qué se conserva, qué se reemplaza o elimina y por qué.

| Tecnología de la propuesta preliminar | Decisión | Motivo |
|---------------------------------------|----------|--------|
| Microservicios | Reemplazada por monolito modular | ADR-01 |
| FastAPI (Python) | Reemplazada por TypeScript sobre Node.js (NestJS) | ADR-07: análisis multicriterio; Python se conserva solo para los scripts de análisis estadístico |
| Next.js 15, TailwindCSS y shadcn/ui | Next.js reemplazado por SPA React con Vite; la biblioteca de componentes se elige por accesibilidad | ADR-08: no hay requisito de renderizado en servidor |
| PostgreSQL | Se mantiene | ADR-04 |
| Redis (colas y caché) | Eliminada | Sin requisito de caché; colas innecesarias por ADR-05 |
| Celery y Temporal | Eliminadas | ADR-05 |
| Ollama y LLM local | Incorporada | Adaptador del clasificador (ADR-02), comparado en V1 con la línea base heurística; modelo y tamaño pendientes |
| Gmail API e IMAP | Fuera del núcleo | Solo si se implementa RF-27 (Could) |
| Stripe Issuing y Lithic | Adaptador opcional | RF-21 (Could); el emisor principal es el simulado |
| OAuth2, JWT y 2FA | Se reduce a autenticación con sesión o JWT | RNF-06 exige autenticación y control de acceso; 2FA e inicio de sesión con terceros no responden a ningún requisito |
| WebSockets | Eliminado | No hay requisito de tiempo real en la interfaz |
| Grafana y Prometheus | Eliminadas | Fuera de alcance (RNF-14) |
| Docker Compose | Se mantiene | ADR-09 |

### Aspectos pendientes del diseño

La arquitectura propuesta tiene puntos aún sin resolver, que se listan para que el lector distinga lo definido de lo abierto:

- el modelo de datos (entidad–relación) y el diagrama de componentes formal (UML o C4) `[[DATO PENDIENTE: modelo entidad–relación y diagrama de componentes formal]]`;
- si Ollama corre dentro del despliegue con Docker Compose o en el equipo anfitrión `[[DECISIÓN: ubicación de Ollama; opciones A) dentro de Docker Compose, B) en el equipo anfitrión; el insumo no trae recomendación]]`;
- cómo se materializa en los módulos y puertos existentes el requisito RF-28 (análisis del correo de confirmación del alta y alerta de permanencia o costos ocultos), cuyo diseño original hablaba de una alerta previa a la contratación `[[DECISIÓN: materialización de RF-28 en los módulos y puertos; el puerto *Clasificador* se define sobre pasos de flujo y patrones, y el correo de confirmación no encaja en esa entrada]]`;
- modelo, tamaño y hardware del LLM local `[[DECISIÓN: modelo y tamaño del LLM local; opciones a confirmar]]` `[[DATO PENDIENTE: hardware donde corre el LLM local]]`, de los que depende la latencia de detección (RNF-09);
- el protocolo de fijación de versión, temperatura y semilla del modelo local.

Con la arquitectura propuesta, corresponde describir en qué orden se construirá y se medirá el sistema.

## Fases de implementación

Esta sección muestra la secuencia prevista de las etapas de implementación y evaluación, derivada de las dependencias entre tareas del plan de trabajo. No se asignan fechas: la entrega final no tiene fecha fijada. El orden refleja que cada etapa produce el insumo de la siguiente, y que el corpus y el prototipo son el camino crítico.

| Etapa | Contenido | Depende de | Producto |
|-------|-----------|------------|----------|
| 1. Esquema del flujo | Esquema JSON del flujo de cancelación (aporte A1), versionado, que incluye el bloque de condiciones de contratación extraídas del correo de confirmación (T-030) | Especificación del bloque de condiciones de contratación (T-028) y trabajo previo del plan sobre los patrones a representar | Esquema publicado y validado con dos flujos |
| 2. Captura del corpus | Captura de 15 a 20 servicios, incluidos los correos de confirmación del alta, con datos personales anonimizados y fecha de captura (T-031) | Esquema del flujo | Flujos y correos anonimizados en el directorio de evidencia del corpus |
| 3. Anotación | Etiquetado por el tesista, anotación independiente de un segundo anotador y cálculo de kappa por patrón mediante script (T-032) | Guía de etiquetado (T-027) y corpus capturado | Verdad de referencia y kappa por patrón |
| 4. Prototipo | Construcción de N1, N2, N3 y los módulos de soporte (T-033); se propone iniciarlo al cerrar el esquema del flujo | Esquema del flujo | Prototipo que permite ejecutar los criterios de V2 y V3 |
| 5. Evaluación | Ejecución de V1 a V5 y análisis de resultados (T-034) | Anotación y prototipo | Resultados con metadatos en el directorio de evidencia de resultados |

`[[DATO PENDIENTE: la tarea de evaluación del plan de trabajo cubre V1 a V5; confirmar en qué etapa se ejecuta el escenario integral V6]]`

Dos observaciones sobre las dependencias. Primero, el prototipo depende solo del esquema del flujo y no del corpus anotado; por lo tanto, su construcción puede avanzar en paralelo con la captura y la anotación, y la evaluación es el punto donde ambas líneas convergen. Segundo, la guía de etiquetado es un insumo de la anotación y debe estar completa antes de entregar los flujos al segundo anotador, ya que este recibe solo la guía y los flujos. El diseño de esa evaluación se describe a continuación.

## Diseño de la validación

Esta sección muestra cómo se validará cada componente: qué se mide, sobre qué instancias, con qué instrumento y contra qué umbral. Todos los umbrales son propuestos y se ajustarán con el profesor de la materia, con el director o tutor una vez designado y con los valores del estado del arte. Ningún resultado de esta validación existe todavía.

### Bloques de validación

La validación se organiza en cinco bloques, uno por componente o atributo de calidad, y un escenario integral final.

| Bloque | Qué valida | Subpregunta | Tipo de evaluación |
|--------|------------|:-----------:|--------------------|
| V1 | Detección de *dark patterns* (N1) | SP1, SP2 | Experimental, sobre corpus etiquetado |
| V2 | Motor de reglas y políticas (N2) | SP3 | Pruebas basadas en escenarios |
| V3 | Emulador de tarjetas (N3) y rendimiento | SP3 | Pruebas funcionales y de carga |
| V4 | Seguridad y privacidad | — (requisitos no funcionales) | Análisis estático y dinámico e inspección |
| V5 | Usabilidad | SP4 | Prueba con usuarios (SUS) |
| V6 | Escenario integral | Pregunta principal | Demostración reproducible de extremo a extremo |

### Corpus y anotación (V1)

El corpus se compone de 15 a 20 servicios por suscripción, con prioridad para los servicios de uso en Argentina y los casos documentados. La unidad de análisis es el par (paso del flujo, patrón); adicionalmente se evalúan el nivel (flujo, patrón) y el índice de riesgo por servicio. Para cada servicio se conserva también el correo de confirmación del alta recibido al crear la cuenta de prueba, con los datos personales anonimizados, y se etiqueta, por campo, la presencia y el valor de las condiciones de contratación (permanencia mínima, penalidad por baja anticipada, renovación automática y precio tras la prueba).

La **guía de etiquetado** define de forma operativa cada uno de los siete patrones del subconjunto provisional (asimetría alta/baja, obstrucción, *confirmshaming*, interferencia visual, interacción forzada o *nagging*, costos o permanencia ocultos y preselección de opciones desfavorables), con ejemplos positivos y negativos, y se elabora a partir de las taxonomías del estado del arte. El subconjunto está pendiente de confirmación contra la literatura `[[CITA PENDIENTE: taxonomías de dark patterns que respaldan cada uno de los siete patrones del subconjunto]]`.

Para controlar el sesgo del anotador, un segundo anotador etiqueta de forma independiente al menos el 30 % del corpus. Se propone a Román Zenobi, profesor de la materia Trabajo Final y no involucrado en el diseño del sistema, sujeto a su aceptación; la alternativa es un compañero de carrera o un docente del área. El protocolo es ciego: el segundo anotador recibe solo la guía y los flujos en formato legible, sin acceso a las etiquetas del tesista ni a las salidas del sistema. Antes de la anotación se realiza una sesión de calibración con un flujo del conjunto de diseño, excluido del cálculo de kappa. Los desacuerdos se discuten después de calcular kappa y se resuelven para formar la verdad de referencia final. El esfuerzo estimado del segundo anotador es del orden de 200 a 300 juicios (de cinco a seis flujos, de cinco a ocho pasos y siete patrones), unas dos a tres horas. Se calcula el coeficiente kappa de Cohen por patrón, con el criterio κ ≥ 0,61 (acuerdo sustancial); los patrones por debajo de ese valor se redefinen o se excluyen del análisis `[[CITA PENDIENTE: coeficiente kappa de Cohen y la interpretación de 0,61 como acuerdo sustancial]]`.

Para evitar el sobreajuste, dado que las heurísticas y las preguntas al clasificador se diseñan observando datos, el corpus se divide en un conjunto de diseño (alrededor del 30 %, de cinco a seis servicios) y un conjunto de prueba (alrededor del 70 %) que no se consulta hasta la evaluación final.

### Métricas y criterios de aceptación de V1

Las métricas de V1 se calculan en tres niveles, resumidos en la tabla.

| Métrica | Nivel | Uso |
|---------|-------|-----|
| Precisión, *recall* (exhaustividad) y F1 por patrón | Paso–patrón | Desempeño de cada patrón |
| F1 macro | Paso–patrón | Resumen global comparable entre clasificadores |
| Tasa de falsos positivos | Paso–patrón | Mide los avisos erróneos de patrón |
| Curva precisión–*recall* por umbral | Paso–patrón | Aprovecha las probabilidades del clasificador para elegir el umbral de operación |
| Exactitud y kappa ponderado del nivel de riesgo | Servicio | Concordancia entre el índice calculado y el asignado por el anotador |
| Latencia p50 y p95 y uso de recursos por flujo | Flujo | Comparación operativa entre clasificadores |

El costo de los errores es asimétrico. Un falso positivo produce una política más restrictiva de lo necesario, pero el usuario la revisa y puede modificarla antes de aplicarla (RF-12). Un falso negativo deja una política laxa sobre un servicio riesgoso. Por eso se prioriza el *recall*. Los criterios de aceptación propuestos son:

- *recall* macro ≥ 0,75 y precisión macro ≥ 0,70 en el conjunto de prueba, para al menos una de las implementaciones del clasificador;
- exactitud del nivel de riesgo por servicio ≥ 0,80;
- latencia por flujo < 30 s (RNF-09), cuyo umbral para el clasificador LLM local depende del hardware donde se ejecuta y no de la red `[[DECISIÓN: umbral de latencia para el clasificador LLM local. Opciones: A) mantener < 30 s medido en el hardware de evaluación declarado; B) fijar un umbral distinto una vez conocidos el modelo y el hardware. Recomendación: B si el modelo elegido no cumple 30 s en el hardware disponible]]` `[[DATO PENDIENTE: hardware donde corre el LLM local]]`.

Un punto metodológico abierto afecta a la exactitud del nivel de riesgo. El plan la define como la concordancia entre el índice calculado y el nivel asignado por el anotador, pero no existe todavía una definición operativa de los niveles bajo, medio y alto para el anotador. Sin ella, esa exactitud no puede medirse de forma independiente de la fórmula del índice, ya que el anotador terminaría reproduciendo la fórmula. `[[DECISIÓN: definición operativa de los niveles de riesgo bajo, medio y alto para el anotador, independiente de la fórmula del índice; el insumo no propone opciones y debe acordarse con el profesor (T-017)]]` Hasta que se resuelva, el criterio de exactitud ≥ 0,80 se mantiene como propuesto sin la garantía de independencia.

### Comparación entre clasificadores (SP2)

La comparación enfrenta dos implementaciones del puerto *Clasificador*: un clasificador basado en un modelo de lenguaje local (LLM local, ejecutado con Ollama) y una línea base heurística. Ambas se evalúan sobre las mismas instancias del conjunto de prueba. Se reportan las diferencias de F1 con intervalos de confianza por *bootstrap* (remuestreo con reposición) y la prueba de McNemar sobre las predicciones pareadas `[[CITA PENDIENTE: método bootstrap para intervalos de confianza de diferencias de F1 y prueba de McNemar para clasificadores pareados]]`. Los análisis se realizan con scripts en Python y bibliotecas establecidas, a partir de las predicciones exportadas por el sistema.

En cada ejecución del clasificador LLM local se registran el modelo, la versión o etiqueta, la cuantización, la temperatura, la semilla, el hardware y la fecha. Se fijan para que la evaluación pueda repetirse, ya que la salida de un modelo de lenguaje puede variar entre ejecuciones y entre equipos. La latencia (p50 y p95) se mide por separado para cada implementación y se reporta junto con el hardware, porque en el clasificador LLM local depende de este. La variación entre ejecuciones se estima con repeticiones de la evaluación `[[DECISIÓN: número de repeticiones por ejecución del clasificador LLM local; el insumo no propone opciones]]`.

### Validación de la alerta de permanencia o costos ocultos (RF-28)

La alerta se valida sobre los correos de confirmación del alta del corpus, con la misma partición diseño/prueba que los flujos del servicio correspondiente. Las métricas son la precisión, el *recall* y el F1 de la extracción por campo (permanencia mínima, penalidad por baja anticipada, renovación automática, precio tras la prueba) y la precisión y el *recall* de la alerta por servicio. Los correos que no informan una condición se etiquetan como "no informado", categoría distinta de "ausente", para no contar como acierto la falta de información. Se registran las mismas condiciones de ejecución del LLM local que en la comparación entre clasificadores.

El criterio de aceptación de la alerta no está fijado `[[DECISIÓN: umbral de aceptación de la alerta, a acordar con el profesor; el insumo recomienda priorizar el recall de la alerta por el mismo argumento de costo asimétrico]]`. Además, el alcance prioriza servicios sin permanencia, por lo que el corpus puede contener pocos correos con permanencia o costos ocultos; por eso se reportan conteos absolutos junto con las métricas `[[DECISIÓN: agregar correos de servicios con permanencia documentada solo para evaluar la alerta; el insumo recomienda hacerlo si el corpus base tiene menos de cinco casos positivos]]`.

### Motor de reglas, emulador, seguridad, usabilidad y escenario integral (V2 a V6)

**V2, motor de reglas y políticas.** Se ejecuta una suite de doce escenarios mínimos (E01 a E12, detallados en el Anexo A) que cubren cobros dentro y fuera de la política vigente (vencimiento, tope de monto y cantidad máxima de cobros), tarjetas congeladas, bloqueadas o destruidas, el reinicio del sistema antes de un vencimiento, la modificación de la política por el usuario, los cobros simultáneos (E10), la propuesta de política según el nivel de riesgo y la alerta previa a la renovación. Los criterios son: 100 % de escenarios aprobados (RNF-02), cero cobros autorizados indebidamente, desvío del vencimiento menor a un minuto (RNF-07) y 100 % de las decisiones registradas en la auditoría con las reglas evaluadas (RF-16, RNF-03). El determinismo se verifica repitiendo cada escenario con resultado idéntico, y se complementa con pruebas basadas en propiedades (generación aleatoria de políticas y cobros, contrastados con un oráculo independiente).

**V3, emulador de tarjetas y rendimiento.** Se prueban todas las transiciones válidas de la máquina de estados de la tarjeta y se verifica que las inválidas sean rechazadas (por ejemplo, reactivar una tarjeta destruida). El rendimiento de autorización se mide con una prueba de carga con una herramienta específica (por ejemplo, k6 o Locust), con una carga acorde a un prototipo (decenas de solicitudes concurrentes) y el criterio p95 < 1 s (RNF-08). La independencia se verifica midiendo la autorización con el clasificador LLM local detenido. La ventana de autorización en tiempo real de los proveedores de emisión, con la que debe contrastarse el umbral, está pendiente de verificación `[[CITA PENDIENTE: ventana de autorización en tiempo real de proveedores de emisión de tarjetas]]`.

**V4, seguridad y privacidad.** La tabla resume los instrumentos y criterios.

| Requisito | Instrumento | Criterio |
|-----------|-------------|----------|
| RNF-04, privacidad | Registro e inspección del tráfico saliente durante la ejecución completa de las pruebas de extremo a extremo, incluido el análisis de correos de confirmación | 0 solicitudes externas con datos del usuario; el clasificador LLM local corre en la misma máquina, por lo que ni el contenido de los flujos ni el de los correos sale de ella |
| RNF-05, datos de tarjeta | Búsqueda automatizada de números de tarjeta (patrón y verificación de Luhn) en base de datos, registros y respuestas de la API | 0 hallazgos en claro |
| RNF-06, seguridad de la aplicación | Escaneo dinámico (por ejemplo, OWASP ZAP) y revisión manual guiada por OWASP Top 10 | 0 hallazgos de severidad alta o crítica sin mitigar |

`[[CITA PENDIENTE: OWASP Top 10, OWASP ZAP, verificación de Luhn y PCI-DSS como guía]]`

**V5, usabilidad.** Es un estudio exploratorio con 10 a 15 personas adultas con al menos dos suscripciones activas, sin exigir formación en informática. Las tareas son registrar una suscripción con período de prueba, consultar el informe de riesgo del servicio, aceptar o ajustar la política propuesta e identificar por qué se rechazó un cobro. Se aplica el cuestionario SUS (*System Usability Scale*, escala de usabilidad del sistema), con criterio de puntaje medio ≥ 68 (RNF-11) `[[CITA PENDIENTE: instrumento SUS y puntaje promedio de referencia de 68]]`, y se mide la tasa de finalización de tareas, con criterio ≥ 80 %. El tiempo por tarea se reporta sin umbral. Una pregunta de comprensión pide al participante explicar con sus palabras por qué su tarjeta tiene esa política, para medir si la explicación del riesgo es entendible (RNF-03). Se descarta el indicador NPS (*net promoter score*) porque mide intención de recomendación y no usabilidad, y con una muestra de este tamaño no aporta información confiable `[[CITA PENDIENTE: respaldo de que NPS mide intención de recomendación y no usabilidad]]`. En lo ético, se requiere consentimiento informado, uso de datos ficticios (los participantes no usan tarjetas ni cuentas reales) y anonimización de los resultados.

**V6, escenario integral.** Es una demostración reproducible que recorre la contribución completa: se analiza un flujo del corpus con riesgo alto (por ejemplo, un servicio cuyo flujo exige canal telefónico o chat de retención); el sistema genera el informe de riesgo con evidencia; el usuario registra una suscripción con siete días de prueba y acepta la política propuesta (tarjeta de un solo uso con vencimiento al fin de la prueba); el comercio simulado intenta el primer cobro al finalizar la prueba; el cobro es rechazado y el usuario ve el motivo y la regla aplicada. El criterio es que el escenario se complete sin intervención manual fuera de las acciones del usuario, y que cada paso quede registrado en la auditoría.

### Matriz resumen

La matriz relaciona cada componente con su subpregunta, los requisitos que cubre, la métrica, el instrumento y el umbral propuesto.

| Componente | Subpregunta | Requisitos | Métrica | Instrumento | Umbral propuesto |
|------------|:-----------:|------------|---------|-------------|------------------|
| N1 Detección | SP1 | RF-03 a RF-07, RF-09 | *Recall* y precisión macro | Corpus etiquetado (conjunto de prueba) | ≥ 0,75 y ≥ 0,70 |
| N1 Detección | SP1 | RF-07 | Exactitud del nivel de riesgo | Corpus etiquetado | ≥ 0,80 (sujeto a la definición operativa pendiente) |
| N1 Detección | SP2 | RF-05 | ΔF1 entre clasificadores | *Bootstrap* y McNemar | Se reporta |
| N1 Detección | SP2 | RNF-09 | Latencia p95 y uso de recursos por flujo | Registro de ejecución con hardware declarado | < 30 s (sujeto a la decisión sobre el umbral) |
| N1 Alerta | SP1 | RF-28 | Precisión y *recall* por campo y de la alerta | Correos de confirmación etiquetados | Por decidir |
| Corpus | SP1 | RF-08 | Kappa de Cohen | Doble anotación ≥ 30 % | ≥ 0,61 |
| N2 Motor | SP3 | RF-11 a RF-16, RNF-02 | Porcentaje de escenarios aprobados | Suite E01–E12 y pruebas por propiedades | 100 % |
| N2 Motor | SP3 | RNF-07 | Desvío del vencimiento | Pruebas temporales | < 1 min |
| N3 Emulador | SP3 | RF-17 a RF-20, RNF-08 | Latencia de autorización p95 | Prueba de carga | < 1 s |
| Seguridad | — | RNF-04 a RNF-06 | Hallazgos | Tráfico saliente, búsqueda de números de tarjeta, OWASP ZAP | 0 / 0 / 0 altos |
| Plataforma | SP4 | RNF-11 | SUS y finalización de tareas | Prueba con usuarios | ≥ 68 y ≥ 80 % |

### Amenazas a la validez

Las amenazas identificadas y sus mitigaciones se resumen a continuación.

| Amenaza | Mitigación |
|---------|------------|
| Corpus pequeño y tomado en una fecha: los resultados no se generalizan a todos los servicios ni a cambios posteriores. | Se declara como limitación; se registra la fecha de captura; se reportan intervalos de confianza. |
| Sesgo del anotador: el tesista diseña el sistema y etiqueta el corpus. | Segundo anotador independiente y cálculo de kappa. |
| Sobreajuste de heurísticas y preguntas al corpus. | Conjunto de prueba reservado y no consultado durante el diseño. |
| Variabilidad del modelo local: la salida del LLM puede cambiar entre ejecuciones, versiones del modelo, cuantizaciones o equipos. | Registro de modelo, versión, cuantización, temperatura, semilla y hardware; parámetros fijados; repeticiones de la evaluación para estimar la variación; línea base heurística determinista como referencia. |
| Pocos casos positivos en la alerta: el alcance prioriza servicios sin permanencia. | Se reportan conteos absolutos junto con las métricas; posible incorporación de correos de servicios con permanencia documentada (decisión pendiente). |
| El emulador no reproduce todas las condiciones de una red de pagos real. | Se declara el alcance simulado; adaptador para un *sandbox* real como demostración opcional. |
| Muestra de usabilidad reducida y no representativa. | Se reporta como estudio exploratorio; se documenta el perfil de participantes. |

Este diseño de validación fija qué se medirá y con qué criterio. Los requisitos que el prototipo debe satisfacer, el diseño detallado de sus componentes y el estado de su implementación se desarrollan en el capítulo siguiente.

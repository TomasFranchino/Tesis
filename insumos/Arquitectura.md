# Arquitectura y decisiones de diseño — SuscripGuard

> **Estado:** borrador v0.2 (29/09/2026) — decisiones **propuestas**, pendientes de revisión. v0.2: ADR-07 y ADR-08 reescritos con análisis multicriterio.
> Responde a los puntos 3 y 4 de la devolución de la Entrega 1: cada decisión se justifica a partir de requisitos concretos de *Requisitos.md* v1.0, no de las tecnologías disponibles.
> Formato: registros de decisión de arquitectura (ADR) abreviados.

---

## 1. Factores que condicionan la arquitectura

| Factor | Origen | Consecuencia |
|--------|--------|--------------|
| Clasificador intercambiable y dependencia de un servicio externo en acceso anticipado | RNF-01, RF-05, riesgo de Jev | Aislar el clasificador detrás de una interfaz propia. |
| Reglas deterministas, trazables y con control de concurrencia (E10) | RNF-02, RNF-03 | Evaluación de reglas en código propio, sobre datos con consistencia transaccional. |
| Autorización independiente de servicios externos, p95 < 1 s | RNF-08 | La ruta de autorización no invoca al clasificador ni a la red externa. |
| Vencimientos puntuales que sobreviven a reinicios | RNF-07 | Planificación persistida, no en memoria. |
| Privacidad: datos del usuario nunca salen del sistema | RNF-04 | Frontera explícita entre el módulo de detección (datos públicos) y el resto. |
| Datos de tarjeta nunca en claro | RNF-05 | Almacenamiento separado y cifrado. |
| Reproducibilidad de la evaluación | RNF-10 | Corpus como artefacto versionado, fuera de la base operativa. |
| Sin exigencia de alta disponibilidad ni escalado; un solo desarrollador; ~5 meses | RNF-14, contexto del Trabajo Final | No hay motivo para desplegar componentes por separado. |

---

## 2. Vista lógica propuesta

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
                         │   │        ├─ adaptador Jev ──────────────┐  └─ adaptador sandbox (opcional)    │
                         │   │        └─ adaptador LLM local (opc.)  │                                     │
                         │   └─► Notificaciones ◄── Planificador (barrido periódico sobre la base)        │
                         └──────────────────────────────────────────┼───────────────────────────────────────┘
                                                                    │ solo flujos del corpus (datos públicos)
  Comercio simulado (proceso aparte) ──► endpoint de autorización   ▼
                                                            TypeSafe AI (externo)
  Corpus versionado (JSON + etiquetas, repositorio) ──► importación (RF-01) y evaluación por lotes (RF-09)
```

---

## 3. Registros de decisión

### ADR-01: Estilo arquitectónico — monolito modular

**Estado:** Propuesto · **Requisitos:** RNF-14, RNF-12, RNF-01, RNF-13, RNF-02

**Contexto.** La Entrega 1 proponía microservicios sin justificación desde los requisitos. Los requisitos piden modificabilidad (clasificador intercambiable, patrones extensibles) y consistencia estricta en la autorización de cobros, pero **no** piden escalado independiente, alta disponibilidad ni despliegues separados.

**Opciones consideradas.**

| Dimensión | A. Microservicios | B. Monolito modular | C. Monolito sin límites internos |
|-----------|-------------------|---------------------|----------------------------------|
| Complejidad operativa | Alta (red, descubrimiento, despliegues múltiples) | Baja | Baja |
| Consistencia en la autorización (E10) | Difícil: el estado de tarjeta, política y cobros quedaría repartido; requiere transacciones distribuidas o compensaciones | Simple: una transacción local | Simple |
| Modificabilidad (RNF-01, RNF-13) | Alta | Alta, mediante interfaces entre módulos | Baja |
| Escalado independiente | Sí | No | No |
| Esfuerzo para un desarrollador en ~5 meses | Alto | Medio | Bajo al inicio, alto al mantener |
| Evidencia para la tesis | Pruebas complicadas por la red | Pruebas de integración directas | Difícil aislar componentes para evaluarlos |

**Decisión.** Opción B: una única aplicación desplegable, dividida en módulos con responsabilidades y dependencias explícitas (sección 2). Los módulos se comunican por interfaces internas, no por red.

**Justificación.** La modificabilidad que piden los requisitos se obtiene con límites internos bien definidos (ADR-02), sin pagar el costo de la distribución. La única ventaja propia de los microservicios, el escalado y despliegue independientes, no responde a ningún requisito (RNF-14). Además, la consistencia de la autorización es más simple y verificable en un solo proceso.

**Excepciones.** El **comercio simulado** corre como proceso aparte porque representa un actor externo: así la autorización se prueba a través de su interfaz real. El **clasificador externo** es, por definición, un servicio remoto.

**Consecuencias.**
- (+) Menos infraestructura; pruebas de extremo a extremo más simples.
- (+) Los límites entre módulos permiten extraer un servicio en el futuro si aparece un requisito que lo justifique.
- (–) Hay que cuidar que los módulos no se acoplen. Mitigación: dependencias solo a través de interfaces públicas de cada módulo, verificadas con pruebas de arquitectura.
- **Revisar si:** apareciera un requisito de escalado o disponibilidad (queda como trabajo futuro).

---

### ADR-02: Puertos y adaptadores para el clasificador y el emisor

**Estado:** Propuesto · **Requisitos:** RF-05, RNF-01, RF-21, RNF-04

**Decisión.** El módulo N1 define un puerto *Clasificador* (entrada: paso del flujo y patrón; salida: etiqueta, confianza y evidencia) con tres adaptadores: heurístico, Jev y LLM local (opcional). El módulo N3 define un puerto *Emisor* con dos adaptadores: simulado y *sandbox* de un proveedor real (opcional).

**Alternativas.** Invocar el servicio externo directamente desde la lógica de negocio: más simple al comienzo, pero ata la tesis a un proveedor en acceso anticipado e impide la comparación que exige SP2.

**Consecuencias.** La comparación entre clasificadores (V1) se reduce a ejecutar la misma evaluación con distinta configuración. El adaptador de Jev es el **único** punto del sistema con salida a Internet desde N1, lo que facilita verificar RNF-04.

---

### ADR-03: Motor de reglas propio y declarativo

**Estado:** Propuesto · **Requisitos:** RF-13, RNF-02, RNF-03, RNF-08

**Opciones.** (a) Motor de reglas genérico (p. ej. Drools o bibliotecas de reglas en JSON); (b) reglas escritas directamente en los controladores; (c) evaluador propio: políticas almacenadas como datos y evaluadas por funciones puras.

**Decisión.** Opción (c). Son solo cinco tipos de regla (RF-13). Un motor genérico agrega un lenguaje y una dependencia que no se aprovechan, y las reglas en los controladores impiden probarlas de forma aislada.

**Consecuencias.** Las funciones puras permiten pruebas basadas en propiedades y determinismo verificable (V2). Cada evaluación devuelve la lista de reglas aplicadas, que se guarda en la auditoría (RNF-03). La autorización valida el vencimiento **en el momento del cobro**: aunque el planificador se atrase, no se autoriza ningún cobro posterior al vencimiento.

---

### ADR-04: Persistencia relacional transaccional y corpus versionado

**Estado:** Propuesto · **Requisitos:** RNF-02 (E10), RF-16, RNF-10

**Decisión.** Base de datos relacional con transacciones ACID y bloqueo por fila (**PostgreSQL**) para usuarios, suscripciones, políticas, tarjetas, cobros y auditoría. El **corpus** (flujos JSON, etiquetas y guía) se versiona en el repositorio y se importa a la base, pero la fuente de verdad es el repositorio.

**Alternativas.** Base documental: menos adecuada para verificar límites con cobros concurrentes. SQLite: viable para un prototipo, pero con concurrencia de escritura limitada, que es justamente lo que prueba E10.

**Consecuencias.** E10 se resuelve con una transacción que bloquea la tarjeta durante la autorización. La evaluación es reproducible desde una versión etiquetada del corpus.

---

### ADR-05: Planificación por barrido periódico sobre la base

**Estado:** Propuesto · **Requisitos:** RNF-07, RF-14, RF-15

**Opciones.** (a) Planificador en memoria: pierde las tareas al reiniciar e incumple E08. (b) Cola de tareas con *broker* (Celery + Redis) o motor de flujos de trabajo (Temporal). (c) Proceso que cada ≤ 30 s consulta en la base las tarjetas a vencer y las alertas pendientes, y las procesa de forma idempotente.

**Decisión.** Opción (c). El estado de las tareas pendientes ya está en la base, por lo que sobrevive a reinicios sin infraestructura adicional. Con un intervalo de 30 s se cumple el desvío menor a 1 minuto. Las opciones (b) resuelven problemas de volumen y de flujos largos que el prototipo no tiene.

**Consecuencias.** Se eliminan Redis, Celery y Temporal del stack preliminar. La correctitud de los cobros no depende del planificador (ADR-03): el planificador solo materializa el cambio de estado y dispara las alertas.

---

### ADR-06: Bóveda interna para datos de tarjeta

**Estado:** Propuesto · **Requisitos:** RNF-05, RNF-06

**Decisión.** Un módulo *Bóveda* guarda el número de tarjeta simulado cifrado con cifrado autenticado (p. ej. AES-GCM) y entrega al resto del sistema un **token**. La clave se toma de la configuración del entorno, nunca de la base. La interfaz solo muestra el número enmascarado, salvo en la emisión. Los logs registran únicamente el token.

**Alternativas.** Un gestor de secretos externo (p. ej. HashiCorp Vault) excede las necesidades del prototipo. Guardar el número en claro incumple RNF-05.

**Consecuencias.** La verificación de V4 (búsqueda de números con Luhn en base, logs y API) tiene un único punto de control. PCI-DSS se usa como guía, no como certificación.

---

### ADR-07: Lenguajes del sistema (backend y frontend)

**Estado:** Propuesto · **Requisitos:** RNF-02, RNF-03, RF-01, RF-04, RF-05, RF-06, RF-10, RF-25, RNF-05, RNF-06, RNF-11 · **Método:** análisis multicriterio ponderado con análisis de sensibilidad

**Contexto.** El backend y el frontend no se eligen por separado: la cantidad de lenguajes y la forma en que los componentes comparten sus contratos de datos dependen de la combinación. Por eso se evalúan **combinaciones de stack** completas. Se excluye deliberadamente la experiencia previa del tesista como criterio: la elección debe surgir de las necesidades del problema.

#### 7.1. Qué exige el problema a un lenguaje

El sistema combina dos cargas de trabajo con exigencias distintas:

1. **Dominio transaccional de pagos (N2, N3):** reglas que deben cumplirse al 100 % (RNF-02), estados de tarjeta con transiciones válidas (RF-19), importes monetarios y autorizaciones concurrentes (E10). Aquí pesa que el **compilador detecte errores**: tipado estático, tipos suma con verificación de exhaustividad (que ningún estado o tipo de regla quede sin tratar) y aritmética monetaria segura.
2. **Procesamiento de flujos y clasificación (N1):** validar flujos contra un esquema (RF-01), invocar al clasificador (RF-04, RF-05) y producir informes con evidencia (RF-06). Aquí pesan la integración con el clasificador y las herramientas de esquemas.

Además, el **esquema del flujo de cancelación** (aporte A1) atraviesa todo el sistema: lo producen los scripts de captura (RF-10), lo validan la importación y el detector (RF-01, RF-03/04), lo muestra la interfaz (RF-25) y lo consume la evaluación (RF-09). Que ese contrato tenga una única definición reduce una fuente concreta de errores.

#### 7.2. Criterios descartados por no discriminar entre opciones

| Criterio | Por qué no discrimina |
|----------|-----------------------|
| Rendimiento | RNF-08 (p95 < 1 s en la autorización) lo cumple cualquier lenguaje de uso general con holgura; la latencia de la detección (RNF-09) la domina la llamada de red al clasificador, no el lenguaje. |
| Bibliotecas estadísticas | La evaluación se desacopla: el sistema exporta las predicciones (JSON/CSV) y el análisis (métricas, *bootstrap*, McNemar, kappa) se realiza con scripts aparte en Python con bibliotecas establecidas (SciPy, statsmodels, scikit-learn), sea cual sea el lenguaje del sistema. Así se usan implementaciones validadas de los métodos estadísticos y se evita programarlos a mano. |
| Popularidad o mercado laboral | No responde a ningún requisito del sistema. |
| Experiencia previa del tesista | Excluida por decisión metodológica. |

#### 7.3. Preselección

| Opción | Resultado | Motivo |
|--------|-----------|--------|
| Python, TypeScript, Kotlin | Pasan a la evaluación | Cubren ambas cargas de trabajo; Python y TypeScript cuentan con SDK oficial de TypeSafe AI; Kotlin ofrece el sistema de tipos más estricto de los candidatos para el dominio de pagos y tiene integración con Jev mediante Spring AI. |
| Java | Representado por Kotlin | Misma plataforma; Kotlin agrega clases selladas con exhaustividad y seguridad frente a nulos. |
| C# (.NET) | Descartado | Perfil similar a Kotlin, sin SDK ni integración documentada con el clasificador. |
| Go | Descartado | Sin tipos suma ni verificación de exhaustividad; sin SDK del clasificador. |
| Rust | Descartado | Máxima seguridad de tipos, pero el costo de desarrollo no se compensa: ningún requisito de rendimiento o memoria lo justifica. |

Para el frontend, el navegador impone **TypeScript** (JavaScript con tipado estático) salvo que la interfaz se genere en el servidor. Por eso se evalúa también una variante con renderizado en el servidor (plantillas + htmx), que evita un segundo lenguaje.

**Combinaciones evaluadas:**
- **S1:** Python (FastAPI) + TypeScript/React (SPA)
- **S2:** Python (FastAPI) + plantillas en el servidor con htmx
- **S3:** TypeScript de punta a punta: Node.js en el backend + TypeScript/React (SPA)
- **S4:** Kotlin (Spring Boot) + TypeScript/React (SPA)

#### 7.4. Criterios y pesos

| Id | Criterio | Requisitos de origen | Peso |
|----|----------|----------------------|:----:|
| K1 | **Correctitud del dominio de pagos:** tipado estático verificado por el compilador, tipos suma con exhaustividad, aritmética monetaria segura, soporte de transacciones. | RNF-02, RNF-03, RF-13, RF-19, E10 | 25 |
| K2 | **Integración con el clasificador y esquemas:** SDK oficial de Jev, validación de esquemas JSON y generación del esquema a partir del código. | RF-01, RF-04, RF-05 | 15 |
| K3 | **Coherencia de contratos:** un único esquema de flujo, informe y política compartido entre captura, detector, API e interfaz; cantidad de lenguajes del sistema. | RF-01, RF-06, RF-10, RF-25 | 15 |
| K4 | **Verificabilidad:** pruebas basadas en propiedades, pruebas de integración contra una base real y de extremo a extremo. | V2, V3, RNF-02 | 15 |
| K5 | **Calidad de la interfaz:** disponibilidad de componentes accesibles y maduros. | RNF-11, V5 | 10 |
| K6 | **Seguridad y madurez web:** autenticación, criptografía (AES-GCM), protecciones por defecto frente a OWASP Top 10. | RNF-05, RNF-06 | 10 |
| K7 | **Costo intrínseco de desarrollo:** verbosidad, configuración y ciclo de compilación y prueba para un equipo de una persona en ~5 meses, independiente de quién programe. | Contexto del Trabajo Final | 10 |

K1 tiene el mayor peso porque N2 y N3 son la parte del núcleo que debe cumplirse sin excepciones, y un error ahí significa un cobro indebido.

#### 7.5. Evaluación (escala 1–5)

| Criterio (peso) | S1 Python + React | S2 Python + htmx | S3 TypeScript + React | S4 Kotlin + React |
|-----------------|:----:|:----:|:----:|:----:|
| K1 (25) | 3 | 3 | 4 | **5** |
| K2 (15) | **5** | **5** | **5** | 3 |
| K3 (15) | 3 | 4 | **5** | 3 |
| K4 (15) | **5** | **5** | 4 | **5** |
| K5 (10) | **5** | 3 | **5** | **5** |
| K6 (10) | 4 | 4 | 4 | **5** |
| K7 (10) | 4 | **5** | 4 | 3 |
| **Puntaje ponderado** | 4,00 | 4,05 | **4,40** | 4,20 |

**Fundamento de los puntajes:**

- **K1.** *Kotlin (5):* clases selladas con `when` exhaustivo verificado por el compilador, seguridad frente a nulos y `BigDecimal`. *TypeScript (4):* uniones discriminadas con verificación de exhaustividad en modo estricto. Tiene dos debilidades conocidas con mitigación estándar: los tipos desaparecen en tiempo de ejecución (se valida en los bordes con esquemas) y `number` es de coma flotante (los importes se representan en enteros de unidades mínimas, p. ej. centavos). *Python (3):* la verificación de tipos (mypy) es opcional y externa al lenguaje; el programa corre aunque los tipos sean incorrectos.
- **K2.** TypeSafe AI publica SDK oficiales para Python y para JavaScript/TypeScript sobre una API HTTP. Kotlin depende de la integración de Spring AI o de un cliente HTTP propio. Pydantic (Python) y Zod (TypeScript) validan el esquema y generan el esquema JSON a partir del código.
- **K3.** *S3 (5):* un único paquete de tipos y esquemas compartido por captura, detector, API e interfaz; además, Playwright, la herramienta de captura, tiene a TypeScript como lenguaje principal. *S2 (4):* un solo lenguaje, pero la interfaz queda en plantillas sin tipado. *S1 y S4 (3):* dos lenguajes; el contrato se sincroniza generando tipos desde OpenAPI, lo que funciona pero agrega un paso que puede desincronizarse.
- **K4.** Python (Hypothesis) y la JVM (Testcontainers, jqwik/Kotest) tienen las herramientas más maduras. TypeScript cuenta con fast-check y Testcontainers para Node, algo menos maduras.
- **K5.** React dispone de bibliotecas de componentes accesibles maduras (p. ej. React Aria, Radix). Con htmx la accesibilidad depende de HTML escrito a mano.
- **K6.** Spring Security es la opción más completa. Las demás cubren los requisitos con bibliotecas establecidas.
- **K7.** S2 tiene la menor configuración (un solo lenguaje, sin compilación del frontend). Kotlin y Spring tienen el ciclo de configuración y compilación más pesado.

#### 7.6. Análisis de sensibilidad

| Prueba | Resultado |
|--------|-----------|
| Cada peso ±10 puntos (uno por vez, renormalizando) | S3 gana en las 14 variaciones; empata con S4 en dos casos (K2 −10 y K3 −10). |
| 100 000 combinaciones aleatorias de pesos, variación moderada alrededor de los pesos base | S3 gana en el 96,6 %; S4 en el 3,4 %. |
| 100 000 combinaciones aleatorias de pesos, variación amplia | S3 gana en el 80,1 %; S4 en el 18,6 %; S2 en el 1,2 %. |
| Punto de inversión | S4 supera a S3 solo si K1 pesa ≥ 32 y K3 ≤ 8, es decir, si se considera que la seguridad de tipos del dominio vale más del triple que tener un contrato único. |

La decisión es **robusta**: solo cambia si se prioriza la seguridad de tipos del dominio de pagos muy por encima de todo lo demás. En ese caso la alternativa es S4 (Kotlin), no Python.

#### 7.7. Decisión

**S3 — TypeScript de punta a punta:**
- **Backend:** TypeScript sobre Node.js (versión LTS), con NestJS como framework. Sus módulos e inyección de dependencias coinciden con el monolito modular (ADR-01) y con los puertos y adaptadores (ADR-02).
- **Frontend:** TypeScript con React, como SPA compilada con Vite, y una biblioteca de componentes accesibles.
- **Esquemas compartidos:** un paquete común con los esquemas en Zod (flujo, informe de riesgo, política, cobro), del que se derivan los tipos de TypeScript y el esquema JSON publicado como parte del aporte A1.
- **Captura de flujos:** Playwright con TypeScript.
- **Análisis estadístico:** scripts en Python, fuera del sistema, sobre las predicciones exportadas.

**Mitigaciones de las debilidades de K1 (obligatorias):**
- Modo `strict` del compilador y prohibición de `any` mediante reglas de lint.
- Importes siempre en enteros de unidades mínimas, con un tipo diferenciado (`Money`) que impide mezclarlos con números comunes.
- Validación con Zod en todo borde de entrada: API, importación de flujos y respuestas del clasificador.
- Estados de tarjeta y tipos de regla como uniones discriminadas con verificación exhaustiva.
- Acceso a datos mediante un constructor de consultas SQL que permita bloqueo explícito de filas (p. ej. Kysely o Drizzle) para resolver E10.

**Consecuencias.**
- (+) Un solo lenguaje en el sistema y un contrato único para el esquema del flujo, que es a la vez aporte de la tesis y eje de todos los módulos.
- (+) SDK oficial del clasificador y herramienta de captura en su lenguaje principal.
- (–) Menor garantía del compilador que Kotlin en el dominio de pagos. Se compensa con las mitigaciones anteriores y con la suite de escenarios y pruebas basadas en propiedades de V2, que valida RNF-02 al 100 %.
- (–) El análisis estadístico queda en un segundo lenguaje, pero fuera del sistema y solo como herramienta de análisis.

---

### ADR-08: Arquitectura del frontend — SPA sin framework de renderizado en servidor

**Estado:** Propuesto · **Requisitos:** RF-22 a RF-26, RNF-11, RNF-12

**Opciones.** (a) SPA en React compilada con Vite; (b) meta-framework con renderizado en servidor (Next.js); (c) plantillas en el servidor con htmx (evaluada como S2 en ADR-07).

**Decisión.** Opción (a). Ningún requisito exige renderizado en el servidor, SEO ni rutas en el borde. Next.js agregaría un segundo servidor de aplicación sin cubrir ninguna necesidad, y el backend igual debe existir por separado porque aloja el planificador (ADR-05) y el dominio transaccional. La SPA se sirve como archivos estáticos y consume la API tipada con los esquemas compartidos.

**Por qué React y no Vue o Svelte.** Las tres son técnicamente adecuadas. React se elige por la madurez de sus bibliotecas de componentes accesibles, que impactan de forma directa en RNF-11 y en la prueba de usabilidad (V5).

---

### ADR-09: Despliegue en contenedores

**Estado:** Propuesto · **Requisitos:** RNF-12, RNF-10

**Decisión.** Docker Compose con tres servicios: aplicación, base de datos y comercio simulado. Se levanta con un único comando, lo que asegura que la evaluación se pueda reproducir en otro equipo, incluido el del tribunal.

---

## 4. Revisión del stack preliminar (Entrega 1)

| Tecnología propuesta en la Entrega 1 | Decisión | Motivo |
|--------------------------------------|----------|--------|
| Microservicios | Reemplazada por monolito modular | ADR-01 |
| FastAPI (Python) | Reemplazada por TypeScript sobre Node.js (NestJS) | ADR-07: análisis multicriterio; Python se conserva solo para los scripts de análisis estadístico |
| Next.js 15 + TailwindCSS + shadcn/ui | Next.js reemplazado por SPA React + Vite; la biblioteca de componentes se elige por accesibilidad | ADR-08: no hay requisito de renderizado en servidor |
| PostgreSQL | Se mantiene | ADR-04 |
| Redis (colas y caché) | Eliminada | Sin requisito de caché; colas innecesarias por ADR-05 |
| Celery / Temporal | Eliminadas | ADR-05 |
| Ollama + LLM local | Opcional | Tercer clasificador en V1 o módulo complementario de correos (RF-27) |
| Gmail API / IMAP | Fuera del núcleo | Solo si se implementa RF-27 (Could) |
| Stripe Issuing / Lithic | Adaptador opcional | RF-21 (Could); el emisor principal es el simulado |
| OAuth2 + JWT + 2FA | Se reduce a autenticación con sesión o JWT | RNF-06 exige autenticación y control de acceso; 2FA e inicio de sesión con terceros no responden a ningún requisito |
| WebSockets | Eliminado | No hay requisito de tiempo real en la interfaz |
| Grafana + Prometheus | Eliminadas | Fuera de alcance (RNF-14) |
| Docker Compose | Se mantiene | ADR-09 |
| **Jev (TypeSafe AI)** | Incorporada | Adaptador del clasificador (ADR-02) |

---

## 5. Trazabilidad requisito → decisión

| Requisito | Decisiones |
|-----------|------------|
| RNF-01 / RF-05 | ADR-02, ADR-07 |
| RNF-02 | ADR-01, ADR-03, ADR-04, ADR-07 (mitigaciones de tipado) |
| RNF-03 | ADR-03 |
| RNF-04 | ADR-02 (única salida externa en N1) |
| RNF-05 | ADR-06 |
| RNF-07 | ADR-05 (+ validación en el cobro, ADR-03) |
| RNF-08 | ADR-01, ADR-03 |
| RNF-10 | ADR-04, ADR-09 |
| RNF-12 | ADR-08, ADR-09 |
| RNF-11 | ADR-07 (K5), ADR-08 |
| RF-01 / RF-10 / RF-25 | ADR-07 (esquemas compartidos) |
| RNF-13 | ADR-01, ADR-02 |
| RNF-14 | ADR-01, ADR-05 |

---

## 6. Pendientes

- Revisar con el profesor de la materia los pesos del análisis multicriterio de ADR-07.
- Revisar en la documentación de TypeSafe AI las limitaciones conocidas de la versión del modelo (jev-1.13) antes de diseñar las preguntas al clasificador.
- Verificar en la documentación de TypeSafe AI el SDK disponible, los límites de uso y los términos para publicar resultados.
- Elaborar el modelo de datos (entidad–relación) y el diagrama de componentes formal (UML o C4) para el capítulo 3.3.

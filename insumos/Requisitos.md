# Requisitos del sistema — SuscripGuard

> **Estado:** v1.1 (02/10/2026) — la v1.0 fue revisada y aprobada por el tesista (29/09/2026). v1.1: aplicadas decisiones B1 y B2 (actor "LLM local (Ollama)" en lugar del clasificador externo; RF-04, RF-05, RNF-04 y RNF-09 ajustados; nuevo RF-28). **Los cambios de v1.1 están pendientes de revisión del tesista.** Responde al punto 3 de la devolución de la Entrega 1: los requisitos se definen **antes** que la arquitectura, y cada decisión tecnológica posterior (Arquitectura.md) deberá referenciar los requisitos que la justifican.
> Base: *Contribucion y alcance.md* (componentes N1–N3, soporte, complementario) y *Objetivos.md* (OE1–OE6).
> Prioridad según MoSCoW: **M** (Must, imprescindible) · **S** (Should, importante) · **C** (Could, deseable) · **W** (Won't, fuera de alcance en esta versión).

---

## 1. Actores

| Actor | Descripción |
|-------|-------------|
| Usuario | Persona que registra sus suscripciones, consulta el riesgo de cada servicio y gestiona sus tarjetas virtuales. |
| Curador del corpus | Rol administrativo (en el prototipo, el tesista) que captura, importa y etiqueta flujos de cancelación. |
| Comercio simulado | Sistema externo simulado que genera solicitudes de cobro sobre las tarjetas virtuales. |
| LLM local (Ollama) | Proceso local, ejecutado en la misma máquina que el prototipo, que corre el modelo de lenguaje y es invocado a través de una interfaz propia. Ya no es un servicio externo de terceros. |
| Planificador (tiempo) | Disparador de las reglas temporales (vencimientos y alertas). |

---

## 2. Requisitos funcionales

### 2.1. N1 — Detección de *dark patterns*

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-01 | El sistema debe permitir importar un flujo de cancelación en formato JSON y validarlo contra el esquema de representación definido. | M | OE1, OE3 |
| RF-02 | El sistema debe registrar los metadatos de cada captura (servicio, fecha, versión del esquema, curador). | M | OE2 |
| RF-03 | El sistema debe detectar los patrones estructurales mediante reglas heurísticas explícitas. | M | OE3 |
| RF-04 | El sistema debe clasificar los patrones semánticos mediante la implementación de clasificador configurada: clasificador basado en un modelo de lenguaje local (LLM local, ejecutado con Ollama) o línea base heurística. | M | OE3 |
| RF-05 | El sistema debe permitir cambiar la implementación del clasificador (clasificador LLM local o línea base heurística) por configuración, sin modificar el resto del módulo. | M | OE3 |
| RF-06 | El sistema debe generar, por servicio, un informe con los patrones detectados, el paso donde ocurren, la evidencia asociada y la confianza de cada detección. | M | OE3 |
| RF-07 | El sistema debe calcular un índice de riesgo de cancelación (bajo / medio / alto) mediante una fórmula documentada y parametrizable. | M | OE3 |
| RF-08 | El sistema debe permitir registrar etiquetas manuales (verdad de referencia) por paso y patrón. | M | OE2 |
| RF-09 | El sistema debe ejecutar la evaluación por lotes sobre el corpus y calcular precisión, *recall*, F1 y tasa de falsos positivos por patrón y por clasificador. | S | OE6 |
| RF-10 | El sistema debería asistir la captura de flujos mediante scripts de navegación que exporten el JSON para su posterior anotación manual. | S | OE2 |
| RF-28 | El sistema debe emitir una alerta previa a la contratación cuando el flujo de alta de un servicio presenta permanencia mínima o costos ocultos. (Numerado a continuación de RF-27 para conservar los identificadores existentes; pertenece a N1.) | `[[DECISIÓN: prioridad M o S — recomendación: M, porque B1(c) la incorpora como parte del mecanismo preventivo; S si se prefiere no comprometer el núcleo y dejarla sujeta al tiempo disponible]]` | OE3 |

### 2.2. N2 — Motor de reglas y políticas

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-11 | El sistema debe proponer una política de tarjeta a partir de los datos de la suscripción y del índice de riesgo del servicio. | M | OE4 |
| RF-12 | El usuario debe poder aceptar, modificar o rechazar la política propuesta antes de su aplicación. | M | OE4 |
| RF-13 | El motor debe soportar, como mínimo, las reglas: vencimiento en fecha fija, vencimiento relativo al fin del período de prueba, tope de monto por cobro, cantidad máxima de cobros y bloqueo manual. | M | OE4 |
| RF-14 | El sistema debe ejecutar automáticamente las reglas temporales (vencer o destruir la tarjeta en la fecha programada). | M | OE4 |
| RF-15 | El sistema debería emitir alertas al usuario con una anticipación configurable a la renovación o al vencimiento. | S | OE4 |
| RF-16 | El sistema debe registrar cada decisión del motor (entrada, reglas evaluadas, resultado y fecha) para su auditoría. | M | OE4, OE6 |

### 2.3. N3 — Emulador de tarjetas virtuales

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-17 | El sistema debe emitir una tarjeta virtual simulada asociada a una única suscripción. | M | OE4 |
| RF-18 | El sistema debe procesar solicitudes de cobro simuladas y autorizarlas o rechazarlas según las políticas vigentes, indicando el motivo del rechazo. | M | OE4 |
| RF-19 | El sistema debe gestionar los estados de la tarjeta (activa, congelada, vencida, destruida) y sus transiciones válidas. | M | OE4 |
| RF-20 | El sistema debe incluir un comercio simulado capaz de ejecutar escenarios de cobro predefinidos (cobros en fecha, posteriores al vencimiento, superiores al tope, repetidos). | M | OE4, OE6 |
| RF-21 | El sistema podría integrar un proveedor real en modo *sandbox* a través de la interfaz de adaptador. | C | OE4 |

### 2.4. Soporte

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-22 | El sistema debe permitir el registro e inicio de sesión de usuarios. | M | OE5 |
| RF-23 | El usuario debe poder registrar manualmente una suscripción (servicio, precio, frecuencia, fin del período de prueba, fecha de renovación). | M | OE5 |
| RF-24 | El sistema debe mostrar un panel con las suscripciones, la tarjeta asociada, el nivel de riesgo del servicio y el gasto mensual estimado. | M | OE5 |
| RF-25 | El usuario debe poder consultar el informe de riesgo de un servicio con la evidencia de cada patrón detectado. | M | OE5 |
| RF-26 | El sistema debería mostrar el historial de cobros autorizados y rechazados por tarjeta. | S | OE5 |

### 2.5. Complementario

| Id | Requisito | Prioridad | OE |
|----|-----------|:---------:|:--:|
| RF-27 | El sistema podría sugerir suscripciones a partir de correos electrónicos, procesando solo metadatos o mediante un modelo local. | C | — |

### 2.6. Fuera de alcance (W)

Emisión de tarjetas reales, análisis de extractos bancarios, extensión de navegador, análisis en vivo de sitios arbitrarios, análisis de imágenes, cancelación automática en nombre del usuario, cartas de cancelación, SSI y monitoreo con Grafana/Prometheus. Motivos en *Contribucion y alcance.md*, sección 4.4.

---

## 3. Requisitos no funcionales

La última columna anticipa la consecuencia de cada requisito sobre el diseño. Es el insumo para justificar las decisiones de *Arquitectura.md* (puntos 3 y 4 de la devolución).

| Id | Atributo | Requisito | Criterio de aceptación (propuesto) | Prioridad | Implicancia arquitectónica |
|----|----------|-----------|-------------------------------------|:---------:|----------------------------|
| RNF-01 | Modificabilidad | El clasificador debe ser intercambiable. | Cambiar de implementación solo requiere configuración; ambas implementaciones pasan la misma suite de pruebas. | M | Interfaz de clasificador + patrón adaptador. |
| RNF-02 | Correctitud | Las reglas de tarjetas deben ser deterministas. | Misma entrada → misma decisión; 100 % de cumplimiento en la suite de escenarios. | M | Reglas implementadas como código/configuración explícita, sin modelos probabilísticos. |
| RNF-03 | Trazabilidad | Toda detección y toda decisión deben ser explicables. | Cada patrón detectado referencia paso y evidencia; cada decisión del motor, las reglas aplicadas. | M | Registro de auditoría persistente. |
| RNF-04 | Privacidad | Ningún dato personal o financiero del usuario debe enviarse a servicios externos. | El clasificador LLM local se ejecuta en la misma máquina, por lo que el contenido de los flujos analizados (información pública de los servicios) no se envía fuera de ella; verificable mediante inspección del tráfico saliente. | M | Frontera clara entre el módulo N1 (datos públicos) y los módulos con datos de usuario. |
| RNF-05 | Seguridad de datos de tarjeta | Los números de tarjeta simulados no deben almacenarse ni registrarse en claro. | Almacenamiento tokenizado o cifrado; ausencia de números completos en logs. Se toma PCI-DSS como guía de buenas prácticas, no como certificación. | M | Separación del almacenamiento de datos sensibles (bóveda o tabla cifrada). |
| RNF-06 | Seguridad de la aplicación | La aplicación debe proteger el acceso a los datos de cada usuario. | Sin hallazgos de severidad alta o crítica en el análisis con referencia a OWASP Top 10. | M | Autenticación y autorización centralizadas. |
| RNF-07 | Puntualidad | Las reglas temporales deben ejecutarse en tiempo. | Vencimiento aplicado con un desvío menor a 1 minuto; 0 cobros autorizados posteriores al vencimiento. | M | Planificador de tareas persistente (sobrevive a reinicios). |
| RNF-08 | Rendimiento (autorización) | La decisión de autorizar o rechazar un cobro debe ser rápida. | p95 < 1 s (a contrastar con las ventanas de autorización en tiempo real de los proveedores de emisión). | S | La autorización no debe depender del clasificador ni de servicios externos. |
| RNF-09 | Rendimiento (detección) | El análisis de un flujo debe completarse en un tiempo razonable. | < 30 s por flujo. Se mide la latencia de cada clasificador por separado. La latencia del clasificador LLM local depende del hardware donde corre, no de la red (umbral definitivo en *Plan de validacion.md*). | C | Procesamiento no crítico; puede ser sincrónico o por lotes. |
| RNF-10 | Reproducibilidad | Los resultados de la evaluación deben poder repetirse. | Corpus, etiquetas y configuración versionados; la evaluación se reejecuta con un único comando. | M | Corpus como artefacto versionado, independiente de la base de datos operativa. |
| RNF-11 | Usabilidad | La plataforma debe ser usable por usuarios no expertos. | Puntaje SUS ≥ 68 (promedio de referencia del instrumento). | S | — |
| RNF-12 | Portabilidad | El prototipo debe poder desplegarse de forma reproducible en un equipo local. | Instalación documentada y levantada con un único comando. | S | Empaquetado del entorno. |
| RNF-13 | Extensibilidad | Nuevos patrones deben poder agregarse sin modificar el motor de reglas. | Agregar un patrón solo afecta al catálogo de patrones y a la fórmula de riesgo. | S | Catálogo de patrones configurable; N2 consume solo el índice de riesgo. |
| RNF-14 | Disponibilidad y escala | No se exige alta disponibilidad ni escalado horizontal. | Prototipo monousuario o de pocos usuarios concurrentes. | — | No hay requisito que obligue a desplegar componentes de forma independiente (relevante para el punto 4: microservicios vs. monolito modular). |

---

## 4. Trazabilidad resumida

| Objetivo | Requisitos funcionales | Requisitos no funcionales |
|----------|------------------------|---------------------------|
| OE1 | RF-01 | RNF-13 |
| OE2 | RF-02, RF-08, RF-10 | RNF-10 |
| OE3 | RF-03 a RF-07, RF-28 | RNF-01, RNF-03, RNF-04, RNF-09 |
| OE4 | RF-11 a RF-21 | RNF-02, RNF-03, RNF-05, RNF-07, RNF-08 |
| OE5 | RF-22 a RF-26 | RNF-06, RNF-11, RNF-12 |
| OE6 | RF-09, RF-16, RF-20 | RNF-02, RNF-07, RNF-10, RNF-11 |

---

## 5. Pendientes

- Validar los criterios de aceptación con el profesor de la materia Trabajo Final (Román Zenobi) y, cuando se designe, con el director/tutor; los umbrales definitivos se fijarán en *Plan de validacion.md*.
- Confirmar el subconjunto de patrones (sección 5.3 de *Contribucion y alcance.md*) con el estado del arte; puede afectar RF-03 y RF-04.
- Verificar la ventana de autorización en tiempo real de los proveedores de emisión (RNF-08).
- Evaluar si conviene expresar los requisitos de usuario también como historias de usuario para la etapa de desarrollo.
- Definir la prioridad de RF-28 (alerta previa a la contratación) y precisar qué flujo analiza (flujo de alta) y con qué patrones (permanencia mínima, costos ocultos), ya que el corpus actual se concibió con flujos de cancelación.
- `[[DECISIÓN: modelo y tamaño del LLM local — opciones a confirmar]]` y `[[DATO PENDIENTE: hardware donde corre el LLM local]]`; de ambos depende el umbral de RNF-09.

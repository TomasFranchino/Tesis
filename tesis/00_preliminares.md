---
title: "SuscripGuard: Control preventivo de suscripciones mediante tarjetas virtuales con políticas basadas en la detección de *dark patterns*"
subtitle: "Trabajo Final de la carrera de Ingeniería Informática"
author: "Tomás Franchino"
date: "[[DATO PENDIENTE: fecha de presentación]]"
---

<!-- NOTA PARA TOMÁS: Preliminares generados a partir de CLAUDE.md (título, tesista, profesor), de "Contribucion y alcance.md" (v0.4) y de la versión vigente de "Objetivos.md". Faltan: universidad, facultad, director o tutor, lugar y fecha, y los agradecimientos (los escribe el tesista). El resumen es provisional: se reescribe al final, cuando existan resultados. Las afirmaciones sobre la literatura que el resumen condensa se respaldan en el Capítulo 1; si la norma de la facultad exige citas en el resumen, hay que agregarlas ahí. -->

# Portada {.unnumbered}

**Carrera:** Ingeniería Informática

**Universidad y facultad:** [[DATO PENDIENTE: universidad y facultad]]

**Profesor de la materia Trabajo Final:** Román Zenobi

**Director/a:** [[DATO PENDIENTE: director o tutor; a la fecha no hay designación]]

**Lugar y fecha:** [[DATO PENDIENTE: lugar y fecha de presentación]]

# Agradecimientos {.unnumbered}

[[DATO PENDIENTE: agradecimientos, los escribe el tesista]]

# Resumen {.unnumbered}

<!-- NOTA PARA TOMÁS: resumen provisional; se reescribe al final con los resultados reales. -->

Los servicios por suscripción realizan cobros recurrentes y, con frecuencia, sus flujos de cancelación incorporan *dark patterns* (patrones oscuros) que dificultan la baja y prolongan cobros no deseados. Las herramientas existentes actúan de manera reactiva, una vez producido el cobro, u ofrecen tarjetas virtuales cuya configuración queda librada al criterio del usuario, sin información sobre el riesgo de cada servicio. Este trabajo propone SuscripGuard, un mecanismo de control preventivo de pagos recurrentes basado en riesgo: el sistema analiza una representación estructurada del flujo de cancelación de un servicio, estima un índice de riesgo a partir de los *dark patterns* detectados y, en función de ese índice, propone y ejecuta una política de vencimiento, tope de monto y cantidad de cobros sobre una tarjeta virtual dedicada a la suscripción. Además, un modelo de lenguaje local analiza el correo de confirmación del alta para alertar sobre permanencia mínima o costos ocultos. El alcance se limita a suscripciones digitales pagadas con tarjeta y sin permanencia mínima, incluidas las pruebas gratuitas.

La evaluación prevista comprende la comparación de un clasificador basado en un modelo de lenguaje local con una línea base heurística sobre un corpus etiquetado de flujos de cancelación de 15 a 20 servicios (precisión, *recall*, F1, falsos positivos y latencia), la verificación del cumplimiento de las reglas en escenarios de prueba y la medición de la usabilidad mediante la escala SUS. A la fecha, el problema, el alcance, los requisitos, la arquitectura y el plan de validación están definidos; el prototipo y el corpus están en construcción, por lo que los resultados se encuentran pendientes. [[RESULTADO PENDIENTE: desempeño de la detección, cumplimiento de reglas, latencia y usabilidad; completar al cierre de la validación]]

**Palabras clave:** *dark patterns* (patrones oscuros); suscripciones; tarjetas virtuales; flujos de cancelación; modelo de lenguaje local; control preventivo de pagos.

# Abstract {.unnumbered}

Subscription services charge users on a recurring basis and, frequently, their cancellation flows include *dark patterns* that make it harder to unsubscribe and prolong unwanted charges. Existing tools act reactively, once the charge has already occurred, or offer virtual cards whose configuration is left to the user's judgment, with no information about the risk of each service. This work proposes SuscripGuard, a risk-based preventive control mechanism for recurring payments: the system analyzes a structured representation of a service's cancellation flow, estimates a risk index from the detected *dark patterns* and, based on that index, proposes and enforces a policy on expiration, amount cap and number of charges over a virtual card dedicated to the subscription. In addition, a local language model analyzes the sign-up confirmation email to warn about minimum commitment periods or hidden costs. The scope is limited to digital subscriptions paid by card with no minimum commitment period, including free trials.

The planned evaluation compares a classifier based on a local language model with a heuristic baseline over a labeled corpus of cancellation flows from 15 to 20 services (precision, recall, F1, false positives and latency), verifies rule compliance in test scenarios, and measures usability with the SUS scale. To date, the problem, the scope, the requirements, the architecture and the validation plan have been defined; the prototype and the corpus are under construction, so results are pending. [[RESULTADO PENDIENTE: detection performance, rule compliance, latency and usability; complete when the validation is finished]]

**Keywords:** *dark patterns*; subscriptions; virtual cards; cancellation flows; local language model; preventive payment control.

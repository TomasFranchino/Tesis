Definición de Objetivos para la Tesis de Ingeniería Informática
> Actualizado el 29/09/2026 tras la devolución de la Entrega 1. Los objetivos vigentes están en la sección final "Objetivos (versión vigente)". Contribución central y alcance: ver *Contribucion y alcance.md*.
Preguntas a responder para lograr los objetivos:
¿Cuál es el conocimiento que se pretende alcanzar?

¿Existe concordancia con el problema de la tesis?
¿Qué quiero hacer en la investigación?
¿A dónde quiero llegar?
1. Objetivo General (¿Qué quiero lograr?)
Debe responder a la meta principal de tu proyecto y englobar la solución central. [1, 2]
¿Qué? ¿Cuál es el producto o solución principal que vas a desarrollar? (Ej: Un sistema de recomendación, una aplicación móvil, un algoritmo predictivo).
Una plataforma que les permita a los usuarios, gestionar sus suscripciones de forma segura, automática y con control total sobre sus pagos recurrentes 
¿Para qué? ¿Cuál es el propósito final o el problema que resuelve? (Ej: Para optimizar la gestión de inventario, para mejorar la seguridad en redes).
Por varios motivos:
Simplificar y esclarecer el funcionamiento de las suscripciones y sus dark patterns.
Evitar el cobro automático al renovar suscripciones no deseadas o extender plazos de uso indebidamente.
Poder automatizar esta gestión y mantener avisado al usuario sobre el estado de sus suscripciones.
Aumentando la seguridad de este tipo de suscripciones mediante tarjetas virtuales descartables o de un solo uso, hasta con límites de crédito evitando que te roben los datos y puedan realizar compras con ellas.
¿Dónde/En quién? ¿A quién va dirigido o sobre qué dominio de datos trabajarás? (Ej: Para la empresa X, para pacientes con diabetes).
Va dirigido sobre todo a latinoamérica en donde tiene una gran proyección el uso de tarjetas de credito y debito a su vez en donde también está creciendo de a poco el consumo de suscripciones, justamente este público con muchas suscripciones que gestionar y orientados a la seguridad es a quienes va orientado esta plataforma.
2. Objetivos Específicos (¿Cómo lo voy a lograr?)
Son los pasos lógicos, medibles y secuenciales que te llevarán a cumplir el objetivo general. Responden a las fases técnicas de la ingeniería.
Investigación: ¿Qué tecnologías, marcos de trabajo (frameworks) o estados del arte necesitas analizar y comparar?
[Nota 29/09/2026: el stack que sigue es PRELIMINAR y NO constituye una decisión. Cada tecnología se justificará a partir de los requisitos (Requisitos.md) en Arquitectura.md, según los puntos 3 y 4 de la devolución.]
La arquitectura básica de la plataforma podría ser algo como lo que describo a continuación:
Arquitectura para analizar:
Frontend: Next.js 15 + TypeScript + TailwindCSS + shadcn/ui (interfaz moderna y usable).
Backend: Python con FastAPI (más adecuado para IA) o Node.js con NestJS.
Base de Datos: PostgreSQL (principal) + Redis (colas y caché).
Autenticación: OAuth2 + JWT + 2FA.
Generación de tarjetas virtuales:
Modo simulado (para TFG): sistema interno que genera tokens ficticios pero funcionales.
Modo real (opcional): integración con Stripe Issuing, Privacy.com API o Revolut (sandbox).
Inteligencia Artificial:
Uso de LLM local (Llama 3.1 8B o Phi-3) vía Ollama para clasificar emails y detectar suscripciones.
Motor de reglas con Temporal.io o Celery + cron jobs.
Otras tecnologías:
Gmail API / IMAP para leer correos.
Docker + Docker Compose para despliegue local.
Grafana + Prometheus para monitoreo (opcional).
Análisis y Diseño: ¿Qué requerimientos funcionales y no funcionales tiene el sistema? ¿Cuál será la arquitectura o el modelo de datos?
Ver Requisitos.md (borrador v0.1, 29/09/2026).
Implementación: ¿Qué módulos, componentes o algoritmos específicos vas a programar o integrar?
Ver sección 4 de Contribucion y alcance.md: núcleo (N1 detección de dark patterns, N2 motor de reglas y políticas, N3 emulador de tarjetas virtuales), soporte y complementario.


Pruebas y Validación: ¿Cómo vas a verificar que el sistema funciona correctamente (pruebas de integración, de rendimiento, o validación con usuarios)?
Ver sección 7 de Contribucion y alcance.md; se desarrollará en Plan de validacion.md.
3. Delimitación y Alcance (¿Hasta dónde llegaré?)
¿Qué queda fuera del proyecto? Define claramente lo que no harás para evitar que el proyecto crezca de manera inmanejable (scope creep).
¿Cuáles son las limitaciones técnicas o de recursos? (Ej: Acceso limitado a datos reales, tiempo de cómputo, etc.).
Ver secciones 4.4 (fuera de alcance) y 6 (supuestos y riesgos) de Contribucion y alcance.md.

## Objetivos (versión vigente — 29/09/2026)

**Título:** SuscripGuard: Control preventivo de suscripciones mediante tarjetas virtuales con políticas basadas en la detección de dark patterns

### Objetivo General
Diseñar, implementar y evaluar un prototipo de plataforma que prevenga cobros recurrentes no deseados mediante tarjetas virtuales cuyas políticas de uso se configuran a partir de la detección automática de *dark patterns* en los flujos de cancelación de los servicios.

### Objetivos Específicos
1. Caracterizar los *dark patterns* presentes en flujos de cancelación de suscripciones y definir un subconjunto detectable junto con un esquema de representación estructurada de dichos flujos.
2. Construir un corpus etiquetado de flujos de cancelación de servicios por suscripción de uso frecuente.
3. Desarrollar un módulo de detección de *dark patterns*, independiente del modelo de clasificación, que genere un índice de riesgo por servicio.
4. Desarrollar un motor de reglas determinista y un emulador de tarjetas virtuales que apliquen políticas de vencimiento, tope de monto y cantidad de cobros a partir de dicho índice.
5. Integrar los componentes en un prototipo web que permita al usuario registrar suscripciones, revisar el riesgo de cada servicio y gestionar sus tarjetas.
6. Evaluar el prototipo en términos de precisión de detección, cumplimiento de reglas, rendimiento y usabilidad.

### Trazabilidad
| Objetivo específico | Subpregunta de investigación | Componente | Aporte |
|---|---|---|---|
| OE1 Caracterizar patrones y esquema | SP1 | N1 | A1, A2 |
| OE2 Corpus etiquetado | SP1, SP2 | N1 | A3 |
| OE3 Módulo de detección | SP1, SP2 | N1 | A2, A5 |
| OE4 Motor de reglas y emulador | SP3 | N2, N3 | A4 |
| OE5 Integración en prototipo web | SP4 | Soporte + N1–N3 | — |
| OE6 Evaluación | SP1–SP4 | Todos | A5 |

(Subpreguntas, componentes y aportes definidos en *Contribucion y alcance.md*, secciones 2, 3.1 y 4.)

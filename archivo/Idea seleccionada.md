Idea seleccionada:
5. El caos de las suscripciones y los "Dark Patterns"
La queja: Es facilísimo suscribirse a un servicio en un clic, pero para cancelar tienes que llamar por teléfono en horario comercial o navegar por 10 menús confusos (Dark Patterns o patrones oscuros).

La solución informática:

Gestores de tarjetas virtuales inteligentes: Una aplicación que genere tarjetas de crédito virtuales para cada servicio con fechas de caducidad automáticas. Si te suscribes a una prueba gratuita de 7 días, el software destruye la tarjeta virtual al sexto día automáticamente, haciendo imposible que te cobren, sin que tengas que lidiar con el botón de cancelación de la empresa.

Cualquiera de estos problemas tiene el potencial para ser un excelente proyecto personal, un producto SaaS (Software as a Service) o una extensión útil y monetizable.

Título Sugerido
"SuscripGuard: Plataforma Inteligente de Gestión de Suscripciones con Tarjetas Virtuales Automatizadas y Detección de Dark Patterns"

Descripción del Proyecto
El objetivo es crear una aplicación que ayude a los usuarios a combatir el "caos de las suscripciones" y los patrones oscuros (dark patterns) mediante automatización inteligente.
La aplicación permitirá generar tarjetas virtuales temporales para cada suscripción, establecer reglas automáticas de expiración y detectar automáticamente suscripciones activas mediante el análisis de correos electrónicos y extractos bancarios.

Objetivos
Objetivo General:
Diseñar, implementar y evaluar una plataforma web que permita a los usuarios gestionar sus suscripciones de forma segura, automática y con control total sobre sus pagos recurrentes.
Objetivos Específicos:
Crear un sistema de generación y gestión de tarjetas virtuales con reglas de caducidad automática.
Implementar un módulo de detección automática de suscripciones mediante análisis de emails y transacciones.
Desarrollar un motor de reglas inteligente para sugerir y ejecutar acciones (pausar, cancelar, alertar).
Incluir un analizador de dark patterns en flujos de cancelación de servicios populares.
Garantizar altos estándares de seguridad y privacidad de datos financieros.
Evaluar la usabilidad, efectividad y seguridad del sistema.

Arquitectura Propuesta
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

Funcionalidades Principales (Alcance)
MVP (Mínimo Viable - Obligatorio):
Registro de usuario y dashboard.
Registro manual de suscripciones.
Generador de tarjetas virtuales con fecha de expiración configurable.
Motor de expiración automática (destruye la tarjeta en la fecha indicada).
Detección básica de suscripciones vía emails.
Reporte de suscripciones activas y gasto mensual.
Extensiones Recomendadas (para destacar):
Análisis automático de correos con IA.
Extensión de navegador (Chrome/Firefox) que detecta flujos de suscripción y ofrece generar tarjeta al instante.
Módulo de análisis de dark patterns (base de datos con patrones de 15-20 servicios populares).
Sugerencias inteligentes ("Netflix subió de precio", "Prueba gratuita termina en 3 días").
Exportación de cartas de cancelación automáticas.

Cronograma Recomendado (5 meses)
Mes 1: Investigación, definición de requisitos, setup del proyecto (arquitectura, Docker), autenticación y dashboard básico.
Mes 2: Motor de tarjetas virtuales + sistema de reglas y expiración automática.
Mes 3: Integración con Gmail + módulo de IA para detección de suscripciones.
Mes 4: Extensión de navegador + módulo de dark patterns + pruebas de seguridad.
Mes 5: Evaluación (usabilidad, rendimiento, seguridad), documentación, memoria y demo final.

Evaluación y Métricas
Técnicas: Tiempo de procesamiento, precisión de detección de suscripciones (con dataset etiquetado), tasa de éxito en expiración automática.
Usabilidad: Pruebas con usuarios (NPS o SUS questionnaire).
Seguridad: Análisis de vulnerabilidades (OWASP), encriptación de datos.
Comparativa: Comparar con herramientas existentes (Rocket Money, Trim, Privacy.com).

Innovaciones que puedes añadir
"Modo Prueba Segura": Al activarse, genera tarjeta + programa expiración + crea recordatorio.
Privacy-First: Opción de correr todo localmente (LLM local + encriptación).
Informe Anual de Suscripciones: Resumen inteligente de gasto "fantasma".
Integración con SSI (si quieres combinar ideas): Guardar credenciales de suscripciones de forma descentralizada.

Ventajas de este Proyecto
Problema muy relatable → tribunal lo entenderá fácilmente.
Demo muy impactante (puedes mostrar en vivo cómo se "autodestruye" una tarjeta).
Combina varias áreas: Desarrollo web, IA, Seguridad, Automatización y UX.
Potencial real de producto (podrías continuarlo después del TFG).
Buen equilibrio entre dificultad técnica y viabilidad.

¿Quieres que ahora te prepare la propuesta formal completa lista para entregar a tu profesor? (con introducción, objetivos, marco teórico, metodología, etc.)
También puedo darte:
Diagrama de arquitectura
Lista de endpoints API
Estructura sugerida de la memoria del TFG
Repositorios y recursos para empezar
Dime cómo quieres continuar. Estoy listo para avanzar al siguiente nivel de detalle. 🔥


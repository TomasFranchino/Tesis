# Reporte Quincenal de Avances de Tesis N° 1

**Proyecto de Trabajo Final de Grado (Tesis):**  
*SuscripGuard: Plataforma Inteligente de Gestión de Suscripciones con Tarjetas Virtuales Automatizadas y Detección de Dark Patterns*

* **Tesista:** Tomas Franchino
* **Carrera:** Ingeniería Informática
* **Profesor / Tutor Académico:** [Nombre del Profesor / Tutor]
* **Fecha de Entrega:** 13 de agosto de 2026
* **Período de Reporte:** Quincena 1 (Inicio y Formulación Metodológica)

---

## 1. Resumen Ejecutivo de Avances

Durante el presente período quincenal, se ha completado la fase inicial de definición conceptual, estructuración del marco de investigación y revisión exhaustiva del estado del arte para la tesis de grado. El proyecto **SuscripGuard** aborda la problemática emergente del "caos de las suscripciones" (*subscription fatigue*) y la proliferación de patrones de diseño manipuladores (*dark patterns*) en servicios digitales recurrentes.

### Matriz de Progreso Quincenal

| Fase de Investigación | Nivel de Avance | Estado Actual |
| :--- | :---: | :--- |
| **1. Definición y Delimitación del Problema** | **100%** | Caracterización de impactos económicos, psicológicos y legales completada. |
| **2. Formulación de Objetivos (General y Específicos)** | **95%** | Objetivos redactados según estándar de ingeniería en verbos infinitivos. |
| **3. Estado del Arte y Antecedentes** | **90%** | Identificación de taxonomías (ACM), marco legal (FTC/DSA) y análisis de casos empíricos. |
| **4. Arquitectura y Stack Tecnológico** | **85%** | Definición de capas (Frontend, Backend, BaaS Sandbox, IA local vía Ollama). |
| **5. Metodología y Plan de Validación** | **75%** | Métricas de rendimiento, usabilidad (SUS/NPS) y matriz de riesgos en definición. |

---

## 2. Definición del Problema y Justificación Académica

El modelo de suscripción ha experimentado un crecimiento acelerado en la economía digital. Sin embargo, este modelo ha derivado en la explotación de asimetrías de información y fricciones intencionadas que afectan directamente al consumidor.

### 2.1. Dimensiones del Impacto

1. **Impacto Económico Directo e Indirecto:**
   * **Gasto hormiga forzado:** Retención indebida mediante trabas burocráticas en el flujo de cancelación que obligan a pagar ciclos adicionales.
   * **Facturación por servicios no gozados:** Cobro de períodos completos posteriores a la solicitud de rescisión.
   * **Intereses por deudas infladas:** Acumulación de recargos sobre saldos no reconocidos que asfixian la capacidad financiera del usuario.
   * **Riesgo del perfil crediticio:** Amenaza de reporte a centrales de riesgo por disputas de cancelación.

2. **Impacto Psicológico y Emocional:**
   * **Frustración e indefensión:** Asimetría extrema entre un canal de alta inmediato (un clic) y un canal de baja inaccesible o laberíntico (*Roach Motel*).
   * **Fatiga por burocracia:** Desgaste psicológico provocado por transferencias infinitas entre operadores o agentes virtuales.

3. **Relevancia Regional (América Latina):**
   A diferencia de los mercados de EE.UU. y Europa, en Latinoamérica se observa un crecimiento acelerado del consumo de suscripciones acompañado de una mayor vulnerabilidad del consumidor y una menor disponibilidad de herramientas tecnológicas de protección financiera.

---

## 3. Estado del Arte y Antecedentes de Investigación

### 3.1. Taxonomía de Patrones Oscuros (*Dark Patterns*)

Basado en investigaciones recientes publicadas en plataformas académicas (ACM Digital Library, IEEE Xplore) y normativas internacionales (FTC *Click-to-Cancel rule*, *Digital Services Act* de la Unión Europea), se clasifican las técnicas de retención abusiva en:

* **Roach Motel (Motel de Cucarachas):** Facilidad para suscribirse, complejidad extrema para cancelar.
* **Sludge (Lodo):** Fricción cognitiva o procedimental deliberada (ej. obligar a llamar por teléfono en horarios acotados).
* **Interferencia Visual / Confirmshaming:** Diseños que manipulan emocionalmente al usuario o disimulan las opciones de baja.
* **Drip Pricing / Sneak into Basket:** Ocultamiento de costos de permanencia o cobros adicionales aplicados gradualmente.

### 3.2. Casos de Estudio Empíricos

1. **Caso DAZN (Streaming - Europa):**
   * *Práctica:* Laberintos de navegación, ofertas emergentes que ocultan el botón de baja, redirección obligatoria a chatbots sin opción de cancelación directa y atención por operadores comerciales de retención.
   * *Incumplimiento Normativo:* Vulneración de la Ley de Servicios Digitales (Art. 25.2) y directivas de consumo que exigen simetría entre el alta y la baja.

2. **Caso Telecentro y DirecTV (Telecomunicaciones - Argentina):**
   * *Práctica:* Sanción por 167 millones de pesos por obstaculización sistemática de bajas, inoperatividad del "botón de baja" obligatorio y la exigencia abusiva de "saldo en cero" como condición previa irreductible para cancelar el servicio.
   * *Aporte a la Tesis:* Demuestra la insuficiencia de la fiscalización estatal ex-post y la necesidad de una solución tecnológica de autodefensa proactiva.

### 3.3. Brecha del Estado del Arte

Actualmente existen gestores de suscripciones (ej. *Rocket Money*, *Trim*) que dependen del acceso completo a cuentas bancarias (alta intrusividad en privacidad) y herramientas de tarjetas virtuales (ej. *Privacy.com*, *Revolut*) orientadas principalmente al mercado estadounidense o corporativo.

**Brecha identificada:** Ninguna solución integra de manera unificada:
1. Generación de tarjetas virtuales temporales con reglas de expiración/autodestrucción automática.
2. Detección automática de suscripciones mediante IA de ejecución local (respeto por la privacidad del correo).
3. Módulo de análisis y concientización sobre *dark patterns*.

```
                                ESTADO DEL ARTE ACTUAL
+-----------------------+     +-----------------------+     +-----------------------+
|  Rocket Money / Trim  |     | Privacy.com / Revolut |     |    SuscripGuard       |
|  (Gestores bancarios) |     |  (Tarjetas Virtuales) |     | (Propuesta de Tesis)  |
+-----------------------+     +-----------------------+     +-----------------------+
| - Alta intrusividad   |     | - Sin IA de emails    |     | + Tarjetas temporales |
| - Sin tarjetas auto   |     | - Enfoque EE.UU./B2B  |     | + IA Local (Ollama)   |
| - Sin análisis Dark UX|     | - Sin análisis Dark UX|     | + Detección Dark UX   |
+-----------------------+     +-----------------------+     +-----------------------+
```

---

## 4. Matriz de Objetivos del Proyecto

### 4.1. Objetivo General
Diseñar, implementar y evaluar una plataforma web integrada que permita a los usuarios gestionar sus suscripciones de forma segura, automática y con control total sobre sus pagos recurrentes mediante tarjetas virtuales descartables y clasificación inteligente con IA.

### 4.2. Objetivos Específicos
1. **Investigar y analizar** las arquitecturas de emisión de tarjetas (*Banking-as-a-Service*), las normativas de seguridad financiera (PCI-DSS tokenization) y las taxonomías de *dark patterns*.
2. **Diseñar la arquitectura del sistema** basada en microservicios/módulos asíncronos para el procesamiento de pagos simulados, el motor de reglas de expiración y el análisis de correos.
3. **Desarrollar un módulo de emisión y gestión de tarjetas virtuales** que ejecute reglas de caducidad automática (autodestrucción por fecha o límite de transacciones).
4. **Implementar un motor de IA local (LLM)** para la detección y clasificación automática de suscripciones y facturas a partir del análisis de correos electrónicos (Gmail API / IMAP).
5. **Construir un analizador de *dark patterns*** que identifique y catalogue flujos engañosos en las principales plataformas de servicios.
6. **Validar la solución** mediante pruebas de usabilidad (Cuestionario SUS/NPS), pruebas de rendimiento técnico y evaluación de seguridad OWASP.

---

## 5. Arquitectura del Sistema y Stack Tecnológico

Para garantizar la viabilidad técnica como Trabajo Final de Grado en Ingeniería Informática, se ha definido una arquitectura moderna, escalable y modular:

```
+-----------------------------------------------------------------------------------+
|                                  CAPA DE PRESENTACIÓN                             |
|              Next.js 15 (App Router) + TypeScript + TailwindCSS + shadcn/ui        |
+-----------------------------------------------------------------------------------+
                                         | REST / WebSockets / JWT Auth
                                         v
+-----------------------------------------------------------------------------------+
|                                 CAPA DE NEGOCIO (API)                             |
|                        Python (FastAPI) / Node.js (NestJS)                        |
+-----------------------------------------------------------------------------------+
       |                                 |                                 |
       v                                 v                                 v
+-----------------------+   +-----------------------+   +-----------------------+
|  MOTOR DE REGLAS & IA |   |   INTEGRACIÓN BaaS    |   | BASE DE DATOS Y CACHÉ |
| - Ollama (Llama 3.1)  |   | - Stripe Issuing API  |   | - PostgreSQL (Core)   |
| - Celery / Temporal   |   |   (Modo Sandbox)      |   | - Redis (Colas/Caché) |
| - Gmail API / IMAP    |   | - Tokenización PCI    |   |                       |
+-----------------------+   +-----------------------+   +-----------------------+
```

### Justificación de Elecciones Tecnológicas:
* **Entorno Sandbox BaaS (Stripe Issuing / Lithic API):** Permite simular el ciclo de vida completo de tarjetas bancarias (emisión, autorización, rechazo por expiración y cobro de webhooks) sin requerir licencias bancarias ni comprometer capital real.
* **IA Local (Ollama + Llama 3.1 8B / Phi-3):** Garantiza un enfoque *Privacy-First*, permitiendo procesar información sensible de correos electrónicos en la infraestructura del usuario o en un entorno controlado sin enviar datos a terceros.

---

## 6. Alineación con la Estructura del Trabajo Final (Memoria)

A continuación se presenta el mapeo de los avances actuales con respecto al índice general aprobado para la tesis de grado:

```
[X] Capítulo 1: Introducción
    [X] 1.1 Antecedentes de la Investigación
    [X] 1.2 Planteamiento del Problema
    [X] 1.3 Justificación
    [X] 1.4 Objetivos (General y Específicos)
[ ] Capítulo 2: Marco Teórico
    [X] 2.1 Bases Teóricas (BaaS, Dark Patterns, LLMs)
    [~] 2.2 Estado del Arte (En proceso de redacción formal)
    [ ] 2.3 Definición de Conceptos Clave
[ ] Capítulo 3: Marco Metodológico
    [X] 3.1 Enfoque y Tipo de Investigación (Ingeniería de Software / Aplicada)
    [X] 3.2 Tecnologías y Herramientas
    [ ] 3.3 Diseño de la Solución / Arquitectura de Sistema
    [ ] 3.4 Fases de Implementación
[ ] Capítulo 4: Desarrollo e Implementación
    [ ] 4.1 Requerimientos del Sistema (Funcionales y No Funcionales)
    [ ] 4.2 Diseño Detallado (Diagramas UML, Modelo ER)
    [ ] 4.3 Implementación del Prototipo
[ ] Capítulo 5: Análisis de Resultados y Validación
    [ ] 5.1 Pruebas de Funcionamiento
    [ ] 5.2 Evaluación de Rendimiento y Métricas (Latencia, Precisión IA)
    [ ] 5.3 Análisis de Usabilidad (SUS / NPS)
[ ] Capítulo 6: Conclusiones y Recomendaciones
```

---

## 7. Preguntas y Puntos de Consulta para el Tutor / Profesor

1. **Formalización del Marco Teórico:** ¿Se recomienda profundizar la taxonomía de *Dark Patterns* desde el enfoque de Economía del Comportamiento (*Behavioral Economics*) o mantener el foco primordial en la perspectiva de Interacción Persona-Computador (HCI) e Ingeniería de Software?
2. **Entorno Sandbox para la Demostración:** Para la defensa del TFG, ¿el tribunal considera adecuado el uso de entornos Sandbox institucionales (Stripe Issuing / Lithic API) combinados con un simulador de pasarela de pagos propio para demostrar el flujo de rechazo de cobros en tiempo real?
3. **Métricas de Evaluación de IA:** ¿Es conveniente medir la precisión del modelo LLM de clasificación de suscripciones mediante una matriz de confusión (Precisión, Recall, F1-Score) sobre un dataset etiquetado de prueba?

---

## 8. Hoja de Ruta y Plan de Trabajo para la Próxima Quincena

### Cronograma de Trabajo Proyectado (Próximas 2 Semanas)
* **Semana 1:**
  * Redacción formal del Capítulo 2.1 (Bases Teóricas) y 2.2 (Estado del Arte) en la memoria principal.
  * Definición de la Especificación de Requerimientos del Sistema (IEEE 830 / Historias de Usuario).
* **Semana 2:**
  * Creación del repositorio base (Setup de Next.js 15, FastAPI, Docker Compose con PostgreSQL y Redis).
  * Configuración del entorno Sandbox de Stripe Issuing y diseño del esquema de la base de datos relacional.

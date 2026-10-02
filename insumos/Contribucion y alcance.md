# Contribución central y alcance del Trabajo Final

**Título de trabajo (definido el 29/09/2026):**
*SuscripGuard: Control preventivo de suscripciones mediante tarjetas virtuales con políticas basadas en la detección de dark patterns*

> **Estado:** borrador v0.3 (02/10/2026). Responde a los puntos 1 y 2 de la devolución de la Entrega 1.
> Título y objetivos confirmados el 29/09/2026 (sección 8).
> v0.3: aplicadas decisiones B1 y B2 (02/10/2026).

---

## 1. Enunciado del problema

Los usuarios de servicios por suscripción no disponen de mecanismos que les permitan controlar los cobros recurrentes **sin depender de la voluntad del proveedor**. Los procesos de cancelación incorporan con frecuencia *dark patterns* (asimetría entre alta y baja, obstrucción, *confirmshaming*, interferencia visual, entre otros) que prolongan cobros no deseados. Las herramientas existentes abordan el problema de manera parcial: los gestores de suscripciones actúan de forma **reactiva** (detectan y asisten la cancelación una vez que el cobro ya ocurre), y los emisores de tarjetas virtuales ofrecen control sobre el medio de pago pero **sin información sobre el riesgo que presenta cada servicio**, por lo que la configuración de límites y vencimientos queda librada al criterio del usuario.

El problema se acota a las **suscripciones digitales pagadas con tarjeta y sin permanencia mínima, incluidas las pruebas gratuitas**, y a los daños que el mecanismo puede prevenir: los cobros posteriores a una baja o a una prueba gratuita. Los daños que derivan de obligaciones contractuales (deuda, intereses, gestiones de cobranza) se tratan como contexto y limitaciones, porque rechazar un cobro no rescinde el contrato.

## 2. Pregunta de investigación

**Pregunta principal:**
¿Es posible prevenir cobros recurrentes no deseados mediante tarjetas virtuales cuyas políticas de uso se configuran automáticamente a partir de la detección de *dark patterns* en los flujos de cancelación de cada servicio?

**Subpreguntas:**

1. ¿Con qué precisión puede detectarse automáticamente un subconjunto de *dark patterns* a partir de una representación estructurada de los flujos de cancelación?
2. ¿Qué diferencia de desempeño (precisión, falsos positivos, latencia) existe entre un clasificador basado en un modelo de lenguaje local (LLM local, ejecutado con Ollama) y una línea base heurística?
3. ¿Cumple el motor de reglas de forma verificable las políticas definidas sobre las tarjetas virtuales (vencimiento, tope de monto, cantidad de cobros)?
4. ¿Resulta la solución usable para el usuario final?

## 3. Contribución central

La contribución central de SuscripGuard es un **mecanismo de control preventivo de pagos recurrentes basado en riesgo**: el sistema analiza el flujo de cancelación de un servicio, estima su nivel de riesgo a partir de los *dark patterns* detectados y, en función de ese riesgo, propone y ejecuta una política sobre una tarjeta virtual dedicada a esa suscripción.

La contribución no reside en cada componente aislado (las tarjetas virtuales y los catálogos de *dark patterns* ya existen), sino en **su integración**: la detección informa la decisión, y la decisión se ejecuta sobre el medio de pago. De este modo, el usuario deja de depender del flujo de cancelación del proveedor.

### 3.1. Aportes específicos

| Id | Aporte | Tipo |
|----|--------|------|
| A1 | Esquema de representación estructurada de flujos de cancelación (pasos, elementos, canales, prominencia) que permite analizarlos automáticamente sin depender de capturas de pantalla. | Modelado |
| A2 | Operacionalización de un subconjunto de la taxonomía de *dark patterns* en reglas heurísticas y en una clasificación con salida validada contra un esquema, con evidencia trazable por paso. | Método |
| A3 | Corpus etiquetado de flujos de cancelación de 15 a 20 servicios, capturado en una fecha determinada. | Datos |
| A4 | Motor de políticas que traduce el índice de riesgo en configuraciones de tarjeta virtual y las ejecuta de forma determinista. | Diseño / implementación |
| A5 | Evaluación comparativa del clasificador LLM local (ejecutado con Ollama) frente a la línea base heurística. | Evaluación |

## 4. Clasificación de componentes

### 4.1. Núcleo (constituye el aporte y se valida con métricas propias)

```
 Flujo de cancelación           Módulo de detección          Motor de reglas             Emulador de tarjetas
 capturado (JSON)       ──►     de dark patterns     ──►     y políticas        ──►      virtuales
 [pasos, elementos,             [heurísticas +               [riesgo + suscripción       [emisión, autorización,
  canales, prominencia]          clasificador]                → política de tarjeta]      rechazo, vencimiento]
                                      │                               │
                                      ▼                               ▼
                               Informe de riesgo              Alertas al usuario
                               por servicio                   (previas a contratación/renov.)
```

- **N1. Módulo de detección de *dark patterns*** (ver sección 5).
- **N2. Motor de reglas y políticas:** recibe los datos de la suscripción (servicio, precio, período de prueba, fecha de renovación) y el índice de riesgo del servicio; propone una política de tarjeta que el usuario confirma o ajusta, y ejecuta las reglas de forma **determinista** (sin intervención de modelos probabilísticos).
- **N3. Emulador de emisión de tarjetas virtuales:** simula el ciclo de vida de la tarjeta (emisión, autorización o rechazo de cobros, bloqueo y destrucción). Se diseña detrás de una interfaz de adaptador, de modo que un proveedor real (p. ej. Stripe Issuing, Lithic o Pomelo) pueda incorporarse sin modificar el núcleo.

### 4.2. Soporte (necesario para que el núcleo funcione; no constituye aporte)

- Registro de usuarios y autenticación.
- Registro manual de suscripciones.
- Panel de suscripciones activas, tarjetas asociadas y gasto mensual.
- Notificaciones (alertas previas a la contratación, a la renovación o al vencimiento).

### 4.3. Complementario (se incorpora solo si el cronograma lo permite)

- **Detección de suscripciones a partir de correos electrónicos.** Si se implementa, deberá respetar el enfoque de privacidad: procesamiento con modelo local o limitado a metadatos (remitente, asunto), sin enviar el contenido de los correos a servicios externos.

### 4.4. Fuera de alcance

| Elemento | Motivo |
|----------|--------|
| Emisión de tarjetas reales / integración productiva con proveedores BaaS | Requiere licencias y cumplimiento PCI-DSS; disponibilidad limitada en Argentina. Se deja preparada la interfaz de adaptador. |
| Análisis de extractos o cuentas bancarias | Alta intrusividad en datos financieros; no aporta a la pregunta de investigación. |
| Extensión de navegador | Amplía el alcance sin aportar a la validación del núcleo. Queda como trabajo futuro. |
| Análisis en vivo de sitios arbitrarios | El análisis se realiza sobre un corpus capturado y controlado. |
| Análisis de capturas de pantalla / imágenes | Se trabaja sobre representación estructurada (texto y atributos del DOM). |
| Cancelación automática en nombre del usuario | Implica credenciales de terceros y riesgos legales; el control se ejerce sobre el medio de pago. |
| Generación de cartas de cancelación, SSI, monitoreo con Grafana/Prometheus | No responden a ninguna subpregunta de investigación. |
| Servicios con permanencia mínima | Bloquear la tarjeta no extingue la obligación contractual y el proveedor puede generar deuda; el mecanismo solo advierte la permanencia antes de contratar. |
| Servicios no pagados con tarjeta | El control se ejerce sobre el medio de pago; otras formas de facturación quedan fuera de su alcance. |
| Servicios no digitales | El análisis y la captura se realizan sobre flujos digitales. |
| Extinción del contrato y gestión de la deuda | Rechazar un cobro no rescinde el contrato; el sistema no extingue obligaciones contractuales ni gestiona deuda, intereses o reclamos. |

## 5. Especificación del módulo de detección de *dark patterns*

### 5.1. Entrada

Una **representación estructurada (JSON)** del flujo de cancelación de un servicio, capturada de forma semiautomática (scripts de navegación + anotación manual) en una fecha registrada. Contiene:

- **Nivel flujo:** servicio, fecha de captura, cantidad de pasos de alta y de baja, canal final requerido para la baja (web, chat, teléfono, correo), si requiere inicio de sesión.
- **Nivel paso:** URL o canal, textos visibles, elementos interactivos con su rol (acción principal, secundaria, enlace), atributos de prominencia derivados del DOM/CSS (tamaño relativo, contraste, posición) y tipo de acción ofrecida (cancelar, oferta de retención, redirección, información).

### 5.2. Proceso

1. **Extracción de rasgos:** normalización de textos y cálculo de atributos derivados (asimetría alta/baja, diferencia de prominencia entre "cancelar" y "retener", cantidad de ofertas de retención).
2. **Detección heurística** de patrones estructurales, que se resuelven con reglas explícitas (p. ej. baja que exige canal telefónico → obstrucción).
3. **Clasificación** de patrones semánticos mediante una **interfaz de clasificador independiente del modelo**, con dos implementaciones:
   - clasificador basado en un modelo de lenguaje local (LLM local, ejecutado con Ollama), cuya salida se valida contra un esquema; [[DECISIÓN: modelo y tamaño del LLM local — opciones a confirmar]]; [[DATO PENDIENTE: hardware donde corre el LLM local]];
   - línea base heurística.
4. **Agregación** de resultados en un índice de riesgo mediante una fórmula documentada y ponderada por patrón.
5. **Alerta previa a la contratación:** cuando se detecta permanencia o costos ocultos (patrón 6), el sistema emite una alerta previa a la contratación, antes de que se genere la tarjeta o el compromiso de pago.

### 5.3. Subconjunto de patrones (a confirmar con el estado del arte)

1. Asimetría alta/baja (*roach motel*)
2. Obstrucción (canal de baja forzado o inoperante)
3. *Confirmshaming*
4. Interferencia visual (opción de retención destacada, baja disimulada)
5. Interacción forzada / *nagging* (ofertas de retención sucesivas)
6. Costos o permanencia ocultos (*sneaking*)
7. Preselección de opciones desfavorables (*preselection*)

### 5.4. Salida

Un **informe de riesgo por servicio** que contiene:

- lista de patrones detectados, con el paso donde ocurren, la evidencia (elemento o texto) y la probabilidad o confianza asociada;
- índice de riesgo de cancelación (niveles bajo / medio / alto);
- alerta previa a la contratación, si se detectó permanencia o costos ocultos;
- fecha de captura del flujo analizado.

El índice de riesgo es la entrada que consume el motor de reglas (N2).

### 5.5. Límites

- No analiza imágenes ni sitios en vivo.
- No emite dictámenes legales: señala patrones, no incumplimientos normativos.
- Los flujos que terminan en canales no digitales (teléfono) se registran como tales, pero su contenido no se analiza.
- El resultado es válido para la fecha de captura; los servicios pueden modificar sus flujos.
- No extingue obligaciones contractuales ni previene deuda en servicios con permanencia: rechazar un cobro no rescinde el contrato. En esos servicios, el mecanismo se limita a la alerta previa a la contratación.

## 6. Supuestos y riesgos

| Riesgo | Mitigación |
|--------|------------|
| El LLM local puede variar su desempeño entre versiones del modelo. | Fijar la versión del modelo y registrarla junto con cada resultado; interfaz de clasificador independiente del modelo; línea base heurística propia. |
| La latencia del LLM local depende del hardware de ejecución. | Registrar el hardware utilizado e informar la latencia junto con él. [[DATO PENDIENTE: hardware donde corre el LLM local]] |
| El LLM local no es determinista: una misma entrada puede producir salidas distintas. | Fijar temperatura y semilla, registrarlas en cada ejecución y validar la salida contra un esquema. [[CITA PENDIENTE: respaldo de que fijar temperatura y semilla reduce la variabilidad en el runtime elegido]] |
| El mecanismo podría usarse en servicios con permanencia, donde rechazar el cobro puede generar deuda. | Alertar antes de contratar cuando se detecta permanencia o costos ocultos y explicitar el límite en el alcance y en la interfaz. |
| Construcción del corpus más costosa de lo previsto. | Limitar a 15–20 servicios; priorizar servicios con uso en Argentina y casos documentados. |
| Flujos detrás de inicio de sesión o que cambian con el tiempo. | Captura con cuentas de prueba; registro de fecha; el corpus es una fotografía, no un monitoreo continuo. |
| Tarjetas simuladas percibidas como "poco reales". | Adaptador para un proveedor real en sandbox como demostración opcional. |

## 7. Vínculo con la validación (a desarrollar en *Plan de validacion.md*)

| Componente | Métrica principal |
|------------|-------------------|
| N1 Detección | Precisión, *recall*, F1 y tasa de falsos positivos por patrón, sobre el corpus etiquetado; comparación clasificador LLM local vs. línea base heurística. |
| N1 Detección | Latencia por flujo analizado. |
| N2 Motor de reglas | Porcentaje de cumplimiento de reglas en escenarios de prueba (objetivo: 100 %). |
| N3 Emulador | Rechazo correcto de cobros tras vencimiento, tope o cantidad de cobros. |
| Plataforma | Usabilidad mediante SUS. |

## 8. Cambios en otros archivos

### 8.1. Título — DECIDIDO (29/09/2026)

- **Título anterior (Entrega 1):** *SuscripGuard: Plataforma Inteligente de Gestión de Suscripciones con Tarjetas Virtuales Automatizadas y Detección de Dark Patterns*.
- **Título adoptado:** *SuscripGuard: Control preventivo de suscripciones mediante tarjetas virtuales con políticas basadas en la detección de dark patterns*.
- **Justificación del cambio (para comunicar en la Entrega 2):** el título anterior enumeraba componentes al mismo nivel. El nuevo expresa la contribución central (control preventivo), el mecanismo (tarjetas virtuales con políticas) y la fuente de información que lo diferencia del estado del arte (detección de *dark patterns*), en línea con el punto 1 de la devolución. Se retiran "plataforma inteligente" y "gestión de suscripciones" porque describen el soporte, no el aporte.
- Se aplica a partir de la Entrega 2. No se modifican los documentos ya entregados.

### 8.2. Objetivo general — CONFIRMADO y aplicado en *Objetivos.md* (29/09/2026)

Diseñar, implementar y evaluar un prototipo de plataforma que prevenga cobros recurrentes no deseados mediante tarjetas virtuales cuyas políticas de uso se configuran a partir de la detección automática de *dark patterns* en los flujos de cancelación de los servicios.

### 8.3. Objetivos específicos — CONFIRMADOS y aplicados en *Objetivos.md* (29/09/2026)

1. Caracterizar los *dark patterns* presentes en flujos de cancelación de suscripciones y definir un subconjunto detectable junto con un esquema de representación estructurada de dichos flujos.
2. Construir un corpus etiquetado de flujos de cancelación de servicios por suscripción de uso frecuente.
3. Desarrollar un módulo de detección de *dark patterns*, independiente del modelo de clasificación, que genere un índice de riesgo por servicio.
4. Desarrollar un motor de reglas determinista y un emulador de tarjetas virtuales que apliquen políticas de vencimiento, tope de monto y cantidad de cobros a partir de dicho índice.
5. Integrar los componentes en un prototipo web que permita al usuario registrar suscripciones, revisar el riesgo de cada servicio y gestionar sus tarjetas.
6. Evaluar el prototipo en términos de precisión de detección, cumplimiento de reglas, rendimiento y usabilidad.

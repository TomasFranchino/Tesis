# Estado del arte comparativo — SuscripGuard

> **Estado:** borrador v0.2 (02/10/2026). Responde al punto 6 de la devolución de la Entrega 1: comparación sistemática entre las soluciones existentes y SuscripGuard, con criterios explícitos, para fundamentar la brecha.
> v0.2: aplicadas decisiones B1 y B2 (02/10/2026).
> Cada antecedente sigue la estructura definida en *1.1 Antecedentes de investigacion.md*: identificación, objetivo, tecnología/metodología, resultados y aporte a la tesis.
> Las correcciones de datos del archivo 1.1 están en la sección 7 y **no se aplicaron todavía**.

---

## 1. Protocolo de búsqueda

Para que la comparación sea reproducible se documenta cómo se buscaron los antecedentes.

- **Fuentes:** ACM Digital Library, IEEE Xplore, arXiv, Google Académico; literatura gris de organismos de protección al consumidor (FTC, ICPEN) y normativa argentina (Boletín Oficial).
- **Cadenas principales:** `"dark patterns" AND (detection OR automated)`; `"dark patterns" AND (subscription OR cancellation)`; `"deceptive design" AND "large language models"`; `"virtual cards" AND "subscription management"`.
- **Criterios de inclusión:** (a) taxonomías o estudios de prevalencia de *dark patterns* con metodología explícita; (b) sistemas de detección automática con métricas publicadas; (c) herramientas de gestión de suscripciones o de tarjetas virtuales para usuarios finales en operación.
- **Período:** 2018–2026 para trabajos académicos; productos vigentes a septiembre de 2026.
- **Pendiente:** búsqueda de antecedentes nacionales y locales en repositorios universitarios argentinos (p. ej. SEDICI-UNLP, RDU-UNC y el repositorio de la propia universidad). En esta primera búsqueda no se identificaron trabajos académicos argentinos sobre detección automática de *dark patterns*.

---

## 2. Antecedentes académicos

### 2.1. Taxonomías y prevalencia

**A1. Gray, Kou, Battles, Hoggatt y Toombs (2018).** *The Dark (Patterns) Side of UX Design.* CHI 2018.
- **Objetivo:** caracterizar los *dark patterns* desde la práctica del diseño UX.
- **Metodología:** análisis de un corpus de ejemplos recolectados por profesionales.
- **Resultados:** taxonomía de cinco estrategias: *nagging*, obstrucción, *sneaking*, interferencia en la interfaz y acción forzada.
- **Aporte:** base conceptual del subconjunto de patrones de SuscripGuard; varios de los 7 patrones elegidos derivan directamente de estas estrategias.

**A2. Mathur, Acar, Friedman, Lucherini, Mayer, Chetty y Narayanan (2019).** *Dark Patterns at Scale: Findings from a Crawl of 11K Shopping Websites.* CSCW 2019.
- **Objetivo:** medir la prevalencia de *dark patterns* en comercio electrónico.
- **Metodología:** rastreo automatizado de ~53 000 páginas de producto en ~11 000 sitios, agrupamiento de textos y revisión manual.
- **Resultados:** 1 818 instancias de 15 tipos en 7 categorías, en 183 sitios; 22 proveedores externos que venden *dark patterns* como servicio.
- **Aporte:** antecedente de detección semiautomática **basada en texto**. Se centra en páginas de producto, no en flujos de cancelación.

**A3. Di Geronimo, Braz, Fregnan, Palomba y Bacchelli (2020).** *UI Dark Patterns and Where to Find Them.* CHI 2020.
- **Objetivo:** medir la presencia de *dark patterns* en aplicaciones móviles y su percepción por los usuarios.
- **Metodología:** inspección manual de 240 aplicaciones populares y estudio con 589 participantes.
- **Resultados:** el 95 % de las aplicaciones contiene al menos un *dark pattern*. La mayoría de los usuarios no los reconoce por sí misma, aunque mejora cuando se le informa del tema.
- **Aporte:** fundamenta que la detección no puede dejarse al usuario y que informar la evidencia tiene valor (RF-06, RF-25).

**A4. Nembaware y Sousa (2025).** *Dark patterns in subscription service cancellation processes.* ECCE 2025 (ACM).
- **Objetivo:** analizar cómo los *dark patterns* obstaculizan la cancelación de suscripciones y su efecto en la experiencia y la confianza.
- **Metodología:** revisión de 28 fuentes académicas y de literatura gris, de la que surgen **44 dark patterns en 10 categorías**; análisis manual de los flujos de cancelación de 6 servicios (The Economist, Bloomberg, Scribd, Adobe, Amazon Prime, Audible); experimento con 34 participantes usando SUS y una escala de confianza.
- **Resultados:** SUS de 36 para el flujo con más patrones (The Economist) frente a 78 para Bloomberg; caída del 28 % en la confianza (p < 0,001); el 12 % volvería a contratar The Economist frente al 79 % en Bloomberg.
- **Aporte:** es el antecedente **más cercano en dominio**. Confirma que el flujo de cancelación es una unidad de análisis válida y aporta una taxonomía específica, pero el análisis es **manual** y no se vincula a ninguna acción de protección.

**A5. ICPEN y GPEN, con la FTC (2024).** *Dark Patterns in Subscription Services Sweep.* Informe público, julio de 2024.
- **Objetivo:** relevar el uso de *dark patterns* en la comercialización de servicios por suscripción.
- **Metodología:** revisión coordinada por autoridades de 26 países de 642 sitios web y aplicaciones por suscripción.
- **Resultados:** el 76 % usaba al menos un posible *dark pattern* y el 67 %, varios. Los más frecuentes fueron *sneaking* e interferencia en la interfaz.
- **Aporte:** dato de prevalencia **específico de suscripciones** y de fuente primaria. Reemplaza a las estadísticas sin fuente del archivo 1.1.

### 2.2. Detección automática

| Id | Trabajo | Entrada | Técnica | Datos | Resultados | Limitación relevante para la tesis |
|----|---------|---------|---------|-------|-----------|-------------------------------------|
| B1 | **AidUI** — Mansur, Salma, Awofisayo y Moran (2023), ICSE 2023 | Capturas de pantalla (móvil y web) | Visión por computadora + PLN | ContextDP: 258 capturas, 301 instancias, 10 tipos | P 0,66 · R 0,67 · F1 0,65 | Pantallas aisladas; dataset pequeño |
| B2 | **UIGuard** — Chen, Sun, Feng, Xing, Lu, Xu y Chen (2023), UIST 2023 | Capturas + jerarquía de la UI (móvil) | Visión + reglas derivadas de taxonomías | 1 353 UIs con patrones y 4 999 benignas de 1 023 apps | P 0,82 · R 0,77 · F1 0,79 | Pantallas aisladas; solo móvil |
| B3 | **AppRay** — Chen et al. (2024), preprint arXiv | Jerarquías, capturas, texto y trazas de interacción | Exploración de la app guiada por LLM (GPT-4) + clasificador contrastivo + reglas | 2 185 instancias (149 dinámicas), 18 tipos, 100 apps | Micro F1 0,76 · macro F1 0,62 · 12 % de falsos positivos en UIs benignas | Analiza secuencias de varios pasos e incluye *roach motel*, pero en apps móviles genéricas y sin vínculo con una acción |
| B4 | **AutoBot** — Nayak, Zhang, Wani, Khandelwal y Fawaz (2024/2025), ACM | Capturas web convertidas en una representación estructurada en texto (*ElementMap*) | Visión (OCR + detector de objetos) → LLM (Gemini, Qwen2.5, Flan-T5) | 11 118 sitios para entrenamiento; 1 152 anotados para evaluación | F1 0,93 (clasificación binaria, Gemini) | Solo patrones estáticos; solo inglés |
| B5 | **DPDGPT** — Lin, Nie, Xue, Zhang y Zhang (2026), *Information and Software Technology* 190 | Capturas (visual + texto) | LLM multimodal con razonamiento en cadena y verificación | 1 609 UIs, 2 015 instancias, 19 tipos | P 0,86 · R 0,91 · F1 0,88 | Pantallas aisladas; sin foco en suscripciones |

**Aportes a la tesis:**
- **B4 respalda directamente una decisión de diseño de SuscripGuard.** AutoBot convierte la interfaz en una **representación estructurada en texto** antes de clasificar con un modelo de lenguaje, y así alcanza el mejor desempeño reportado. Es el mismo enfoque del aporte A1 (esquema estructurado del flujo), que además permite usar un clasificador de solo texto, como el clasificador basado en un modelo de lenguaje local (LLM local, ejecutado con Ollama) previsto para SuscripGuard.
- **B3 es el antecedente técnico más cercano:** analiza secuencias de varios pasos y detecta *roach motel*. Muestra que el análisis de flujos es viable, y que el desempeño por tipo de patrón es bastante menor que el global (macro F1 0,62 frente a micro 0,76).
- **Referencia para los umbrales:** los trabajos publicados reportan F1 entre 0,62 y 0,93. Los umbrales propuestos en *Plan de validacion.md* (*recall* ≥ 0,75, precisión ≥ 0,70) caen dentro de ese rango.

---

## 3. Soluciones comerciales

| Solución | Qué hace | Mecanismo | Disponibilidad | Limitación frente al problema |
|----------|----------|-----------|----------------|-------------------------------|
| **Rocket Money** | Detecta suscripciones y ofrece un servicio que cancela en nombre del usuario | Vinculación con cuentas bancarias; gestión manual de cancelaciones | EE.UU. | Reactivo: actúa después del cobro; exige acceso a datos bancarios |
| **Privacy.com** | Tarjetas virtuales bloqueadas a un comercio, de un solo uso, con límite de gasto, pausables | Emisor de tarjetas virtuales | Solo ciudadanos o residentes de EE.UU. | Da el mecanismo, pero el usuario configura cada tarjeta sin información sobre el riesgo del servicio |
| **Revolut** (tarjetas desechables) | Tarjeta virtual cuyos datos se regeneran después de cada uso | Banco digital | Según país; **disponibilidad en Argentina a verificar** | Solo uso único; sin reglas por suscripción |
| **Billeteras argentinas** (Ualá, Mercado Pago, Naranja X, Brubank, Lemon) | Tarjetas virtuales prepagas | Billetera o banco digital | Argentina | **Controles por comercio, de uso único o con vencimiento: a relevar en cada aplicación**; no se documentó gestión de suscripciones basada en riesgo |
| **Stripe Issuing, Lithic, Pomelo** | APIs para que empresas emitan tarjetas | Infraestructura BaaS (Pomelo es argentina) | Empresas; Pomelo opera en Latinoamérica | No son productos para usuarios finales; son posibles proveedores del adaptador *Emisor* (ADR-02) |

**Marco regulatorio (no es una herramienta, pero condiciona el problema):**
- **Argentina:** la Disposición 954/2025 de la Subsecretaría de Defensa del Consumidor y Lealtad Comercial regula el botón de baja y prohíbe exigir registros o trámites adicionales. La Disposición 3/2026 (6 de febrero de 2026) admite verificaciones de identidad "razonables".
- **EE.UU.:** la regla *Click-to-Cancel* de la FTC fue anulada por la Corte de Apelaciones del 8.º Circuito en julio de 2025. La FTC reabrió el proceso en marzo de 2026 y, mientras tanto, sanciona bajo ROSCA y la Sección 5 de la FTC Act.

**Lectura para la justificación:** la regulación avanza, pero actúa después de que se produce el daño y sus plazos se miden en años. El caso de Telecentro y DirecTV (archivo 1.1) muestra que aun con botón de baja obligatorio persisten los incumplimientos. Esto refuerza la necesidad de una protección que dependa del usuario y no del proveedor.

---

## 4. Criterios de comparación

| Id | Criterio | Por qué importa para el problema |
|----|----------|----------------------------------|
| G1 | Detecta o registra suscripciones | Condición para gestionarlas |
| G2 | Control preventivo sobre el medio de pago, con reglas por suscripción | Evita el cobro en lugar de reclamarlo después |
| G3 | Política configurada a partir de información sobre el servicio | Distingue controlar de controlar con criterio |
| D1 | Foco en flujos de cancelación de suscripciones | Es donde se concentra el daño |
| D2 | Análisis automatizado | Escala más allá de la inspección manual |
| D3 | Analiza secuencias de varios pasos, no pantallas aisladas | *Roach motel* y obstrucción solo se ven en el flujo completo |
| D4 | Evidencia explicable por cada detección | Confianza y comprensión del usuario (A3) |
| D5 | Métricas de desempeño publicadas o previstas | Validez científica |
| X1 | No requiere acceso a cuentas bancarias ni correos del usuario | Privacidad |
| X2 | Aplicable en Argentina / servicios en español | Contexto de la tesis |

---

## 5. Comparación sistemática

Referencias: ● cumple · ◐ parcial · ○ no cumple · — no aplica · n/r no reportado

| Solución | G1 | G2 | G3 | D1 | D2 | D3 | D4 | D5 | X1 | X2 |
|----------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Rocket Money | ● | ○ | ○ | ○ | — | — | — | ○ | ○ | ○ |
| Privacy.com | ◐ | ● | ○ | ○ | — | — | — | ○ | ◐ | ○ |
| Revolut (desechables) | ○ | ◐ | ○ | ○ | — | — | — | ○ | ● | ◐ |
| Billeteras argentinas | ○ | ◐ | ○ | ○ | — | — | — | ○ | ● | ● |
| A4 Nembaware y Sousa | — | — | — | ● | ○ | ● | ● | ◐ | — | ○ |
| B1 AidUI | — | — | — | ○ | ● | ○ | ● | ● | — | n/r |
| B2 UIGuard | — | — | — | ○ | ● | ○ | ● | ● | — | n/r |
| B3 AppRay | — | — | — | ◐ | ● | ● | ◐ | ● | — | n/r |
| B4 AutoBot | — | — | — | ○ | ● | ○ | ● | ● | — | ○ |
| B5 DPDGPT | — | — | — | ○ | ● | ○ | ◐ | ● | — | n/r |
| **SuscripGuard** | ◐ | ● | ● | ● | ● | ● | ● | ● (previstas) | ● | ● |

**Notas sobre SuscripGuard:**
- **G1 ◐:** el registro es manual; la detección por correo es complementaria.
- **D2 ●:** el análisis es automático, pero la **captura** de los flujos es semiautomática (RF-10).
- **D3 ●:** sobre flujos capturados; no incluye exploración autónoma de aplicaciones como AppRay.
- **D5:** las métricas están **previstas** en *Plan de validacion.md*; todavía no hay resultados.

---

## 6. Brecha identificada

La revisión muestra tres líneas de trabajo que avanzan por separado:

1. **Detección automática de *dark patterns* (B1–B5).** Madura en pantallas aisladas y, recientemente, en secuencias (B3). Sin embargo:
   - ningún trabajo toma como objeto de análisis los **flujos de cancelación de suscripciones**, con su asimetría entre alta y baja y la derivación entre canales;
   - la detección es un fin en sí mismo (auditoría o concientización): **ningún trabajo usa el resultado para tomar una acción de protección**;
   - los datos y herramientas se centran en inglés (explícito en B4), y **no se identificaron corpus de flujos de cancelación en español ni de servicios usados en Argentina**.
2. **Estudios del dominio de cancelación (A4, A5).** Confirman el problema y aportan taxonomías, pero son **manuales**.
3. **Herramientas de control de pagos (Privacy.com, Revolut, billeteras).** Ofrecen el mecanismo preventivo, pero **sin información sobre el riesgo del servicio**: la configuración queda librada al criterio del usuario. Las más completas no están disponibles en Argentina.

**Formulación de la brecha:**
No se identificaron trabajos ni productos que detecten automáticamente *dark patterns* en flujos de cancelación de suscripciones y usen ese resultado para configurar un control preventivo sobre el medio de pago. Tampoco se identificaron para servicios en español ni para el contexto argentino. SuscripGuard propone cerrar esa brecha integrando las tres líneas.

**Alcance de la afirmación:** la brecha vale para la búsqueda documentada en la sección 1. Se ampliará con la búsqueda en repositorios nacionales antes de la versión final.

---

## 7. Correcciones al archivo *1.1 Antecedentes de investigacion.md* (pendientes de aplicar)

| Afirmación actual | Problema | Corrección propuesta |
|-------------------|----------|----------------------|
| "Los hogares estadounidenses gastan en promedio $273 USD al mes… el 89 % subestima…" | Sin fuente identificable | Reemplazar por C+R Research (2022), n = 1 000: gasto estimado USD 86/mes frente a USD 219 real; el 42 % había olvidado cobros de suscripciones que ya no usaba |
| "El mercado global… ~$536 mil millones en 2025 y $859 mil millones para 2026" | Sin fuente primaria; un crecimiento del 60 % en un año no es verosímil | Eliminar o reemplazar por una fuente primaria verificable |
| "41 % reporta fatiga…; 47 % canceló…" | Sin fuente | Verificar o eliminar |
| "42 % de estadounidenses han seguido pagando suscripciones olvidadas" | Sin cita | Mantener, citando C+R Research (2022) |
| "Amazon Prime (multado por la FTC con $2,5 mil millones en 2025)" | No fue una multa | Acuerdo con la FTC de septiembre de 2025 por USD 2 500 millones, que incluye una sanción civil y reembolsos a consumidores |
| "FTC (Click-to-Cancel rule, aunque con desafíos judiciales)" | Desactualizado | Anulada por el 8.º Circuito en julio de 2025; la FTC reabrió el proceso (ANPRM) en marzo de 2026 |
| "Trim, Mint y similares" | Mint dejó de operar en 2024; el estado de Trim no está verificado | Quitar Mint; verificar Trim o reemplazarlo |
| "Resolución 954 de la Secretaría de Defensa del Consumidor de la Nación" | Denominación incorrecta | Disposición 954/2025 de la Subsecretaría de Defensa del Consumidor y Lealtad Comercial, complementada por la Disposición 3/2026 |
| "Estudios recientes identifican taxonomías de 44+ dark patterns…" | Sin atribución | Atribuir a Nembaware y Sousa (2025), ECCE 2025 |
| Enlace `dl.acm.org/doi/epdf/10.1145/3637336` | No se pudo identificar a qué trabajo corresponde | Verificar título y autores o quitar |

---

## 8. Referencias

- Chen, J. et al. (2023). *Unveiling the Tricks: Automated Detection of Dark Patterns in Mobile Applications.* UIST 2023. https://portal.fis.tum.de/en/publications/unveiling-the-tricks-automated-detection-of-dark-patterns-in-mobi/
- Chen, J. et al. (2024). *From Exploration to Revelation: Detecting Dark Patterns in Mobile Apps.* arXiv. https://arxiv.org/abs/2411.18084
- C+R Research (2022), citado en CNBC. https://www.cnbc.com/2022/06/02/consumers-spend-133-more-monthly-on-subscriptions-than-they-realize.html
- Di Geronimo, L. et al. (2020). *UI Dark Patterns and Where to Find Them.* CHI 2020. https://dl.acm.org/doi/10.1145/3313831.3376600
- FTC (2025). *FTC Secures Historic $2.5 Billion Settlement Against Amazon.* https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-secures-historic-25-billion-settlement-against-amazon
- Gray, C. M. et al. (2018). *The Dark (Patterns) Side of UX Design.* CHI 2018. https://dl.acm.org/doi/10.1145/3173574.3174108
- ICPEN (2024). *Dark Patterns in Subscription Services Sweep — Public Report.* https://www.icpen.org/sites/default/files/2024-07/Public%20Report%20ICPEN%20Dark%20Patterns%20Sweep.pdf
- Lin, F. et al. (2026). *DPDGPT: Using Multimodal Large Language Models for Automated Detection of Dark Patterns.* Information and Software Technology, 190. https://www.sciencedirect.com/science/article/abs/pii/S0950584925002757
- Mansur, S. M. H. et al. (2023). *AidUI: Toward Automated Recognition of Dark Patterns in User Interfaces.* ICSE 2023. https://arxiv.org/abs/2303.06782
- Mathur, A. et al. (2019). *Dark Patterns at Scale.* CSCW 2019. https://arxiv.org/abs/1907.07032
- Nayak, A. et al. (2024/2025). *Automatically Detecting Online Deceptive Patterns.* https://arxiv.org/abs/2411.07441 · https://dl.acm.org/doi/10.1145/3719027.3765191
- Nembaware, F. E. y Sousa, S. C. (2025). *Dark patterns in subscription service cancellation processes.* ECCE 2025. https://doi.org/10.1145/3746175.3746211
- Privacy.com — controles de tarjeta. https://www.privacy.com/control
- Rocket Money — gestión de suscripciones. https://www.rocketmoney.com/feature/manage-subscriptions
- Disposición 954/2025 y Disposición 3/2026 (Argentina). https://noetingeryarmando.com/boton-de-baja-y-boton-de-arrepentimiento-verificacion-de-identidad-y-alcance-de-la-disposicion-3-2026/ · https://www.argentina.gob.ar/normativa/nacional/norma-423007
- Regla *Click-to-Cancel*: anulación y nueva reglamentación. https://www.fenwick.com/insights/publications/eighth-circuit-vacates-ftcs-click-to-cancel-rule · https://www.jonesday.com/en/insights/2026/05/ftc-revives-clicktocancel-rule-new-risks-for-subscription-businesses

<!-- NOTA PARA TOMÁS: borrador inicial del Capítulo 2. Insumos usados: `insumos/Estado del arte comparativo.md` (completo, salvo su sección 7 de correcciones sin verificar, de la que solo se tomó la denominación correcta de la Disposición 954/2025), `insumos/Contribucion y alcance.md` (secciones 1, 3, 4.4, 5 y 6), `gestion/GLOSARIO.md` (solo cinco términos, sin definiciones) y `insumos/Plan de validacion.md` (sección 2.1). `bibliografia/referencias.bib` está vacío y no hay fichas verificadas: toda afirmación respaldada en la literatura lleva `[[CITA PENDIENTE: …]]` y las cifras de los antecedentes provienen del archivo de estado del arte, sin haber sido contrastadas con las fuentes originales. Lo que falta: (a) bases teóricas generales (modelo de suscripción, definición de *dark pattern*, tarjetas virtuales, métricas de clasificación) que no están en los insumos; (b) fuentes primarias de la normativa (T-007); (c) mapeo de los siete patrones a las taxonomías (T-012); (d) búsqueda de antecedentes nacionales; (e) corrección de la frase sobre el rango de F1 y los umbrales (T-014), que no se reprodujo. Las secciones de justificación y de brecha conviene que se reescriban con la voz del tesista. -->

# Marco teórico

Este capítulo fija las bases conceptuales y el estado del arte sobre los que se apoya SuscripGuard. Primero se presentan los conceptos que sustentan el problema (suscripciones, *dark patterns* o patrones oscuros, detección automática, tarjetas virtuales y marco normativo). Luego se reseñan los antecedentes académicos y comerciales y se los compara con criterios explícitos para delimitar la brecha que el trabajo propone atender. Por último, se definen los términos que el resto de la memoria utiliza con un sentido preciso. El capítulo no incluye resultados propios: los antecedentes se reseñan con las cifras que sus autores reportan, que se contrastarán con las fuentes originales (véanse los marcadores de cita pendiente).

## Bases teóricas

Esta sección reúne los conceptos necesarios para formular el problema y el enfoque de solución. Se parte del modelo de suscripción y de la asimetría entre alta y baja, se presentan los *dark patterns* y sus taxonomías, se acotan los siete patrones que interesan en los flujos de cancelación, se describen los enfoques de detección automática y los mecanismos de control sobre el medio de pago, y se cierra con el marco normativo que condiciona el problema.

### Suscripciones, renovación automática y pruebas gratuitas

Esta subsección describe el modelo de negocio por suscripción en lo que es relevante para el problema: la renovación automática, la prueba gratuita y la asimetría entre la contratación y la baja.

En un servicio por suscripción, el usuario autoriza cobros periódicos a cambio del acceso continuado a un servicio digital. La renovación se produce de forma automática: el cobro siguiente ocurre salvo que el usuario realice una acción explícita de baja. Muchos servicios ofrecen además una prueba gratuita, es decir, un período inicial sin cargo tras el cual el servicio comienza a cobrarse al precio regular si el usuario no cancela antes de que termine. [[CITA PENDIENTE: desarrollar el modelo de suscripción, la renovación automática y la prueba gratuita con fuentes académicas o institucionales (marco teórico, T-024)]]

El rasgo que vuelve problemático este modelo es la asimetría entre el alta y la baja. Los insumos del trabajo describen que los procesos de cancelación incorporan con frecuencia *dark patterns* que prolongan cobros no deseados, y que el alta y la baja de un mismo servicio pueden exigir esfuerzos muy distintos: cantidad de pasos, canal requerido, necesidad de iniciar sesión o derivación a un canal no digital. [[CITA PENDIENTE: estudios que documenten la asimetría entre alta y baja y sus consecuencias económicas para los usuarios (marco teórico, T-024)]]

Para el usuario, el resultado práctico es que los cobros recurrentes quedan sujetos a la voluntad del proveedor: aunque el usuario decida terminar la relación, el cobro continúa mientras el flujo de cancelación no se complete con éxito. El problema que aborda esta tesis se acota a las suscripciones digitales pagadas con tarjeta y sin permanencia mínima, incluidas las pruebas gratuitas, y a los daños que un control sobre el medio de pago puede prevenir: los cobros posteriores a una baja o al fin de una prueba gratuita. Los daños que derivan de obligaciones contractuales, como la deuda, los intereses o las gestiones de cobranza, se consideran contexto y limitación, porque rechazar un cobro no rescinde el contrato. Esta distinción reaparece al tratar la permanencia mínima en los conceptos clave y en el alcance del Capítulo 1.

La subsección siguiente presenta el concepto de *dark pattern* y las taxonomías que permiten describir las prácticas que se manifiestan en esos flujos.

### Los *dark patterns* (patrones oscuros): concepto y taxonomías

Esta subsección presenta el concepto de *dark pattern* y las tres taxonomías que, según el estado del arte relevado, sirven de base para describirlos: la de Gray et al., la de Mathur et al. y la de Nembaware y Sousa.

Los *dark patterns* (patrones oscuros) son elementos de diseño de interfaz que inducen al usuario a tomar decisiones que no tomaría en otras condiciones o que lo perjudican. [[CITA PENDIENTE: definición de *dark pattern* tomada de una fuente primaria (p. ej. Gray et al., 2018, o la bibliografía sobre diseño engañoso); los insumos no la formulan de manera explícita (marco teórico, T-024)]]

Gray, Kou, Battles, Hoggatt y Toombs (2018) abordaron el fenómeno desde la práctica del diseño de experiencia de usuario (UX): analizaron un corpus de ejemplos recolectados por profesionales y propusieron una taxonomía de cinco estrategias: *nagging* (insistencia reiterada), obstrucción, *sneaking* (inclusión encubierta de costos o condiciones), interferencia en la interfaz y acción forzada. [[CITA PENDIENTE: Gray, Kou, Battles, Hoggatt y Toombs (2018), *The Dark (Patterns) Side of UX Design*, CHI 2018; verificar la formulación de las cinco estrategias]] Esta taxonomía es la base conceptual del subconjunto de patrones de SuscripGuard.

Mathur et al. (2019) adoptaron un enfoque de medición: rastrearon de forma automatizada alrededor de 53 000 páginas de producto en unos 11 000 sitios de comercio electrónico, agruparon los textos y revisaron manualmente los resultados. Identificaron 1 818 instancias de 15 tipos de *dark patterns*, agrupados en 7 categorías, presentes en 183 sitios, y registraron 22 proveedores externos que ofrecen *dark patterns* como servicio. [[CITA PENDIENTE: Mathur, Acar, Friedman, Lucherini, Mayer, Chetty y Narayanan (2019), *Dark Patterns at Scale: Findings from a Crawl of 11K Shopping Websites*, CSCW 2019; verificar cifras]] Su trabajo es un antecedente de detección semiautomática basada en texto, aunque se centra en páginas de producto y no en flujos de cancelación.

Nembaware y Sousa (2025) elaboraron la taxonomía más próxima al dominio de esta tesis. A partir de una revisión de 28 fuentes académicas y de literatura gris, relevaron 44 *dark patterns* en 10 categorías relacionados con la cancelación de suscripciones. [[CITA PENDIENTE: Nembaware y Sousa (2025), *Dark patterns in subscription service cancellation processes*, ECCE 2025; verificar la cifra de 44 patrones en 10 categorías y las 28 fuentes]] Su aporte principal para esta tesis es haber tomado el flujo de cancelación como unidad de análisis, un criterio que se retoma en el estado del arte.

Las tres taxonomías difieren en el nivel de abstracción (estrategias, tipos, patrones por categoría) y en la procedencia de sus datos (práctica profesional, rastreo automatizado, revisión de literatura). Ninguna fue concebida específicamente para decidir sobre un medio de pago; adaptar la que mejor se ajuste a los flujos de cancelación es parte del trabajo previsto. La subsección siguiente concreta esa adaptación en los siete patrones que se analizarán.

### Los *dark patterns* en los flujos de cancelación

Esta subsección presenta los siete patrones que SuscripGuard prevé detectar en los flujos de cancelación, tal como los definen los documentos de trabajo del proyecto, y señala qué parte de su definición está aún por confirmar.

El subconjunto elegido es el siguiente. Los nombres de cuatro de los patrones coinciden con los de estrategias de la taxonomía de Gray et al. (*nagging*, *sneaking*, obstrucción e interferencia), pero el mapeo explícito entre cada patrón y las taxonomías no está completo; se resolverá junto con la guía de etiquetado.

| Patrón | Descripción en el diseño del proyecto | Señal operativa prevista |
|--------|---------------------------------------|--------------------------|
| Asimetría alta/baja (*roach motel*, trampa de entrada fácil y salida difícil) | La baja exige más esfuerzo que el alta. | Diferencia entre la cantidad de pasos de alta y de baja registrados en el flujo. |
| Obstrucción | Canal de baja forzado o inoperante. | Regla explícita: una baja que exige canal telefónico se marca como obstrucción. |
| *Confirmshaming* (culpabilización al rechazar una oferta) | [[CITA PENDIENTE: definición del patrón; los insumos solo lo nombran]] | Clasificación de los textos visibles de cada paso con el clasificador. |
| Interferencia visual | Opción de retención destacada o baja disimulada. | Atributos de prominencia derivados del DOM/CSS (tamaño relativo, contraste, posición) y diferencia de prominencia entre "cancelar" y "retener". |
| Interacción forzada / *nagging* | Ofertas de retención sucesivas. | Cantidad de ofertas de retención en el flujo. |
| Costos o permanencia ocultos (*sneaking*) | Permanencia mínima o costos ocultos del servicio. [[CITA PENDIENTE: definición del patrón; los insumos solo lo nombran]] | Análisis del correo de confirmación del alta (véase abajo). |
| Preselección de opciones desfavorables (*preselection*) | Opciones desfavorables para el usuario marcadas de antemano. | [[DATO PENDIENTE: señal operativa del patrón; los insumos no la especifican]] |

<!-- NOTA PARA TOMÁS: la descripción de "costos o permanencia ocultos" y de "preselección" es una paráfrasis mínima de los nombres que figuran en Contribucion y alcance.md §5.3; los insumos no traen una definición más elaborada. Las definiciones operativas con ejemplos positivos y negativos se elaborarán en la guía de etiquetado (Plan de validacion.md §2.1). -->

El subconjunto está a confirmar con el estado del arte: el mapeo detallado de cada patrón a las taxonomías anteriores (tarea de mapeo de patrones, T-012) está pendiente y puede ajustar la lista. [[DECISIÓN: confirmar o modificar el subconjunto de siete patrones tras el mapeo con las taxonomías; la lista actual es la de Contribucion y alcance.md §5.3 y no se modifica hasta que el tesista responda]]

Los patrones se clasifican según dónde se observan. Los seis primeros se manifiestan en el flujo de cancelación y se analizan sobre su representación estructurada. El de costos o permanencia ocultos, en cambio, se manifiesta en el alta: las condiciones de contratación (permanencia mínima, penalidad por baja anticipada, renovación automática, precio tras la prueba) se informan, o deberían informarse, al contratar. Por eso se lo analiza sobre el correo de confirmación del alta y sustenta la alerta de permanencia o costos ocultos, que se emite cuando el análisis del correo con el clasificador basado en un modelo de lenguaje local (LLM local) detecta esas condiciones. El diseño parte de que estas condiciones deben informarse en la confirmación de la contratación. [[CITA PENDIENTE: norma que obliga a informar la permanencia mínima y los cargos en el correo o comprobante de confirmación de la suscripción; jurisdicción y alcance (verificación de la norma aplicable, T-029)]]

Queda abierta una decisión sobre el momento de la alerta. Dado que el correo de confirmación llega después del alta, la alerta no puede ser previa a la contratación. [[DECISIÓN: momento de la alerta. A) redefinirla como alerta temprana posterior al alta, vinculada con el derecho de revocación de la contratación a distancia (requiere cita de la norma y del plazo, T-029); B) conservar además el análisis del flujo de alta para emitir una alerta realmente previa, lo que amplía el corpus. Recomendación de los insumos: A, porque mantiene el corpus y el alcance técnico definidos]]

La alerta tiene límites propios. Depende de lo que informe el correo: si una condición no figura, no se detecta y su ausencia se registra como tal, no como "sin permanencia". Además, la alerta no evita la deuda en servicios con permanencia, porque bloquear la tarjeta no extingue la obligación contractual.

La subsección siguiente aborda cómo se puede detectar estos patrones de manera automática.

### Detección automática: representaciones estructuradas y modelos de lenguaje

Esta subsección resume lo que enseñan los antecedentes sobre cómo representar una interfaz para analizarla automáticamente y presenta la distinción entre una línea base heurística y un clasificador basado en un modelo de lenguaje.

Los sistemas relevados en el estado del arte difieren en lo que toman como entrada. La mayoría analiza pantallas aisladas, ya sea capturas de pantalla (AidUI, DPDGPT), capturas junto con la jerarquía de la interfaz (UIGuard) o capturas de sitios web convertidas en una representación intermedia (AutoBot). Una excepción es AppRay, que explora aplicaciones móviles de manera guiada por un modelo de lenguaje y analiza secuencias de varios pasos, lo que le permite incluir patrones como el *roach motel*, que solo se aprecian en el flujo completo. [[CITA PENDIENTE: verificar en las fuentes originales la entrada y la técnica de cada sistema (marco teórico, T-024)]]

De esos antecedentes se desprende una idea de diseño: convertir primero la interfaz en una representación estructurada en texto y clasificar después. AutoBot transforma las capturas web en una representación en texto (*ElementMap*) mediante OCR y un detector de objetos, y luego clasifica con un modelo de lenguaje; reporta el mejor desempeño del conjunto de antecedentes relevados (F1 de 0,93 en clasificación binaria). [[CITA PENDIENTE: Nayak, Zhang, Wani, Khandelwal y Fawaz (2024/2025), *Automatically Detecting Online Deceptive Patterns*; verificar la técnica y el F1 reportados]] Este enfoque respalda la decisión de SuscripGuard de trabajar sobre una representación estructurada (JSON) del flujo, que contiene textos visibles, elementos interactivos con su rol, atributos de prominencia y canal de baja, y que permite emplear un clasificador de solo texto sin analizar imágenes. El esquema de esa representación constituye el aporte A1 de la tesis y se describe en el Capítulo 4.

La segunda idea es la complementariedad entre reglas y modelos. Algunos patrones son estructurales y se resuelven con reglas explícitas (por ejemplo, una baja que exige el canal telefónico). Otros son semánticos y requieren interpretar el texto. Para estos, SuscripGuard prevé una interfaz de clasificador independiente del modelo con dos implementaciones. La primera es un clasificador basado en un modelo de lenguaje local (LLM local), ejecutado localmente con la herramienta Ollama, cuya salida se valida contra un esquema. La segunda es una línea base heurística, basada en reglas, que sirve de referencia para medir si el modelo de lenguaje aporta algo respecto de una solución simple (aporte A5 y subpregunta SP2). Mantener el análisis en un modelo local responde también a una restricción de privacidad: los correos de confirmación contienen datos personales y no se envían a servicios externos. [[CITA PENDIENTE: respaldo técnico del funcionamiento de modelos locales con Ollama y de la validación de salidas contra un esquema; los insumos no lo documentan (marco teórico, T-024)]]

Los modelos de lenguaje no son deterministas: una misma entrada puede producir salidas distintas, y el desempeño puede variar entre versiones del modelo. El diseño prevé fijar la versión del modelo, la temperatura y la semilla, y registrarlas junto con cada resultado. [[CITA PENDIENTE: respaldo de que fijar temperatura y semilla reduce la variabilidad en el entorno de ejecución elegido]] Por esta razón, el motor de reglas que ejecuta la política de tarjeta es determinista y no incorpora ningún componente probabilístico.

La detección produce un índice de riesgo; su uso sobre el medio de pago es el objeto de la subsección siguiente.

### Tarjetas virtuales y control preventivo del medio de pago

Esta subsección presenta las tarjetas virtuales como mecanismo de control sobre el medio de pago y explica por qué el control es preventivo y no reactivo.

Una tarjeta virtual es un número de tarjeta que se emite de forma digital, sin soporte físico, y puede asociarse a un uso acotado. [[CITA PENDIENTE: definición de tarjeta virtual y descripción del ciclo de vida de emisión, autorización y rechazo en una fuente técnica o institucional (marco teórico, T-024)]] Las soluciones relevadas muestran distintas formas de acotar ese uso: tarjetas bloqueadas a un comercio, de un solo uso, con límite de gasto o pausables (Privacy.com), tarjetas cuyos datos se regeneran después de cada uso (Revolut) y tarjetas virtuales prepagas ofrecidas por billeteras y bancos digitales argentinos. Detrás de estos productos existen proveedores de infraestructura de emisión para empresas (Stripe Issuing, Lithic y Pomelo, esta última de origen argentino). [[CITA PENDIENTE: fuentes oficiales de cada solución; los insumos solo citan las páginas de Privacy.com y de Rocket Money, y no hay fuentes verificadas para el resto]]

El control sobre el medio de pago es preventivo porque actúa antes del cobro: si la tarjeta está vencida, alcanzó su tope de monto o agotó la cantidad de cobros permitida, la autorización se rechaza. Se diferencia así de la gestión reactiva de suscripciones, que detecta el cobro una vez producido y asiste la cancelación. Esta propiedad permite que el usuario deje de depender del flujo de cancelación del proveedor.

SuscripGuard aplica esa propiedad con una tarjeta virtual dedicada a cada suscripción y una política de tarjeta que combina vencimiento, tope de monto y cantidad de cobros. A diferencia de los productos relevados, donde el usuario configura cada tarjeta sin información sobre el riesgo del servicio, la política se propone a partir del índice de riesgo de cancelación y el usuario la confirma o ajusta. Dado que la emisión de tarjetas reales requiere licencias y cumplimiento del estándar PCI-DSS [[CITA PENDIENTE: requisitos regulatorios y de seguridad de la emisión de tarjetas reales, incluida la disponibilidad de proveedores en Argentina]], el prototipo emulará el ciclo de vida de la tarjeta (emisión, autorización o rechazo, bloqueo y destrucción) detrás de una interfaz de adaptador, de modo que un proveedor real pueda incorporarse sin modificar el núcleo.

La última base conceptual es el marco normativo, que establece obligaciones para los proveedores y permite entender los límites de una solución centrada en el usuario.

### Marco normativo

Esta subsección describe las normas que regulan la baja de servicios por suscripción en Argentina y en Estados Unidos, y relaciona esa regulación con el problema.

En Argentina, la Disposición 954/2025 de la Subsecretaría de Defensa del Consumidor y Lealtad Comercial regula el botón de baja y prohíbe exigir registros o trámites adicionales para darse de baja. La Disposición 3/2026, del 6 de febrero de 2026, admite verificaciones de identidad "razonables" en ese trámite. [[CITA PENDIENTE: fuente oficial primaria (texto de las disposiciones en el Boletín Oficial o en la base de normativa nacional) en lugar de los comentarios de estudios jurídicos que figuran hoy como referencia; verificar la denominación, el alcance, el plazo de vigencia y la cita textual (tarea de verificación de normativa, T-007)]]

En Estados Unidos, la regla *Click-to-Cancel* de la Comisión Federal de Comercio (FTC) fue anulada por la Corte de Apelaciones del 8.º Circuito en julio de 2025; la FTC reabrió el proceso reglamentario en marzo de 2026 y, mientras tanto, sanciona estas prácticas bajo la ley ROSCA y la Sección 5 de la FTC Act. [[CITA PENDIENTE: fuente oficial primaria (resolución judicial, aviso de la FTC y texto de las leyes citadas) en lugar de los comentarios de estudios jurídicos que figuran hoy como referencia (T-007)]]

La relación entre esta normativa y el problema es de complementariedad, no de sustitución. La regulación avanza, pero actúa después de que se produce el daño y sus plazos se miden en años; además, aun con botón de baja obligatorio, persisten incumplimientos, como ilustra el caso de Telecentro y DirecTV. [[CITA PENDIENTE: fuente del caso Telecentro y DirecTV, mencionado en los documentos de trabajo previos y todavía no verificado; confirmar que corresponde al contexto de la Disposición 954/2025]] Esto fundamenta el interés por una protección que dependa del usuario y no del proveedor. Cabe precisar lo que no se afirma: SuscripGuard no emite dictámenes legales, señala patrones y no incumplimientos normativos, y no se sostiene que su uso resuelva los casos de incumplimiento ni que reemplace los reclamos ante las autoridades.

Cerrada la presentación de las bases, la sección siguiente examina qué han hecho otros trabajos y productos frente a este problema.

## Estado del arte

Esta sección documenta cómo se buscaron los antecedentes, reseña los trabajos académicos y las soluciones comerciales, los compara con criterios explícitos y formula la brecha que el trabajo propone atender. Las fuentes citadas están pendientes de verificación bibliográfica, por lo que las cifras se reproducen tal como figuran en los documentos de trabajo.

### Protocolo de búsqueda

Para que la comparación sea reproducible se documentó el modo de búsqueda. Las fuentes consultadas fueron ACM Digital Library, IEEE Xplore, arXiv y Google Académico, además de literatura gris de organismos de protección al consumidor (FTC e ICPEN) y de normativa argentina publicada en el Boletín Oficial. Las cadenas principales fueron `"dark patterns" AND (detection OR automated)`, `"dark patterns" AND (subscription OR cancellation)`, `"deceptive design" AND "large language models"` y `"virtual cards" AND "subscription management"`.

Se incluyeron: (a) taxonomías o estudios de prevalencia de *dark patterns* con metodología explícita; (b) sistemas de detección automática con métricas publicadas; y (c) herramientas de gestión de suscripciones o de tarjetas virtuales para usuarios finales en operación. El período cubierto es 2018–2026 para los trabajos académicos y septiembre de 2026 para los productos vigentes.

Queda pendiente la búsqueda de antecedentes nacionales y locales en repositorios universitarios argentinos, por ejemplo SEDICI-UNLP, RDU-UNC y el repositorio de la propia universidad. En la primera búsqueda no se identificaron trabajos académicos argentinos sobre detección automática de *dark patterns*. [[DATO PENDIENTE: resultado de la búsqueda en repositorios universitarios argentinos y fecha en que se realizó]] Como consecuencia, la brecha que se formula al final de la sección vale para la búsqueda documentada aquí.

### Taxonomías y estudios de prevalencia

Esta subsección reseña los cinco trabajos que describen y miden el fenómeno. Las taxonomías de Gray et al. (2018), Mathur et al. (2019) y Nembaware y Sousa (2025) se presentaron en las bases teóricas; aquí se resume su aporte a la tesis y se agregan los estudios de Di Geronimo et al. (2020) y de ICPEN y GPEN (2024).

Gray et al. (2018) aportan la taxonomía de cinco estrategias que sirve de base conceptual al subconjunto de patrones. Mathur et al. (2019) aportan un antecedente de detección semiautomática basada en texto, aunque en páginas de producto. Nembaware y Sousa (2025) son el antecedente más cercano en dominio. Además de la revisión que produjo su taxonomía, analizaron manualmente los flujos de cancelación de seis servicios (The Economist, Bloomberg, Scribd, Adobe, Amazon Prime y Audible) y realizaron un experimento con 34 participantes, con la escala de usabilidad SUS y una escala de confianza. El flujo con más patrones (The Economist) obtuvo un SUS de 36, frente a 78 de Bloomberg; la confianza cayó un 28 % (p < 0,001) y el 12 % de los participantes volvería a contratar The Economist, frente al 79 % en Bloomberg. [[CITA PENDIENTE: Nembaware y Sousa (2025), ECCE 2025; verificar las cifras del experimento, que se reproducen tal como figuran en los documentos de trabajo]] Su análisis es manual y no se vincula con ninguna acción de protección.

Di Geronimo, Braz, Fregnan, Palomba y Bacchelli (2020) inspeccionaron manualmente 240 aplicaciones móviles populares y realizaron un estudio con 589 participantes. Reportan que el 95 % de las aplicaciones contiene al menos un *dark pattern* y que la mayoría de los usuarios no los reconoce por sí misma, aunque mejora cuando se le informa del tema. [[CITA PENDIENTE: Di Geronimo, Braz, Fregnan, Palomba y Bacchelli (2020), *UI Dark Patterns and Where to Find Them*, CHI 2020; verificar cifras]] Este resultado fundamenta que la detección no puede dejarse librada al usuario y que informarle la evidencia de cada detección tiene valor.

ICPEN y GPEN, con la FTC (2024), publicaron un informe de una revisión coordinada por autoridades de 26 países sobre 642 sitios web y aplicaciones por suscripción. Reportan que el 76 % usaba al menos un posible *dark pattern* y el 67 %, varios, y que los más frecuentes fueron *sneaking* e interferencia en la interfaz. [[CITA PENDIENTE: ICPEN (2024), *Dark Patterns in Subscription Services Sweep: Public Report*, julio de 2024; verificar cifras y metodología directamente en el informe primario]] Es el dato de prevalencia específico de suscripciones con fuente primaria que se utilizará en la justificación.

En conjunto, estos trabajos confirman que el problema existe y que afecta a los servicios por suscripción, pero son estudios de caracterización y medición. La subsección siguiente revisa los sistemas que intentan detectar los patrones de manera automática.

### Sistemas de detección automática

Esta subsección compara cinco sistemas de detección automática de *dark patterns* según su entrada, técnica, datos, resultados reportados y limitación relevante para la tesis.

| Sistema (autores, año) | Entrada | Técnica | Datos | Resultados reportados | Limitación relevante |
|------------------------|---------|---------|-------|----------------------|----------------------|
| AidUI (Mansur, Salma, Awofisayo y Moran, 2023; ICSE 2023) | Capturas de pantalla (móvil y web) | Visión por computadora y procesamiento de lenguaje natural | ContextDP: 258 capturas, 301 instancias, 10 tipos | P 0,66; R 0,67; F1 0,65 | Pantallas aisladas; conjunto de datos pequeño |
| UIGuard (Chen, Sun, Feng, Xing, Lu, Xu y Chen, 2023; UIST 2023) | Capturas y jerarquía de la interfaz (móvil) | Visión y reglas derivadas de taxonomías | 1 353 interfaces con patrones y 4 999 benignas, de 1 023 aplicaciones | P 0,82; R 0,77; F1 0,79 | Pantallas aisladas; solo móvil |
| AppRay (Chen et al., 2024; preprint en arXiv) | Jerarquías, capturas, texto y trazas de interacción | Exploración de la aplicación guiada por un modelo de lenguaje (GPT-4), clasificador contrastivo y reglas | 2 185 instancias (149 dinámicas), 18 tipos, 100 aplicaciones | F1 micro 0,76; F1 macro 0,62; 12 % de falsos positivos en interfaces benignas | Analiza secuencias e incluye *roach motel*, pero en aplicaciones móviles genéricas y sin vínculo con una acción |
| AutoBot (Nayak, Zhang, Wani, Khandelwal y Fawaz, 2024/2025; ACM) | Capturas web convertidas en una representación estructurada en texto (*ElementMap*) | Visión (OCR y detector de objetos) y luego modelo de lenguaje (Gemini, Qwen2.5, Flan-T5) | 11 118 sitios para entrenamiento; 1 152 anotados para evaluación | F1 0,93 (clasificación binaria, Gemini) | Solo patrones estáticos; solo inglés |
| DPDGPT (Lin, Nie, Xue, Zhang y Zhang, 2026; *Information and Software Technology*, vol. 190) | Capturas (visual y texto) | Modelo de lenguaje multimodal con razonamiento en cadena y verificación | 1 609 interfaces, 2 015 instancias, 19 tipos | P 0,86; R 0,91; F1 0,88 | Pantallas aisladas; sin foco en suscripciones |

[[CITA PENDIENTE: fuentes originales de AidUI (ICSE 2023), UIGuard (UIST 2023), AppRay (arXiv 2024), AutoBot (2024/2025) y DPDGPT (2026); las cifras de la tabla se toman del documento de estado del arte del proyecto y no fueron contrastadas con los trabajos originales. P: precisión; R: *recall* o exhaustividad]]

Dos observaciones surgen de la tabla. La primera es que la mayoría de los sistemas analiza pantallas aisladas; solo AppRay analiza secuencias de varios pasos, lo que demuestra que el análisis de flujos es viable, aunque su desempeño por tipo de patrón es menor que el global (F1 macro de 0,62 frente a F1 micro de 0,76). AutoBot, por su parte, ilustra la ventaja de una representación estructurada en texto como paso previo a la clasificación.

La segunda observación es de método: las métricas reportadas no son directamente comparables entre sí. Algunos trabajos informan una clasificación binaria (la interfaz tiene o no un patrón, como el F1 de 0,93 de AutoBot) y otros promedios por tipo de patrón (como el F1 macro de AppRay). Además, los conjuntos de datos, la cantidad de tipos y las unidades de análisis difieren. Por eso, las cifras de la tabla describen cada trabajo por separado y no establecen una escala de desempeño común. [[DATO PENDIENTE: criterio con el que se justificarán los umbrales de desempeño de la validación frente a estas cifras; está en revisión por la inconsistencia ya detectada en el documento de estado del arte (tarea T-014, corrección de la comparación de métricas)]]

Ninguno de estos sistemas vincula su resultado con una acción de protección: la detección es un fin en sí mismo, como auditoría o concientización. La siguiente subsección revisa las soluciones comerciales que sí ofrecen un mecanismo de acción.

### Soluciones comerciales

Esta subsección repasa las herramientas disponibles para el usuario final que gestionan suscripciones o controlan el medio de pago, y su limitación frente al problema.

| Solución | Qué hace | Mecanismo | Disponibilidad | Limitación frente al problema |
|----------|----------|-----------|----------------|-------------------------------|
| Rocket Money | Detecta suscripciones y ofrece un servicio que cancela en nombre del usuario | Vinculación con cuentas bancarias; gestión manual de cancelaciones | EE.UU. | Reactivo: actúa después del cobro; exige acceso a datos bancarios |
| Privacy.com | Tarjetas virtuales bloqueadas a un comercio, de un solo uso, con límite de gasto y pausables | Emisor de tarjetas virtuales | Solo ciudadanos o residentes de EE.UU. | Da el mecanismo, pero el usuario configura cada tarjeta sin información sobre el riesgo del servicio |
| Revolut (tarjetas desechables) | Tarjeta virtual cuyos datos se regeneran después de cada uso | Banco digital | Según el país; [[DATO PENDIENTE: disponibilidad en Argentina, a verificar]] | Solo uso único; sin reglas por suscripción |
| Billeteras argentinas (Ualá, Mercado Pago, Naranja X, Brubank, Lemon) | Tarjetas virtuales prepagas | Billetera o banco digital | Argentina | [[DATO PENDIENTE: controles por comercio, de uso único o con vencimiento que ofrece cada aplicación; a relevar]]; no se documentó gestión de suscripciones basada en riesgo |
| Stripe Issuing, Lithic, Pomelo | Interfaces de programación para que empresas emitan tarjetas | Infraestructura de emisión como servicio (Pomelo es argentina) | Empresas; Pomelo opera en Latinoamérica | No son productos para usuarios finales; son posibles proveedores para el adaptador de emisión del prototipo |

[[CITA PENDIENTE: fuentes oficiales de cada producto, con fecha de consulta; los documentos de trabajo solo traen las páginas de Privacy.com y de Rocket Money]]

Las soluciones se dividen en dos grupos. Los gestores de suscripciones, como Rocket Money, detectan las suscripciones y asisten la cancelación, pero actúan después del cobro y exigen acceso a datos bancarios. Los emisores de tarjetas virtuales, como Privacy.com y Revolut, ofrecen el mecanismo preventivo, pero la configuración queda librada al criterio del usuario y no incorporan información sobre el riesgo de cada servicio. Las más completas no están disponibles en Argentina, y de las billeteras locales aún no se relevó qué controles ofrece cada una. Los proveedores de infraestructura, por su parte, no están dirigidos al usuario final, pero constituyen una vía de integración posible.

La comparación entre todos los antecedentes requiere criterios explícitos, que se presentan a continuación.

### Criterios y comparación sistemática

Esta subsección define diez criterios de comparación, los aplica a los antecedentes y a SuscripGuard, y aclara el estatus de lo que se afirma sobre este último.

Los criterios se agrupan según lo que permiten distinguir. Los criterios G describen las capacidades de gestión y control, los criterios D las capacidades de detección y los criterios X las condiciones de contexto.

| Id | Criterio | Por qué importa para el problema |
|----|----------|----------------------------------|
| G1 | Detecta o registra suscripciones | Condición para gestionarlas |
| G2 | Control preventivo sobre el medio de pago, con reglas por suscripción | Evita el cobro en lugar de reclamarlo después |
| G3 | Política configurada a partir de información sobre el servicio | Distingue controlar de controlar con criterio |
| D1 | Foco en flujos de cancelación de suscripciones | Es donde se concentra el daño |
| D2 | Análisis automatizado | Escala más allá de la inspección manual |
| D3 | Analiza secuencias de varios pasos, no pantallas aisladas | El *roach motel* y la obstrucción solo se ven en el flujo completo |
| D4 | Evidencia explicable por cada detección | Confianza y comprensión del usuario |
| D5 | Métricas de desempeño publicadas o previstas | Validez científica |
| X1 | No requiere acceso a cuentas bancarias ni correos del usuario | Privacidad |
| X2 | Aplicable en Argentina o a servicios en español | Contexto de la tesis |

La matriz usa la leyenda siguiente: ● cumple; ◐ cumple parcialmente; ○ no cumple; — no aplica; n/r no reportado.

| Solución | G1 | G2 | G3 | D1 | D2 | D3 | D4 | D5 | X1 | X2 |
|----------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Rocket Money | ● | ○ | ○ | ○ | — | — | — | ○ | ○ | ○ |
| Privacy.com | ◐ | ● | ○ | ○ | — | — | — | ○ | ◐ | ○ |
| Revolut (desechables) | ○ | ◐ | ○ | ○ | — | — | — | ○ | ● | ◐ |
| Billeteras argentinas | ○ | ◐ | ○ | ○ | — | — | — | ○ | ● | ● |
| Nembaware y Sousa | — | — | — | ● | ○ | ● | ● | ◐ | — | ○ |
| AidUI | — | — | — | ○ | ● | ○ | ● | ● | — | n/r |
| UIGuard | — | — | — | ○ | ● | ○ | ● | ● | — | n/r |
| AppRay | — | — | — | ◐ | ● | ● | ◐ | ● | — | n/r |
| AutoBot | — | — | — | ○ | ● | ○ | ● | ● | — | ○ |
| DPDGPT | — | — | — | ○ | ● | ○ | ◐ | ● | — | n/r |
| **SuscripGuard (previsto)** | ◐ | ● | ● | ● | ● | ● | ● | ● (previstas) | ● | ● |

<!-- NOTA PARA TOMÁS: la matriz es la del documento Estado del arte comparativo.md §5 sin cambios. Es una valoración del propio tesista, no verificada en las fuentes; las celdas de las billeteras argentinas y de Revolut dependen de datos que figuran como "a relevar" (ver la tabla de soluciones comerciales). -->

Los valores de la fila de SuscripGuard corresponden a lo previsto en el diseño, no a lo verificado: el prototipo no existe y no hay resultados. Cuatro notas precisan su alcance.

- **G1 (parcial):** el registro de suscripciones es manual; la detección por correo electrónico es complementaria y solo se incorporará si el cronograma lo permite.
- **D2:** el análisis es automático, pero la captura de los flujos es semiautomática (scripts de navegación y anotación manual).
- **D3:** el análisis de secuencias opera sobre flujos capturados; no incluye exploración autónoma de aplicaciones como AppRay.
- **D5:** las métricas están previstas en el plan de validación (Capítulo 3); todavía no hay resultados.

Asimismo, la valoración de SuscripGuard en D4 y en X1 depende de decisiones de diseño que se desarrollan en el Capítulo 4: la salida del módulo de detección incluye, por cada patrón, el paso, la evidencia (elemento o texto) y la confianza asociada, y el análisis de los correos de confirmación se realiza únicamente con el modelo local. [[DECISIÓN: el criterio X1 se formuló como "no requiere acceso a cuentas bancarias ni correos del usuario", pero desde la decisión del 02/10/2026 el sistema analiza el correo de confirmación del alta, que contiene datos personales. Opciones: A) reformular X1 como "no requiere acceso a cuentas bancarias ni al buzón de correo del usuario; los datos personales que procesa no salen de su equipo" y mantener ● (compatible con la importación manual de un solo correo); B) mantener la redacción actual de X1 y bajar SuscripGuard a ◐. Recomendación: A, siempre que se elija la importación manual del correo y no la lectura del buzón]]

De la matriz se desprende un patrón: ningún antecedente cumple a la vez los criterios de control preventivo (G2), política basada en información del servicio (G3), foco en flujos de cancelación (D1) y análisis de secuencias (D3). Ese patrón da origen a la brecha que se formula a continuación.

### Brecha identificada

Esta subsección formula la brecha, delimita el alcance de la afirmación y vincula la formulación con la pregunta de investigación.

La revisión muestra tres líneas de trabajo que avanzan por separado. La primera es la detección automática de *dark patterns*, que madura en pantallas aisladas y, más recientemente, en secuencias (AppRay). Sin embargo, según la búsqueda realizada: (i) ningún trabajo toma como objeto de análisis los flujos de cancelación de suscripciones, con su asimetría entre alta y baja y la derivación entre canales; (ii) la detección es un fin en sí mismo, y ningún trabajo usa el resultado para tomar una acción de protección; y (iii) los datos y las herramientas se centran en el inglés, y no se identificaron corpus de flujos de cancelación en español ni de servicios usados en Argentina. La segunda línea son los estudios del dominio de cancelación (Nembaware y Sousa; ICPEN y GPEN), que confirman el problema y aportan taxonomías, pero son manuales. La tercera son las herramientas de control de pagos (Privacy.com, Revolut, billeteras), que ofrecen el mecanismo preventivo pero sin información sobre el riesgo del servicio.

A partir de ello se formula la brecha: no se identificaron trabajos ni productos que detecten automáticamente *dark patterns* en flujos de cancelación de suscripciones y usen ese resultado para configurar un control preventivo sobre el medio de pago; tampoco se identificaron para servicios en español ni para el contexto argentino. SuscripGuard se propone integrar las tres líneas. Esa integración, y no cada componente por separado, constituye la contribución central, y es lo que la pregunta de investigación pone a prueba: si es posible prevenir cobros recurrentes no deseados mediante tarjetas virtuales cuyas políticas se configuran a partir de la detección de *dark patterns* en los flujos de cancelación.

La afirmación vale para la búsqueda documentada en el protocolo. Es una afirmación de ausencia, y como tal depende de la exhaustividad de la búsqueda; por eso se la ampliará con la revisión de repositorios nacionales antes de la versión final. [[DATO PENDIENTE: resultado de la búsqueda de antecedentes nacionales y locales; si se identifican trabajos, la formulación de la brecha deberá ajustarse]] Además, el alcance de la afirmación no incluye la eficacia del enfoque: que no existan antecedentes no implica que el mecanismo propuesto funcione, lo cual se evaluará con la validación descripta en el Capítulo 3.

Con la brecha delimitada, resta fijar el vocabulario con el que el resto de la memoria se refiere a sus elementos.

## Definición de conceptos clave

Esta sección fija el sentido con que se emplean en la memoria los términos principales. Las definiciones se derivan del diseño del proyecto; las que requieren respaldo bibliográfico se marcan como pendientes.

| Término | Definición |
|---------|------------|
| *Dark pattern* (patrón oscuro) | Elemento de diseño de interfaz que induce al usuario a tomar decisiones que lo perjudican o que no tomaría en otras condiciones. [[CITA PENDIENTE: definición de una fuente primaria (marco teórico, T-024)]] |
| Flujo de cancelación | Secuencia de pasos, elementos y canales que el usuario debe recorrer para dar de baja una suscripción. Incluye el canal final requerido (web, chat, teléfono o correo). |
| Representación estructurada del flujo | Descripción en formato JSON de un flujo de cancelación a dos niveles: el flujo (servicio, fecha de captura, cantidad de pasos de alta y de baja, canal final, necesidad de inicio de sesión) y cada paso (canal, textos visibles, elementos interactivos con su rol, atributos de prominencia y tipo de acción ofrecida). Corresponde al aporte A1. |
| Corpus etiquetado | Conjunto de 15 a 20 flujos de cancelación de servicios por suscripción, junto con los correos de confirmación del alta de esos servicios, capturado en una fecha determinada y etiquetado por patrón según una guía de etiquetado. Su unidad de análisis es el par (paso del flujo, patrón). Corresponde al aporte A3. |
| Índice de riesgo de cancelación | Nivel (bajo, medio o alto) que resume el riesgo de un servicio, obtenido al agregar los patrones detectados mediante una fórmula documentada y ponderada por patrón. Es la entrada del motor de reglas. |
| Política de tarjeta | Conjunto de reglas de uso aplicadas a la tarjeta virtual de una suscripción: vencimiento, tope de monto y cantidad de cobros. Se propone a partir del índice de riesgo y el usuario la confirma o ajusta. |
| Tarjeta virtual | Tarjeta de pago emitida de forma digital, sin soporte físico, que puede dedicarse a una sola suscripción y acotarse en su uso. [[CITA PENDIENTE: definición de una fuente técnica o institucional (T-024)]] |
| Emulador de emisión | Componente que simula el ciclo de vida de una tarjeta virtual (emisión, autorización o rechazo de cobros, bloqueo y destrucción) detrás de una interfaz de adaptador, de modo que un proveedor real pueda incorporarse sin modificar el núcleo. Corresponde al componente N3. |
| Motor de reglas determinista | Componente que traduce el índice de riesgo y los datos de la suscripción en una política de tarjeta y la ejecuta sin intervención de modelos probabilísticos, de modo que el mismo conjunto de entradas produce siempre el mismo resultado. Corresponde al componente N2. |
| Clasificador basado en un modelo de lenguaje local (LLM local) | Implementación de la interfaz de clasificación que emplea un modelo de lenguaje ejecutado localmente (con Ollama), con la salida validada contra un esquema. Se emplea para los patrones semánticos y para analizar el correo de confirmación del alta. |
| Línea base heurística | Implementación alternativa de la misma interfaz de clasificación, basada en reglas explícitas, que sirve de referencia para comparar el desempeño del clasificador basado en un LLM local. |
| Permanencia mínima | Período durante el cual el usuario contrae la obligación contractual de mantener el servicio, de modo que bloquear la tarjeta no extingue la obligación y el proveedor puede generar deuda. Los servicios con permanencia mínima quedan fuera del alcance del control; el sistema solo emite una alerta. [[CITA PENDIENTE: definición jurídica de la permanencia en la normativa aplicable (T-029)]] |
| Prueba gratuita | Período inicial sin cargo tras el cual el servicio pasa a cobrarse al precio regular si el usuario no cancela. Se incluye en el alcance del problema. [[CITA PENDIENTE: definición de una fuente (T-024)]] |
| Alerta de permanencia o costos ocultos | Aviso al usuario emitido cuando el análisis del correo de confirmación del alta detecta permanencia mínima o costos ocultos (permanencia, penalidad por baja anticipada, renovación automática, precio tras la prueba). Incluye el fragmento del correo que la respalda. |
| Falso positivo / falso negativo | En la detección, un patrón señalado donde no existe (falso positivo) y un patrón existente que no se detecta (falso negativo). La tasa de falsos positivos se reportará por patrón. [[CITA PENDIENTE: definición estándar de las métricas de clasificación (precisión, *recall*, F1) (T-024)]] |
| Kappa de Cohen | Coeficiente de acuerdo entre dos anotadores que se calculará por patrón para evaluar la confiabilidad del etiquetado del corpus. Se fijó como criterio un valor mayor o igual que 0,61 (acuerdo sustancial); los patrones por debajo de ese valor se redefinen o se excluyen del análisis. [[CITA PENDIENTE: definición del coeficiente y de la escala de interpretación del acuerdo (T-024)]] |

El Capítulo 3 retoma estos términos para describir el enfoque metodológico, el corpus y el plan de validación, y el Capítulo 4 detalla cómo se materializan en el diseño del prototipo.

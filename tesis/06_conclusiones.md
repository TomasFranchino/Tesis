<!-- NOTA PARA TOMÁS: las conclusiones las escribe el tesista con su voz cuando existan los resultados. Este borrador deja solo la estructura, lo que quedó establecido en el diseño (sin presentarlo como resultado empírico) y las limitaciones tomadas del alcance y del plan de validación. Los trabajos futuros se limitan a lo que los documentos de trabajo dejan explícitamente para después. -->

# Conclusiones y recomendaciones

Este capítulo cierra la memoria. Presenta las conclusiones organizadas según las preguntas de investigación, las limitaciones del trabajo y las líneas que quedan abiertas para trabajos posteriores. A la fecha de este borrador la validación no se ejecutó, por lo que las conclusiones empíricas permanecen pendientes y solo se consignan las que corresponden a las decisiones de diseño.

## Conclusiones

Esta sección responde, en una conclusión por subpregunta y una sobre la pregunta principal, a lo planteado en la Introducción. Cada conclusión se redactará a partir de los resultados del Capítulo 5 y se limitará a lo que los datos respalden dentro del alcance definido.

**Sobre la primera subpregunta (SP1).** La precisión con que puede detectarse automáticamente un subconjunto de *dark patterns* (patrones oscuros) a partir de una representación estructurada de los flujos de cancelación se concluirá a partir del desempeño por patrón, el acuerdo entre anotadores y la exactitud del nivel de riesgo. [[RESULTADO PENDIENTE: conclusión sobre SP1, bloque de validación V1]]

**Sobre la segunda subpregunta (SP2).** La diferencia de desempeño entre el clasificador basado en un modelo de lenguaje local (LLM local) y la línea base heurística, en precisión, falsos positivos y latencia, se concluirá a partir de la comparación pareada de ambos sobre el mismo conjunto de prueba. Cualquiera sea el signo de la diferencia, constituye un hallazgo. [[RESULTADO PENDIENTE: conclusión sobre SP2, bloque de validación V1]]

**Sobre la tercera subpregunta (SP3).** El cumplimiento verificable de las políticas de vencimiento, tope de monto y cantidad de cobros por parte del motor de reglas se concluirá a partir de la suite de escenarios, la puntualidad y el rendimiento de autorización. [[RESULTADO PENDIENTE: conclusión sobre SP3, bloques de validación V2 y V3]]

**Sobre la cuarta subpregunta (SP4).** La usabilidad de la solución para un usuario no experto se concluirá a partir del puntaje SUS, la finalización de tareas y la comprensión de la política, con la salvedad de que se trata de un estudio exploratorio. [[RESULTADO PENDIENTE: conclusión sobre SP4, bloque de validación V5]]

**Sobre la pregunta principal.** Si es posible prevenir cobros recurrentes no deseados mediante tarjetas virtuales cuyas políticas se configuran a partir de la detección de *dark patterns* se concluirá integrando las respuestas anteriores y el escenario integral de extremo a extremo, dentro de un emulador de tarjetas y un corpus capturado en una fecha determinada. [[RESULTADO PENDIENTE: conclusión sobre la pregunta principal, bloques de validación V1 a V6]]

### Lo establecido en la etapa de diseño

Independientemente de los resultados, la etapa de diseño dejó establecidas tres cuestiones que condicionan la lectura de todo el trabajo. La primera es el alcance acotado: el mecanismo actúa sobre suscripciones digitales pagadas con tarjeta y sin permanencia mínima, porque rechazar un cobro no rescinde el contrato; en los servicios con permanencia, bloquear la tarjeta no extingue la obligación y el proveedor puede generar deuda, de modo que allí el sistema se limita a alertar. La segunda es que la arquitectura se derivó de los requisitos y no al revés: la ausencia de requisitos de escalado independiente o alta disponibilidad (RNF-14) fundamentó la elección de un monolito modular en lugar de microservicios (ADR-01, el primero de los registros de decisión de arquitectura). La tercera es un plan de validación con criterios de aceptación explícitos, propuestos antes de observar resultados, que distingue lo que el prototipo debe cumplir de lo que se reporta cualquiera sea su valor. Estas cuestiones son decisiones de diseño y no resultados empíricos.

## Limitaciones

Esta sección reúne las limitaciones del alcance y de la validez que el lector debe tener presentes al interpretar los resultados.

Respecto del alcance, el sistema no extingue obligaciones contractuales ni gestiona deuda, intereses o reclamos, y no previene la deuda en servicios con permanencia mínima; en ellos su aporte se reduce a la alerta de permanencia o costos ocultos, que depende de lo que informe el correo de confirmación del alta. Si una condición no figura en el correo, no se detecta, y su ausencia se registra como tal. El módulo de detección no emite dictámenes legales, ya que señala patrones y no incumplimientos normativos; no analiza imágenes ni sitios en vivo, y los flujos que terminan en canales no digitales, como el teléfono, se registran como tales sin analizar su contenido. Las tarjetas son simuladas: el emulador no reproduce todas las condiciones de una red de pagos real, y no se emiten tarjetas reales ni se integra un proveedor productivo.

Respecto de la validez, el corpus es pequeño (15 a 20 servicios) y se captura en una fecha determinada, por lo que los resultados valen para esa fecha y no se generalizan a todos los servicios ni a cambios posteriores de sus flujos. El tesista diseña el sistema y también etiqueta el corpus, lo que se mitiga con un segundo anotador independiente, aunque queda un riesgo de sesgo. Las heurísticas y las preguntas al clasificador se diseñan mirando datos, lo que se mitiga reservando un conjunto de prueba. La salida del LLM local puede variar entre ejecuciones, versiones del modelo, cuantizaciones y equipos, y su latencia depende del hardware, por lo que se registran las condiciones de ejecución. En la alerta de permanencia o costos ocultos, el corpus puede contener pocos casos positivos. Por último, la muestra de usabilidad es reducida y no representativa, por lo que se interpreta como exploratoria. [[RESULTADO PENDIENTE: limitaciones adicionales que surjan de la ejecución de la validación]]

## Recomendaciones y trabajos futuros

Esta sección enumera las líneas que los documentos de diseño dejan explícitamente para una etapa posterior y las que surjan de la validación.

- **Extensión de navegador.** Quedó fuera del alcance porque amplía el trabajo sin aportar a la validación del núcleo.
- **Integración con un proveedor real en *sandbox* (entorno de pruebas).** El emulador se diseñó detrás de una interfaz de adaptador, de modo que un proveedor real pueda incorporarse sin modificar el núcleo; una demostración opcional con un entorno de pruebas del proveedor permitiría contrastar el emulador con una red real.
- **Análisis en vivo de sitios.** El análisis se realizó sobre un corpus capturado y controlado; extenderlo a sitios en vivo requeriría resolver la variación de los flujos en el tiempo.
- **Detección de suscripciones a partir de correos electrónicos.** Es un componente complementario que, de implementarse, debe respetar el enfoque de privacidad (modelo local o metadatos). `[[DATO PENDIENTE: si este componente se incorporó al prototipo o queda como trabajo futuro]]`
- **Escalado o despliegue independiente de componentes.** El monolito modular admite extraer un servicio si apareciera un requisito de escalado o de disponibilidad, que hoy no existe (ADR-01).
- **Hallazgos de la validación.** [[RESULTADO PENDIENTE: líneas abiertas que surjan de los resultados del Capítulo 5]]

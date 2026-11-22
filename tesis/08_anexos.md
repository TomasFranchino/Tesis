<!-- NOTA PARA TOMÁS: los anexos B, C y D están como estructura con marcadores; se completan cuando existan la guía de etiquetado, el registro de uso de IA consolidado y el prototipo. El Anexo A es el contenido definitivo del Plan de validación (escenarios mínimos E01 a E12). -->

# Anexos {.unnumbered}

## Anexo A. Escenarios de prueba del motor de reglas {.unnumbered}

La siguiente tabla reúne los doce escenarios mínimos con los que se valida el motor de reglas (bloque V2 del Capítulo 3) y el resultado esperado en cada caso; los resultados obtenidos se reportan en el Capítulo 5.

| Id | Escenario | Resultado esperado |
|----|-----------|--------------------|
| E01 | Cobro dentro de la política vigente | Autorizado |
| E02 | Cobro posterior a la fecha de vencimiento | Rechazado, con motivo de vencimiento |
| E03 | Cobro al finalizar el período de prueba (vencimiento relativo) | Rechazado |
| E04 | Cobro por monto superior al tope | Rechazado, con motivo de tope |
| E05 | Cobro que excede la cantidad máxima de cobros | Rechazado, con motivo de cantidad |
| E06 | Cobro sobre tarjeta congelada o bloqueada manualmente | Rechazado |
| E07 | Cobro sobre tarjeta destruida | Rechazado |
| E08 | Reinicio del sistema antes de un vencimiento programado | El vencimiento se aplica igual (RNF-07) |
| E09 | Modificación de la política por el usuario antes de un cobro | Se aplica la política nueva |
| E10 | Dos cobros simultáneos que, juntos, superan el límite | Se autoriza como máximo uno |
| E11 | Servicio con riesgo alto, medio o bajo | Se propone la política definida para cada nivel |
| E12 | Alerta previa a la renovación | Se emite con la anticipación configurada |

: Escenarios de prueba del motor de reglas y resultado esperado.

## Anexo B. Guía de etiquetado {.unnumbered}

Este anexo contendrá la guía con la que se etiqueta el corpus de flujos de cancelación y de correos de confirmación del alta, y que recibe también el segundo anotador. Incluirá la definición operativa de cada uno de los siete patrones, elaborada a partir de las taxonomías del estado del arte, con ejemplos positivos y negativos; las condiciones de contratación que se etiquetan en los correos de confirmación (permanencia mínima, penalidad por baja anticipada, renovación automática y precio tras la prueba), con la distinción entre "no informado" y "ausente"; y el criterio para asignar el nivel de riesgo (bajo, medio o alto) a cada servicio. `[[DATO PENDIENTE: guía de etiquetado (tarea de redacción de la guía, T-027)]]`

## Anexo C. Declaración de uso de herramientas de inteligencia artificial {.unnumbered}

Esta declaración se elaborará a partir del registro de uso de inteligencia artificial que el proyecto mantiene durante todo su desarrollo, en el que se anota cada intervención sobre el texto de la memoria. `[[DATO PENDIENTE: declaración de uso de IA, se redacta en la etapa final]]`

## Anexo D. Manual de instalación y uso del prototipo {.unnumbered}

Este anexo describirá cómo instalar y usar el prototipo. El despliegue previsto se levanta con un único comando (RNF-12, requisito de portabilidad). [[RESULTADO PENDIENTE: manual de instalación y uso, depende del prototipo]]

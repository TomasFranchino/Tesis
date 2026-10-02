# Auditoría B1/B2 (T-010, T-011, T-019) — 02/10/2026

Solo lectura; no se corrigió nada. Excluidos `archivo/` y `.git/`.

## 1. Menciones a Jev / TypeSafe / "decisión estructurada" (grep -rni)
(a) Documentos de contenido (insumos/, tesis/, guias/, CLAUDE.md, LEEME, .claude/, scripts/, bibliografia/): **0 menciones**. OK.
(b) Historia/decisión en gestion/ (esperables):
- gestion/TABLERO.md:25 (T-011), :33 (T-019)
- gestion/BITACORA.md:26 (registro de B2)
- gestion/DIAGNOSTICO.md:35 (B2 original)
- gestion/GUIA.md:107, :118, :141 (cronograma/compuerta F1 citan "Jev" / T-011). Informativo: GUIA.md es guía de gestión, no contenido.
- Nota: DIAGNOSTICO.md:49 coincide por "decisión estructurada"/"jev" parcial (falso positivo de patrón, tema I5).

## 2. Residuos de "servicio externo", SDK, acceso anticipado, Choice/Noul en insumos/
- IMPORTANTE — insumos/Arquitectura.md:233: "calcularon con el K2 anterior (SDK de un servicio externo)". Es explicación de por qué la tabla 7.6 está obsoleta; legítimo mientras exista el `[[RESULTADO PENDIENTE]]` (T-016), pero debe desaparecer al recalcular.
- MENOR — insumos/Arquitectura.md:173 (C#): "sin SDK ni integración documentada con el clasificador" dentro de un `[[DECISIÓN]]` que lo reconoce como motivo caduco; pendiente de resolver.
- insumos/Requisitos.md:16: "Ya no es un servicio externo de terceros" (glosario; alusión a lo anterior, redundante en un documento vigente). MENOR.
- "Acceso anticipado", "SDK oficial", "Choice", "Noul": 0 en insumos/.

## 3. Coherencia SP2 / A5 / RF-04 / ADR-02 / Plan §2.4 / Objetivos
Coherentes en LLM local (Ollama) vs. línea base heurística: Contribución :26, :44, :106-107, :156; Requisitos RF-04 :30, RF-05 :31; Arquitectura ADR-02 :83-91; Plan §2.4 :57-63. ADR-07 (K2) y tabla 7.5 recalculados; aritmética verificada (S1 4,00; S2 4,05; S3 4,40; S4 4,35; inversión con K2=5 de S4: 4,50).
- IMPORTANTE — insumos/Objetivos.md:60-79 (versión vigente): OE3 habla de "módulo independiente del modelo de clasificación" (compatible), pero ni OE3 ni OE6 mencionan la comparación LLM local vs. heurística; la trazabilidad la cubre solo por A5 en :74/:77. No hay contradicción, solo cobertura implícita.
- IMPORTANTE — insumos/Arquitectura.md:233 y :235: tablas 7.6 y conclusión de robustez sin recalcular (T-016); T-019 solo recalculó 7.5. La decisión S3 (7.7) se apoya en S3 vs S4 por 0,05 puntos con K2 de S4 sin cita.
- IMPORTANTE (preexistente de fondo, ligado a SP2): los puntajes K2 dependen de 6+ `[[CITA PENDIENTE]]` sobre Ollama (Arquitectura :171, :173, :217, :255, :328).
- MENOR — insumos/Objetivos.md:35 (historial, antes de la sección vigente): "Llama 3.1 8B o Phi-3 vía Ollama" para clasificar emails; es el proyecto antiguo, no contradice pero genera confusión con el modelo pendiente de decisión.
- Modelo/tamaño y hardware: `[[DECISIÓN]]`/`[[DATO PENDIENTE]]` consistentes en Contribución :106/:145, Plan :62/:178, Requisitos :125, Arquitectura :324-325. OK.

## 4. Coherencia del alcance B1
Consistente: Contribución §1 (:16), §4.4 (:87-91), §5.2 paso 5 (:109), §5.4 (:127), §5.5 (:138), §6 (:147); Definición de problema (:4-14 separa daños prevenidos / no prevenidos); Requisitos RF-28 (:37).
- IMPORTANTE — RF-28 :37 y Requisitos :124: la alerta opera sobre el "flujo de alta", pero Contribución §5.1 (entrada) y el corpus A3 (Contribución :42; Objetivos OE2) se definen como flujos de cancelación. Hueco de diseño: ningún OE ni validación (Plan §3–§4) cubre la alerta previa (RF-28 sin fila de validación; el Plan solo lo declara pendiente en :180). Promesa sin respaldo en la validación, reconocida como pendiente.
- IMPORTANTE — Objetivos.md (vigente) OE1–OE3 no mencionan alerta previa ni el alcance acotado (permanencia/prueba gratuita); el objetivo general :59 sigue en "cobros recurrentes no deseados" sin acotar. Contribución §8 no registra B1 como cambio a Objetivos.
- BLOQUEANTE (tribunal): RF-28 y patrón 6 (Contribución :118) exigen detectar "permanencia/costos ocultos" en alta, pero §5.3 sigue "a confirmar" y Requisitos :124 admite que el corpus no la contempla; sin esto, B1(c) no es implementable ni evaluable.
- MENOR — Definicion de problema.md:8-10, :17: adjetivos valorativos sin respaldo ("abusivo", "usureros", "prácticas abusivas") contra regla de estilo; con CITA PENDIENTE en parte.
- MENOR — Definicion de problema.md:27 `[[DECISIÓN]]` sobre emocional sin resolver; :19 ídem costo de oportunidad.
- MENOR — Requisitos.md:37: prioridad de RF-28 `[[DECISIÓN]]` abierta (recomendación M).

## 5. check_ids.py (salida en gestion/revisiones/ids.md)
- SP1–SP4 usados y no definidos: preexistente (T-003).
- A1–A5 definidos en dos archivos (Contribución vs. Estado del arte): preexistente (T-002).
- Sin otros hallazgos; sin RF/OE/ADR huérfanos reportados. RF-28 no aparece como problema de ids.

## Resumen
BLOQUEANTE 1 · IMPORTANTE 6 · MENOR 6. Cero residuos de Jev/TypeSafe en contenido.

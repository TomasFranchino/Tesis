Propuestas de Temas para Tesis de Ingeniería Informática
A continuación, se presentan tres posibles temas para el trabajo final (tesis) de Ingeniería Informática. Cada propuesta busca aplicar tecnologías de vanguardia para la resolución de problemas en distintos ámbitos.



5. Tarjetas virtuales y "Dark Patterns" de suscripciones
Precedentes en el mercado: Sí, y son empresas multimillonarias.

Tarjetas Virtuales: Privacy.com es exactamente la solución que describí. Te permite generar tarjetas con límites de gasto exactos o de un solo uso para que nadie te cobre de más. Neo-bancos como Revolut también ofrecen tarjetas desechables gratuitas.

Gestores de suscripciones: Aplicaciones como Rocket Money (antes Truebill) se conectan a tu cuenta bancaria, detectan suscripciones recurrentes y ofrecen cancelarlas por ti.

La oportunidad: Muchas de estas herramientas (como Privacy.com) operan casi exclusivamente en Estados Unidos o regiones muy específicas. En Latinoamérica y España, el mercado para tarjetas virtuales desechables y de fácil uso sigue teniendo muchísimo espacio para crecer.

Como ves, la clave no siempre es inventar la rueda, sino hacerla rodar mejor, más rápido o en un terreno donde todavía no ha llegado.

¿Te gustaría que analicemos las debilidades de alguna de estas herramientas existentes para ver qué "ventaja injusta" o mejora podrías desarrollar en un proyecto propio?

Es un proyecto espectacular para una tesis de grado en ingeniería informática porque toca temas críticos: seguridad, integración con APIs externas, bases de datos transaccionales, y resuelve un problema real.

Ahora, vamos con una dosis de realidad necesaria y muy directa: Como desarrollador solitario, tú no puedes simplemente escribir un algoritmo que genere números de tarjetas Visa o Mastercard válidas de la nada. El sistema financiero mundial está (afortunadamente) muy blindado. Para emitir tarjetas reales necesitas alianzas con bancos, cumplimiento de normativas de seguridad extremas (PCI-DSS) y mucho capital.

Pero no te desanimes, aquí está el secreto de cómo lo hacen las startups y cómo puedes hacerlo tú para tu tesis.

El secreto de la industria: BaaS (Banking-as-a-Service)
Las empresas como Privacy.com no son bancos. Utilizan proveedores de "Infraestructura bancaria como servicio" (BaaS) o APIs de emisión de tarjetas (Card Issuing APIs). Estas empresas intermediarias ya tienen las licencias bancarias y te exponen una API REST común y corriente para que tú, con código, crees tarjetas.

Para un desarrollador solitario, el flujo real es este:

Tu sistema hace una petición POST a la API del proveedor: "Crea una tarjeta virtual para el usuario Juan con límite de $10 USD y que expire mañana".

El proveedor se comunica con la red (Visa/Mastercard), crea la tarjeta y te devuelve el número (PAN), CVV y fecha de caducidad.

Tú muestras esa tarjeta en tu aplicación.

Proveedores reales que puedes usar:
Stripe Issuing: Es el más famoso a nivel mundial. Tienen una documentación increíble para desarrolladores.

Lithic: Curiosamente, esta es la empresa matriz de Privacy.com. Abrieron su API al público para que cualquiera construya lo que ellos construyeron.

Pomelo o Dock: Si estás apuntando al mercado latinoamericano, estas son las infraestructuras que usan las fintechs locales.

¿Cómo enfocar esto para tu Tesis de Grado?
Para una tesis universitaria, no necesitas mover dinero real. Ningún tribunal evaluador te va a exigir que gastes miles de dólares en licencias reales o que pases certificaciones legales. El valor de tu tesis estará en la arquitectura del software.

Así es como deberías encarar el proyecto:

1. Usa el entorno "Sandbox" (Modo de prueba):
Regístrate en Stripe Issuing o Lithic y usa sus entornos de prueba. Podrás programar todo el flujo, generar tarjetas virtuales (que solo funcionan en entornos de prueba de pasarelas de pago falsas) y simular que el usuario hace compras y cancela suscripciones.

2. Enfócate en el desafío de Ingeniería Informática:
Tu tesis no será sobre finanzas, será sobre cómo construiste un sistema robusto. Puedes destacar en tu documento:

Arquitectura de Microservicios: Un servicio maneja los usuarios, otro se comunica con la API de emisión de tarjetas, y otro maneja las notificaciones.

Seguridad (Tokenización): Demostrar cómo tu base de datos nunca guarda el número de tarjeta completo (para simular el cumplimiento de la norma PCI-DSS), sino que usas tokens o bóvedas de datos seguras.

Procesos en segundo plano (Cron Jobs / Workers): El algoritmo central de tu tesis: un sistema asíncrono que revisa constantemente las tarjetas en la base de datos y hace una llamada a la API para destruirlas o congelarlas automáticamente cuando pasa la fecha límite o se supera el límite de cobro.

Manejo de Webhooks: Tu sistema tendrá que escuchar eventos (webhooks) del proveedor. Por ejemplo, si Netflix intenta cobrar y la tarjeta tiene fondos insuficientes, tu proveedor te mandará un evento a tu servidor y tu app deberá notificar al usuario.

El veredicto
Es una idea brillante para una tesis porque demuestra que sabes conectar el mundo de la programación con soluciones del mundo real a nivel empresarial (APIs financieras, seguridad, arquitecturas asíncronas).

¿Te gustaría que esbozamos cuáles serían los "Objetivos Generales y Específicos" para presentarlos en el anteproyecto de tu tesis, o prefieres que armemos un diagrama conceptual de la base de datos que necesitarías?


Crear un compilador para representar un video con simbolos y que así pese menos tamaño la reproduccion de videos.

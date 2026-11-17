# Entrega de webhooks y reintentos

Cuando ocurre un evento, enviamos una petición `POST` a cada endpoint registrado para
ese tipo de evento. La entrega es asíncrona: la respuesta a tu llamada a la API no
espera a tu endpoint.

## Criterio de éxito

Se considera que un endpoint ha aceptado un evento cuando devuelve cualquier código de
estado `2xx` en un plazo de 10 segundos. Cualquier otro desenlace —un estado distinto de
`2xx`, un tiempo de espera agotado o un error de conexión— cuenta como intento fallido.

## Calendario de reintentos

Las entregas fallidas se reintentan hasta 8 veces en 24 horas, con espera exponencial y
dispersión aleatoria:

| Intento | Espera desde el intento anterior |
|---|---|
| 1 | inmediato |
| 2 | 30 segundos |
| 3 | 2 minutos |
| 4 | 10 minutos |
| 5 | 1 hora |
| 6 | 3 horas |
| 7 | 6 horas |
| 8 | 12 horas |

Tras el octavo intento fallido, el evento se marca como `exhausted` y no se realizan más
intentos.

## Idempotencia

Cada evento lleva un `event_id` único que se mantiene igual entre reintentos. Tu endpoint
debe tratar las entregas repetidas del mismo `event_id` como un mismo evento.
Recomendamos conservar los identificadores ya procesados durante al menos 7 días.

## Orden

No garantizamos el orden. Dos eventos creados con milisegundos de diferencia pueden
llegar en cualquier orden. Si tu integración depende del orden, compara el campo
`created_at` en lugar de fiarte del momento de llegada.

## Desactivación de un endpoint

Un endpoint que falla de forma continua durante 72 horas se desactiva automáticamente.
Enviamos un correo al titular de la cuenta y conservamos los eventos fallidos durante 30
días. Reactivar el endpoint no los reenvía; puedes reenviar eventos manualmente desde el
panel.

## Pruebas

Usa el botón «Enviar evento de prueba» del panel para entregar un evento sintético
`ping`. Los eventos de prueba siguen el mismo calendario de reintentos, pero quedan
excluidos de la regla de desactivación automática.

[← Volver a Oficio](/)

# QA de localización — lista de verificación

Antes de entregar una traducción, se comprueba todo esto. Sin excepciones.

## Integridad

- [ ] Todos los números coinciden con el original: 10 s, 8 veces, 24 h, 72 h, 30 días, 7 días.
- [ ] Todas las tablas tienen las mismas filas y el mismo orden.
- [ ] Los identificadores de código no se traducen: `POST`, `2xx`, `event_id`, `created_at`, `exhausted`, `ping`.
- [ ] Los valores literales del API se mantienen aunque parezcan inglés (`exhausted`).
- [ ] No falta ni sobra ninguna sección.

## Terminología

- [ ] Cada término sigue el glosario (`glossary.csv`).
- [ ] El mismo término se traduce igual en todo el documento.
- [ ] "endpoint" se mantiene; no se alterna con "punto de conexión".

## Lenguaje

- [ ] Tuteo consistente; no se mezcla con "usted".
- [ ] Sin calcos literales: "la respuesta no espera a tu endpoint", no "no espera por".
- [ ] Sin anglicismos innecesarios donde existe equivalente natural.
- [ ] Comillas angulares «» en el texto en español.
- [ ] Los números de sección y los enlaces internos siguen funcionando.

## Voz

- [ ] Se lee como si estuviera escrito en español, no como una traducción.
- [ ] No se añade ni se quita información.
- [ ] No se "mejora" el original: si el original es ambiguo, se pregunta.

## Entrega

- [ ] Archivo en el mismo formato que el original (`.md`, `.html`, `.json`).
- [ ] Sin marcas de revisión, comentarios ni `TODO` en el archivo final.
- [ ] Glosario actualizado si apareció un término nuevo.

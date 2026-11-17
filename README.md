# Oficio — small technical work

Sitio público y demos ejecutables de **Oficio**, un taller técnico pequeño:
limpieza de datos, scrapers y localización técnica.

- **Sitio:** https://oficioivo-hub.github.io/oficio-site/
- **Contacto:** oficio.ivo@gmail.com

## Demos

| Carpeta | Qué demuestra | Cómo se comprueba |
|---|---|---|
| [`demos/01-csv-clean`](demos/01-csv-clean) | CSV sucio → CSV limpio, con descartes trazables | 13 pruebas unitarias + ejecución de punta a punta |
| [`demos/02-scraper`](demos/02-scraper) | Extractor de 60 líneas, sin dependencias, con rate limit | `python3 scrape_books.py --pages 2` |
| [`demos/03-localization`](demos/03-localization) | Traducción técnica EN→ES con glosario y QA | Comparación término a término contra el glosario |

## Por qué esto es público

Porque una promesa no es una prueba. Cualquiera puede leer el código, ejecutar las
pruebas y comprobar que funciona antes de contratar nada.

Todo el código es de biblioteca estándar: sin dependencias, sin `pip install`, sin
sorpresas.

## Estado

Las pruebas corren en cada push (ver la pestaña **Actions**). Si el badge está en verde,
el código funciona en una máquina limpia, no solo en la mía.

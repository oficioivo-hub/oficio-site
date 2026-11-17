# 02 — Extractor de catálogo (scraper)

Extractor de 60 líneas, sin dependencias, sobre `books.toscrape.com` — un sitio público
creado específicamente para practicar scraping. No es un objetivo real: es la prueba
de que sé escribir un extractor limpio y educado.

```bash
python3 scrape_books.py --pages 2 --out books.csv
```

```
  pagina 1: 20 libros
  pagina 2: 20 libros

40 libros -> books.csv
```

## Decisiones que importan

- **`HTMLParser` de la biblioteca estándar, no regex.** El HTML cambia; las regex se
  rompen en silencio. Un parser falla de forma visible.
- **User-Agent identificable** con correo de contacto. Si el dueño del sitio quiere
  bloquearme o avisarme, puede.
- **0,6 s entre peticiones** por defecto, configurable. Un extractor que martillea un
  servidor es un extractor que consigue que lo bloqueen.
- **Límite de páginas explícito.** Nunca "todas" por defecto.
- **Timeout de 15 s** y salida a CSV con cabecera.

## Lo que este script no hace (a propósito)

- No rota proxies ni User-Agents para evadir bloqueos.
- No ignora `robots.txt`.
- No extrae datos personales.
- No scrapea sitios cuyo ToS lo prohíbe.

Esa lista es la razón por la que un cliente puede contratarme sin revisar el contrato
con un abogado. El scraping legítimo es una herramienta; el resto es un pasivo.

## Cuándo esto vale dinero

Cuando alguien necesita un catálogo de 5.000 referencias que solo existe en una web sin
API, actualizado cada lunes. Se entrega como script + cron + CSV, y se cobra por entrega.

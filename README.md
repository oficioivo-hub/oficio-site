# Oficio — small technical work

Public site and runnable demos for **Oficio**, a small technical workshop: data cleanup,
scrapers and technical localization.

- **Site:** https://oficioivo-hub.github.io/oficio-site/
- **Contact:** oficio.ivo@gmail.com

## Demos

| Folder | What it proves | How to check it |
|---|---|---|
| [`demos/01-csv-clean`](demos/01-csv-clean) | Messy CSV → clean CSV, with traceable rejects | 13 unit tests plus a full end-to-end run |
| [`demos/02-scraper`](demos/02-scraper) | A 60-line, dependency-free extractor with rate limits | `python3 scrape_books.py --pages 2` |
| [`demos/03-localization`](demos/03-localization) | EN→ES technical translation with glossary and QA | Term-by-term comparison against the glossary |

## Why this is public

Because a promise is not proof. Anyone can read the code, run the tests and check that it
works before hiring anyone.

All code uses the standard library only: no dependencies, no `pip install`, no surprises.

## Status

Tests run locally with:

```bash
cd demos/01-csv-clean && python3 -m unittest discover -v
```

No client data, no secrets and no internal strategy live in this repository. The private
repository holds the ledger and the operations.

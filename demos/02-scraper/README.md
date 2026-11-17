← [Back to Oficio](../../)

# 02 — Catalogue scraper

A 60-line, dependency-free scraper for `books.toscrape.com` — a public site built
specifically for scraping practice. It is not a real target: it's the proof that the
extractor is clean and polite.

```bash
python3 scrape_books.py --pages 2 --out books.csv
```

```
  pagina 1: 20 libros
  pagina 2: 20 libros

40 libros -> books.csv
```

## Decisions that matter

- **`HTMLParser` from the standard library, not regex.** HTML changes; regexes break
  silently. A parser fails visibly.
- **Identifiable User-Agent** with a contact address. If the site owner wants to block me
  or warn me, they can.
- **0.6 s between requests** by default, configurable. A scraper that hammers a server is
  a scraper that gets blocked.
- **Explicit page limit.** Never "all" by default.
- **15 s timeout** and CSV output with a header row.

## What this script does not do, on purpose

- No proxy or User-Agent rotation to evade blocks.
- No ignoring `robots.txt`.
- No personal data extraction.
- No scraping of sites whose ToS forbids it.

That list is why a client can hire the workshop without a lawyer reading the contract.
Legitimate scraping is a tool; the rest is a liability.

## When this is worth money

When someone needs a 5,000-item catalogue that only exists on a website with no API,
refreshed every Monday. Delivered as a script plus a schedule, paid per deliverable.

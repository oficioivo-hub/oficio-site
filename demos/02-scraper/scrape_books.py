#!/usr/bin/env python3
"""Extractor de catalogo de books.toscrape.com (sitio de practica publico).

Solo biblioteca estandar. Educado por defecto: 0,6 s entre peticiones,
User-Agent identificable y limite de paginas explicito.

Uso:
    python3 scrape_books.py --pages 2 --out books.csv
"""

from __future__ import annotations

import argparse
import csv
import time
import urllib.request
from html.parser import HTMLParser

BASE = "https://books.toscrape.com/catalogue/page-{}.html"
USER_AGENT = "OficioBot/0.1 (+taller tecnico; contacto: oficio.ivo@gmail.com)"


class CatalogueParser(HTMLParser):
    """Extrae titulo, precio, valoracion y disponibilidad de cada libro."""

    def __init__(self) -> None:
        super().__init__()
        self.books: list[dict[str, str]] = []
        self._current: dict[str, str] | None = None
        self._field: str | None = None
        self._buffer: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class") or ""
        if tag == "article" and "product_pod" in classes:
            self._current = {"title": "", "price": "", "rating": "", "availability": ""}
        elif self._current is not None:
            if tag == "a" and attrs.get("title") and not self._current["title"]:
                self._current["title"] = attrs["title"]
            elif tag == "p" and "star-rating" in classes:
                self._current["rating"] = classes.split()[-1]
            elif "price_color" in classes:
                self._field, self._buffer = "price", []
            elif "availability" in classes:
                self._field, self._buffer = "availability", []

    def handle_data(self, data):
        if self._field:
            self._buffer.append(data)

    def handle_endtag(self, tag):
        if self._current is None:
            return
        if self._field and tag in ("p", "span"):
            text = " ".join("".join(self._buffer).split())
            self._current[self._field] = text
            self._field, self._buffer = None, []
        elif tag == "article":
            self.books.append(self._current)
            self._current = None
            self._field, self._buffer = None, []


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extrae el catalogo de books.toscrape.com")
    parser.add_argument("--pages", type=int, default=2, help="paginas a recorrer (20 libros cada una)")
    parser.add_argument("--out", default="books.csv")
    parser.add_argument("--delay", type=float, default=0.6, help="segundos entre peticiones")
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    for page in range(1, args.pages + 1):
        html = fetch(BASE.format(page))
        catalogue = CatalogueParser()
        catalogue.feed(html)
        rows.extend(catalogue.books)
        print(f"  pagina {page}: {len(catalogue.books)} libros")
        time.sleep(args.delay)

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["title", "price", "rating", "availability"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{len(rows)} libros -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

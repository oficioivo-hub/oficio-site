#!/usr/bin/env python3
"""Normaliza un CSV de clientes sucio y separa lo irrecuperable.

Sin dependencias externas: solo biblioteca estandar. Se ejecuta en cualquier
maquina con Python 3.9+ sin instalar nada.

Uso:
    python3 clean.py data/messy_sales.csv -o out

Salida:
    out/clean.csv    registros validos y deduplicados
    out/rejects.csv  registros descartados con motivo
    out/report.json  resumen legible por maquina
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

DATE_FORMATS = (
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%Y/%m/%d",
    "%d.%m.%Y",
    "%b %d %Y",
    "%B %d %Y",
    "%d-%m-%Y",
)

COUNTRY_MAP = {
    "es": "ES", "spain": "ES", "espana": "ES", "españa": "ES",
    "us": "US", "usa": "US", "united states": "US",
    "cl": "CL", "chile": "CL",
    "ar": "AR", "argentina": "AR",
    "mx": "MX", "mexico": "MX", "méxico": "MX",
    "de": "DE", "germany": "DE",
    "ie": "IE", "ireland": "IE",
    "bg": "BG", "bulgaria": "BG",
    "ma": "MA", "morocco": "MA",
    "pt": "PT", "portugal": "PT",
}

PLAN_MAP = {
    "free": "free",
    "basic": "basic",
    "pro": "pro",
    "enterprise": "enterprise",
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
CURRENCY_RE = re.compile(r"(?i)\b(usd|eur|clp|ars|mxn|gbp)\b")

OUTPUT_FIELDS = ["id", "name", "email", "signup_date", "amount", "plan", "country"]


def norm_ws(value: str) -> str:
    """Colapsa espacios repetidos y recorta extremos."""
    return re.sub(r"\s+", " ", (value or "")).strip()


def parse_date(raw: str) -> str:
    text = norm_ws(raw)
    if not text:
        raise ValueError("fecha vacia")
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"fecha no reconocida: {raw!r}")


def parse_amount(raw: str) -> Decimal:
    text = norm_ws(raw)
    if not text:
        raise ValueError("importe vacio")
    text = CURRENCY_RE.sub("", text)
    text = text.replace("$", "").replace("€", "").strip()
    if "," in text and "." in text:
        # 1.234,56 -> 1234.56
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")
    try:
        value = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"importe no parseable: {raw!r}") from exc
    if value < 0:
        raise ValueError(f"importe negativo: {raw!r}")
    return value.quantize(Decimal("0.01"))


def parse_email(raw: str) -> str:
    email = norm_ws(raw).lower()
    if not email:
        raise ValueError("email vacio")
    if not EMAIL_RE.match(email):
        raise ValueError(f"email invalido: {raw!r}")
    return email


def parse_plan(raw: str) -> str:
    plan = norm_ws(raw).lower()
    return PLAN_MAP.get(plan, "other")


def parse_country(raw: str) -> str:
    key = norm_ws(raw).lower()
    if not key:
        return "??"
    return COUNTRY_MAP.get(key, key.upper()[:2])


def clean_row(row: dict, line: int):
    """Devuelve (registro_limpio, None) o (None, motivo)."""
    try:
        record = {
            "id": norm_ws(row.get("id", "")),
            "name": norm_ws(row.get("customer_name") or row.get("name") or ""),
            "email": parse_email(row.get("email", "")),
            "signup_date": parse_date(row.get("signup_date", "")),
            "amount": str(parse_amount(row.get("amount", ""))),
            "plan": parse_plan(row.get("plan", "")),
            "country": parse_country(row.get("country", "")),
        }
    except ValueError as exc:
        return None, {"line": line, "reason": str(exc), "raw": dict(row)}
    return record, None


def clean_rows(rows: list[dict]) -> tuple[list[dict], list[dict], dict]:
    cleaned: list[dict] = []
    rejects: list[dict] = []
    seen: set[tuple[str, str, str]] = set()
    duplicates = 0
    blank = 0

    for index, row in enumerate(rows, start=2):  # 2 = primera fila de datos
        if not any(norm_ws(v) for v in row.values()):
            blank += 1
            continue

        record, reason = clean_row(row, index)
        if record is None:
            rejects.append(reason)
            continue

        key = (record["email"], record["signup_date"], record["amount"])
        if key in seen:
            duplicates += 1
            rejects.append({"line": index, "reason": "duplicado", "raw": dict(row)})
            continue
        seen.add(key)
        cleaned.append(record)

    report = {
        "rows_in": len(rows),
        "rows_out": len(cleaned),
        "rejected": len(rejects),
        "duplicates": duplicates,
        "blank_rows": blank,
        "reject_reasons": dict(Counter(r["reason"].split(":")[0] for r in rejects)),
        "total_amount": str(sum(Decimal(r["amount"]) for r in cleaned)),
        "by_country": dict(Counter(r["country"] for r in cleaned)),
        "by_plan": dict(Counter(r["plan"] for r in cleaned)),
    }
    return cleaned, rejects, report


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = []
        for raw in reader:
            rows.append({norm_ws(k).lower(): v for k, v in raw.items() if k is not None})
        return rows


def write_csv(path: Path, records: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow(record)
    print(f"  {path}  ({len(records)} filas)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Limpia un CSV de clientes.")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--out", type=Path, default=Path("out"))
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"ERROR: no existe {args.input}", file=sys.stderr)
        return 1

    rows = read_csv(args.input)
    cleaned, rejects, report = clean_rows(rows)

    write_csv(args.out / "clean.csv", cleaned, OUTPUT_FIELDS)
    write_csv(args.out / "rejects.csv", rejects, ["line", "reason"])
    (args.out / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print()
    print(f"entrada      {report['rows_in']}")
    print(f"salida       {report['rows_out']}")
    print(f"rechazadas   {report['rejected']}  ({report['duplicates']} duplicadas, "
          f"{report['blank_rows']} vacias)")
    print(f"importe      {report['total_amount']}")
    print(f"paises       {', '.join(f'{k}:{v}' for k, v in sorted(report['by_country'].items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

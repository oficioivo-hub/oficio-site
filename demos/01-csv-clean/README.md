← [Back to Oficio](../../)

# 01 — Client CSV cleanup

A real CSV arrives with dates in four formats, currency symbols, double spaces in names,
uppercase emails, plans written three different ways and duplicate rows. This script turns
it into one auditable format — and reports exactly what it dropped, and why.

**No dependencies.** Standard library only. No `pip install`, no virtualenv, no surprises
in production.

## What it handles

| Problem in the input | Result |
|---|---|
| `2024-03-05`, `05/03/2024`, `2024/03/09`, `16.03.2024`, `Mar 11 2024` | `YYYY-MM-DD` |
| `$19.99`, `19,99`, `USD 29.00`, `$ 25,50`, `1.234,56` | `Decimal`, 2 places |
| `ANA@Example.COM ` | `ana@example.com` |
| ` PRO `, `pro`, `Pro` | `pro` |
| `España`, `es`, `ES` | `ES` |
| Duplicate rows | removed |
| Email without TLD, impossible date, negative or empty amount | moved to `rejects.csv` with a reason and line number |
| Blank rows | counted, not written |

## Guarantees the tests enforce

- **Idempotent** — cleaning the output returns exactly the same output.
- **Traceable** — every dropped row has a line number and a reason.
- **Deterministic** — same input, same output, no network, no randomness.

## Run it

```bash
python3 clean.py data/messy_sales.csv -o out
```

```
  out/clean.csv  (17 rows)
  out/rejects.csv  (6 rows)

rows in      24
rows out     17
rejected     6  (2 duplicates, 1 blank)
total amount 346.87
countries    AR:1, CL:3, DE:1, ES:6, IE:1, MA:1, MX:1, PT:1, US:2
```

## Tests

```bash
python3 -m unittest discover -v
# Ran 13 tests ... OK
```

The suite covers every parser separately and the full flow against the fixture: counts,
total amount, reason per line, absence of duplicates, output format and idempotence.

## Output

- `out/clean.csv` — valid records: `id, name, email, signup_date, amount, plan, country`
- `out/rejects.csv` — `line, reason`
- `out/report.json` — counts, total amount, breakdown by country and plan

## When this is worth money

When someone has 40,000 customer rows exported from three systems and needs a list that
imports into their CRM without breaking. That job is paid per deliverable, not per hour,
and it's accepted or rejected by looking at the report.

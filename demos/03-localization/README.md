← [Back to Oficio](../../)

# 03 — Technical localization, EN → ES

A real documentation page translated from English to Spanish, plus the two things that
make technical translation verifiable instead of opinion: a **glossary** and a **QA
checklist**.

## What's in here

| File | What it is |
|---|---|
| [`source/webhook-retries.en.md`](source/webhook-retries.en.md) | The English source: webhook delivery and retry policy |
| [`es/webhook-retries.es.md`](es/webhook-retries.es.md) | The Spanish translation |
| [`glossary.csv`](glossary.csv) | 12 terms: how each one is translated, and what not to do |
| [`QA.md`](QA.md) | The 20-point checklist applied before delivery |

## How to judge this

You don't need Spanish to check the two things that break technical translations:

1. **Numbers and table rows match.** 10 s, 8 attempts, 24 h, 72 h, 30 days, 7 days — all
   present in both files, in the same order.
2. **Code identifiers are untouched.** `POST`, `2xx`, `event_id`, `created_at`, `ping`
   appear exactly as written. Including `exhausted`, which is an API value and stays in
   English even though it looks translatable.

If those two hold and the glossary is followed, the translation is auditable. Everything
else is style, and style is negotiable.

## Why the glossary exists

Without one, "endpoint" becomes "endpoint" on page one, "punto de conexión" on page four
and "extremo" on page nine. It reads like three different people translated it. With a
glossary, it reads like one.

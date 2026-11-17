← [Back to Oficio](../../)

# Localization QA — checklist

Every item is checked before delivery. No exceptions.

## Integrity

- [ ] Every number matches the source: 10 s, 8 attempts, 24 h, 72 h, 30 days, 7 days.
- [ ] Every table has the same rows in the same order.
- [ ] Code identifiers are not translated: `POST`, `2xx`, `event_id`, `created_at`, `exhausted`, `ping`.
- [ ] API literal values stay as written, even when they look translatable (`exhausted`).
- [ ] No section missing, none added.

## Terminology

- [ ] Every term follows the glossary.
- [ ] The same term is translated the same way throughout the document.
- [ ] "endpoint" stays "endpoint"; it does not alternate with "punto de conexión".

## Language

- [ ] Consistent informal register; never mixed with formal address.
- [ ] No literal calques.
- [ ] No unnecessary anglicisms where a natural equivalent exists.
- [ ] Spanish typographic quotes «» used in Spanish prose.
- [ ] Section numbers and internal links still resolve.

## Voice

- [ ] Reads as if it were written in Spanish, not translated into it.
- [ ] Nothing added, nothing removed.
- [ ] The source is not "improved": if it's ambiguous, ask.

## Delivery

- [ ] Same file format as the source (`.md`, `.html`, `.json`).
- [ ] No review marks, comments or `TODO` left in the final file.
- [ ] Glossary updated if a new term appeared.

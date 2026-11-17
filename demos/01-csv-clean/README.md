# 01 — Limpieza de CSV de clientes

Un CSV real suele venir con fechas en cuatro formatos, importes con símbolo de moneda,
nombres con doble espacio, correos en mayúsculas, planes escritos de tres maneras y
filas duplicadas. Este script lo deja en un formato único y auditable — y dice
exactamente qué descartó y por qué.

**Sin dependencias.** Solo biblioteca estándar de Python. No hay `pip install`, no hay
entorno virtual, no hay sorpresas en producción.

## Qué hace

| Problema en la entrada | Resultado |
|---|---|
| `2024-03-05`, `05/03/2024`, `2024/03/09`, `16.03.2024`, `Mar 11 2024` | `YYYY-MM-DD` |
| `$19.99`, `19,99`, `USD 29.00`, `$ 25,50`, `1.234,56` | `Decimal` con 2 decimales |
| `ANA@Example.COM ` | `ana@example.com` |
| ` PRO `, `pro`, `Pro` | `pro` |
| `España`, `es`, `ES` | `ES` |
| Filas duplicadas | eliminadas |
| Email sin TLD, fecha imposible, importe negativo o vacío | apartadas en `rejects.csv` con motivo y número de línea |
| Filas en blanco | contadas, no escritas |

Garantías que verifican las pruebas:

- **Idempotente**: limpiar la salida devuelve exactamente la misma salida.
- **Trazable**: cada descarte tiene línea y motivo.
- **Determinista**: mismo input, mismo output, sin red y sin azar.

## Ejecutar

```bash
python3 clean.py data/messy_sales.csv -o out
```

```
  out/clean.csv  (17 filas)
  out/rejects.csv  (6 filas)

entrada      24
salida       17
rechazadas   6  (2 duplicadas, 1 vacias)
importe      346.87
paises       AR:1, CL:3, DE:1, ES:6, IE:1, MA:1, MX:1, PT:1, US:2
```

## Pruebas

```bash
python3 -m unittest discover -v
# Ran 13 tests ... OK
```

Las pruebas cubren cada parser por separado y el flujo completo contra el fixture:
conteos, importe total, motivo por línea, ausencia de duplicados, formato de salida e
idempotencia.

## Salida

- `out/clean.csv` — registros válidos: `id, name, email, signup_date, amount, plan, country`
- `out/rejects.csv` — `line, reason`
- `out/report.json` — conteos, importe total, desglose por país y plan

## Cuándo esto vale dinero

Cuando alguien tiene 40.000 filas de clientes exportadas de tres sistemas y necesita
una lista que se pueda importar a su CRM sin que se rompa. Ese trabajo se cobra por
entrega, no por hora, y se acepta o se rechaza mirando el reporte.

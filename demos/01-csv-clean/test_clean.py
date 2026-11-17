#!/usr/bin/env python3
"""Pruebas del limpiador. Ejecutar: python3 -m unittest discover -v"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import clean  # noqa: E402

FIXTURE = Path(__file__).parent / "data" / "messy_sales.csv"


class TestParsers(unittest.TestCase):
    def test_fechas_validas(self):
        casos = {
            "2024-03-05": "2024-03-05",
            "05/03/2024": "2024-03-05",
            "2024/03/09": "2024-03-09",
            "16.03.2024": "2024-03-16",
            "Mar 11 2024": "2024-03-11",
            "  2024-03-25  ": "2024-03-25",
        }
        for entrada, esperado in casos.items():
            with self.subTest(entrada=entrada):
                self.assertEqual(clean.parse_date(entrada), esperado)

    def test_fecha_invalida(self):
        for entrada in ["", "2024-13-45", "mañana", "31/02/2024"]:
            with self.subTest(entrada=entrada):
                with self.assertRaises(ValueError):
                    clean.parse_date(entrada)

    def test_importes(self):
        casos = {
            "19.99": "19.99",
            "$19.99": "19.99",
            " 19.99 ": "19.99",
            "USD 29.00": "29.00",
            "19,99": "19.99",
            "$ 25,50": "25.50",
            "1.234,56": "1234.56",
            "0.00": "0.00",
        }
        for entrada, esperado in casos.items():
            with self.subTest(entrada=entrada):
                self.assertEqual(str(clean.parse_amount(entrada)), esperado)

    def test_importes_invalidos(self):
        for entrada in ["", "   ", "-5.00", "gratis", "19.99.99"]:
            with self.subTest(entrada=entrada):
                with self.assertRaises(ValueError):
                    clean.parse_amount(entrada)

    def test_email(self):
        self.assertEqual(clean.parse_email("ANA@Example.COM "), "ana@example.com")
        for entrada in ["", "carla.ruiz@example", "sin arroba.com", "@example.com"]:
            with self.subTest(entrada=entrada):
                with self.assertRaises(ValueError):
                    clean.parse_email(entrada)

    def test_plan_desconocido_no_rompe(self):
        self.assertEqual(clean.parse_plan("PRO "), "pro")
        self.assertEqual(clean.parse_plan("Premium"), "other")

    def test_pais(self):
        self.assertEqual(clean.parse_country("España"), "ES")
        self.assertEqual(clean.parse_country("chile"), "CL")
        self.assertEqual(clean.parse_country(""), "??")


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        rows = clean.read_csv(FIXTURE)
        self.cleaned, self.rejects, self.report = clean.clean_rows(rows)

    def test_conteos(self):
        self.assertEqual(self.report["rows_in"], 24)
        self.assertEqual(self.report["rows_out"], 17)
        self.assertEqual(self.report["rejected"], 6)
        self.assertEqual(self.report["duplicates"], 2)
        self.assertEqual(self.report["blank_rows"], 1)

    def test_importe_total(self):
        self.assertEqual(self.report["total_amount"], "346.87")

    def test_motivos_por_linea(self):
        motivos = {r["line"]: r["reason"].split(":")[0] for r in self.rejects}
        self.assertEqual(motivos[4], "email invalido")
        self.assertEqual(motivos[6], "importe vacio")
        self.assertEqual(motivos[7], "duplicado")
        self.assertEqual(motivos[17], "importe negativo")
        self.assertEqual(motivos[20], "fecha no reconocida")
        self.assertEqual(motivos[25], "duplicado")

    def test_sin_duplicados(self):
        claves = [(r["email"], r["signup_date"], r["amount"]) for r in self.cleaned]
        self.assertEqual(len(claves), len(set(claves)))

    def test_invariantes_de_salida(self):
        for r in self.cleaned:
            with self.subTest(email=r["email"]):
                self.assertRegex(r["signup_date"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertRegex(r["amount"], r"^\d+\.\d{2}$")
                self.assertEqual(r["email"], r["email"].lower())
                self.assertNotIn("  ", r["name"])
                self.assertRegex(r["country"], r"^[A-Z?]{2}$")

    def test_idempotencia(self):
        """Limpiar la salida debe dar exactamente lo mismo."""
        otra_vez, rechazos, _ = clean.clean_rows(self.cleaned)
        self.assertEqual(otra_vez, self.cleaned)
        self.assertEqual(rechazos, [])


if __name__ == "__main__":
    unittest.main()

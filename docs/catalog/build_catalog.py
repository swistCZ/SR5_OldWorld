#!/usr/bin/env python3
"""Vytvoří jednotný TSV katalog herních položek SW1938.

Zdrojová data zůstávají v původních dávkách. Tento skript je pouze sjednotí do
jedné tabulky vhodné pro import do Google Sheets.

Použití z kořene repozitáře:
    python3 docs/catalog/build_catalog.py

Výstup:
    docs/catalog/shadowwar1938_catalog.tsv
"""
from __future__ import annotations

import csv
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
OUT = Path(__file__).resolve().parent / "shadowwar1938_catalog.tsv"

SOURCE_FILES = [
    *sorted((DOCS / "weapons").glob("batch*.tsv")),
    DOCS / "accessories" / "batchAC1_doplnky.tsv",
    DOCS / "armor" / "batchA1_zbroj.tsv",
    DOCS / "gear" / "batchG1_vybaveni.tsv",
    DOCS / "qualities" / "batchQ1_kvality.tsv",
    DOCS / "vehicles" / "batchV1_vozidla.tsv",
]

HEADERS = [
    "ID", "Typ", "Číslo", "Název", "Kategorie", "Technické informace",
    "Popis", "Země", "Rok", "Historický status", "Role", "Poškození",
    "AP", "Režim palby", "RC", "Munice / kapacita", "Conceal",
    "Accuracy", "Reach", "Dostupnost", "Cena", "Dovednost",
    "Výchozí vybavení", "Rating", "Kapacita zbroje", "ArmorOverride",
    "Handling", "Speed", "Acceleration", "Body", "Armor", "Sensor",
    "Seats", "Pilot", "Mount", "Efekt / vlastnost", "Bonus",
    "Poznámka", "Zdrojový soubor", "Zdrojový řádek",
]


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for number, row in enumerate(reader, start=2):
            yield number, {key: (value or "").strip() for key, value in row.items() if key}


def first(row, *names):
    for name in names:
        if row.get(name, ""):
            return row[name]
    return ""


def category(row):
    return first(row, "SR5 kategorie", "SW1938 kategorie", "Skupina", "Kategorie")


def item_name(row):
    return first(row, "Zbraň", "Doplňek", "Zbroj", "Vybavení", "Kvalita", "Vozidlo")


def item_type(path: Path, row):
    folder = path.parent.name
    if folder == "weapons":
        return "Zbraň"
    return {
        "accessories": "Doplněk ke zbrani",
        "armor": "Zbroj",
        "gear": "Vybavení",
        "qualities": "Kvalita",
        "vehicles": "Vozidlo",
    }.get(folder, folder)


def make_row(path, source_line, row):
    name = item_name(row)
    typ = item_type(path, row)
    number = first(row, "Číslo")
    identifier = f"{typ}:{number}:{name}"
    return {
        "ID": identifier,
        "Typ": typ,
        "Číslo": number,
        "Název": name,
        "Kategorie": category(row),
        "Technické informace": first(row, "Technické informace"),
        "Popis": first(row, "Popis"),
        "Země": first(row, "Země"),
        "Rok": first(row, "Rok"),
        "Historický status": first(row, "Typ"),
        "Role": first(row, "Role"),
        "Poškození": first(row, "DMG", "Damage"),
        "AP": first(row, "AP"),
        "Režim palby": first(row, "Mode"),
        "RC": first(row, "RC"),
        "Munice / kapacita": first(row, "Ammo", "Kapacita"),
        "Conceal": first(row, "Conceal"),
        "Accuracy": first(row, "Accuracy"),
        "Reach": first(row, "Reach"),
        "Dostupnost": first(row, "Avail"),
        "Cena": first(row, "Cost"),
        "Dovednost": first(row, "Useskill"),
        "Výchozí vybavení": first(row, "Defaultní vybavení"),
        "Rating": first(row, "Rating"),
        "Kapacita zbroje": first(row, "Armor"),
        "ArmorOverride": first(row, "ArmorOverride"),
        "Handling": first(row, "Handling"),
        "Speed": first(row, "Speed"),
        "Acceleration": first(row, "Accel"),
        "Body": first(row, "Body"),
        "Armor": first(row, "Armor"),
        "Sensor": first(row, "Sensor"),
        "Seats": first(row, "Seats"),
        "Pilot": first(row, "Pilot"),
        "Mount": first(row, "Mount"),
        "Efekt / vlastnost": first(row, "Efekt", "Vlastnost", "BonusTyp"),
        "Bonus": "",
        "Poznámka": first(row, "Poznámka"),
        "Zdrojový soubor": str(path.relative_to(ROOT)),
        "Zdrojový řádek": str(source_line),
    }


def main():
    output = []
    quality_groups = OrderedDict()

    for path in SOURCE_FILES:
        if not path.exists():
            raise FileNotFoundError(path)
        for source_line, row in read_rows(path):
            if not item_name(row):
                continue
            if path.parent.name == "qualities":
                key = (item_name(row), row.get("Kategorie", ""), row.get("Karma", ""))
                if key not in quality_groups:
                    quality_groups[key] = (path, source_line, row, [])
                if row.get("BonusTyp"):
                    quality_groups[key][3].append(
                        ": ".join(part for part in (
                            row.get("BonusTyp", ""), row.get("BonusCil", ""),
                            row.get("BonusHodnota", ""), row.get("Podminka", ""),
                        ) if part)
                    )
            else:
                output.append(make_row(path, source_line, row))

    for path, source_line, row, bonuses in quality_groups.values():
        result = make_row(path, source_line, row)
        result["Bonus"] = " | ".join(bonuses)
        result["Poznámka"] = first(row, "Poznámka")
        output.append(result)

    output.sort(key=lambda item: (item["Typ"], item["Kategorie"], item["Číslo"], item["Název"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output)
    print(f"Vytvořeno: {OUT.relative_to(ROOT)}")
    print(f"Položek: {len(output)}")


if __name__ == "__main__":
    main()

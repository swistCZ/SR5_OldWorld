#!/usr/bin/env python3
"""Sestavi custom_armor.xml pro Chummer z TSV (docs/armor/batchA1_zbroj.tsv).

Kategorie jsou uz v TSV pojmenovane "SW1938 - ...", takze se pouziji primo.
Atributy kategorii zrcadli SR5 (blackmarket="Armor").
armoroverride umoznuje vrstveni zbroji (jako Mortimer/Ulysses v SR5).

Pouziti: python3 build_armor_xml.py
"""
import csv, uuid, os
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
OUT = os.path.join(ROOT, "Chummer5a", "customdata", "ShadowWar 1938", "custom_armor.xml")
TSV = os.path.join(HERE, "batchA1_zbroj.tsv")
SOURCE = "SW1938"
GUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, "shadowwar1938-armor")


def guid(name):
    return str(uuid.uuid5(GUID_NS, name))


def main():
    with open(TSV, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        rows = [dict(zip(header, r)) for r in reader]

    cats = sorted({r["SW1938 kategorie"].strip() for r in rows})

    root = ET.Element("chummer")
    cats_el = ET.SubElement(root, "categories")
    for c in cats:
        ET.SubElement(cats_el, "category", {"blackmarket": "Armor"}).text = c

    armors_el = ET.SubElement(root, "armors")

    def add(a, tag, val):
        if val is None:
            return
        val = str(val).strip()
        if val == "" or val == "-":
            return
        ET.SubElement(a, tag).text = val

    for r in rows:
        name = r["Zbroj"].strip()
        a = ET.SubElement(armors_el, "armor")
        add(a, "id", guid(name))
        add(a, "name", name)
        add(a, "category", r["SW1938 kategorie"])
        add(a, "armor", r["Armor"])
        add(a, "armoroverride", r["ArmorOverride"])
        add(a, "armorcapacity", r["Kapacita"])
        add(a, "avail", r["Avail"])
        add(a, "cost", r["Cost"])
        add(a, "source", SOURCE)
        add(a, "page", r["Číslo"])

    header_txt = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<!--\n"
        "  SHADOW WAR 1938 - custom armor (generated from docs/armor/*.tsv).\n"
        "  Custom categories \"SW1938 - ...\"; armoroverride enables layering.\n"
        "  Do not edit by hand; edit the TSV and re-run build_armor_xml.py.\n"
        "-->\n"
    )
    ET.indent(root, space="  ")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header_txt + ET.tostring(root, encoding="unicode") + "\n")

    print(f"Zapsano: {OUT}")
    print(f"Zbroji: {len(rows)} | kategorii: {len(cats)}")


if __name__ == "__main__":
    main()

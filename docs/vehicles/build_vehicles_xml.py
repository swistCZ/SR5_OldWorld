#!/usr/bin/env python3
"""Sestavi custom_vehicles.xml pro Chummer z TSV (docs/vehicles/batchV1_vozidla.tsv).

Kategorie jsou v TSV pojmenovane "SW1938 - ...", takze se pouziji primo.
Atributy kategorii zrcadli SR5 (blackmarket="Vehicles").

Pouziti: python3 build_vehicles_xml.py
"""
import csv, uuid, os
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
OUT = os.path.join(ROOT, "Chummer5a", "customdata", "ShadowWar 1938", "custom_vehicles.xml")
TSV = os.path.join(HERE, "batchV1_vozidla.tsv")
SOURCE = "SW1938"
GUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, "shadowwar1938-vehicle")


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
        ET.SubElement(cats_el, "category", {"blackmarket": "Vehicles"}).text = c

    veh_el = ET.SubElement(root, "vehicles")

    def add(v, tag, val):
        if val is None:
            return
        val = str(val).strip()
        if val == "" or val == "-":
            return
        ET.SubElement(v, tag).text = val

    for r in rows:
        name = r["Vozidlo"].strip()
        v = ET.SubElement(veh_el, "vehicle")
        add(v, "id", guid(name))
        add(v, "name", name)
        add(v, "page", r["Číslo"])
        add(v, "source", SOURCE)
        add(v, "accel", r["Accel"])
        add(v, "armor", r["Armor"])
        add(v, "avail", r["Avail"])
        add(v, "body", r["Body"])
        add(v, "category", r["SW1938 kategorie"])
        add(v, "cost", r["Cost"])
        add(v, "handling", r["Handling"])
        add(v, "pilot", r["Pilot"])
        add(v, "sensor", r["Sensor"])
        add(v, "speed", r["Speed"])
        add(v, "seats", r["Seats"])

    header_txt = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<!--\n"
        "  SHADOW WAR 1938 - custom vehicles (generated from docs/vehicles/*.tsv).\n"
        "  Custom categories \"SW1938 - ...\"; source SW1938.\n"
        "  Do not edit by hand; edit the TSV and re-run build_vehicles_xml.py.\n"
        "-->\n"
    )
    ET.indent(root, space="  ")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header_txt + ET.tostring(root, encoding="unicode") + "\n")

    print(f"Zapsano: {OUT}")
    print(f"Vozidel: {len(rows)} | kategorii: {len(cats)}")
    ids = [guid(r["Vozidlo"].strip()) for r in rows]
    print("GUID unikatni:", len(ids) == len(set(ids)))


if __name__ == "__main__":
    main()

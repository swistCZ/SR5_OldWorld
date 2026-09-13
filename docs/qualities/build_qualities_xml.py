#!/usr/bin/env python3
"""Sestavi custom_qualities.xml pro Chummer z TSV (docs/qualities/batchQ1_kvality.tsv).

POZOR: Chummer urcuje pozitivni/negativni kvalitu podle <category> ("Negative"
= negativni, cokoli jineho = pozitivni). Proto se kategorie NEMENI na vlastni -
zustava standardni "Positive"/"Negative" (kvuli chargen pravidlum).

Bonusy: jeden radek TSV = jeden bonus. Kvality se seskupi podle nazvu.
Podporovane BonusTyp: initiative, skill, skillcategory, spellresistance,
judgeintentionsdefense, toxincontactresist, pathogencontactresist,
damageresistance, notoriety, specificattribute.

Pouziti: python3 build_qualities_xml.py
"""
import csv, uuid, os
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
OUT = os.path.join(ROOT, "Chummer5a", "customdata", "ShadowWar 1938", "custom_qualities.xml")
TSV = os.path.join(HERE, "batchQ1_kvality.tsv")
SOURCE = "SW1938"
GUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, "shadowwar1938-quality")


def guid(name):
    return str(uuid.uuid5(GUID_NS, name))


def read_tsv(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        return [dict(zip(header, r)) for r in reader]


def make_bonus(bonus_el, btype, target, value, condition):
    if not btype:
        return
    if btype == "initiative":
        el = ET.SubElement(bonus_el, "initiative", {"precedence": "0"})
        el.text = value
    elif btype == "skillcategory":
        el = ET.SubElement(bonus_el, "skillcategory")
        ET.SubElement(el, "name").text = target
        ET.SubElement(el, "bonus").text = value
        if condition:
            ET.SubElement(el, "condition").text = condition
    elif btype == "specificskill":
        el = ET.SubElement(bonus_el, "specificskill")
        ET.SubElement(el, "name").text = target
        ET.SubElement(el, "bonus").text = value
        if condition:
            ET.SubElement(el, "condition").text = condition
    elif btype == "specificattribute":
        el = ET.SubElement(bonus_el, "specificattribute")
        ET.SubElement(el, "name").text = target
        ET.SubElement(el, "val").text = value
    else:
        # jednoduche tagy s textem (spellresistance, notoriety, ...)
        el = ET.SubElement(bonus_el, btype)
        el.text = value
        if condition:
            ET.SubElement(el, "condition").text = condition


def main():
    rows = read_tsv(TSV)

    # seskupit podle nazvu (zachovat poradi)
    order = []
    groups = {}
    for r in rows:
        name = r["Kvalita"].strip()
        if name not in groups:
            groups[name] = []
            order.append(name)
        groups[name].append(r)

    root = ET.Element("chummer")
    qual_el = ET.SubElement(root, "qualities")

    for name in order:
        grp = groups[name]
        first = grp[0]
        q = ET.SubElement(qual_el, "quality")
        ET.SubElement(q, "id").text = guid(name)
        ET.SubElement(q, "name").text = name
        ET.SubElement(q, "karma").text = first["Karma"].strip()
        ET.SubElement(q, "category").text = first["Kategorie"].strip()
        if first["Max"].strip():
            ET.SubElement(q, "max").text = first["Max"].strip()
        # bonusy
        bonuses = [r for r in grp if r["BonusTyp"].strip()]
        if bonuses:
            bonus_el = ET.SubElement(q, "bonus")
            for r in bonuses:
                make_bonus(bonus_el, r["BonusTyp"].strip(), r["BonusCil"].strip(),
                           r["BonusHodnota"].strip(), r["Podminka"].strip())
        ET.SubElement(q, "source").text = SOURCE
        ET.SubElement(q, "page").text = first["Číslo"].strip()

    header_txt = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<!--\n"
        "  SHADOW WAR 1938 - custom qualities (generated from docs/qualities/*.tsv).\n"
        "  Categories stay standard (Positive/Negative) because Chummer derives\n"
        "  the quality type from the category. Source: SW1938.\n"
        "  Do not edit by hand; edit the TSV and re-run build_qualities_xml.py.\n"
        "-->\n"
    )
    ET.indent(root, space="  ")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header_txt + ET.tostring(root, encoding="unicode") + "\n")

    print(f"Zapsano: {OUT}")
    print(f"Kvalit: {len(order)}")
    ids = [guid(n) for n in order]
    print("GUID unikatni:", len(ids) == len(set(ids)))


if __name__ == "__main__":
    main()

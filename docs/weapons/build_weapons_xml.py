#!/usr/bin/env python3
"""Sestavi custom_weapons.xml pro Chummer z TSV davky (davky 1-10).

Vlastni kategorie (varianta B): zbrane se zaradi do kategorii "SW1938 - ...",
aby se v Chummeru daly filtrovat oddelene. Kazda kategorie zrcadli atributy
(type, gunneryspec, blackmarket) puvodni SR5 kategorie, aby fungovala munice.
Kazda zbran dostane explicitni <range>, protoze vlastni kategorie nejsou
v ranges.xml.

Pouziti: python3 build_weapons_xml.py
"""
import csv, uuid, os, re
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "Chummer5a", "customdata", "ShadowWar 1938", "custom_weapons.xml")
SOURCE = "SW1938"
GUID_NS = uuid.uuid5(uuid.NAMESPACE_URL, "shadowwar1938")

BATCHES = [
    "batch01_pistole.tsv", "batch01_nove.tsv",
    "batch02_samopaly.tsv",
    "batch03_brokovnice.tsv", "batch03_nove.tsv",
    "batch04_pusky.tsv", "batch04_nove.tsv",
    "batch05_utocne.tsv",
    "batch06_odstrelovaci.tsv",
    "batch07_kulomety.tsv",
    "batch08_chladne.tsv",
    "batch09_tezke.tsv",
    "batch10_setting.tsv",
]

# Puvodni SR5 kategorie -> nase kategorie + atributy + range
MAP = {
    "Holdouts":            ("SW1938 – Pistols",           dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Holdouts"),
    "Light Pistols":       ("SW1938 – Pistols",           dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Light Pistols"),
    "Heavy Pistols":       ("SW1938 – Pistols",           dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Heavy Pistols"),
    "Machine Pistols":     ("SW1938 – Pistols",           dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Machine Pistols"),
    "Submachine Guns":     ("SW1938 – Submachine Guns",   dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Submachine Guns"),
    "Shotguns":            ("SW1938 – Shotguns",          dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Shotguns"),
    "Sporting Rifles":     ("SW1938 – Rifles",            dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Sporting Rifles"),
    "Assault Rifles":      ("SW1938 – Assault Rifles",    dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Assault Rifles"),
    "Sniper Rifles":       ("SW1938 – Sniper Rifles",     dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Sniper Rifles"),
    "Light Machine Guns":  ("SW1938 – Machine Guns",      dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Light Machine Guns"),
    "Medium Machine Guns": ("SW1938 – Machine Guns",      dict(type="gun", gunneryspec="Ballistic", blackmarket="Weapons"), "Medium/Heavy Machinegun"),
    "Blades":              ("SW1938 – Melee",             dict(type="melee", blackmarket="Weapons"), None),
    "Clubs":               ("SW1938 – Melee",             dict(type="melee", blackmarket="Weapons"), None),
    "Flamethrowers":       ("SW1938 – Flamethrowers",     dict(type="flame", gunneryspec="Energy", blackmarket="Weapons"), "Flamethrowers"),
    "Assault Cannons":     ("SW1938 – Anti-Tank Rifles",  dict(type="cannon", gunneryspec="Ballistic", blackmarket="Weapons"), "Assault Cannons"),
    "Grenade Launchers":   ("SW1938 – Mortars",           dict(type="glauncher", gunneryspec="Artillery", blackmarket="Weapons"), "Grenade Launchers"),
    "Exotic Ranged Weapons": ("SW1938 – Tesla & Occult",  dict(type="exotic", blackmarket="Weapons"), "Sporting Rifles"),
}


def guid(name):
    return str(uuid.uuid5(GUID_NS, name))


def load_rows():
    rows = []
    for b in BATCHES:
        path = os.path.join(HERE, b)
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t")
            header = next(reader)
            for line in reader:
                rows.append(dict(zip(header, line)))
    return rows


def main():
    rows = load_rows()
    used_cats = {}
    weapons = []
    skipped = []

    for r in rows:
        cat = r["SR5 kategorie"].strip()
        if cat not in MAP:
            skipped.append(r["Zbraň"])
            continue
        custom_cat, attrs, rng = MAP[cat]
        used_cats[custom_cat] = attrs
        weapons.append((r, custom_cat, rng))

    # sestav XML
    root = ET.Element("chummer")

    cats_el = ET.SubElement(root, "categories")
    for cat in sorted(used_cats):
        ET.SubElement(cats_el, "category", used_cats[cat]).text = cat

    weapons_el = ET.SubElement(root, "weapons")
    for r, custom_cat, rng in weapons:
        name = r["Zbraň"].strip()
        w = ET.SubElement(weapons_el, "weapon")

        def add(tag, val):
            if val is None:
                return
            val = str(val).strip()
            if val == "":
                return
            ET.SubElement(w, tag).text = val

        add("id", guid(name))
        add("name", name)
        add("category", custom_cat)
        # ranged vs melee
        add("type", "Melee" if custom_cat == "SW1938 – Melee" else "Ranged")
        add("conceal", r["Conceal"])
        add("accuracy", r["Accuracy"])
        add("reach", r["Reach"] if r["Reach"].strip() else "0")
        add("damage", r["DMG"])
        add("ap", r["AP"])
        add("mode", r["Mode"])
        add("rc", r["RC"])
        add("ammo", r["Ammo"])
        add("avail", r["Avail"])
        add("cost", r["Cost"])
        add("source", SOURCE)
        add("page", r["Číslo"])
        if rng:
            add("range", rng)
        add("useskill", r["Useskill"])
        if custom_cat == "SW1938 – Melee":
            add("spec", r["Useskill"])  # Blades / Clubs

    # zapis s hlavickou
    header = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<!--\n"
        "  SHADOW WAR 1938 - custom weapons (generated from docs/weapons/*.tsv).\n"
        "  Source book: SW1938. Custom categories \"SW1938 - ...\" for easy filtering.\n"
        "  Do not edit by hand; edit the TSV sheets and re-run build_weapons_xml.py.\n"
        "-->\n"
    )
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header + body + "\n")

    print(f"Zapsano: {OUT}")
    print(f"Zbrani: {len(weapons)} | kategorii: {len(used_cats)}")
    if skipped:
        print(f"Preskoceno (kategorie mimo mapu): {skipped}")
    # kontrola unikatnosti GUID
    ids = [guid(r["Zbraň"].strip()) for r, _, _ in weapons]
    print("GUID unikatni:", len(ids) == len(set(ids)))


if __name__ == "__main__":
    main()

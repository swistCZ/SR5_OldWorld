#!/usr/bin/env python3
"""Sestavi custom_weapons.xml pro Chummer z TSV davky (davky 1-10).

Vlastni kategorie (varianta B): zbrane se zaradi do kategorii "SW1938 - ...",
aby se v Chummeru daly filtrovat oddelene. Kazda kategorie zrcadli atributy
(type, gunneryspec, blackmarket) puvodni SR5 kategorie, aby fungovala munice.
Kazda zbran dostane explicitni <range>, protoze vlastni kategorie nejsou
v ranges.xml.

Granaty (kategorie "Gear") zustavaji kategorii "Gear" jako v SR5 - pristupuji
se pres Gear (addweapon), ne pres seznam zbrani.

Pouziti: python3 build_weapons_xml.py
"""
import csv, uuid, os
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

# Granaty: zustavaji "Gear" (jako v SR5), pristupuje se pres Gear
GRENADE_RANGE = "Standard Grenade"

# Weapontype pro settingove zbrane (jinak fallback z kategorie)
TESLA_CAT = "SW1938 – Tesla & Occult"
WEAPONTYPE_OVERRIDE = {"Geist-Werfer": "occult"}

# Doplňky na zbraně
ACCESSORY_TSV = os.path.join(HERE, "..", "accessories", "batchAC1_doplnky.tsv")
GUID_NS_ACC = uuid.uuid5(uuid.NAMESPACE_URL, "shadowwar1938-accessory")


def guid(name):
    return str(uuid.uuid5(GUID_NS, name))


def guid_acc(name):
    return str(uuid.uuid5(GUID_NS_ACC, name))


def load_accessories():
    path = os.path.normpath(ACCESSORY_TSV)
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        return [dict(zip(header, r)) for r in reader]


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
    grenades = []

    for r in rows:
        cat = r["SR5 kategorie"].strip()
        if cat == "Gear":
            grenades.append(r)
            continue
        if cat not in MAP:
            continue
        custom_cat, attrs, rng = MAP[cat]
        used_cats[custom_cat] = attrs
        weapons.append((r, custom_cat, rng))

    root = ET.Element("chummer")

    cats_el = ET.SubElement(root, "categories")
    for cat in sorted(used_cats):
        ET.SubElement(cats_el, "category", used_cats[cat]).text = cat

    weapons_el = ET.SubElement(root, "weapons")

    def add(w, tag, val):
        if val is None:
            return
        val = str(val).strip()
        if val == "":
            return
        ET.SubElement(w, tag).text = val

    # normalni zbrane
    for r, custom_cat, rng in weapons:
        name = r["Zbraň"].strip()
        w = ET.SubElement(weapons_el, "weapon")
        add(w, "id", guid(name))
        add(w, "name", name)
        add(w, "category", custom_cat)
        add(w, "type", "Melee" if custom_cat == "SW1938 – Melee" else "Ranged")
        add(w, "conceal", r["Conceal"])
        add(w, "accuracy", r["Accuracy"])
        add(w, "reach", r["Reach"] if r["Reach"].strip() else "0")
        add(w, "damage", r["DMG"])
        add(w, "ap", r["AP"])
        add(w, "mode", r["Mode"])
        add(w, "rc", r["RC"])
        add(w, "ammo", r["Ammo"])
        add(w, "avail", r["Avail"])
        add(w, "cost", r["Cost"])
        add(w, "source", SOURCE)
        add(w, "page", r["Číslo"])
        if rng:
            add(w, "range", rng)
        add(w, "useskill", r["Useskill"])
        if custom_cat == "SW1938 – Melee":
            add(w, "spec", r["Useskill"])
        if custom_cat == TESLA_CAT:
            add(w, "weapontype", WEAPONTYPE_OVERRIDE.get(name, "tesla"))

    # granaty (kategorie Gear, jako v SR5)
    for r in grenades:
        name = r["Zbraň"].strip()
        w = ET.SubElement(weapons_el, "weapon")
        add(w, "id", guid(name))
        add(w, "name", name)
        add(w, "category", "Gear")
        add(w, "type", "Ranged")
        add(w, "conceal", r["Conceal"])
        add(w, "accuracy", r["Accuracy"])
        add(w, "reach", r["Reach"] if r["Reach"].strip() else "0")
        add(w, "damage", r["DMG"])
        add(w, "ap", r["AP"])
        add(w, "mode", r["Mode"])
        add(w, "rc", r["RC"])
        add(w, "ammo", r["Ammo"])
        add(w, "avail", r["Avail"])
        add(w, "cost", r["Cost"])
        add(w, "source", SOURCE)
        add(w, "page", r["Číslo"])
        add(w, "range", GRENADE_RANGE)
        add(w, "useskill", r["Useskill"])

    # doplnky na zbrane
    accessories = load_accessories()
    accs_el = ET.SubElement(root, "accessories")
    for r in accessories:
        name = r["Doplňek"].strip()
        a = ET.SubElement(accs_el, "accessory")
        add(a, "id", guid_acc(name))
        add(a, "name", name)
        add(a, "mount", r["Mount"] if r["Mount"].strip() != "-" else "")
        add(a, "avail", r["Avail"])
        add(a, "cost", r["Cost"])
        add(a, "source", SOURCE)
        add(a, "page", r["Číslo"])
        add(a, "rating", "0")
        for col, tag in (("Accuracy", "accuracy"), ("AP", "ap"), ("Damage", "damage"),
                         ("RC", "rc"), ("Conceal", "conceal")):
            val = r[col].strip()
            if val and val != "-":
                add(a, tag, val)

    header = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        "<!--\n"
        "  SHADOW WAR 1938 - custom weapons + accessories (from docs/weapons/*.tsv).\n"
        "  Source book: SW1938. Custom categories \"SW1938 - ...\" for easy filtering.\n"
        "  Do not edit by hand; edit the TSV sheets and re-run build_weapons_xml.py.\n"
        "-->\n"
    )
    ET.indent(root, space="  ")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header + ET.tostring(root, encoding="unicode") + "\n")

    total = len(weapons) + len(grenades)
    print(f"Zapsano: {OUT}")
    print(f"Zbrani: {len(weapons)} + granatu: {len(grenades)} = {total} | kategorii: {len(used_cats)}")
    print(f"Doplnku: {len(accessories)}")
    ids = [guid(r["Zbraň"].strip()) for r, _, _ in weapons] + [guid(r["Zbraň"].strip()) for r in grenades]
    print("GUID unikatni:", len(ids) == len(set(ids)))


if __name__ == "__main__":
    main()

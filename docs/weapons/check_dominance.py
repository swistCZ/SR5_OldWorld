#!/usr/bin/env python3
"""Kontrola dominance zbrani v TSV davce.

Pravidlo: v ramci stejne SR5 kategorie nesmi jedna zbran dominovat druhe
(byt ve vsech osach stejne dobra nebo lepsi a v alespon jedne striktne lepsi).

Osy:
  vetsi = lepsi : DMG, Accuracy, RC, Ammo, Mode (versatilita palby)
  mensi = lepsi : AP (zapornejsi), Conceal, Cost, Avail
Pouziti: python3 check_dominance.py batch01_pistole.tsv
"""
import sys, re

POSITIVE = ("DMG", "Accuracy", "RC", "Ammo", "Mode", "Reach")  # vyssi = lepsi
NEGATIVE = ("AP", "Conceal", "Cost", "Avail")                  # nizsi = lepsi


def num(s):
    m = re.search(r"-?\d+(?:\.\d+)?", s or "")
    return float(m.group()) if m else None


MODE_SCORE = {
    frozenset({"SS"}): 1,
    frozenset({"SA"}): 2,
    frozenset({"SS", "SA"}): 2,
    frozenset({"BF"}): 2,
    frozenset({"SA", "BF"}): 3,
    frozenset({"BF", "FA"}): 3,
    frozenset({"FA"}): 3,
    frozenset({"SA", "BF", "FA"}): 4,
}


def mode_score(s):
    parts = frozenset(p.strip().upper() for p in (s or "").split("/") if p.strip())
    return MODE_SCORE.get(parts, 2)


def avail_score(s):
    n = num(s)
    if n is None:
        return None
    letter = (s or "").strip().upper()[-1]
    pen = {"R": 0.0, "F": 1.0}.get(letter, 0.5)  # nizsi = lepsi
    return n + pen


def value(col, raw):
    if col == "Avail":
        return avail_score(raw)
    if col == "Mode":
        return mode_score(raw)
    return num(raw)


def dominates(a, b, axes):
    """True, pokud a dominuje b (vse >= a alespon 1 >)."""
    strictly_better = False
    for col in axes:
        av, bv = value(col, a[col]), value(col, b[col])
        if av is None or bv is None:
            continue
        if col in NEGATIVE:
            av, bv = -av, -bv
        if av < bv:
            return False
        if av > bv:
            strictly_better = True
    return strictly_better


def main(path):
    lines = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    header = lines[0].split("\t")
    rows = [dict(zip(header, l.split("\t"))) for l in lines[1:]]
    axes = [c for c in POSITIVE + NEGATIVE if c in header]

    by_cat = {}
    for r in rows:
        by_cat.setdefault(r["SR5 kategorie"], []).append(r)

    problems = 0
    for cat, items in by_cat.items():
        for i, a in enumerate(items):
            for b in items[i + 1:]:
                if dominates(a, b, axes):
                    print(f"DOMINANCE: '{a['Zbraň']}' dominuje '{b['Zbraň']}' ({cat})")
                    problems += 1
                elif dominates(b, a, axes):
                    print(f"DOMINANCE: '{b['Zbraň']}' dominuje '{a['Zbraň']}' ({cat})")
                    problems += 1
    print(f"\nZkontrolovano {len(rows)} zbrani v {len(by_cat)} kategoriich. "
          f"Problemy: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "batch01_pistole.tsv"))

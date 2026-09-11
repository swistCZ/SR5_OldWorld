#!/usr/bin/env python3
"""Obecna kontrola dominance pro libovolny TSV (zbroj, vybaveni).

Pouziti:
  python3 check_dominance_generic.py <tsv> <sloupec_kategorie> <pozitivni_osy_oddelene_carkou> <negativni_osy>
Napriklad pro zbroj:
  python3 check_dominance_generic.py armor/batchA1_zbroj.tsv "SW1938 kategorie" "Armor,Kapacita" "Avail,Cost"
"""
import sys, re


def num(s):
    m = re.search(r"-?\d+(?:\.\d+)?", s or "")
    return float(m.group()) if m else None


def avail_score(s):
    n = num(s)
    if n is None:
        return None
    letter = (s or "").strip().upper()[-1]
    return n + {"R": 0.0, "F": 1.0}.get(letter, 0.5)


def value(col, raw):
    if col == "Avail":
        return avail_score(raw)
    return num(raw)


def dominates(a, b, pos, neg):
    strict = False
    for col in pos + neg:
        av, bv = value(col, a[col]), value(col, b[col])
        if av is None or bv is None:
            continue
        if col in neg:
            av, bv = -av, -bv
        if av < bv:
            return False
        if av > bv:
            strict = True
    return strict


def main(path, catcol, pos, neg):
    lines = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    header = lines[0].split("\t")
    rows = [dict(zip(header, l.split("\t"))) for l in lines[1:]]
    pos = [c for c in pos if c in header]
    neg = [c for c in neg if c in header]
    by_cat = {}
    for r in rows:
        by_cat.setdefault(r[catcol], []).append(r)
    problems = 0
    for cat, items in by_cat.items():
        for i, a in enumerate(items):
            for b in items[i + 1:]:
                if dominates(a, b, pos, neg):
                    print(f"DOMINANCE: '{a[header[1]]}' dominuje '{b[header[1]]}' ({cat})")
                    problems += 1
                elif dominates(b, a, pos, neg):
                    print(f"DOMINANCE: '{b[header[1]]}' dominuje '{a[header[1]]}' ({cat})")
                    problems += 1
    print(f"\nZkontrolovano {len(rows)} polozek v {len(by_cat)} kategoriich. Problemy: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4].split(",")))

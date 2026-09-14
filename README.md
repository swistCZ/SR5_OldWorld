# SHADOW WAR — Shadowrun Old World

Domácí hra na motivy *SHADOW WAR — Evropa na prahu druhé světové války*
(dieselpunk/teslapunk alternativní historie) postavená na pravidlech **SR5**.

Tento repozitář obsahuje:

- **vlastní datový balíček `ShadowWar 1938`** pro Chummer 5e
  (zbraně, zbroj, vybavení, kvality, vozidla, knihy a kategorie),
- zdrojové tabulky a skripty, ze kterých se XML generuje (`docs/`),
- návrhy a poznámky k vývoji (`docs/superpowers/specs/`, `docs/notes/`),
- settingový dokument `WW II - shadow setting.md`,
- konvence práce pro vývoj (`AGENTS.md`).

> Chummer samotný je cizí GPL program, proto **není v gitu**, ale je přiložený
> v [Releases](https://github.com/swistCZ/SR5_OldWorld/releases/latest).

---

## Jak začít hrát (Windows)

1. **Stáhni ZIP** z [nejnovějšího release](https://github.com/swistCZ/SR5_OldWorld/releases/latest)
   (soubor `ShadowWar1938_Chummer_v1.zip`).
2. **Rozbal ho celý** na libovolné místo (např. `C:\Chummer-SW1938\`).
   Nespouštěj Chummer přímo ze ZIPu a nepřesouvej jednotlivé soubory.
3. **Spusť** `Chummer5a\Chummer5.exe`.
   - Chummer vyžaduje **.NET Framework 4.8** (na Windows 10/11 už obvykle je).
   - Pokud chybí, Windows si řekne o instalaci.
4. **Zapni náš balíček** v Chummeru:
   - `Options` → `Character Settings` → sekce **Custom Data**
     → zaškrtni `ShadowWar 1938`.
   - Ve stejné nabídce v **Books / Sources** zaškrtni
     `Shadow War 1938 Core` (kód `SW1938`).
5. (Volitelné) V `Options` můžeš načíst hotový profil **ShadowWar**
   (uložený jako `Chummer5a\settings\ShadowWar.xml`).

Potom už jen založ postavu a v seznamech zbraní/zbroje/vybavení se objeví
položky se zdrojem `SW1938`.

---

## Co je kde

```
Chummer5a/customdata/ShadowWar 1938/   # vlastní balíček (verzovaný)
  manifest.xml          # metadata balíčku (GUID)
  custom_books.xml      # kniha SW1938
  custom_weapons.xml    # zbraně
  custom_armor.xml      # zbroj
  custom_gear.xml       # vybavení a munice
  custom_qualities.xml  # kvality
  custom_vehicles.xml   # vozidla
docs/                   # zdrojové tabulky + generovací skripty
docs/superpowers/specs/ # schválené návrhy (design)
docs/notes/             # poznámky k custom záznamům
WW II - shadow setting.md
```

## Pro vývojáře

Veškerý vlastní obsah patří do `Chummer5a/customdata/ShadowWar 1938/`,
**nikdy do oficiálního `Chummer5a/data/`**. Podrobnosti a konvence viz
[`AGENTS.md`](AGENTS.md).

Nové sekce nejdřív navrhujeme ve `docs/superpowers/specs/` a poznámky ukládáme
do `docs/notes/`. Aktuálně je navržená, zatím neimplementovaná dávka
**výbušniny a ženijní materiál** (`docs/superpowers/specs/2026-09-13-...`).

Chummer 5e je open source (GPLv3):
<https://github.com/chummer5a/chummer5a>

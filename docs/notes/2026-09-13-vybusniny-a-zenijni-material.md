# Poznámky: Výbušniny a ženijní materiál (dávka E)

- **Datum:** 2026-09-13
- **Status:** návrh schválen, čeká na implementaci
- **Spec:** `docs/superpowers/specs/2026-09-13-vybusniny-a-zenijni-material-design.md`

## Rozhodnutí

- **Munici neděláme** — běžnou munici pokrývají pravidla SR5 (výslovné přání).
- **Kategorie:**
  - běžné trhaviny/roznětky/miny → oficiální `Explosives` (kvůli mechanice trhavin),
  - nevybušný ženijní materiál → nová `SW1938 – Ženijní materiál`,
  - settingové nálože → nová `SW1938 – Tesla & okultní nálože`.
- **Pipeline:** dva nové TSV (`docs/explosives/batchE1_vybusniny.tsv`,
  `batchE2_zenijni.tsv`) + rozšíření `docs/gear/build_gear_xml.py`; jediný výstup
  `custom_gear.xml`.
- **Běžné položky (~35):** trhaviny (9), roznětky a zapalovače (10), miny a nástrahy (6),
  ženijní materiál a překážky (10).
- **Čísla jsou pracovní** — DV, AP, prahy, ceny a dostupnost si uživatel dodatečně upraví.

## Settingové nálože (7)

Kořeny hrůzy, které uživatel zvolil: **funkce vzpírající se fyzice**, **původ z ostatků
a smrti**, **neznámo (něco se otevře/přivolá)** a **tělesná hrůza**. Psychická hrůza
(paměť, jména) záměrně vynechána. Vyhýbáme se re-skinům běžných udělátek — hrůza musí
plynout z vlastní mechaniky nálože.

1. **Der Magnet** — magnetický puls trhá kov z okolí i z těl.
2. **Dušezmar (Seelenbrand)** — studený oheň vysává život, zůstává mrtvá zóna.
3. **Hohlraumladung (Dutá nálož)** — prostor se zhroutí do sebe, hmota slisovaná.
4. **Lichtfresser (Požírač světla)** — koule pohlcující světlo a teplo, slepota a chlad.
5. **Das Netz (Síť)** — vlákna srostlá s masem, area denial.
6. **Der Schlund (Chřtán)** — zem se otevře, pohltí a zavře bez stopy; nalezený artefakt.
7. **Beinladung (Kostěná nálož)** — kostní prach z hromadného hrobu; kosti rostou
   okamžitě, obchází zbroj; použití je válečný zločin.

## Otevřené body

- Přesné hodnoty (DV, AP, prahy, trvání), ceny a dostupnost.
- Názvy: pracovně mix češtiny a dobové němčiny; sjednotit, až bude obsah hotový.
- Ověření v Chummeru (Windows): zobrazení trhavin, DV, kategorií a zdroje `SW1938`.
- Po dokončení vytvořit release `v2` s přepočítaným ZIPem.

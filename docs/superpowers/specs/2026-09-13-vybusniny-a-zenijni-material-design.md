# Design: Výbušniny a ženijní materiál (dávka E) — SHADOW WAR 1938

- **Datum:** 2026-09-13
- **Status:** ke schválení (spec)
- **Zdroj knihy:** `SW1938`
- **Navazující dokumenty:** `docs/explosives/vybusniny_pravidla.md`, `docs/gear/build_gear_xml.py`

## 1. Cíl

Doplnit do custom balíčku `ShadowWar 1938` dobové výbušniny, roznětky, miny a ženijní
materiál a k tomu sadu temných settingových (tesla/okultních) náloží. Držíme pravidlo
settingu: **běžné = realistický rok 1938, vzácné = fantastické a nedokonalé.**

## 2. Rozsah

**V rozsahu:**
- běžné trhaviny, roznětky a zapalovače, miny a nástrahy,
- nevybušný ženijní materiál a překážky,
- 7 settingových náloží (níže),
- rozšíření generátoru `custom_gear.xml`,
- dokument pravidel.

**Mimo rozsah:**
- běžná munice (pokrývají ji SR5 pravidla — výslovné přání),
- kouzla, metatypy, dovednosti a magie obecně (používáme základ SR5),
- automatizace speciálních efektů v Chummeru (řeší GM).

## 3. Struktura a pipeline

- `docs/explosives/batchE1_vybusniny.tsv` — trhaviny, roznětky, miny.
- `docs/explosives/batchE2_zenijni.tsv` — nevybušný ženijní materiál a překážky.
- `docs/explosives/vybusniny_pravidla.md` — efekty, SR5 Demolitions, blast, nastražení,
  bezpečnost, settingové nálože, poznámka o citlivém obsahu.
- `docs/gear/build_gear_xml.py` — rozšířit o čtení obou TSV; zůstává **jediný generátor**
  `custom_gear.xml` (negenerujeme nový XML soubor).
- `Chummer5a/customdata/ShadowWar 1938/custom_gear.xml` — regenerovaný výstup.

Každý záznam dostane deterministický GUID (`uuid5`) a `source = SW1938` jako dosud.

## 4. Kategorie v Chummeru

- Běžné trhaviny, roznětky, miny → **oficiální `Explosives`** (blackmarket `Weapons`),
  aby seděla mechanika trhavin (Demolitions, DV, `weight`, `minrating`, `ratinglabel`).
- Nevybušný ženijní materiál → nová **`SW1938 – Ženijní materiál`**.
- Settingové nálože → nová **`SW1938 – Tesla & okultní nálože`**.

Filtrování podle zdroje `SW1938` funguje i u oficiální kategorie.

## 5. Obsah

### 5.1 Běžné položky (~35)
- **Trhaviny (9):** střelný prach, dynamit, gelignit/trhací želatina, TNT, amatol,
  ekrazit, ledek (AN), nitroglycerin, trhací nálož.
- **Roznětky a zapalovače (10):** elektrická a zápalná rozbuška, zápalnice, detonační
  šňůra, mechanický časový zapalovač, chemický zpožďovač, odtrhový spínač, tlakový
  spínač, tripwire past, elektrický odpalovač, baterie.
- **Miny a nástrahy (6):** protitanková (Tellermine 35), protipěchotní (S-mine 35),
  lehká dřevěná, nášlapná, nástražná, těžká protitanková.
- **Ženijní materiál a překážky (10):** ostnatý drát, čeští ježci, kolejnicové zátarasy,
  betonové bloky, Bangalore torpedo, pytle s pískem, demoliční nářadí, trhací klíny,
  detektor min, odminovací/demoliční sada.

**Duplicity:** `Satchel Charge`, `Sticky Bomb` a granáty už v datech jsou (batch09) —
nepřidáváme znovu.

### 5.2 Settingové nálože (7)

Společný rámec: `Rating` (1–6) = síla; poloměr = `Rating` m, pokud není řečeno jinak;
obrana `Body + Armor` (s AP), pokud není řečeno jinak; nastražení/odpálení `Demolitions`.

1. **Der Magnet (Magnetická mina)** — *DE/SU.* Protitanková; po výbuchu vytvoří
   magnetický puls v poloměru `Rating` m. Kov, šrapnely i úlomky v tělech jsou trhány
   ke středu. Kdo má v těle kov (šrapnely, destičky, implantáty), utrpí `Rating`P,
   AP −2, a zbroj z nemagnetického materiálu nechrání; vozidla a kovové konstrukce
   v oblasti jsou vyřazeny. Ranění s kovem v sobě jsou doslova roztrháni.
2. **Dušezmar (Seelenbrand)** — *DE/SU.* Studený oheň v poloměru `Rating` m,
   `Rating`P (chlad/nekrotická energie), AP −2. Nezanechá popáleniny, ale vysátá,
   zmrzlá těla. Na `Rating` hodin zůstane „mrtvá zóna", kde nefunguje teplo ani
   magie (GM).
3. **Hohlraumladung (Dutá nálož)** — *CS.* Sféra `Rating/2` m; vše uvnitř se rozdrtí do
   středu. **DV** `(Rating+2)P`, **AP** −4; kryt nepomáhá. Bez zvuku, záblesku a kouře;
   proti bariérám jako dvojnásobná nálož. Zůstane slisovaná hmota, těla neidentifikovatelná.
4. **Lichtfresser (Požírač světla)** — *DE.* Koule `Rating` m na `Rating` kol. Pohltí
   nemagické světlo a teplo (svítilny, oheň, IR/termovize uvnitř nefungují); zrakem
   orientované akce nemožné (−6, pokud má cíl jiný smysl). **Chlad** `Rating/2`S za kolo,
   AP −2. Magické světlo jen pokud překoná nálož (GM). Astrál neovlivňuje. Odlišeno od
   Dušezmaru: ten bere život, tento světlo a smysly.
5. **Das Netz (Síť)** — *FR.* Oblak lepkavých vláken `Rating` m. Obrana
   `Reaction + Body` proti prahu `Rating × 2`; neúspěch = přilepen (nehybný, −4 na akce).
   Vytržení = Extended `Strength`, práh `Rating × 3`, každý pokus 2P (trhání tkáně);
   řezání pomůže, ale poškodí i předměty. Předměty a vozidla pevně spojí; po `Rating`
   hodinách vlákno zkřehne. Astrál neovlivňuje.
6. **Der Schlund (Chřtán)** — *neznámý původ, nalezený.* Během 1 kola se v okruhu
   `Rating` m otevře propast hluboká `Rating × 2` m. Obrana `Reaction` proti prahu
   `Rating × 2`, jinak pád dovnitř. Na konci **příštího** kola se zavře: uvnitř
   `Rating × 2`P bez ohledu na zbroj (drcení/pohřbení). Po zavření hladký povrch,
   žádný kráter, sutiny ani těla — jen tenká jizva. Záchrana lanem jen do 1 kola.
   Z pod země je občas slyšet klepání. Astrální cestou se dovnitř nedostaneš.
7. **Beinladung (Kostěná nálož)** — *DE.* Vyrobena z kostí a zubů z hromadného hrobu
   (rituál, vyžaduje ostatky). Oblak prachu `Rating` m; obrana `Body + Willpower`
   (zbroj nepomůže — působí zevnitř). Neúspěch: kosti začnou **okamžitě** růst —
   **DV** `Rating`P, **AP 0**, ignoruje zbroj; navíc −2 na fyzické akce a 1P na konci
   každého kola, dokud zásah neoperuje lékař (`First Aid`/`Surgery`, práh `Rating × 2`);
   magie léčí normálně. Mrtvé tělo je zevnitř roztrhané kostěnými výrůstky. Na stroje
   neúčinkuje. Použití je zvrhlost a válečný zločin.

**Poznámka:** konkrétní čísla (DV, AP, práhy, ceny, dostupnost) jsou pracovní a uživatel
si je může dodatečně upravit.

## 6. Modelace v Chummeru

Podle oficiálního vzoru SR5/RG:
- `<rating>` (max síla/DV), `<minrating>`, `<weight>` (kg na rating), `<ratinglabel>`
  u délkových položek (např. zápalnice v metrech),
- `<cost>` (`Rating * X`) nebo pevná cena, `<avail>`, `<source>SW1938`, `<page>`,
- roznětky rating 0 s pevnou cenou.

Chummer automaticky neumí speciální efekty — jsou v `vybusniny_pravidla.md` a řeší je GM.

## 7. Verifikace

- XML je dobře formované, GUID unikátní (kontrola ve skriptu jako u zbraní).
- Manuální test v Chummeru (Windows): položky se objeví, trhaviny ukazují DV, kategorie
  a zdroj `SW1938` sedí.
- Znovu spuštění generátoru je idempotentní (stejné GUID).

## 8. Release

Po dokončení a ověření vytvořit release `v2` s přepočítaným ZIPem (stejný postup jako `v1`).

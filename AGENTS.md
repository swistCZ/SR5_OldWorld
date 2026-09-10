# AGENTS.md — SHADOW WAR / Shadowrun Old World

Tento soubor definuje, jak mám (asistent) pracovat v tomto projektu. Řídím se jím v každé relaci.
Cíl projektu: **upravit Chummer 5a tak, aby sloužil jako nástroj pro správu postav v domácí hře**
založené na settingu *SHADOW WAR — Evropa na prahu druhé světové války* (soubor `WW II - shadow setting.md`).

---

## 1. Účel a role

- Jsem asistent pro **konzistentní a bezpečné přizpůsobování Chummeru** pro náš domácí setting.
- **NEUPRAVUJI oficiální data Chummeru** (`Chummer5a/data/*`). Veškerý náš obsah jde do
  **vlastního custom balíčku** v `Chummer5a/customdata/ShadowWar 1938/`. To umožňuje:
  - snadnou aktivaci/vypnutí,
  - přenositelnost mezi instalacemi,
  - čistou historii v gitu,
  - vždy obnovitelnou oficiální verzi.
- Budu postupovat **postupně, po sekcích** (zbraně, zbroj, vybavení, kvality, metatypy, …),
  vždy po domluvě s uživatelem.

---

## 2. Jak se mám chovat

### Obecné zásady
- **Konzistence:** Každý nový záznam musí zapadat do stávající struktury Chummeru i do předchozí
  naší práce. Držím se schématu XML dat (viz oddíl 4).
- **Plán před změnou:** U každé větší sekce nejdřív navrhnu plán/rozsah a počkám na schválení.
  Neprovádím rozsáhlé změny naslepo.
- **Mluvím s uživatelem:** Při nejasnostech se ptám (jednu otázku po druhé). Neodhaduji zásadní
  rozhodnutí bez vědomí uživatele.
- **Verifikace:** Po každé změně ověřím, že je soubor validní (dobře formovaný XML, správné tagy)
  a že záznamy odpovídají pravidlům SR5.
- **Historická věrnost settingu:** Hodnoty (ceny, dostupnost, poškození) navrhuji s ohledem na
  reálné zbraně/vybavení roku 1938 i na základní pravidlo settingu:
  *„čím běžnější, tím realističtější; čím vzácnější, tím fantastičtější“*.

### Co dělám / nedělám
- ✅ Přidávám a upravuji **custom** zbraně, zbroj, vybavení, kvality, metatypy a další.
- ✅ Používám **superpowers** (brainstorming, writing-plans, TDD, systematic-debugging, atd.).
- ❌ Neměním oficiální `data/*.xml` ani binárky Chummeru.
- ❌ Nezavádím obskurní hodnoty, které odporují pravidlům SR5 bez výslovného souhlasu.
- ❌ Neupravuji `Chummer5.exe` ani jiné binárky.

---

## 3. Struktura projektu

```
Shadowrun_Old_World/
├── AGENTS.md                       # tento soubor (konvence práce)
├── WW II - shadow setting.md       # zdrojový setting (historie, mocnosti, pravidla)
├── docs/superpowers/specs/         # designové dokumenty (z brainstormingu)
├── docs/notes/                     # poznámky o našich custom záznamech (volitelné)
└── Chummer5a/
    ├── Chummer5.exe                # aplikace (Windows, nespouštím já)
    ├── data/                       # OFICIÁLNÍ data — NEEDITOVAT (mimo git)
    └── customdata/
        └── ShadowWar 1938/         # NÁŠ custom balíček (verzovaný v gitu)
            ├── manifest.xml
            ├── custom_books.xml
            ├── custom_weapons.xml
            ├── custom_armor.xml
            ├── custom_gear.xml
            └── ... (další podle potřeby)
```

---

## 4. Datové schéma Chummeru (SR5) — konvence pro nové záznamy

Zdroje struktury: `Chummer5a/data/` + vzorové balíčky v `customdata/`.

### Společné prvky každého záznamu
- `id` — **unikátní GUID** (nový pro každý záznam; nikdy neduplikovat).
- `source` — kód knihy z našeho `custom_books.xml` (např. `SW1938`), nikdy SR5 apod.
- `page` — číslo „stránky" našeho vlastního katalogu (řídím číslováním).
- `name` — anglický identifikátor; český popis dle potřeby v poznámkách.
- `category` — musí odpovídat existující nebo nově definované kategorii.

### Zbraň (`weapon`)
- `type` = `Ranged` | `Melee`
- `conceal`, `accuracy`, `reach`, `damage` (např. `8P`, `({STR}+2)S`), `ap`, `mode`
  (SA/SS/BF/FA/0), `rc`, `ammo` (např. `8(c)`, `30(c)`)
- `avail` (může být vzorec, např. `(Rating*2)+2F`), `cost` (číslo nebo `Variable(x-y)`)
- volitelně `useskill`, `weapontype`, `range`, `sizecategory`, `spec`,
  `accessorymounts`/`mount`, `accessories`/`accessory`, `required`/`forbidden`/`oneof`

### Zbroj (`armor`)
- `armor` (hodnota zbroje), `armorcapacity`, `avail`, `cost`
- volitelně `gears`/`usegear`, `bonus`, `addmodcategory`, `mods`, `required`

### Vybavení (`gear`)
- `rating` (0 = bez ratingu), `avail`, `cost` (+ `costfor` pro balení), `category`
- munice: `weaponbonus` (`<ap>`, `<damage>`), `ammoforweapontype` (gun/bow/…)
- vzorce ceny: `(Rating*30)`, `Variable(20-100000)`
- volitelně `hide`, `gears`/`usegear` (přibalené vybavení)

### Knihy (`books`)
- `id` (GUID), `name`, `code` (kód používaný v `source`).

---

## 5. Konzistentní proces přidávání/úprav obsahu

Při každém požadavku na nový obsah postupuji podle superpowers:
brainstorming → spec → writing-plans → (TDD, kde to dává smysl) → implementace → verifikace.

### Pracovní postup (krok za krokem)
1. **Ujasnění rozsahu** (brainstorming): zjistím, co přesně chci přidat/upravit, k čemu to slouží,
   jaké hodnoty, do jaké sekce.
2. **Návrh** (spec/design): představím návrh hodnot a struktury záznamu(ů) a nechám si ho schválit.
3. **Implementace**: zapíšu záznamy do odpovídajících `custom_*.xml` v našem balíčku
   `ShadowWar 1938/` (ne do `data/`).
4. **Verifikace**: ověřím dobře formovanost XML a shodu se schématem (validátorem/ručně).
5. **Commit**: zazálohuji do gitu s jasnou zprávou (pouze pokud uživatel požádá o commit).

### Konvence pojmenování souborů v balíčku
- `manifest.xml` — metadata balíčku (unikátní GUID, autoři, popis).
- `custom_books.xml` — naše knihy (zdroj `SW1938`).
- `custom_weapons.xml`, `custom_armor.xml`, `custom_gear.xml`, `custom_qualities.xml`,
  `custom_metatypes.xml`, `custom_skills.xml`, `custom_vehicles.xml`, … — podle typu obsahu.

### Aktivace v Chummeru
- Po uložení custom dat je v Chummeru (Options → Character Settings) potřeba:
  1. zapnout náš custom balíček **ShadowWar 1938**,
  2. aktivovat naši knihu/kódy (např. `SW1938`) v seznamu povolených zdrojů.
- Tento krok provádí uživatel ve Windows (Chummer nespouštím já).

---

## 6. Používání superpowers

- **brainstorming** — vždy před návrhem nové sekce/obsahu (design, hodnoty, rozsah).
- **writing-plans** — u vícekrokových úprav (nové sekce, větší dávky záznamů).
- **test-driven-development / verification-before-completion** — u skriptů/validace
  (např. ověřovací skript pro XML).
- **systematic-debugging** — pokud Chummer načte špatně data (špatně formátované XML apod.).
- **dispatching-parallel-agents** — u větších nezávislých bloků (např. najednou zbraně + zbroj).
- **finishing-a-development-branch / receiving-code-review** — u dokončení větších změn.

---

## 7. Nejdůležitější pravidla (zkráceně)

1. Veškerý náš obsah → `Chummer5a/customdata/ShadowWar 1938/`, nikdy do `data/`.
2. Každý záznam má **unikátní GUID** a `source` = náš kód knihy.
3. Respektuji schéma Chummeru a pravidla SR5.
4. Nejdřív návrh, pak schválení uživatelem, pak implementace.
5. Verzuji v gitu jen naši vlastní práci.
6. Při nejistotě se ptám uživatele.
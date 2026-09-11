# Doplňky na zbraně SHADOW WAR — efekty a pravidla

Tento dokument vysvětluje **mechanické efekty** doplňků na zbraně (dávka AC1,
`docs/accessories/batchAC1_doplnky.tsv`). Běžné doplňky (mířidla, pažby, zásobníky)
mají efekt přímo ve sloupci „Efekt"; zde jsou podrobně rozebrány **settingové
(okultní/teslapunk) a speciální** doplňky, jejichž působení chce jasná pravidla.

Základní konvence: `+RC` = zpětná kompenzace, `+Acc` = přesnost, `-Conceal` =
lépe skryté, `±DMG` = úprava poškození, `±AP` = průraznost.

---

## Okultní a teslapunkové doplňky

> **Poznámka k astrálnímu prostoru.** Podle SR5 jsou meatworld a astrál oddělené:
> bytost v astrálu nemůže působit na fyzické věci a fyzická věc nemůže působit
> na astrální entity. Proto jsme **odstranili** dřívější nápady na „astrální
> zaměřovač" (fyzický přístroj vidící astrál), „okultní rytiny" (fyzická zbraň
> zasahující nehmotné entity) a „stříbrné vložky" proti nadpřirozeným bytostem.
> Fyzické zbraně působí jen na **materializované** entity. Toto oddělení zůstává
> zachováno.

---

### 71. Elektroizolační obal (Setting)
**Co to je.** Obal z izolačního materiálu (guma, bakelit, tkanina) chránící
zbraň a střelce před elektrickým výbojem.

**Efekt.**
- Chrání **střelce i zbraň** před elektrickým výbojem — zejména při **glitchi
  tesla zbraně** (kdy se výboj vrací do střelce) **snižuje poškození na polovinu**.
- **+2 kostky** na odolání elektrickému poškození z vlastní zbraně.

**Nedostatky.** Bez efektu proti běžným zbraním. Vzácný (`10F`, 800).

---

### 72. Měděná cívka (Setting)
**Co to je.** Přídavná měděná cívka zesilující tesla zbraně.

**Efekt.**
- **+1 DMG** nebo **+1 výboj** (delší výdrž) u tesla zbraní — volí se při instalaci.
- **Riziko:** při glitchi je šance na přetížení (zbraň se vybije do střelce)
  **zvýšena** — GM hodí navíc.

**Nedostatky.** Funguje jen na tesla zbraně; vzácná (`14F`, 2 500).

---

### 48. Infračervený konvertor / 57. Infračervená svítilna (Setting)
**Co to je.** Rané experimentální IR přístroje (v roce 1938 skutečně existovaly
prototypy).

**Efekt.**
- **Konvertor:** střelec vidí v temnotě (jako termovize) — **ruší postihy za tmu**.
- **Svítilna:** osvětluje cíl v IR spektru; viditelné **pouze přes IR přístroj**,
  takže nepřítel bez IR techniky nic nevidí.
- Kombinace dává tichý noční průzkum/útok.

**Nedostatky.** Velmi vzácné (`10F`/`12F`), energeticky náročné, křehké.

---

## Speciální (ne-settingové) doplňky

### 3. Tlumič plamene / 4. Tlumič
- **Tlumič plamene:** -2 na odhalení střelby **zrakem** (potlačuje záblesk).
- **Tlumič (zvukový):** -4 na odhalení střelby **sluchem**. Vzácný (`9F`).

### 5. Dlouhá / 6. Zkrácená hlaveň
- **Dlouhá:** +1 Acc, ale +1 Conceal (hůř skrytá).
- **Zkrácená:** -1 DMG, ale -1 Conceal (lépe skrytá).

### 16. Dvojnožka / 17. Stativ
- **Dvojnožka:** +2 RC, jen když je zbraň v poloze (ležící/na podložce).
- **Stativ:** +6 RC, jen když je nasazený (těžké zbraně).

### 25. Odstranění pažby
- -1 RC, ale -2 Conceal (výrazně lépe skrytá) — „sawed-off" efekt.

### 30. Lapač nábojnic
- -2 na forenzní sledování zbraně (nezanechává nábojnice).

### 34. Prodloužený / 35. Bubnový zásobník
- **Prodloužený:** +50 % kapacity, +1 Conceal.
- **Bubnový:** výrazně +kapacita, +2 Conceal (objemný).

### 40. Rychlotažné pouzdro
- Tasení zbraně jako **volná akce**.

### 61. Selektivní spoušť
- Přidá režim **selektivní palby** (SA/BF/FA) zbrani, která ho nemá. Vzácná (`8F`).

### 70. Ghillie omotávka
- -2 Conceal (výrazně lepší skrytí v terénu).

---

## Poznámka pro Chummer

- Efekty ve sloupci „Efekt" odpovídají hodnotám v TSV.
- Chummer umí přímo modelovat `rc`, `accuracy`, `conceal`, `damage`, `ap`, `mount`.
- **Speciální efekty** (vidění v IR, zásah nehmotných entit, stříbro, ochrana před
  výbojem, zesílení tesla) Chummer automaticky neumí — jsou v poznámkách a v tomto
  dokumentu; ve hře je řeší GM.
- Zdroj: `SW1938`.

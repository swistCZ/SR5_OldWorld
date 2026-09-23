# Jednotný katalog SW1938

`shadowwar1938_catalog.tsv` je jednotný export herních položek ze zdrojových TSV v `docs/`.
Je určený pro import do Google Sheets.

## Aktualizace katalogu

Z kořene repozitáře spusť:

```bash
python3 docs/catalog/build_catalog.py
```

Skript načítá pouze katalogová data:

- zbraně,
- doplňky ke zbraním,
- zbroje,
- vybavení,
- kvality,
- vozidla.

Python skripty, XML, Markdown pravidla a ostatní pomocné soubory se do exportu nezařazují.

U kvalit se více bonusových řádků sloučí do jednoho řádku položky ve sloupci `Bonus`.
Sloupce, které pro daný typ položky nedávají smysl, zůstávají prázdné. Sloupce
`Zdrojový soubor` a `Zdrojový řádek` umožňují dohledat původ každé položky.

Výstupní soubor používá UTF-8 a tabulátor jako oddělovač, takže ho lze přímo
importovat do Google Sheets.

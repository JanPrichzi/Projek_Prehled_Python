# Přehled zpráv, důvěry a kurzů

Python projekt, který na jednom místě propojuje aktuální mediální sentiment, makroekonomickou důvěru a kurzový vývoj koruny. Výstup zobrazuje jak v konzoli, tak formou interaktivního HTML přehledu v notebookovém prostředí (Google Colab).

## Hlavní funkce

* **Analýza sentimentu zpráv (ČT24):** Stahuje 10 nejnovějších hlavních zpráv z RSS ČT24 a hodnotí titulky podle váženého slovníku celých slov a sousloví (váhy `-1` až `+1`, skóre jednotlivého článku je omezeno na interval `[-1, +1]`).
* **Ekonomická důvěra (ČSÚ):** Připojuje se k API Českého statistického úřadu (formát JSON-stat) a načítá nejnovější hodnotu *Souhrnného indikátoru důvěry*.
* **Analýza kurzů (ČNB):** Stahuje denní i historické kurzy všech měn z ČNB, počítá 90denní klouzavý průměr (MA90), procentuální odchylku a vyhodnocuje výhodnost pro exportéry a importéry.
* **Interaktivní přehled:** Vykresluje přehlednou kartu s rozklikávacím detailem hodnocených článků a přepínačem všech měn ČNB.

## Struktura projektu

| Soubor | Popis |
| :--- | :--- |
| `main.py` | Hlavní spouštěcí skript propojující všechny moduly a závěrečné vyhodnocení dne. |
| `sentiment.py` | Načítání slovníku z CSV (se zálohou na výchozí slovník), hledání celých slov přes `re` a skórování titulků. |
| `zpravy.py` | Stažení RSS zpráv z ČT24 a jejich ohodnocení. |
| `csu.py` | Komunikace s API ČSÚ a extrakce nejnovějšího Souhrnného indikátoru důvěry. |
| `kurzy_cnb.py` | Stažení denních a ročních kurzů ČNB, výpočet 90denního průměru a odchylky. |
| `prehled_html.py` | Vygenerování a vykreslení interaktivního HTML/JS přehledu přes `IPython.display`. |
| `slova.csv` | Tabulka klíčových slov rozdělených do sloupců podle vah (oddělovač `;`). |
| `requirements.txt` | Seznam potřebných Python knihoven. |

## Ověřené verze prostředí

Skript byl otestován a ověřen v následujícím prostředí (Google Colab):

| Prostředí / Knihovna | Verze | Poznámka |
| :--- | :--- | :--- |
| **Python** | `3.13.18` | Jazykové prostředí |
| **feedparser** | `6.0.14` | Externí knihovna, pro stahování RSS zpráv z ČT24 |
| **requests** | `2.32.4` | Externí knihovna, pro komunikaci s API  |
| **pandas** | `2.2.3` | Externí knihovna, pro práci s tabulkami (filtrování, hledání řádků) |
| **pyjstat** | `2.4.0` | Externí knihovna, pro rozluštění složitého statistického formátu JSON-stat od ČSÚ |
| **IPython** | `7.34.0` | Součást Colabu / Jupyteru, pro vykreslení interaktivního HTML v notebooku |
| **re** | `2.2.1` | Standardní modul Pythonu, pro hledání celých samostatných slov (nebo sousloví) |
| **json** | `2.0.9` | Standardní modul Pythonu, který umožňuje vašemu kódu analyzovat a serializovat data JSON (JavaScript Object Notation). |

## Spuštění v Google Colabu

Otevřete nový notebook na [colab.research.google.com](https://colab.research.google.com), vložte do buňky následující kód a spusťte jej:

```python
%cd /content
!rm -rf Projek_Prehled_Python
!git clone https://github.com/JanPrichzi/Projek_Prehled_Python.git
%cd Projek_Prehled_Python
!pip install -q -r requirements.txt
%run main.py
```

Po spuštění se v konzoli vypíše načtený slovník, jednotlivé zprávy i souhrnné statistiky a pod buňkou se vykreslí tlačítko **▶ Spustit přehled** s interaktivní kartou.

## Lokální spuštění

```bash
git clone https://github.com/JanPrichzi/Projek_Prehled_Python.git
cd Projek_Prehled_Python
pip install -r requirements.txt
python main.py
```

> **Poznámka:** Při spuštění v běžném terminálu se vypíše kompletní textová analýza do konzole. Pro zobrazení interaktivní HTML karty je potřeba skript spustit v Jupyter Notebooku nebo Google Colabu.

## Úprava slovníku (`slova.csv`)

Slovník je uložen v souboru `slova.csv` s oddělovačem středník (`;`). První řádek tvoří číselné váhy sloupců (např. `-1`, `-0,5`, `-0,25`, `0`, `0,25`, `0,5`, `1`) a pod nimi jsou vypsána konkrétní slova nebo sousloví. Sloupce s váhou `0` nebo nečíselným názvem skript automaticky ignoruje.

## Zdroje dat

* **Zprávy:** [ČT24 – Hlavní zprávy (RSS)](https://ct24.ceskatelevize.cz/rss/hlavni-zpravy)
* **Důvěra:** [ČSÚ – Konjunkturální průzkumy (API)](https://csu.gov.cz/konjunkturalni-pruzkumy)
* **Kurzy:** [ČNB – Kurzy devizového trhu](https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/)

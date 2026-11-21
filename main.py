import re
import sys
import json
import feedparser
import requests
import pandas as pd
from pyjstat import pyjstat

from sentiment import nacti_slovnik_z_csv, vypis_slovnik_do_konzole
from zpravy import stahni_zpravy
from csu import ziskej_indikator_duvery_csu_presne
from kurzy_cnb import nacti_kurzy_vsechny_meny_cnb
from prehled_html import vykresli_html_prehled

# ==========================================
# NASTAVENÍ PROJEKTU (VŠE NA JEDNOM MÍSTĚ)
# ==========================================
CSV_SLOVA_ZDROJ = "https://raw.githubusercontent.com/JanPrichzi/Projek_Prehled_Python/main/slova.csv"
ZAKLADNI_SKORE = 2.0  # Korekce negativity zpráv – mění se pouze zde

# Výpis aktuálních verzí Pythonu a knihoven
print("VERZE KNIHOVEN:")
print("-" * 60)
print(f"Python:     {sys.version.split()[0]}")
print(f"feedparser: {getattr(feedparser, '__version__', 'není dostupná')}")
print(f"requests:   {requests.__version__}")
print(f"pandas:     {pd.__version__}")
print(f"pyjstat:    {getattr(pyjstat, '__version__', 'není dostupná')}")
print(f"re:         {getattr(re, '__version__', 'vestavěný modul')}")
print(f"json:       {getattr(json, '__version__', 'vestavěný modul')}")
print("-" * 60 + "\n")

print("=== ANALÝZA NÁLADY VE SPOLEČNOSTI A KURZU ===\n")

# Načtení slovníku z CSV (raw odkaz na GitHubu)
SLOVNIK_SENTIMENTU = nacti_slovnik_z_csv(CSV_SLOVA_ZDROJ, oddelovac=";")
vypis_slovnik_do_konzole(SLOVNIK_SENTIMENTU)

# A) Zpracování zpráv
skore_dne, detaily_zprav = stahni_zpravy(
    vrat_detaily=True,
    slovnik_podle_vahy=SLOVNIK_SENTIMENTU,
    zakladni_skore=ZAKLADNI_SKORE,
)
print(f"\nCELKOVÉ SKÓRE ZPRÁV: {skore_dne:g}")

# B) Získání dat z ČSÚ
index_csu, obdobi_csu = ziskej_indikator_duvery_csu_presne(vrat_obdobi=True)

# C) Kurz ČNB a odchylka od 90denního klouzavého průměru (všechny měny pro interaktivní přehled)
try:
    vsechny_kurzy_cnb = nacti_kurzy_vsechny_meny_cnb(okno_dni=90, neutralni_pasmo_pct=0.5)
except Exception as e:
    print(f"Chyba při načítání kurzů ČNB: {e}")
    vsechny_kurzy_cnb = {}

kurz_info = vsechny_kurzy_cnb.get("EUR")

if kurz_info is not None:
    print(
        f"KURZ {kurz_info['kod']}/CZK ({kurz_info['datum']}): "
        f"{kurz_info['aktualni_kurz']:.3f} Kč | "
        f"MA90: {kurz_info['ma90']:.3f} Kč | "
        f"Odchylka: {kurz_info['odchylka_pct']:+.2f} %"
    )
    print(f"STAV KURZU: {kurz_info['souhrn']}")

if index_csu is not None:
    obdobi_text = f" ({obdobi_csu})" if obdobi_csu else ""
    print(f"SOUHRNNÝ INDIKÁTOR DŮVĚRY (ČSÚ){obdobi_text}: {index_csu} %")

    # D) Finální vyhodnocení (zkombinování zdrojů)
    print("\nZÁVĚREČNÉ VYHODNOCENÍ DNE:")
    print("-" * 60)

    if skore_dne < 0 and index_csu < 100:
        print("Těžký den. Zprávy jsou negativní a ekonomická důvěra lidí je podprůměrná.")
    elif skore_dne >= 0 and index_csu >= 100:
        print("Skvělý den! Pozitivní zprávy a vysoká důvěra ve společnosti.")
    else:
        print("Smíšený den. Společenská nálada a zprávy v médiích se rozcházejí.")
else:
    print("\nNepodařilo se spojit s API ČSÚ.")

# Vykreslení interaktivního HTML přehledu
vykresli_html_prehled(
    skore_zprav=skore_dne,
    detaily_clanku=detaily_zprav,
    index_duvery=index_csu,
    obdobi_duvery=obdobi_csu,
    kurzy_dict=vsechny_kurzy_cnb,
    vychozi_mena="EUR",
    zakladni_skore=ZAKLADNI_SKORE,
)

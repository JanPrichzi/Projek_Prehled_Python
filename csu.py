import pandas as pd
import requests
from pyjstat import pyjstat


def ziskej_indikator_duvery_csu_presne(vrat_obdobi=False):
    """
    Připojí se na API ČSÚ, získá data ve formátu JSON-stat,
    převede je na přehlednou tabulku a vyfiltruje přesně náš ukazatel za poslední měsíc.
    """
    url = "https://data.csu.gov.cz/api/dotaz/v1/data/vybery/KPR1T1"
    hlavicky = {"Accept": "application/json"}  # Říkáme serveru, že chceme čistá data (JSON)

    try:
        odpoved = requests.get(url, headers=hlavicky, timeout=15)
        if odpoved.status_code == 200:  # 200 = úspěšné připojení
            dataset = pyjstat.Dataset.read(odpoved.text)
            df = dataset.write('dataframe')

            # Najdeme řádky, které PŘESNĚ odpovídají našemu ukazateli, a zahodíme prázdné hodnoty
            maska = df.isin(['Souhrnný indikátor']).any(axis=1)
            nase_data = df[maska].dropna(subset=['value'])

            if not nase_data.empty:
                print("🔍 KONTROLNÍ VÝPIS Z PANDAS (prvních 5 záznamů - ty nejnovější!):")
                print("-" * 60)
                sloupce_k_vypisu = [
                    col for col in nase_data.columns
                    if any(k in col.lower() for k in ['value', 'čas', 'cas', 'rok', 'měsíc', 'mesic'])
                ]

                if sloupce_k_vypisu:
                    print(nase_data[sloupce_k_vypisu].head(5))
                else:
                    print(nase_data.head(5))
                print("-" * 60)

                nejnovejsi_hodnota = round(float(nase_data['value'].iloc[0]), 1)

                # Bezpečně zjistíme nejnovější období (např. "říjen 2026")
                obdobi_hodnota = ""
                casove_sloupce = [
                    col for col in nase_data.columns
                    if any(k in col.lower() for k in ['měsíc', 'mesic', 'čas', 'cas', 'období', 'obdobi'])
                ]
                if casove_sloupce:
                    hodnota_obdobi = nase_data[casove_sloupce[0]].iloc[0]
                    if pd.notna(hodnota_obdobi):
                        obdobi_hodnota = str(hodnota_obdobi).strip()

                if vrat_obdobi:
                    return nejnovejsi_hodnota, obdobi_hodnota
                return nejnovejsi_hodnota
            else:
                print("Přesný název 'Souhrnný indikátor' nebyl nalezen.")
                return (None, "") if vrat_obdobi else None
        else:
            print(f"API ČSÚ hlásí chybu: {odpoved.status_code}")
            return (None, "") if vrat_obdobi else None

    except Exception as e:
        print(f"Chyba při zpracování: {e}")
        return (None, "") if vrat_obdobi else None

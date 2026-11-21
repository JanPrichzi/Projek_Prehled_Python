import requests


def nacti_kurzy_vsechny_meny_cnb(okno_dni=90, neutralni_pasmo_pct=0.5):
    """
    Stáhne aktuální denní kurzy všech měn z ČNB a spočítá jejich
    90denní klouzavý průměr a procentuální odchylku.
    Vrací slovník {kod_meny: {...}}.
    """
    url_denni = "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt"

    odpoved = requests.get(url_denni, timeout=15)
    odpoved.raise_for_status()
    radky = odpoved.text.splitlines()

    datum_kurzu = radky[0].split()[0] if radky else "neznámé"
    rok = datum_kurzu.split(".")[-1] if "." in datum_kurzu else "2026"

    def nacti_rok_kurzy(r):
        u = f"https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/rok.txt?rok={r}"
        resp = requests.get(u, timeout=15)
        if resp.status_code != 200:
            return {}, []
        lines = resp.text.splitlines()
        if not lines:
            return {}, []
        hdr = lines[0].split("|")
        col_map = {}
        for idx, item in enumerate(hdr[1:], start=1):
            parts = item.strip().split()
            if len(parts) == 2:
                mnoz = float(parts[0].replace(",", "."))
                kod = parts[1].strip()
                col_map[kod] = (idx, mnoz)
        return col_map, lines[1:]

    col_map_akt, data_akt = nacti_rok_kurzy(rok)
    col_map_pred, data_pred = nacti_rok_kurzy(str(int(rok) - 1))

    vysledky = {}

    for radek in radky[2:]:
        casti = radek.split("|")
        if len(casti) >= 5:
            zeme = casti[0].strip()
            mena_nazev = casti[1].strip()
            mnozstvi = float(casti[2].strip().replace(",", "."))
            kod = casti[3].strip()
            kurz_raw = float(casti[4].strip().replace(",", "."))
            aktualni_kurz = kurz_raw / mnozstvi

            historie = []
            if kod in col_map_pred:
                idx_p, mnoz_p = col_map_pred[kod]
                for r in data_pred:
                    p = r.split("|")
                    if len(p) > idx_p:
                        try:
                            historie.append(float(p[idx_p].strip().replace(",", ".")) / mnoz_p)
                        except ValueError:
                            pass

            if kod in col_map_akt:
                idx_a, mnoz_a = col_map_akt[kod]
                for r in data_akt:
                    p = r.split("|")
                    if len(p) > idx_a:
                        try:
                            historie.append(float(p[idx_a].strip().replace(",", ".")) / mnoz_a)
                        except ValueError:
                            pass

            posledni_okno = historie[-okno_dni:] if historie else [aktualni_kurz]
            ma90 = sum(posledni_okno) / len(posledni_okno)
            odchylka_pct = ((aktualni_kurz - ma90) / ma90) * 100

            if odchylka_pct > neutralni_pasmo_pct:
                export_stav = "Výhodnější 😊"
                import_stav = "Nevýhodnější 😞"
                souhrn = f"Výhoda pro exportéry ({odchylka_pct:+.2f} % nad MA{okno_dni})"
            elif odchylka_pct < -neutralni_pasmo_pct:
                export_stav = "Nevýhodnější 😞"
                import_stav = "Výhodnější 😊"
                souhrn = f"Výhoda pro importéry ({odchylka_pct:+.2f} % pod MA{okno_dni})"
            else:
                export_stav = "Neutrální 😐"
                import_stav = "Neutrální 😐"
                souhrn = f"Neutrální pásmo (±{neutralni_pasmo_pct} % kolem MA{okno_dni})"

            vysledky[kod] = {
                "kod": kod,
                "nazev": mena_nazev,
                "zeme": zeme,
                "datum": datum_kurzu,
                "aktualni_kurz": round(aktualni_kurz, 3),
                "ma90": round(ma90, 3),
                "odchylka_pct": round(odchylka_pct, 2),
                "export_stav": export_stav,
                "import_stav": import_stav,
                "souhrn": souhrn,
            }

    return vysledky


def ziskej_odchylku_kurzu_cnb(mena="EUR", okno_dni=90, neutralni_pasmo_pct=0.5):
    """
    Vrátí informace o vybrané měně ve stejném formátu jako dříve.
    """
    try:
        vsechny_meny = nacti_kurzy_vsechny_meny_cnb(okno_dni=okno_dni, neutralni_pasmo_pct=neutralni_pasmo_pct)
        if mena not in vsechny_meny:
            print(f"Měna {mena} nebyla v denním kurzu ČNB nalezena.")
            return None
        info = vsechny_meny[mena]
        return {
            "mena": info["kod"],
            "datum": info["datum"],
            "aktualni_kurz": info["aktualni_kurz"],
            "klouzavy_prumer": info["ma90"],
            "odchylka_pct": info["odchylka_pct"],
            "vyhodnost": info["souhrn"],
        }
    except Exception as e:
        print(f"Chyba při načítání kurzu ČNB: {e}")
        return None

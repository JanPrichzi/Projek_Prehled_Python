import re
import pandas as pd

VYCHOZI_SLOVNIK_SENTIMENTU = {
    1.0: ["pomoc", "úspěch"],
    0.5: ["dohoda", "záchrana", "vítaly", "vítali"],
    0.25: ["vyhrál", "připomněl", "připomněli", "připomněly", "obnovuje", "obnovují", "obnovil"],
    -0.25: ["uzavře", "pokuta", "neplatný"],
    -0.5: ["nehoda", "hrozba", "zřítil", "zřítila", "sabotáž", "únik"],
    -1.0: [
        "smrt", "krize", "vražda", "zranění", "zraněných", "útočit",
        "útočili", "zaútočili", "kybernetický útok", "útok", "zabíjelo",
        "útoku", "útoků"
    ],
}


def nacti_slovnik_z_csv(zdroj_csv, oddelovac=";"):
    """
    Načte tabulku klíčových slov z CSV (lokální cesta nebo URL, např. raw GitHub).
    Očekává hlavičky sloupců jako váhy (např. -1, -0,5, -0,25, 0, 0,25, 0,5, 1).
    Pokud soubor není dostupný, vrátí záložní výchozí slovník.
    """
    if not zdroj_csv:
        print("ℹ️ Nebyla zadána cesta k CSV, používám výchozí vestavěný slovník.")
        return VYCHOZI_SLOVNIK_SENTIMENTU

    try:
        df = pd.read_csv(zdroj_csv, sep=oddelovac, dtype=str)
        slovnik_podle_vahy = {}

        for sloupec in df.columns:
            nazev_sloupce = str(sloupec).strip().replace(",", ".")
            try:
                vaha = float(nazev_sloupce)
            except ValueError:
                # Sloupce jako "Nevím/Neutrál/K zařazení" přeskočíme
                continue

            if vaha == 0:
                continue

            slova = []
            for hodnota in df[sloupec].dropna():
                ciste_slovo = str(hodnota).strip().strip('"').strip("'").lower()
                if ciste_slovo:
                    slova.append(ciste_slovo)

            if slova:
                slovnik_podle_vahy[vaha] = slova

        if not slovnik_podle_vahy:
            print("⚠️ CSV bylo načteno, ale neobsahuje platné sloupce s váhami. Používám výchozí slovník.")
            return VYCHOZI_SLOVNIK_SENTIMENTU

        print(f"✅ Slovník klíčových slov úspěšně načten z: {zdroj_csv}")
        return slovnik_podle_vahy

    except Exception as e:
        print(f"⚠️ Nepodařilo se načíst CSV ({e}). Používám výchozí vestavěný slovník.")
        return VYCHOZI_SLOVNIK_SENTIMENTU


def vypis_slovnik_do_konzole(slovnik_podle_vahy):
    """
    Vypíše všechna načtená klíčová slova podle jejich váhy do konzole,
    aby bylo hned vidět, že načítání funguje.
    """
    print("\n📚 NAČTENÝ SLOVNÍK KLÍČOVÝCH SLOV:")
    print("-" * 60)
    celkem_slov = 0

    for vaha in sorted(slovnik_podle_vahy.keys(), reverse=True):
        slova = slovnik_podle_vahy[vaha]
        celkem_slov += len(slova)
        znaminko = "+" if vaha > 0 else ""
        print(f"Váha {znaminko}{vaha:g} ({len(slova)}): {', '.join(slova)}")

    print("-" * 60)
    print(f"Celkem slov/sousloví: {celkem_slov}\n")


def obsahuje_cele_slovo(text, výraz):
    """
    Ověří, zda se v textu vyskytuje celé slovo nebo sousloví (ne jen část jiného slova).
    Např. 'vyhrál' najde 'vyhrál', ale nenajde 'nevyhrál'.
    """
    vzor = rf"(?<!\w){re.escape(výraz.lower())}(?!\w)"
    return re.search(vzor, text) is not None


def zhodnot_titulek(titulek, slovnik_podle_vahy=VYCHOZI_SLOVNIK_SENTIMENTU):
    """
    Tato funkce dostane text titulku, převede ho na malá písmena
    a podle obsažených celých slov / sousloví ze slovníku mu přiřadí skóre
    omezené v rozmezí od -1 do +1.
    """
    titulek_mala_pismena = str(titulek).lower()
    skore = 0.0

    for vaha, seznam_slov in slovnik_podle_vahy.items():
        for slovo in seznam_slov:
            if obsahuje_cele_slovo(titulek_mala_pismena, slovo):
                skore += vaha

    # Omezení skóre jednotlivého článku na interval [-1, +1]
    return max(-1.0, min(1.0, skore))

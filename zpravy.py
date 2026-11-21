import feedparser
from sentiment import VYCHOZI_SLOVNIK_SENTIMENTU, zhodnot_titulek


def stahni_zpravy(vrat_detaily=False, slovnik_podle_vahy=VYCHOZI_SLOVNIK_SENTIMENTU):
    """
    Stáhne aktuální zprávy z ČT24, ohodnotí je pomocí funkce z modulu sentiment
    a vrátí celkové skóre (případně i seznam detailů článků pro HTML výstup).
    """
    rss_url = "https://ct24.ceskatelevize.cz/rss/hlavni-zpravy"
    feed = feedparser.parse(rss_url)

    celkove_skore_zprav = 0.0
    pocet_clanku = 10  # Kolik nejnovějších zpráv chceme hodnotit
    detaily_clanku = []

    print("DNEŠNÍ HLAVNÍ ZPRÁVY:")
    print("-" * 60)

    for clanek in feed.entries[:pocet_clanku]:
        titulek = clanek.title
        skore_clanku = zhodnot_titulek(titulek, slovnik_podle_vahy)
        celkove_skore_zprav += skore_clanku

        # Přiřazení smajlíku pro vizuální přehlednost v konzoli
        oznaceni = "😊" if skore_clanku > 0 else "😞" if skore_clanku < 0 else "😐"
        print(f"{oznaceni} (Skóre: {skore_clanku:g}) | {titulek}")

        detaily_clanku.append({
            "titulek": titulek,
            "skore": round(skore_clanku, 2),
            "oznaceni": oznaceni
        })

    if vrat_detaily:
        return celkove_skore_zprav, detaily_clanku
    return celkove_skore_zprav

import os
import re
import sys
import requests
from bs4 import BeautifulSoup

URL = "https://trouverunlogement.lescrous.fr/tools/47/search?occupationModes=alone&bounds=4.782253280282021_45.805392737249164_4.9058494716882715_45.695192390203836"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

ABSENCE_TEXT = "Aucun logement trouvé en France"

def fetch_text(url: str) -> str:
    r = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"s+", " ", text).strip()
    return text

def send_telegram(message: str) -> None:
    resp = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "protect_content": True
        },
        timeout=20
    )
    resp.raise_for_status()

def main():
    text = fetch_text(URL)

    print(text[:1500])

    if ABSENCE_TEXT not in text:
        send_telegram(
            "Alerte CROUS : le message d’absence a disparu sur ta page Lyon. Vérifie immédiatement : "
            + URL
        )
        print("ALERTE ENVOYEE")
    else:
        print("AUCUN LOGEMENT POUR L INSTANT")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERREUR: {e}")
        sys.exit(1)

import os
import re
import requests
from bs4 import BeautifulSoup

URL = "https://trouverunlogement.lescrous.fr/tools/47/search?occupationModes=alone&bounds=4.710192382335663_45.87846929513082_4.957384765148164_45.65814005497071&locationName=Lyon"
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def clean_text(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    return re.sub(r"s+", " ", text).strip()

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
        timeout=20
    )

r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
text = clean_text(r.text)

no_result = "Aucun logement trouvé pour Lyon" in text
positive_keywords = [
    "Résidence",
    "RESIDENCE",
    "Logement individuel",
    "Logement"
]
has_positive = any(k in text for k in positive_keywords)

if (not no_result) and has_positive:
    send_telegram("Alerte CROUS Lyon : résultat possible détecté, vérifie immédiatement.")

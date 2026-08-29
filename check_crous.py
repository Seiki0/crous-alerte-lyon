import requests
from bs4 import BeautifulSoup
import os

URL = "https://trouverunlogement.lescrous.fr/tools/47/search?occupationModes=alone&bounds=4.710192382335663_45.87846929513082_4.957384765148164_45.65814005497071&locationName=Lyon"
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
text = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True)

if "Aucun logement trouvé pour Lyon" not in text:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": "Alerte CROUS Lyon : la page a changé, vérifie vite."},
        timeout=20
    )

import requests
from bs4 import BeautifulSoup
import re

URL = "https://trouverunlogement.lescrous.fr/tools/47/search?occupationModes=alone&bounds=4.782253280282021_45.805392737249164_4.9058494716882715_45.695192390203836"

r = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, "html.parser")
text = soup.get_text(" ", strip=True)
text = re.sub(r"s+", " ", text).strip()

print(text[:1500])

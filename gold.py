import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://ngoctham.com/bang-gia-vang/"

headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(URL, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

text = soup.get_text("\n")
lines = text.split("\n")

gold_price = None

for i, line in enumerate(lines):
    if "Nhẫn 999.9" in line:
        for j in range(i, i + 40):
            if "Giá bán" in lines[j] or "GIÁ BÁN" in lines[j]:
                for k in range(j, j + 10):
                    if any(c.isdigit() for c in lines[k]):
                        gold_price = lines[k].strip()
                        break
                break
        break

embed = {
    "title": "💰 GOLD DASHBOARD",
    "color": 0xF1C40F,
    "fields": [
        {"name": "Loại vàng", "value": "Nhẫn 999.9", "inline": True},
        {"name": "Giá bán", "value": gold_price or "Không lấy được", "inline": True}
    ],
    "timestamp": datetime.utcnow().isoformat()
}

requests.post(
    WEBHOOK,
    json={"embeds": [embed]}
)

print("GOLD SENT")

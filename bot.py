import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# ================= BTC =================
btc_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
btc = requests.get(btc_url).json()["bitcoin"]["usd"]

# ================= GOLD =================
gold_url = "https://ngoctham.com/bang-gia-vang/"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(gold_url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

rows = soup.select("table tr")

gold_price = None

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 3:
        name = cols[0].get_text(strip=True)
        price = cols[2].get_text(strip=True)

        if "Nhẫn 999.9" in name:
            gold_price = price
            break

# ================= DISCORD CARD =================
embed = {
    "title": "📊 MARKET DASHBOARD",
    "color": 0x3498db,
    "fields": [
        {
            "name": "💰 BTC",
            "value": f"${btc:,.2f}",
            "inline": True
        },
        {
            "name": "🥇 Gold (Nhẫn 999.9)",
            "value": gold_price or "N/A",
            "inline": True
        }
    ]
}

requests.post(
    WEBHOOK,
    json={"embeds": [embed]}
)

print("DONE")

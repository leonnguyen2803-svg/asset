import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

# ================= BTC USD =================
btc_api = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
btc_usd = requests.get(btc_api).json()["bitcoin"]["usd"]

# ================= USD -> VND (Remitano scrape) =================
url = "https://remitano.com/vn"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(res.text, "html.parser")

text = soup.get_text(" ")
vnd_rate = None

# fallback scan rate (approx logic)
for word in text.split():
    if "VND" in word:
        try:
            # lấy số gần nhất (fallback đơn giản)
            num = float(''.join(c for c in word if c.isdigit() or c == '.'))
            if 20000 < num < 30000:
                vnd_rate = num
                break
        except:
            pass

# nếu fail → fallback cứng
if not vnd_rate:
    vnd_rate = 25000  # safe fallback

btc_vnd = btc_usd * vnd_rate

# ================= DISCORD EMBED =================
embed = {
    "title": "📊 CRYPTO DASHBOARD",
    "color": 0x2ecc71,
    "fields": [
        {
            "name": "💰 BTC (USD)",
            "value": f"${btc_usd:,.2f}",
            "inline": True
        },
        {
            "name": "🇻🇳 BTC (VND)",
            "value": f"{btc_vnd:,.0f} VND",
            "inline": True
        },
        {
            "name": "💱 Rate",
            "value": f"1 USD ≈ {vnd_rate} VND",
            "inline": False
        }
    ]
}

requests.post(WEBHOOK, json={"embeds": [embed]})

print("DONE")

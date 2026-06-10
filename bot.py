import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
headers = {"User-Agent": "Mozilla/5.0"}

# ================= BTC =================
btc = requests.get(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
    timeout=10
).json()["bitcoin"]["usd"]

btc_vnd = btc * 25000

# ================= GOLD =================
try:
    gold_url = "https://ngoctham.com/bang-gia-vang/"
    res = requests.get(gold_url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    gold_price = None

    for row in soup.select("table tr"):
        cols = row.find_all("td")
        if len(cols) >= 3:
            if "Nhẫn 999.9" in cols[0].get_text():
                gold_price = cols[2].get_text(strip=True)
                break
except:
    gold_price = None

# ================= FPT (VNDirect API - STABLE) =================
def get_fpt():
    try:
        url = "https://finfo-api.vndirect.com.vn/v4/stock_prices?q=code:FPT"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data["data"][0]["close"]
    except:
        return None

fpt = get_fpt()

# ================= DISCORD EMBED =================
embed = {
    "title": "📊 MARKET DASHBOARD",
    "color": 0x00b894,
    "fields": [
        {
            "name": "₿ BTC (USD)",
            "value": f"${btc:,.2f}",
            "inline": True
        },
        {
            "name": "₿ BTC (VND)",
            "value": f"{btc_vnd:,.0f} VND",
            "inline": True
        },
        {
            "name": "🥇 GOLD (Nhẫn 999.9)",
            "value": gold_price or "N/A",
            "inline": False
        },
        {
            "name": "📈 FPT (VNDirect)",
            "value": f"{fpt}" if fpt else "N/A",
            "inline": False
        }
    ]
}

requests.post(
    WEBHOOK,
    json={"embeds": [embed]}
)

print("DONE")

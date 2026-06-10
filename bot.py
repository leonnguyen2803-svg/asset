import requests
import os
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]
headers = {"User-Agent": "Mozilla/5.0"}

# ================= BTC =================
btc_usd = requests.get(
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
    timeout=10
).json()["bitcoin"]["usd"]

btc_buy = 63200

btc_vnd_rate = 25000

btc_vnd = btc_usd * btc_vnd_rate
btc_buy_vnd = btc_buy * btc_vnd_rate

btc_profit = ((btc_usd - btc_buy) / btc_buy) * 100

# ================= GOLD =================
try:
    url = "https://ngoctham.com/bang-gia-vang/"
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    gold_price = None

    for row in soup.select("table tr"):
        cols = row.find_all("td")
        if len(cols) >= 3:
            name = cols[0].get_text(strip=True)
            price = cols[2].get_text(strip=True)

            if "Nhẫn 999.9" in name:
                gold_price = int(price.replace(".", "").replace(",", ""))
                break
except:
    gold_price = None

gold_buy = 17300000

if gold_price:
    gold_profit = ((gold_price - gold_buy) / gold_buy) * 100
else:
    gold_profit = None

# ================= FORMAT =================
btc_sign = "🟢" if btc_profit >= 0 else "🔴"
gold_sign = "🟢" if gold_profit and gold_profit >= 0 else "🔴"

message = f"""📊 MARKET REPORT

₿ BTC: ${btc_usd:,.0f}
₿ BTC: {btc_vnd:,.0f} VND
{btc_sign} BTC P/L: {btc_profit:+.2f}%

🥇 Nhẫn vàng trơn 1 chỉ: {gold_price or 'N/A'} VND
{gold_sign} GOLD P/L: {gold_profit:+.2f}% if gold_profit is not None else 'N/A'
"""

requests.post(
    WEBHOOK,
    json={"content": message}
)

print("DONE")

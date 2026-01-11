import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.goodreturns.in/gold-rates/bhopal.html"

def fetch_gold_rate():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    price_24k = None
    price_22k = None

    tds = soup.find_all("td")

    for i, td in enumerate(tds):
        text = td.get_text(strip=True)

        if "24" in text and price_24k is None:
            # price is usually 1–2 cells after purity
            for next_td in tds[i+1:i+4]:
                val = next_td.get_text(strip=True)
                if "₹" in val:
                    price_24k = val
                    break

        if "22" in text and price_22k is None:
            for next_td in tds[i+1:i+4]:
                val = next_td.get_text(strip=True)
                if "₹" in val:
                    price_22k = val
                    break

    if not price_24k or not price_22k:
        raise Exception("Gold prices not extracted correctly")

    return price_24k, price_22k

def send_telegram(message):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(api, data=data)

if __name__ == "__main__":
    p24, p22 = fetch_gold_rate()

    msg = (
        "🏅 Bhopal Gold Rate (Today)\n\n"
        f"24K (10g): {p24}\n"
        f"22K (10g): {p22}\n\n"
        "Source: GoodReturns"
    )

    send_telegram(msg)

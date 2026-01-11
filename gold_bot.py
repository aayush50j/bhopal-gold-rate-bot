import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.livemint.com/gold-prices/bhopal"

def fetch_gold_rate():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    price_24k = None
    price_22k = None

    # LiveMint clearly labels karat values
    for div in soup.find_all("div"):
        text = div.get_text(" ", strip=True)

        if "24 Carat" in text and "₹" in text:
            price_24k = text.split("₹")[-1].split()[0]

        if "22 Carat" in text and "₹" in text:
            price_22k = text.split("₹")[-1].split()[0]

    if not price_24k or not price_22k:
        raise Exception("Failed to extract gold rates from LiveMint")

    return price_24k, price_22k

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

if __name__ == "__main__":
    p24, p22 = fetch_gold_rate()

    msg = (
        "🏅 Bhopal Gold Rate (Per 10g)\n\n"
        f"24K: ₹{p24}\n"
        f"22K: ₹{p22}\n\n"
        "Source: LiveMint"
    )

    send_telegram(msg)

import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def fetch_gold_rate():
    URL = "https://www.indmoney.com/gold-rates/bhopal"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    price_24k = None
    price_22k = None

    divs = soup.find_all("div")
    for div in divs:
        text = div.get_text(" ", strip=True)
        if "10 gm" in text and "24" in text and "₹" in text:
            parts = text.split("₹")
            for part in parts[1:]:
                num = part.split()[0].replace(",", "")
                if num.isdigit():
                    price_24k = num
        if "10 gm" in text and "22" in text and "₹" in text:
            parts = text.split("₹")
            for part in parts[1:]:
                num = part.split()[0].replace(",", "")
                if num.isdigit():
                    price_22k = num

    if not price_24k or not price_22k:
        raise Exception("Failed to find gold prices on the page")

    return price_24k, price_22k

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

if __name__ == "__main__":
    p24, p22 = fetch_gold_rate()
    msg = (
        "🏅 Bhopal Gold Rate (Per 10g)\n\n"
        f"24K: ₹{p24}\n"
        f"22K: ₹{p22}"
    )
    send_telegram(msg)

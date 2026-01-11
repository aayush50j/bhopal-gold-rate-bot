import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def fetch_gold_rate():
    url = "https://www.5paisa.com/commodity-trading/gold/Bhopal"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    price_24k = None
    price_22k = None

    # Look for prices inside the table rows
    for tr in soup.find_all("tr"):
        text = tr.get_text(" ", strip=True)

        # Check if this row contains 24K and a 10g value
        if "24K Gold / 10gm" in text or "24K" in text and "10gm" in text:
            # Extract the number after ₹
            parts = text.split("₹")
            for part in parts:
                clean = part.replace(",", "").strip().split()
                if clean and clean[0].isdigit():
                    price_24k = clean[0]

        # Check if this row contains 22K and a 10g value
        if "22K Gold / 10gm" in text or "22K" in text and "10gm" in text:
            parts = text.split("₹")
            for part in parts:
                clean = part.replace(",", "").strip().split()
                if clean and clean[0].isdigit():
                    price_22k = clean[0]

    if not price_24k or not price_22k:
        raise Exception("Failed to extract gold prices — page structure may have changed")

    return price_24k, price_22k

def send_telegram(message):
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(send_url, data=data)

if __name__ == "__main__":
    try:
        p24, p22 = fetch_gold_rate()
        message = (
            "🏅 Bhopal Gold Rate (Per 10g)\n\n"
            f"24K: ₹{p24}\n"
            f"22K: ₹{p22}"
        )
        send_telegram(message)
    except Exception as e:
        send_telegram(f"⚠ Error fetching gold rate: {e}")

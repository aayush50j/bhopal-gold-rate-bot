import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def fetch_gold_rate():
    import requests
    from bs4 import BeautifulSoup

    URL = "https://www.5paisa.com/commodity-trading/gold/bhopal"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    price_24k = None
    price_22k = None

    # Look for table rows with 10 gram and the values
    for tr in soup.find_all("tr"):
        cols = tr.get_text(" ", strip=True)
        # Extract 24K ten gram
        if "10 gram" in cols and "24K" in cols:
            parts = cols.split()
            for i, part in enumerate(parts):
                if "₹" in part and part.replace("₹", "").replace(",", "").isdigit():
                    price_24k = part.replace("₹", "").replace(",", "")
        # Extract 22K ten gram
        if "10 gram" in cols and "22K" in cols:
            parts = cols.split()
            for i, part in enumerate(parts):
                if "₹" in part and part.replace("₹", "").replace(",", "").isdigit():
                    price_22k = part.replace("₹", "").replace(",", "")

    if not price_24k or not price_22k:
        raise Exception("Failed to extract gold price from 5paisa")

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

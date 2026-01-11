import os
import requests

BOT_TOKEN = os.getenv("8541609986:AAEVQpXwF8AXemsZRvxyEjrypxtGr-YHP2A")
CHAT_ID = os.getenv("850468837")

def send_test_message():
    url = f"https://api.telegram.org/bot{8541609986:AAEVQpXwF8AXemsZRvxyEjrypxtGr-YHP2A}/sendMessage"
    data = {
        "chat_id": 850468837,
        "text": "✅ Telegram bot connected successfully!"
    }
    requests.post(url, data=data)

if __name__ == "__main__":
    send_test_message()

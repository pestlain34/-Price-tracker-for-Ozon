import requests
import os
def send_graph_photo():
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    bot_token = TELEGRAM_TOKEN
    chat_id = CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open('price_chart.png' , 'rb') as photo:
        payload = {
            "chat_id": chat_id,
            "caption": "📈 График изменения цен"
        }
        files = {
            "photo": photo
        }
        requests.post(url, data=payload, files=files)
def send_telegram_message(message):
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    bot_token = TELEGRAM_TOKEN
    chat_id = CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url , data=payload)

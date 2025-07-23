# telegram_bot.py
import requests
import time
from configs import BOT_TOKEN
from deepseek import chat as deepseek_chat

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

class TelegramBot:
    def __init__(self):
        self.offset = None  # Keeps track of last message seen

    def get_updates(self):
        try:
            response = requests.get(
                f"{BASE_URL}/getUpdates",
                params={"timeout": 60, "offset": self.offset},
                timeout=65
            )
            return response.json()
        except Exception as e:
            print(f"Failed to fetch updates: {e}")
            return {"ok": False, "result": []}

    def send_message(self, chat_id, text):
        try:
            requests.post(
                f"{BASE_URL}/sendMessage",
                json={"chat_id": chat_id, "text": text},
                timeout=10
            )
        except Exception as e:
            print(f"Failed to send message: {e}")

    def handle_message(self, message):
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        print(f"User: {text}")
        if not text:
            return
        reply = deepseek_chat(text)
        self.send_message(chat_id, reply)

    def run(self):
        print("🤖 Telegram bot is now running...")
        while True:
            updates = self.get_updates()
            if updates.get("ok"):
                for update in updates["result"]:
                    self.offset = update["update_id"] + 1
                    if "message" in update:
                        self.handle_message(update["message"])
            time.sleep(1)

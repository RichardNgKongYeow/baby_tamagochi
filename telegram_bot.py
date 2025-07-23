import requests
import time
from configs import BOT_TOKEN
from deepseek import chat as deepseek_chat

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

class TelegramBot:
    def __init__(self):
        self.offset = None  # Used to keep track of processed messages

    def get_updates(self):
        url = f"{BASE_URL}/getUpdates"
        params = {"timeout": 60, "offset": self.offset}
        response = requests.get(url, params=params)
        return response.json()

    def send_message(self, chat_id, text):
        url = f"{BASE_URL}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        requests.post(url, json=payload)

    def handle_message(self, message):
        chat_id = message["chat"]["id"]
        if "text" in message:
            user_input = message["text"]
            try:
                response = deepseek_chat(user_input)
            except Exception as e:
                response = f"Error: {str(e)}"
            self.send_message(chat_id, response)

    def run(self):
        print("🤖 Bot is running...")
        while True:
            updates = self.get_updates()
            if updates.get("ok"):
                for update in updates["result"]:
                    self.offset = update["update_id"] + 1
                    if "message" in update:
                        self.handle_message(update["message"])
            time.sleep(1)

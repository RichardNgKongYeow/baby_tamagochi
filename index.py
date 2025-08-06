from telegram_bot import TelegramBot
import deepseek
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure API keys
tele_bot_api_key = os.getenv("TELE_BOT_TOKEN")

if __name__ == "__main__":
    print("🚀 Launching DeepSeek...")

    # Start DeepSeek model
    if not deepseek.run_deepseek():
        print("❌ Failed to launch DeepSeek model.")
        exit(1)

    # Wait for DeepSeek to be ready
    if not deepseek.wait_for_deepseek():
        print("❌ DeepSeek didn't become ready in time. Exiting.")
        exit(1)

    print("✅ DeepSeek is ready. Launching Telegram bot...")
    bot = TelegramBot(bot_token=tele_bot_api_key)
    bot.run()

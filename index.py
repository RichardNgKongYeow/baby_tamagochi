from telegram_bot import TelegramBot
from configs import BOT_TOKEN
import deepseek

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
    bot = TelegramBot(bot_token=BOT_TOKEN)
    bot.run()

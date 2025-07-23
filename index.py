from deepseek import run_docker_desktop, run_deepseek, wait_for_deepseek
from telegram_bot import TelegramBot

if __name__ == "__main__":
    # Start Docker Desktop if needed
    if not run_docker_desktop():
        print("Docker failed to start.")
        exit(1)

    # Run DeepSeek
    if not run_deepseek():
        print("Failed to launch DeepSeek model.")
        exit(1)

    # Wait for it to be ready
    if not wait_for_deepseek():
        print("DeepSeek didn't become ready in time.")
        exit(1)

    # Launch Telegram bot
    bot = TelegramBot()
    bot.run()
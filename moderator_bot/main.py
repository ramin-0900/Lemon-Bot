from bot import setup_bot
from dotenv import load_dotenv
from pathlib import Path
import os

def main():
    env_path = Path('.') / '..' / '.env'
    load_dotenv(dotenv_path=env_path)
    
    bot_token = os.getenv("DISCORD_TOKEN")

    if not bot_token:
        print("خطا: توکن ربات در فایل .env یافت نشد یا خالی است.")
        return

    bot = setup_bot()
    bot.run(bot_token)

if __name__ == "__main__":
    main()

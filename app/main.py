import os
from dotenv import load_dotenv
from app.entities.bot.bot import TelegramBot


def main():
    load_dotenv()
    TOKEN = os.getenv('telegram_bot_token')
    bot = TelegramBot(TOKEN)
    bot.run()


if __name__ == '__main__':
    main()

from telebot import TeleBot
from bot import handlers
from bot.config import TOKEN
import threading

bot = TeleBot(TOKEN)

handlers.register_handlers(bot)


def main():
    reminder_thread = threading.Thread(
        target=handlers.check_reminder_every_minutes, args=(bot,), daemon=True
    )
    reminder_thread.start()
    bot.infinity_polling()

import logging
import sqlite3
import telebot
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext



bot = telebot.TeleBot("")

TOKEN = ""



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



#@bot.message_handler(commands=['start'])
#def start_message(message):
#    bot.send_message(message.chat.id, 'Добро пожаловать')

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Please send your Telegram ID, in-game nickname, and I will save your IP address.')


def check_user(update: Update, context: CallbackContext):
    conn = connection_db()
    telegram_id = update.message.from_user.id
    c = conn.cursor()


def connection_db():
    conn = sqlite3.connect('db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (telegram_id INTEGER PRIMARY KEY,
                nickname TEXT,
                ip_address TEXT)''')
    conn.commit()
    return conn


def save_user(update: Update, context: CallbackContext):
    conn = connection_db()
    telegram_id = update.message.from_user.id
    nickname = update.message.text.split()[1]
    ip_address = update.message.chat.ip
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (telegram_id, nickname, ip_address) VALUES (?, ?, ?)",
              (telegram_id, nickname, ip_address))
    conn.commit()
    conn.close()
    if c.rowcount == 0:
        update.message.reply_text("Пользователь уже существует :)")
    else:
        update.message.reply_text('Пользователь зарегистрирован')






def main(start_command=None):
    updater = Updater('6682932102:AAHMz1UAGuE3er-ArL9DNJKCdev5m-XGPjY', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

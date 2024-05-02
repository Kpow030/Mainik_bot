import sqlite3
import telebot
import telegram




conn = sqlite3.connect('database.sqlite', check_same_thread=False)
cursor = conn.cursor()



bot = telebot.TeleBot("6682932102:AAHMz1UAGuE3er-ArL9DNJKCdev5m-XGPjY")

TOKEN = "6682932102:AAHMz1UAGuE3er-ArL9DNJKCdev5m-XGPjy"
# Подключаемся к базе данных
def db_table_val(user_id: int, ip_address: str, telegram_id: int, game_nick: str):
    cursor.execute('INSERT INTO users(user_id, ip_address, telegram_id, game_nick) VALUES (?, ?, ?, ?)',
                (user_id, ip_address, telegram_id, game_nick))
    conn.commit()

def get_ip_address(message):
    if hasattr(message, 'headers') and 'X-Forwarded-For' in message.headers:
        return message.headers['X-Forwarded-For']
   # else:
       # return message.remote_addr


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Ваше имя добавлено в базу данных!')

    user_id = message.from_user.id
    ip_address = get_ip_address(message)
    telegram_id = message.from_user.id
    game_nick = message.from_user.username

    db_table_val(user_id, ip_address, telegram_id, game_nick)

# Запускаем бота
bot.polling(non_stop=True)
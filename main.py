import socket
import requests
import sqlite3
import telebot
import threading

bot = telebot.TeleBot('your-token-bot')

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.sqlite')
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def add_user_to_db(self, telegram_id, ip_address, game_nickname):
        self.cursor.execute("INSERT INTO users (telegram_id, ip_address, game_nickname) VALUES (?,?,?)",
                           (telegram_id, ip_address, game_nickname))
        self.conn.commit()

    def get_user_from_db(self, telegram_id):
        self.cursor.execute("SELECT * FROM users WHERE telegram_id =?", (telegram_id,))
        user = self.cursor.fetchone()
        return user

def allow_user_to_play(telegram_id):
    # Call game server API to allow user to play
    response = requests.post('https://your-game-server.com/api/allow_user', json={'user_id': telegram_id})
    if response.status_code == 200:
        print(f"User {telegram_id} allowed to play")
    else:
        print(f"Error allowing user {telegram_id} to play: {response.text}")

@bot.message_handler(commands=['start'])
def add_user_from_server(message):
    bot.send_message(message.from_user.id, 'Hi, you need to register to play on our server.'
                                            ' Just enter your nickname in the game. If you have been registered before,'
                                            ' we will just check and give you access to the server. Thank you '
                                             'For using our server. Have a nice game')

@bot.message_handler(content_types=['text'])
def register(message):
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        bot.send_message(message.from_user.id, "Error when getting an IP address.")
        return
    telegram_id = message.from_user.id
    game_nickname = message.text
    user = None
    with Database() as db:
        user = db.get_user_from_db(telegram_id)
    if user is None:
        with Database() as db:
            db.add_user_to_db(telegram_id, ip_address, game_nickname)
            allow_user_to_play(telegram_id)
        bot.send_message(message.from_user.id, "Thanks! Your information has been added to the database. Now you can play.")
  else:
  bot.send_message(message.from_user.id , "You are already registered.")
  bot.send_message(message.from_user.id , f"Your ID: {user[1]}\nYour IP: {user[2]}\nYour nickname: {user[3]}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling(none_stop=True, interval=0)

# Close the database connection when the program exits
Database().close()

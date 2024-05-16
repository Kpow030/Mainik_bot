import telebot
import sqlite3
import requests



# Install token-bot
bot = telebot.TeleBot('')

# Connection to database
conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()

# Creating a table if it does not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE, ip_address TEXT, game_nickname TEXT)''')
conn.commit()


# Function to add a user to the database
def add_user_to_db(telegram_id, ip_address, game_nickname):
    conn_thread = sqlite3.connect('database.sqlite', check_same_thread=False)
    cursor_thread = conn_thread.cursor()
    cursor_thread.execute("INSERT INTO users (telegram_id, ip_address, game_nickname) VALUES (?,?,?)",
                          (telegram_id, ip_address, game_nickname))
    conn_thread.commit()
    conn_thread.close()

# Get user from db
def get_user_from_db(telegram_id):
    conn_thread = sqlite3.connect('database.sqlite', check_same_thread=False)
    cursor_thread = conn_thread.cursor()
    cursor_thread.execute("SELECT * FROM users WHERE telegram_id =?", [telegram_id])
    user = cursor_thread.fetchone()
    conn_thread.close()
    return user



def allow_user_to_play(telegram_id):
    # Call game server API to allow user to play
    response = requests.post('https://your-game-server.com/api/allow_user', json={'user_id': telegram_id})
    if response.status_code == 200:
        print(f"User {telegram_id} allowed to play")
    else:
        print(f"Error allowing user {telegram_id} to play: {response.text}")



# A function for adding a user to the database
@bot.message_handler(commands=['start'])
def add_user_from_server(message):
    bot.send_message(message.from_user.id, 'Hi, you need to register to play on our server.'
                                            ' Just enter your nickname in the game. If you have been registered before,'
                                            ' we will just check and give you access to the server. Thank you '
                                             'For using our server. Have a nice game')

# Register from server
@bot.message_handler(content_types=['text'])
def register(message):
    ip_address = message.from_user.id
    telegram_id = message.from_user.id
    game_nickname = message.text
    user = get_user_from_db(message.from_user.id)
    if get_user_from_db(telegram_id) is None:
        add_user_to_db(telegram_id, ip_address, game_nickname)
        bot.send_message(message.from_user.id, "Thanks! You have been added to our server.")
        allow_user_to_play(telegram_id)  # Allow user to play on game server
    else:
        bot.send_message(message.from_user.id, "You are already registered.")
        bot.send_message(message.from_user.id , f"Your ID: {user[1]}\Your IP: {user[2]}\Your nickname: {user[3]}")



# Starting bot
bot.polling(none_stop=True, interval=0)


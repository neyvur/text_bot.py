import telebot
from datetime import datetime

TOKEN = "8123716274:AAHrGxV9fOj1N4aOI0Ogj-sXGJyMB4o6wGk"
ADMIN_ID = 7011196294 

bot = telebot.TeleBot(TOKEN)

KEYWORDS = ["новости", "скидка", "технологии", "любовь"]

print("Команды: /add, /users")

@bot.message_handler(commands=['add'])
def add_keyword(message):
    try:
        word = message.text.split(maxsplit=1)[1].strip().lower()

        if word not in KEYWORDS:
            KEYWORDS.append(word)
            bot.reply_to(message, f"слово «{word}» в кормане")
        else:
            bot.reply_to(message, f"слово «{word}» уже у тебя")
    except IndexError:
        bot.reply_to(message, "правильное написание * /add __")

@bot.message_handler(commands=['users'])
def show_users(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Бокини йепсан")
        return

    try:
        with open("users.txt", "r", encoding="utf-8") as f:
            users = set(line.strip() for line in f.readlines())
        if users:
            bot.reply_to(message, f"Пользователи:\n" + "\n".join(users))
        else:
            bot.reply_to(message, "Пользователей пока нет.")
    except FileNotFoundError:
        bot.reply_to(message, "Файл с пользователями не найден.")

def log_message(user_id, username, text, reply):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - ID: {user_id} - USER: @{username} - MSG: {text} - REPLY: {reply}\n")

def save_user(user_id, username):
    user_line = f"{user_id} @{username}"
    try:
        with open("users.txt", "r", encoding="utf-8") as f:
            users = f.read().splitlines()
        if user_line not in users:
            with open("users.txt", "a", encoding="utf-8") as f:
                f.write(user_line + "\n")
    except FileNotFoundError:
        with open("users.txt", "w", encoding="utf-8") as f:
            f.write(user_line + "\n")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    matched = [word for word in KEYWORDS if word in text]

    if matched:
        reply = f"ключевые слова: {', '.join(matched)}"
    else:
        reply = "ниче нет"

    bot.reply_to(message, reply)
    save_user(message.from_user.id, message.from_user.username or "без username")
    log_message(message.from_user.id, message.from_user.username or "без username", message.text, reply)

print("Бот приступил к работе...")
bot.polling()

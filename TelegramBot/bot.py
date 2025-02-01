import telebot
import requests
import os
from .handlers import bot

if __name__ == "__main__":
    bot.polling()


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://backend:8000")

bot = telebot.TeleBot(TOKEN)

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для управления привычками. Войдите в систему с помощью /login.")

@bot.message_handler(commands=['login'])
def login(message):
    bot.send_message(message.chat.id, "Введите логин и пароль через пробел (пример: user123 пароль123)")
    bot.register_next_step_handler(message, process_login)

def process_login(message):
    data = message.text.split()
    if len(data) != 2:
        bot.send_message(message.chat.id, "Неверный формат. Попробуйте снова.")
        return
    username, password = data
    response = requests.post(f"{API_URL}/token/", data={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        users[message.chat.id] = token
        bot.send_message(message.chat.id, "Успешный вход! Используйте /habits для управления привычками.")
    else:
        bot.send_message(message.chat.id, "Ошибка входа. Проверьте логин и пароль.")

@bot.message_handler(commands=['habits'])
def get_habits(message):
    token = users.get(message.chat.id)
    if not token:
        bot.send_message(message.chat.id, "Сначала войдите в систему с /login.")
        return
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/habits/", headers=headers, params={"user_id": message.chat.id})
    if response.status_code == 200:
        habits = response.json()
        text = "\n".join([f"{h['id']}. {h['name']} (Дней подряд: {h['completed_days']})" for h in habits])
        bot.send_message(message.chat.id, text or "У вас пока нет привычек. Добавьте с помощью /add_habit.")
    else:
        bot.send_message(message.chat.id, "Ошибка получения списка привычек.")

@bot.message_handler(commands=['add_habit'])
def add_habit(message):
    bot.send_message(message.chat.id, "Введите название новой привычки:")
    bot.register_next_step_handler(message, process_add_habit)

def process_add_habit(message):
    token = users.get(message.chat.id)
    if not token:
        bot.send_message(message.chat.id, "Сначала войдите в систему с /login.")
        return
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/habits/", headers=headers, json={"name": message.text, "user_id": message.chat.id})
    if response.status_code == 200:
        bot.send_message(message.chat.id, "Привычка успешно добавлена!")
    else:
        bot.send_message(message.chat.id, "Ошибка при добавлении.")

bot.polling()

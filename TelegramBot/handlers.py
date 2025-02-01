import telebot
import requests
import os
from .config import TOKEN, API_URL

bot = telebot.TeleBot(TOKEN)
users = {}

def send_login(message):
    bot.send_message(message.chat.id, "Введите логин и пароль через пробел:")
    bot.register_next_step_handler(message, process_login)

def process_login(message):
    data = message.text.split()
    if len(data) != 2:
        bot.send_message(message.chat.id, "Неверный формат. Попробуйте снова.")
        return
    username, password = data
    response = requests.post(f"{API_URL}/token/", data={"username": username, "password": password})
    if response.status_code == 200:
        users[message.chat.id] = response.json()["access_token"]
        bot.send_message(message.chat.id, "Успешный вход!")
    else:
        bot.send_message(message.chat.id, "Ошибка входа. Проверьте логин и пароль.")

def send_habits(message):
    token = users.get(message.chat.id)
    if not token:
        bot.send_message(message.chat.id, "Сначала войдите в систему с /login.")
        return
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/habits/", headers=headers)
    if response.status_code == 200:
        habits = response.json()
        text = "\n".join([f"{h['id']}. {h['name']} (Дней подряд: {h['completed_days']})" for h in habits])
        bot.send_message(message.chat.id, text or "У вас пока нет привычек.")
    else:
        bot.send_message(message.chat.id, "Ошибка получения списка привычек.")

bot.add_message_handler({"function": send_login, "commands": ["login"]})
bot.add_message_handler({"function": send_habits, "commands": ["habits"]})

from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import check_and_update_habits, send_reminders
import telebot
import os
from .config import TOKEN

bot = telebot.TeleBot(TOKEN)

def send_reminder(chat_id):
    """Отправляет напоминание пользователю в Telegram."""
    bot.send_message(chat_id, "Напоминание: отметьте выполнение своих привычек!")

def start_reminder_listener():
    """Ожидает запросы на напоминания от backend."""
    from flask import Flask, request

    app = Flask(__name__)

    @app.route("/send_reminder/", methods=["POST"])
    def reminder():
        data = request.json
        chat_id = data.get("chat_id")
        if chat_id:
            send_reminder(chat_id)
        return "OK", 200

    app.run(host="0.0.0.0", port=8000)

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(check_and_update_habits, "cron", hour=0)  # Обновление привычек в 00:00
    scheduler.add_job(send_reminders, "interval", hours=1)  # Напоминания каждый час
    scheduler.start()

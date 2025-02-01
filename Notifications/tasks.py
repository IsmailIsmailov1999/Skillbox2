from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Habit, User
from .crud import get_habits, update_habit_streak
import requests
import os

TELEGRAM_BOT_API = os.getenv("TELEGRAM_BOT_API", "http://telegram_bot:8000")

def check_and_update_habits():
    """Обновляет привычки пользователей каждый день."""
    db: Session = SessionLocal()
    habits = get_habits(db)

    for habit in habits:
        if habit.completed_days < habit.target_days:
            habit.completed_days = 0  # Сброс серии, если не выполнена
        else:
            habit.completed_days += 1  # Продолжение серии

        update_habit_streak(db, habit.id, habit.completed_days)

    db.commit()
    db.close()

def send_reminders():
    """Отправляет напоминания пользователям."""
    db: Session = SessionLocal()
    users = db.query(User).all()

    for user in users:
        requests.post(f"{TELEGRAM_BOT_API}/send_reminder/", json={"chat_id": user.chat_id})

    db.close()

# Telegram Habit Tracker

Этот проект представляет собой сервис для управления привычками через Telegram-бота.

## 🚀 Установка и запуск

1. **Склонировать репозиторий**
   ```sh
   git clone https://github.com/your-repo/habit-tracker.git
   cd habit-tracker
   
Настроить переменные окружения Создайте .env и укажите значения:
DATABASE_URL=postgresql://user:password@db/track_habits
SECRET_KEY=supersecretkey
TELEGRAM_BOT_TOKEN=your_bot_token
API_URL=http://backend:8000

Запустить с Docker
docker-compose up --build

Использование
/start – Начать работу
/login – Вход в систему
/habits – Показать список привычек
/add_habit – Добавить привычку
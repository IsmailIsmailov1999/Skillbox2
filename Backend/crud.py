from sqlalchemy.orm import Session
from . import models, schemas

def create_habit(db: Session, habit: schemas.HabitCreate, user_id: int):
    db_habit = models.Habit(name=habit.name, user_id=user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def get_habits(db: Session, user_id: int):
    return db.query(models.Habit).filter(models.Habit.user_id == user_id).all()

def update_habit(db: Session, habit_id: int, habit_data: schemas.HabitUpdate):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        habit.completed_days = habit_data.completed_days
        habit.is_active = habit_data.is_active
        db.commit()
        db.refresh(habit)
    return habit

def delete_habit(db: Session, habit_id: int):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        db.delete(habit)
        db.commit()
    return habit

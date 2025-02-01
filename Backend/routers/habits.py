from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import HabitCreate, HabitResponse
from ..crud import create_habit, get_habits
from ..dependencies import get_db

router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("/", response_model=HabitResponse)
def add_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    return create_habit(db, habit)

@router.get("/", response_model=list[HabitResponse])
def list_habits(db: Session = Depends(get_db)):
    return get_habits(db)

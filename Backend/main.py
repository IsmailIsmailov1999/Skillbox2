from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from typing import List
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .auth import create_access_token, authenticate_user, hash_password, get_current_user
from .database import SessionLocal
from . import models, schemas

@app.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered"}

@app.post("/token/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me/")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return {"username": current_user.username}

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/habits/", response_model=schemas.HabitResponse)
def create_habit(habit: schemas.HabitCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_habit(db, habit, user_id)

@app.get("/habits/", response_model=List[schemas.HabitResponse])
def read_habits(user_id: int, db: Session = Depends(get_db)):
    return crud.get_habits(db, user_id)

@app.put("/habits/{habit_id}", response_model=schemas.HabitResponse)
def update_habit(habit_id: int, habit: schemas.HabitUpdate, db: Session = Depends(get_db)):
    db_habit = crud.update_habit(db, habit_id, habit)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return db_habit

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    db_habit = crud.delete_habit(db, habit_id)
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"message": "Habit deleted"}

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HabitBase(BaseModel):
    name: str

class HabitCreate(HabitBase):
    pass

class HabitUpdate(HabitBase):
    is_active: bool
    completed_days: int

class HabitResponse(HabitBase):
    id: int
    created_at: datetime
    completed_days: int
    is_active: bool

    class Config:
        from_attributes = True

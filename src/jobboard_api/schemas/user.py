from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime   # ← changed from str to datetime!

    class Config:
        from_attributes = True   # this allows SQLModel → Pydantic conversion
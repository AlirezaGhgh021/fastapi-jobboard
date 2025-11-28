from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    description: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    location: Optional[str] = None
    is_remote: bool = False

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    location: Optional[str]
    is_remote: bool
    created_at: datetime
    company_id: int
    owner_id: int

    class Config:
        from_attributes = True
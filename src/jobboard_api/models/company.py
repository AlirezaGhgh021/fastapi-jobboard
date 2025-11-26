from datetime import datetime
from typing import Optional

from sqlalchemy import table
from sqlmodel import SQLModel, Field



class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    created_at : datetime = Field(default_factory=datetime.utcnow)

    #who owns the company
    owner_id: int = Field(foreign_key='user.id')
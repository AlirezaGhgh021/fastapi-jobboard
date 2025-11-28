from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index = True)
    description: str
    salary_min: Optional[int]= None
    salary_max: Optional[int]= None
    location: Optional[str]= None
    is_remote: bool= False
    created_at: datetime = Field(default_factory=datetime.now)

    #Foreign keys
    company_id : int= Field(foreign_key='company.id')
    owner_id: int= Field(foreign_key='user.id')


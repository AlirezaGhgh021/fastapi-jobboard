from datetime import datetime
from typing import Optional

from pydantic.v1 import BaseModel


class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None

class CompanyOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    website: Optional[str]
    logo_url: Optional[str]
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
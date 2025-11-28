from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    cover_letter: Optional[str] = None

class ApplicationOut(BaseModel):
    id: int
    cover_letter: Optional[str]
    resume_path: str
    applied_at: datetime
    job_id: int
    applicant_id: int

    class Config:
        from_attributes = True
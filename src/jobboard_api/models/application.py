from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cover_letter: Optional[str] = None
    resume_path: str | None = Field(default=None, nullable=True)
    applied_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    job_id: int = Field(foreign_key="job.id")
    applicant_id: int = Field(foreign_key="user.id")
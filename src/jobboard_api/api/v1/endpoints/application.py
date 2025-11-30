# src/jobboard_api/api/v1/endpoints/application.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import select
import shutil
import os

from src.jobboard_api.database import AsyncSession, get_db
from src.jobboard_api.models.application import Application
from src.jobboard_api.schemas.application import ApplicationOut
from src.jobboard_api.models.user import User
from src.jobboard_api.models.job import Job
from src.jobboard_api.core.security import get_current_user_final

router = APIRouter(prefix="/applications", tags=["applications"])

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{job_id}/apply", response_model=ApplicationOut, status_code=201)
async def apply_to_job(
    job_id: int,
    cover_letter: str | None = None,
    resume: UploadFile = File(...),                      # ← REQUIRED AGAIN — WORKS 100%
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_final)
):
    # Check job exists
    job = (await db.execute(select(Job).where(Job.id == job_id))).scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Prevent double apply
    if (await db.execute(select(Application).where(
        Application.job_id == job_id,
        Application.applicant_id == current_user.id
    ))).scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already applied")

    # Resume is REQUIRED and validated
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes allowed")

    resume_path = f"{UPLOAD_DIR}/resume_{current_user.id}_{job_id}.pdf"
    with open(resume_path, "wb") as f:
        shutil.copyfileobj(resume.file, f)

    app = Application(
        job_id=job_id,
        applicant_id=current_user.id,
        cover_letter=cover_letter,
        resume_path=resume_path
    )
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return app


@router.get("/me", response_model=list[ApplicationOut])
async def my_applications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_final)
):
    result = await db.execute(select(Application).where(Application.applicant_id == current_user.id))
    return result.scalars().all()
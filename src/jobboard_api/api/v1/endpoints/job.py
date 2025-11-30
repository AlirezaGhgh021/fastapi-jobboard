from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from src.jobboard_api.database import AsyncSession, get_db
from src.jobboard_api.models.job import Job
from src.jobboard_api.schemas.job import JobCreate, JobOut
from src.jobboard_api.models.user import User
from src.jobboard_api.models.company import Company
from src.jobboard_api.core.security import get_current_user, get_current_user_from_cookie

router = APIRouter(prefix='/jobs', tags=['jobs'])

@router.post('/', response_model=JobOut, status_code=status.HTTP_201_CREATED)
async def create_job(
        job_in: JobCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_cookie or get_current_user)
):
    # Get user's company
    result = await db.execute(select(Company).where(Company.owner_id == current_user.id))
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(status_code=403, detail='create a company first')

    job = Job(
        **job_in.dict(),
        company_id=company.id,
        owner_id=current_user.id
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job

@router.get('/', response_model=list[JobOut])
async def list_jobs(db: AsyncSession= Depends(get_db)):
    result = await db.execute(select(Job))
    return result.scalars().all()

@router.get('/{job_id}', response_model=JobOut)
async def get_job(job_id: int, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
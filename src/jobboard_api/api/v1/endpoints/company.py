from errno import EOWNERDEAD

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from jobboard_api.database import AsyncSession, get_db
from jobboard_api.models.company import Company
from jobboard_api.schemas.company import CompanyCreate, CompanyOut
from jobboard_api.models.user import User
from jobboard_api.core.security import get_current_user

router = APIRouter(prefix='/companies', tags=['companies'])

#create my company
@router.post('/', response_model=CompanyOut, status_code=status.HTTP_201_CREATED)
async def create_company(
        company_in : CompanyCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    #One company per user for now
    existing = await db.execute(select(Company).where(Company.owner_id == current_user.id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='You already have a company')

    company = Company(**company_in.dict(), owner_id=current_user.id)
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company

#list all companies
@router.get('/', response_model=list[CompanyOut])
async def list_companies(db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company))
    return result.scalars().all()

#get my company
@router.get('/me', response_model=CompanyOut)
async def my_company(
        db:AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Company).where(Company.owner_id == current_user.id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail='You Dont Have a company yet')
    return company
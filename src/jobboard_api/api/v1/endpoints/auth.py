from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from jobboard_api.database import AsyncSession, get_db
from jobboard_api.models.user import User
from jobboard_api.schemas.user import UserCreate, UserOut
from jobboard_api.core.security import get_password_hash
from jobboard_api.core.security import get_current_user
from src.jobboard_api.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email.lower())
    result = await db.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password and create user
    hashed_password = get_password_hash(user_data.password)   # ← now returns str

    new_user = User(                                          # ← THIS LINE WAS MISSING!
        email=user_data.email.lower(),
        hashed_password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # find user
    statement = select(User).where(User.email == form_data.username.lower())
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={'www-Authenticate': "Bearer"},
        )

    access_token = create_access_token(data={'sub': str(user.id)})
    return {'access_token':access_token, 'token_type':'bearer'}

@router.get('/me', response_model=UserOut)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
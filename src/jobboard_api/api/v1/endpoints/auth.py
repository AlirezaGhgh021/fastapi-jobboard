from fastapi import Response, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from src.jobboard_api.database import AsyncSession, get_db
from src.jobboard_api.models.user import User
from src.jobboard_api.schemas.user import UserCreate, UserOut
from src.jobboard_api.core.security import get_password_hash, get_current_user_from_cookie
from src.jobboard_api.core.security import get_current_user
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
async def login(
    response: Response,                                          # ADD THIS
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    statement = select(User).where(User.email == form_data.username.lower())
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={'sub': str(user.id)})

    # THIS SETS THE COOKIE SO BROWSER STAYS LOGGED IN
    response.set_cookie(
        key="auth_token",
        value=access_token,
        httponly=True,
        secure=False,           # True in production
        samesite="lax",
        max_age=60*60*24*7
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/me', response_model=UserOut)
async def read_user_me(
    cookie_user = Depends(get_current_user_from_cookie),   # tries cookie first
    token_user = Depends(get_current_user),                # falls back to Bearer
):
    if not (cookie_user or token_user):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return cookie_user or token_user
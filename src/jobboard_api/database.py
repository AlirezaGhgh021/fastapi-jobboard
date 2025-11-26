from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# We changed the port to 5433
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5433/jobboard"

# This creates the async engine
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True = we see SQL in terminal (great for learning)

# This is the session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# This function will be used as a FastAPI dependency
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
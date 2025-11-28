from fastapi import FastAPI
from jobboard_api.core.config import settings
from jobboard_api.api.v1.endpoints.auth import router as auth_router  # ← add this
from jobboard_api.api.v1.endpoints.company import router as company_router
from jobboard_api.api.v1.endpoints.job import router as job_router

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    debug=settings.DEBUG
)

@app.get("/")
async def root():
    return {"message": "Welcome to your future job board API! Ready to rule FastAPI?"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


app.include_router(auth_router)
app.include_router(company_router)
app.include_router(job_router)
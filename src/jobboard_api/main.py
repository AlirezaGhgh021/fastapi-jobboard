# src/jobboard_api/main.py
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from src.jobboard_api.core.config import settings
from src.jobboard_api.api.v1.endpoints.auth import router as auth_router
from src.jobboard_api.api.v1.endpoints.company import router as company_router
from src.jobboard_api.api.v1.endpoints.job import router as job_router
from src.jobboard_api.api.v1.endpoints.application import router as application_router

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None
)

# THIS MAKES SWAGGER SHOW EMAIL + PASSWORD FORM
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    return {"message": "JobBoard API — Ready to conquer!"}

app.include_router(auth_router)
app.include_router(company_router)
app.include_router(job_router)
app.include_router(application_router)
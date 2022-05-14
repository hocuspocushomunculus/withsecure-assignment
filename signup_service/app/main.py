from fastapi import FastAPI

from .api.signup import signup

app = FastAPI(
    openapi_url="/api/v1/signupsrv/openapi.json", docs_url="/api/v1/signupsrv/docs"
)

app.include_router(signup, prefix="/api/v1/signupsrv", tags=["signup"])

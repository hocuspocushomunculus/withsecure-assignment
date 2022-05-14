from fastapi import FastAPI

from .api.weather import weather

app = FastAPI(
    openapi_url="/api/v1/weathersrv/openapi.json", docs_url="/api/v1/weathersrv/docs"
)

app.include_router(weather, prefix="/api/v1/weathersrv", tags=["weather"])

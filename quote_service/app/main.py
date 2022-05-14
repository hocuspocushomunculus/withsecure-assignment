from fastapi import FastAPI
from .api.quote import quote

app = FastAPI(
    openapi_url="/api/v1/quotesrv/openapi.json", docs_url="/api/v1/quotesrv/docs"
)

app.include_router(quote, prefix="/api/v1/quotesrv", tags=["quote"])

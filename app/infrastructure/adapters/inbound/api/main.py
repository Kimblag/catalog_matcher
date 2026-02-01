from fastapi import FastAPI

from app.infrastructure.adapters.inbound.api.routers.catalog import \
    catalog_router
from app.infrastructure.adapters.inbound.api.routers.requirements import \
    requirement_router
from app.infrastructure.adapters.inbound.api.routers.templates import \
    template_router

app = FastAPI(
    title="Catalog Requirement Matcher API",
    description="API for matching catalog items with requirements using embeddings and vector search.",
    version="1.0.0",
)


app.include_router(router=catalog_router, prefix="/api")
app.include_router(router=requirement_router, prefix="/api")
app.include_router(router=template_router, prefix="/api")

from app.infrastructure.adapters.inbound.api.middleware.error_handler_middleware import (
    ErrorHandlerMiddleware,
)
from app.infrastructure.adapters.inbound.api.routers.catalog import catalog_router
from app.infrastructure.adapters.inbound.api.routers.requirements import (
    requirement_router,
)
from app.infrastructure.adapters.inbound.api.routers.templates import template_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Catalog Requirement Matcher API",
    description="API for matching catalog items with requirements using embeddings and vector search.",
    version="1.0.0",
)

app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=catalog_router, prefix="/api")
app.include_router(router=requirement_router, prefix="/api")
app.include_router(router=template_router, prefix="/api")

from typing import Any
from pydantic import BaseModel


class CatalogItemDTO(BaseModel):
    item_id: str
    name: str
    category: str | None
    subcategory: str | None
    description: str | None
    unit: str | None
    provider: str | None
    active: bool
    attributes: dict[str, Any]


class CatalogListDTO(BaseModel):
    items: list[CatalogItemDTO]

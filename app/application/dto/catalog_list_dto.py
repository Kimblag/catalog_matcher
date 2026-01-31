from typing import Optional
from pydantic import BaseModel


class CatalogItemDTO(BaseModel):
    item_id: str
    name: str
    category: str
    description: str
    subcategory: Optional[str] = None
    unit: Optional[str] = None
    provider: Optional[str] = None
    active: bool
    attributes: Optional[dict[str, str]] = None


class CatalogListDTO(BaseModel):
    catalog: list[CatalogItemDTO]


from typing import Any
from pydantic import BaseModel


class MatchItemDTO(BaseModel):
    catalog_item_id: str
    name: str
    category: str | None
    subcategory: str | None
    description: str | None
    unit: str | None
    provider: str | None
    attributes: dict[str, Any]
    score: float

class RequirementMatchDTO(BaseModel):
    requirement: dict[str, Any]
    matches: list[MatchItemDTO]

class MatchResultDTO(BaseModel):
    results: list[RequirementMatchDTO]

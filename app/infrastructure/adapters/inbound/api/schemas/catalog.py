from datetime import datetime
from typing import Any
from pydantic import BaseModel


class CatalogListOut(BaseModel):
    catalog: list[dict[str, Any]] = []
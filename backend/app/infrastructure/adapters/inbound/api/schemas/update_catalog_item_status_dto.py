from pydantic import BaseModel


class UpdateCatalogItemStatusDTO(BaseModel):
    active: bool

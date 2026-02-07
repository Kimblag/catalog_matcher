from typing import Optional

from app.domain.exceptions.invalid_catalog_item_exception import InvalidCatalogItemException
from dataclasses import dataclass, field, replace


@dataclass(frozen=True, slots=True)
class CatalogItem:

    item_id: str
    name: str
    category: str
    subcategory: Optional[str]
    description: str
    unit: Optional[str]
    provider: Optional[str]
    active: bool = field(default=True)
    attributes: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        self._validate()


    def _validate(self) -> None:

        # validate if item_id is valid
        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise InvalidCatalogItemException("item_id must be a non-empty string.")

        # Validate name
        if (self.name is not None and not isinstance(self.name, str)) or not self.name.strip():
            raise InvalidCatalogItemException("name is invalid.")

        # Validate category
        if (self.category is not None and not isinstance(self.category, str)) or not self.category.strip():
            raise InvalidCatalogItemException("category is invalid.")

        # Validate description
        if (self.description is not None and not isinstance(self.description, str)) or not self.description.strip():
            raise InvalidCatalogItemException("description is invalid.")

        # Validate the optional if there is one
        if self.attributes is not None and not isinstance(self.attributes, dict):
            raise InvalidCatalogItemException("attributes is invalid. It must be a dictionary.")
        if self.unit is not None and (not isinstance(self.unit, str) or not self.unit.strip()):
            raise InvalidCatalogItemException("unit is invalid. It must be a non-empty string.")
        if self.provider is not None and (not isinstance(self.provider, str) or not self.provider.strip()):
            raise InvalidCatalogItemException("provider is invalid. It must be a non-empty string.")
        if self.subcategory is not None and (not isinstance(self.subcategory, str) or not self.subcategory.strip()):
            raise InvalidCatalogItemException("subcategory is invalid. It must be a non-empty string.")


    def _replace_and_validate(self, **changes) -> "CatalogItem":
        new_item = replace(self, **changes)
        new_item._validate()
        return new_item

    # Behavior
    def update_status(self, active: bool) -> "CatalogItem":
        return self._replace_and_validate(active=active)

    def update_name(self, new_name: str) -> "CatalogItem":
        return self._replace_and_validate(name=new_name)

    def update_attributes(self, new_attributes: dict[str, str]) -> "CatalogItem":
        # merge dictonaries
        updated_attrs = {**self.attributes, **new_attributes}
        return self._replace_and_validate(attributes=updated_attrs)

    def replace_attributes(self, new_attributes: dict[str, str]) -> "CatalogItem":
        return self._replace_and_validate(attributes=new_attributes)

    def update_description(self, new_description: str) -> "CatalogItem":
        return self._replace_and_validate(description=new_description)

    def update_category(self, new_category: str) -> "CatalogItem":
        return self._replace_and_validate(category=new_category)

    def update_unit(self, new_unit: str) -> "CatalogItem":
        return self._replace_and_validate(unit=new_unit)

    def update_provider(self, new_provider: str) -> "CatalogItem":
        return self._replace_and_validate(provider=new_provider)

    def update_subcategory(self, new_subcategory: str) -> "CatalogItem":
        return self._replace_and_validate(subcategory=new_subcategory)
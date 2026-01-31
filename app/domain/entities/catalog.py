from datetime import datetime
from typing import Any, Optional

from app.domain.entities.catalog_item import CatalogItem
from app.domain.enums.catalog_sources import CatalogSource
from app.domain.exceptions.item_not_found_exception import ItemNotFoundException


class Catalog:
    version: int
    last_updated: datetime
    source: CatalogSource
    items: dict[str, CatalogItem]

    def __init__(self, catalog_source: CatalogSource = CatalogSource.MANUAL):
        self.version: int = 0
        self.last_updated: datetime = datetime.now()
        self.source: CatalogSource = catalog_source
        self.items: dict[str, CatalogItem] = {}


    # Behavior
    ## Add update item
    def add_or_update_item(self,
                           item_id: str,
                           name: Optional[str] = None,
                           category: Optional[str] = None,
                           description: Optional[str] = None,
                           subcategory: Optional[str] = None,
                           unit: Optional[str] = None,
                           provider: Optional[str] = None,
                           attributes: Optional[dict[str, str]] = None,
                           ) -> None:
        # Verify if it exists
        existing_item = self.items.get(item_id, None)

        # if not exists, create it
        if existing_item is None:
            new_item = CatalogItem(
                item_id=item_id,
                name=name,
                category=category,
                description=description,
                subcategory=subcategory,
                unit=unit,
                provider=provider,
                attributes=attributes or {},
            )
            self.items[item_id] = new_item
        else:
            # update
            updated_item = existing_item

            if name is not None:
                updated_item = updated_item.update_name(name)
            if category is not None:
                updated_item = updated_item.update_category(category)
            if description is not None:
                updated_item = updated_item.update_description(description)
            if subcategory is not None:
                updated_item = updated_item.update_subcategory(subcategory)
            if unit is not None:
                updated_item = updated_item.update_unit(unit)
            if provider is not None:
                updated_item = updated_item.update_provider(provider)
            if attributes is not None:
                updated_item = updated_item.replace_attributes(attributes)

            self.items[item_id] = updated_item

        # update version and last updated
        self.version += 1
        self.last_updated = datetime.now()


    def _add_or_update_item_internal(
        self,
        item_id: str,
        name: Optional[str],
        category: Optional[str],
        description: Optional[str],
        subcategory: Optional[str],
        unit: Optional[str],
        provider: Optional[str],
        attributes: Optional[dict[str, str]],
    ) -> None:
        """Internal method to add items by batches."""
        existing_item = self.items.get(item_id)

        if existing_item is None:
            self.items[item_id] = CatalogItem(
                item_id=item_id,
                name=name,
                category=category,
                description=description,
                subcategory=subcategory,
                unit=unit,
                provider=provider,
                attributes=attributes or {},
            )
        else:
            updated_item = existing_item
            if name is not None:
                updated_item = updated_item.update_name(name)
            if category is not None:
                updated_item = updated_item.update_category(category)
            if description is not None:
                updated_item = updated_item.update_description(description)
            if subcategory is not None:
                updated_item = updated_item.update_subcategory(subcategory)
            if unit is not None:
                updated_item = updated_item.update_unit(unit)
            if provider is not None:
                updated_item = updated_item.update_provider(provider)
            if attributes is not None:
                updated_item = updated_item.replace_attributes(attributes)

            self.items[item_id] = updated_item


    ## add or update in batches
    def add_or_update_items_batch(self, list_items: list[dict[str, Any]]) -> dict[str, Any]:
        errors: dict[str, Any] = {}

        for item in list_items:
            item_id = item.get("item_id", None)
            if not item_id:
                errors[item_id or f"no_id_{len(errors)}"] = "Missing item_id"
                continue

            try:
                self._add_or_update_item_internal(
                    item_id=item_id,
                    name=item.get("name"),
                    category=item.get("category"),
                    description=item.get("description"),
                    subcategory=item.get("subcategory"),
                    unit=item.get("unit"),
                    provider=item.get("provider"),
                    attributes=item.get("attributes", {}),
                )
            except Exception as e:
                 errors[item_id] = str(e)

        
        if len(errors) != len(list_items):
            self.version += 1
            self.last_updated = datetime.now()

        return errors


    ## activate item
    def activate_item(self, item_id: str) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        activated_item = existing_item.activate()
        self.items[item_id] = activated_item


    ## deactivate item
    def deactivate_item(self, item_id: str) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        deactivated_item = existing_item.deactivate()
        self.items[item_id] = deactivated_item


    ## update_item_name
    def update_item_name(self, item_id: str, new_name: str) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        updated_item = existing_item.update_name(new_name)
        self.items[item_id] = updated_item

    ## update_item_category
    def update_item_category(self, item_id: str, new_category: str) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        updated_item = existing_item.update_category(new_category)
        self.items[item_id] = updated_item

    ## update_item_subcategory
    def update_item_subcategory(self, item_id: str, new_subcategory: str) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        updated_item = existing_item.update_subcategory(new_subcategory)
        self.items[item_id] = updated_item

    ## update_item_description
    def update_item_description(self, item_id: str, new_description: str) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        updated_item = existing_item.update_description(new_description)
        self.items[item_id] = updated_item

    ## update_item_unit
    def update_item_unit(self, item_id: str, new_unit: str) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        updated_item = existing_item.update_unit(new_unit)
        self.items[item_id] = updated_item

    ## update_item_provider
    def update_item_provider(self, item_id: str, new_provider: str) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        updated_item = existing_item.update_provider(new_provider)
        self.items[item_id] = updated_item
   
   
    ## update_item_attributes
    def update_item_attributes(self, item_id: str, new_attributes: dict[str, str]) -> None:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        updated_item = existing_item.replace_attributes(new_attributes)
        self.items[item_id] = updated_item

    # Getters

    ## get_version
    def get_version(self) -> int:
        return self.version

    ## get_last_updated
    def get_last_updated(self) -> datetime:
        return self.last_updated

    ## get_source
    def get_source(self) -> str:
        return self.source.name

    ## get_items
    def get_items(self) -> dict[str, CatalogItem]:
        return self.items.copy()

    ## get_item
    def get_item(self, item_id: str) -> CatalogItem:
        existing_item = self.items.get(item_id, None)
        if existing_item is None:
            raise ItemNotFoundException()
        return existing_item
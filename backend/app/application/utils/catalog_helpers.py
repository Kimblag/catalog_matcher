from typing import Any
from app.application.exceptions.unsupported_catalog_source_exception import UnsupportedCatalogSourceException
from app.domain.enums.catalog_sources import CatalogSource
from app.domain.entities.catalog_item import CatalogItem


def resolve_source(file_path: str) -> CatalogSource:
        extension = file_path.rsplit(".", 1)[-1].lower()

        if extension == "csv":
            return CatalogSource.CSV
        if extension == "xlsx":
            return CatalogSource.XLSX

        raise UnsupportedCatalogSourceException(extension)


def convert_to_catalog_items(
    items_data: list[dict[str, Any]]
) -> list[CatalogItem]:
    catalog_items = []

    for item_data in items_data:
        catalog_item = CatalogItem(
            item_id=item_data["item_id"],
            name=item_data["name"],
            category=item_data["category"],
            description=item_data["description"],
            subcategory=item_data.get("subcategory"),
            unit=item_data.get("unit"),
            provider=item_data.get("provider"),
            attributes=item_data.get("attributes", {}),
        )
        catalog_items.append(catalog_item)

    return catalog_items
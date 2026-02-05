# Contexto
## Domain
### Entidades
```python
class Catalog:
    version: int
    last_updated: datetime
    source: CatalogSource
    items: dict[str, CatalogItem]

    def __init__(self, catalog_source: CatalogSource):
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
    def batch_upsert(self, list_items: list[dict[str, Any]]) -> dict[str, str]:
        errors: dict[str, str] = {}

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
                    attributes=item.get("attributes", None),
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

```

```python
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
    def activate(self) -> "CatalogItem":
        return self._replace_and_validate(active=True)

    def deactivate(self):
        return replace(self, active=False)

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
```


### Enums
```python
from enum import Enum
class CatalogSource(Enum):
    CSV = 'CSV'
    JSON = 'JSON'
    MANUAL = 'MANUAL'
    XLSX = 'XLSX'
```

## Application
### Ports
```python

class CatalogRepository(Protocol):
    def get(self) -> list[dict[str, Any]]:
        ...
    def save(self, catalog: list[dict[str, Any]]) -> None:
        ...
```

```python
from typing import Protocol
class FileReader(Protocol):
    def read_catalog(self, file_path: str) -> list[dict[str, Any]]:
        ...


    def read_requirements(self, file_path: str) -> list[dict[str, Any]]:
        ...
```

```python
from typing import Protocol
class NormalizerCatalog(Protocol):
    def normalize_catalog_items(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ...

class NormalizerRequirement(Protocol):
    def normalize_requirements(
        self,
        raw_requirements: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        ...
```

```python
from typing import Protocol
class VectorRepository(Protocol):
    def save(self, items: list[dict]) -> None:
        ...

    def search(self, query_embedding: list[float], top_k: int) -> list[tuple[str, float]]:
        ...
```

```python
from typing import Protocol
class EmbeddingService(Protocol):
    def get_embedding(self, text: str) -> list[float]:
        ...
```

### Normalizer de catalog catalog_normalizer y de requirements
```python
from app.application.exceptions.catalog_normalization_exception import CatalogNormalizationException
from app.application.ports.normalizer import Normalizer


class CatalogNormalizer(Normalizer):
    _REQUIRED_FIELDS: set[str] = {
        "item_id",
        "name",
        "category",
        "description",
    }

    _OPTIONAL_FIELDS: set[str] = {
        "subcategory",
        "unit",
        "provider",
        "attributes",
    }

    def normalize_catalog_items(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []

        for index, item in enumerate(raw_items):
            if not isinstance(item, dict):
                raise CatalogNormalizationException(
                     f"Item at index {index} is not a dictionary."
                )
            normalized_item = self._normalize_item(item, index)
            normalized.append(normalized_item)
            
        return normalized

    
    def _normalize_item(self, item: dict[str, str], index: int) -> dict[str, str]:
        normalized_item: dict[str, str] = {}

        # normalize keys
        for key, value in item.items():
            # remove blanks and pass to lower case
            normalized_key = key.strip().lower()
            normalized_value = value.strip().lower() if isinstance(value, str) else value
            normalized_item[normalized_key] = normalized_value

        # Validate required fields
        missing = self._REQUIRED_FIELDS - normalized_item.keys()
        if missing:
            raise CatalogNormalizationException(
                f"Item at index {index} is missing required fields: {missing}"
                )

        return normalized_item
```

```python
class RequirementNormalizer(NormalizerRequirement):
    _REQUIRED_FIELDS: set[str] = {
        "name",
        "quantity",
        "unit"
   }
    
    _OPTIONAL_FIELDS: set[str] = {
        "description",
        "category",
        "subcategory",
        "priority",
        "provider",
        "attributes"
    }

    def normalize_requirement_items(self, raw_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized: list[dict[str, Any]] = []

        for index, item in enumerate(raw_items):
            if not isinstance(item, dict):
                raise RequirementNormalizationException(
                     f"Item at index {index} is not a dictionary."
                )
            normalized_item = self._normalize_item(item, index)
            normalized.append(normalized_item)
            
        return normalized

    
    def _normalize_item(self, item: dict[str, str], index: int) -> dict[str, str]:
        normalized_item: dict[str, str] = {}

        # normalize keys
        for key, value in item.items():
            # remove blanks and pass to lower case
            normalized_key = key.strip().lower()
            normalized_value = value.strip().lower() if isinstance(value, str) else value
            normalized_item[normalized_key] = normalized_value

        # Validate required fields
        missing = self._REQUIRED_FIELDS - normalized_item.keys()
        if missing:
            raise RequirementNormalizationException(
                f"Item at index {index} is missing required fields: {missing}"
                )
        return normalized_item
```

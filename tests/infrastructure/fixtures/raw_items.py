import pytest
from typing import Any

@pytest.fixture
def raw_catalog_items_valid() -> list[dict[str, Any]]:
    return [
        {
            "item_id": "ITEM-001",
            "name": "Tornillo",
            "category": "Ferretería",
            "description": "Tornillo de acero",
            "unit": "unidad",
            "provider": "Acme",
        },
        {
            "item_id": "ITEM-002",
            "name": "Tuerca",
            "category": "Ferretería",
            "description": "Tuerca hexagonal",
            "unit": "unidad",
            "provider": "Acme",
        },
        {
            "item_id": "ITEM-003",
            "name": "Arandela",
            "category": "Ferretería",
            "description": "Arandela de metal",
            "unit": "unidad",
            "provider": "Beta",
        },
        {
            "item_id": "ITEM-004",
            "name": "Clavo",
            "category": "Ferretería",
            "description": "Clavo de acero inoxidable",
            "unit": "unidad",
            "provider": "Acme",
        },
        {
            "item_id": "ITEM-005",
            "name": "Martillo",
            "category": "Herramientas",
            "description": "Martillo de carpintero",
            "unit": "unidad",
            "provider": "Delta",
        },
        {
            "item_id": "ITEM-006",
            "name": "Destornillador",
            "category": "Herramientas",
            "description": "Destornillador plano 10cm",
            "unit": "unidad",
            "provider": "Delta",
        },
    ]

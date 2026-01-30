from enum import Enum


class CatalogSource(Enum):
    CSV = 'CSV'
    JSON = 'JSON'
    MANUAL = 'MANUAL'
    XLSX = 'XLSX'
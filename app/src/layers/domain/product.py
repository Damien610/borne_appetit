from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Category:
    uuid: str
    name: str
    icon_url: str
    description: str


@dataclass
class Product:
    uuid: str
    name: str
    image_url: str
    price: float
    description: str
    categories: List[str]
    allergens: str
    nutritional_values: str

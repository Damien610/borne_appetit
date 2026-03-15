from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Restaurant:
    uuid: str
    name: str
    uri_name: str
    logo: Optional[str] = None
    favicon: Optional[str] = None
    welcome_image: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    primary_hexa: Optional[str] = None
    secondary_hexa: Optional[str] = None

@dataclass
class Terminal:
    uuid: str
    restaurant_uuid: str
    name: str
    location: Optional[str] = None

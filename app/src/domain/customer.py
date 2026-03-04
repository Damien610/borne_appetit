from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    """Entité Client"""
    restaurant_id: str
    customer_id: str
    email: str
    loyalty_code: str
    loyalty_points: int = 0
    order_date: Optional[datetime] = None

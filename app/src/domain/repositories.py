from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import Restaurant, Terminal
from domain.customer import Customer

class RestaurantRepository(ABC):
    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[Restaurant]:
        pass
    
    @abstractmethod
    def get_by_uri(self, uri: str) -> Optional[Restaurant]:
        pass

class TerminalRepository(ABC):
    @abstractmethod
    def get_by_uuid(self, uuid: str) -> Optional[Terminal]:
        pass

class CustomerRepository(ABC):
    @abstractmethod
    def get_by_email(self, restaurant_id: str, email: str) -> Optional[Customer]:
        pass
    
    @abstractmethod
    def get_by_loyalty_code(self, loyalty_code: str) -> Optional[Customer]:
        pass
    
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        pass
    
    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        pass

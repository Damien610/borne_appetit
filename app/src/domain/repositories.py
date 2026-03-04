from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import Restaurant, Terminal

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

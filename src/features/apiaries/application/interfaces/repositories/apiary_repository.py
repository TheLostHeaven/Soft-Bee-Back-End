from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.features.apiaries.domain.entities.apiary import Apiary

class ApiaryRepository(ABC):
    @abstractmethod
    def get_all_apiaries(self) -> List[Apiary]:
        pass

    @abstractmethod
    def get_apiary_by_id(self, apiary_id: UUID) -> Optional[Apiary]:
        pass

    @abstractmethod
    def create_apiary(self, apiary: Apiary) -> Apiary:
        pass

    @abstractmethod
    def update_apiary(self, apiary: Apiary) -> Apiary:
        pass

    @abstractmethod
    def delete_apiary(self, apiary_id: UUID) -> None:
        pass

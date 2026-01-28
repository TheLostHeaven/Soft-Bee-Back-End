from abc import ABC, abstractmethod
from typing import List, Optional
from src.features.apiaries.domain.entities.apiary import Apiary

class ApiaryRepository(ABC):
    @abstractmethod
    def get_all_apiaries(self) -> List[Apiary]:
        pass

    @abstractmethod
    def get_all_apiaries_by_user_id(self, user_id: str) -> List[Apiary]:
        pass

    @abstractmethod
    def get_apiary_by_id(self, apiary_id: str) -> Optional[Apiary]:
        pass
    
    @abstractmethod
    def get_apiary_by_id_and_user_id(self, apiary_id: str, user_id: str) -> Optional[Apiary]:
        pass

    @abstractmethod
    def find_by_user_id_and_name(self, user_id: str, name: str) -> Optional[Apiary]:
        pass

    @abstractmethod
    def create_apiary(self, apiary: Apiary) -> Apiary:
        pass

    @abstractmethod
    def update_apiary(self, apiary: Apiary) -> Apiary:
        pass

    @abstractmethod
    def delete_apiary(self, apiary_id: str) -> None:
        pass

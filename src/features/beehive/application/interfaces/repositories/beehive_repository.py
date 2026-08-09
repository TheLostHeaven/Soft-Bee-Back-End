from abc import ABC, abstractmethod
from typing import List, Optional
from src.features.beehive.domain.entities.beehive import Beehive
from src.features.beehive.application.dto.beehive_dto import CreateBeehiveDTO, UpdateBeehiveDTO
from uuid import UUID

class IBeehiveRepository(ABC):
    @abstractmethod
    def create_beehive(self, beehive_dto: CreateBeehiveDTO) -> Beehive:
        pass

    @abstractmethod
    def get_beehive_by_id(self, id: UUID) -> Optional[Beehive]:
        pass

    @abstractmethod
    def get_all_beehives_by_apiary_id(self, apiary_id: UUID) -> List[Beehive]:
        pass

    @abstractmethod
    def update_beehive(self, id: UUID, beehive_dto: UpdateBeehiveDTO) -> Beehive:
        pass

    @abstractmethod
    def delete_beehive(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def exists_by_apiary_and_number(self, apiary_id: UUID, hive_number: int) -> bool:
        pass

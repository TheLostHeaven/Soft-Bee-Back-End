from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.features.treatments.domain.entities.treatment import Treatment, TreatmentFollowup

class TreatmentRepository(ABC):
    @abstractmethod
    def save(self, treatment: Treatment) -> Treatment:
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> Optional[Treatment]:
        pass

    @abstractmethod
    def find_by_hive_id(self, hive_id: UUID) -> List[Treatment]:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def save_followup(self, followup: TreatmentFollowup) -> TreatmentFollowup:
        pass

    @abstractmethod
    def delete_followup(self, followup_id: UUID) -> bool:
        pass

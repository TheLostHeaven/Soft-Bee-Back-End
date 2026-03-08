from typing import List
from uuid import UUID
from src.features.treatments.application.dto.treatment_dto import TreatmentDTO
from src.features.treatments.application.interfaces.repositories.treatment_repository import TreatmentRepository
from src.features.treatments.application.mappers.treatment_mapper import TreatmentMapper

class GetTreatmentsByHiveUseCase:
    def __init__(self, repository: TreatmentRepository):
        self.repository = repository

    def execute(self, hive_id: UUID) -> List[TreatmentDTO]:
        treatments = self.repository.find_by_hive_id(hive_id)
        return [TreatmentMapper.to_dto(t) for t in treatments]

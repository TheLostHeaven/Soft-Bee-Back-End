from uuid import UUID
from typing import Optional
from src.features.treatments.application.dto.treatment_dto import TreatmentDTO
from src.features.treatments.application.interfaces.repositories.treatment_repository import TreatmentRepository
from src.features.treatments.application.mappers.treatment_mapper import TreatmentMapper

class GetTreatmentByIdUseCase:
    def __init__(self, repository: TreatmentRepository):
        self.repository = repository

    def execute(self, id: UUID) -> Optional[TreatmentDTO]:
        treatment = self.repository.find_by_id(id)
        if not treatment:
            return None
        return TreatmentMapper.to_dto(treatment)

from uuid import UUID
from src.features.treatments.application.interfaces.repositories.treatment_repository import TreatmentRepository

class DeleteTreatmentUseCase:
    def __init__(self, repository: TreatmentRepository):
        self.repository = repository

    def execute(self, id: UUID) -> bool:
        return self.repository.delete(id)

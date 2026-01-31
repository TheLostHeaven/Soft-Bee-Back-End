from src.features.beehive.application.interfaces.repositories.beehive_repository import IBeehiveRepository
from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException
from uuid import UUID

class DeleteBeehiveUseCase:
    def __init__(self, repository: IBeehiveRepository):
        self.repository = repository

    def execute(self, beehive_id: UUID) -> bool:
        if not self.repository.delete_beehive(beehive_id):
            raise BeehiveNotFoundException(beehive_id)
        return True

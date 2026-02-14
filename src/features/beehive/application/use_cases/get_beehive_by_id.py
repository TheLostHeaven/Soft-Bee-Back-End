from typing import Optional
from src.features.beehive.application.dto.beehive_dto import BeehiveDTO
from src.features.beehive.application.interfaces.repositories.beehive_repository import IBeehiveRepository
from src.features.beehive.application.mappers.beehive_mapper import BeehiveMapper
from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException
from uuid import UUID


class GetBeehiveByIdUseCase:
    def __init__(self, repository: IBeehiveRepository):
        self.repository = repository

    def execute(self, id: UUID) -> Optional[BeehiveDTO]:
        beehive = self.repository.get_beehive_by_id(id)
        if not beehive:
            raise BeehiveNotFoundException(id)
        return BeehiveMapper.to_dto(beehive)

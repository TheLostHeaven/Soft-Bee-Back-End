from typing import List
from src.features.beehive.application.dto.beehive_dto import BeehiveDTO
from src.features.beehive.application.interfaces.repositories.beehive_repository import IBeehiveRepository
from src.features.beehive.application.mappers.beehive_mapper import BeehiveMapper
from uuid import UUID

class GetAllBeehivesByApiaryIdUseCase:
    def __init__(self, repository: IBeehiveRepository):
        self.repository = repository

    def execute(self, apiary_id: UUID) -> List[BeehiveDTO]:
        beehives = self.repository.get_all_beehives_by_apiary_id(apiary_id)
        return [BeehiveMapper.to_dto(beehive) for beehive in beehives]

from src.features.beehive.application.dto.beehive_dto import UpdateBeehiveDTO, BeehiveDTO
from src.features.beehive.application.interfaces.repositories.beehive_repository import IBeehiveRepository
from src.features.beehive.application.mappers.beehive_mapper import BeehiveMapper
from uuid import UUID


class UpdateBeehiveUseCase:
    def __init__(self, repository: IBeehiveRepository):
        self.repository = repository

    def execute(self, beehive_id: UUID, beehive_dto: UpdateBeehiveDTO) -> BeehiveDTO:
        beehive = self.repository.update_beehive(beehive_id, beehive_dto)
        return BeehiveMapper.to_dto(beehive)

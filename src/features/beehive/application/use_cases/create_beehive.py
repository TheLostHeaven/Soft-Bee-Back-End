from src.features.beehive.application.dto.beehive_dto import CreateBeehiveDTO, BeehiveDTO
from src.features.beehive.application.interfaces.repositories.beehive_repository import IBeehiveRepository
from src.features.beehive.application.mappers.beehive_mapper import BeehiveMapper


class CreateBeehiveUseCase:
    def __init__(self, repository: IBeehiveRepository):
        self.repository = repository

    def execute(self, beehive_dto: CreateBeehiveDTO) -> BeehiveDTO:
        beehive = self.repository.create_beehive(beehive_dto)
        return BeehiveMapper.to_dto(beehive)

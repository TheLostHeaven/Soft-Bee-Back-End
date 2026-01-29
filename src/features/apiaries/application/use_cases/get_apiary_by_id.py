from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError
from uuid import UUID

class GetApiaryById:
    def __init__(self, apiary_repository: ApiaryRepository):
        self.apiary_repository = apiary_repository

    def execute(self, apiary_id: UUID) -> ApiaryDto:
        apiary = self.apiary_repository.get_apiary_by_id(apiary_id)
        if not apiary:
            raise ApiaryNotFoundError(f"Apiary with ID '{apiary_id}' not found.")
        return ApiaryMapper.to_dto(apiary)

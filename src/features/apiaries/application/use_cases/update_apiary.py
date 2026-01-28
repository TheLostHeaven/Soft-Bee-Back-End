from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto, UpdateApiaryDto
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError, PermissionDeniedException

class UpdateApiary:
    def __init__(self, apiary_repository: ApiaryRepository):
        self.apiary_repository = apiary_repository

    def execute(self, apiary_id: str, update_dto: UpdateApiaryDto, authenticated_user_id: str) -> ApiaryDto:
        existing_apiary = self.apiary_repository.get_apiary_by_id_and_user_id(apiary_id, authenticated_user_id)
        if not existing_apiary:
            raise ApiaryNotFoundError(f"Apiary with ID '{apiary_id}' not found or you don't have permission to access it.")
        
        updated_apiary_entity = ApiaryMapper.from_update_dto_to_entity(update_dto, existing_apiary)
        updated_apiary = self.apiary_repository.update_apiary(updated_apiary_entity)
        return ApiaryMapper.to_dto(updated_apiary)

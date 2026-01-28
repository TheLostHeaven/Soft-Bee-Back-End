from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto, CreateApiaryDto
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper
from src.features.apiaries.domain.entities.apiary import Apiary
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryAlreadyExistsError, PermissionDeniedException

class CreateApiary:
    def __init__(self, apiary_repository: ApiaryRepository):
        self.apiary_repository = apiary_repository

    def execute(self, create_dto: CreateApiaryDto, authenticated_user_id: str) -> ApiaryDto:
        if str(create_dto.user_id) != authenticated_user_id:
            raise PermissionDeniedException("Cannot create apiaries for another user.")

        # Check if an apiary with the same name already exists for the same user
        existing_apiary = self.apiary_repository.find_by_user_id_and_name(authenticated_user_id, create_dto.name)
        
        if existing_apiary:
            raise ApiaryAlreadyExistsError(f"Apiary with name '{create_dto.name}' already exists for this user.")

        apiary_entity = ApiaryMapper.from_create_dto_to_entity(create_dto)
        created_apiary = self.apiary_repository.create_apiary(apiary_entity)
        return ApiaryMapper.to_dto(created_apiary)

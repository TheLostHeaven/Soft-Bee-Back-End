import logging
from src.features.user.application.interfaces.repositories.user_repository_interface import IUserRepository
from src.features.user.application.dto.user_dto import UserDTO, UpdateUserDTO
from src.features.user.application.mappers.user_mapper import UserMapper
from src.features.user.domain.exceptions.user_exceptions import UserNotFoundError
from uuid import UUID

logger = logging.getLogger(__name__)

class UpdateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID, update_dto: UpdateUserDTO) -> UserDTO:
        logger.info(f"UpdateUserUseCase: Executing for user_id={user_id}, update_dto={update_dto}")
        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            logger.warning(f"UpdateUserUseCase: User with ID '{user_id}' not found.")
            raise UserNotFoundError(f"User with ID '{user_id}' not found.")
        
        updated_user_entity = UserMapper.from_update_dto_to_entity(update_dto, existing_user)
        logger.info(f"UpdateUserUseCase: Mapped to updated_user_entity (username={updated_user_entity.username}, email={updated_user_entity.email.value}, phone={updated_user_entity.phone})")
        
        updated_user = self.user_repository.update(updated_user_entity)
        return UserMapper.to_dto(updated_user)

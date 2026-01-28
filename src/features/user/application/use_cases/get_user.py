from src.features.user.application.interfaces.repositories.user_repository_interface import IUserRepository
from src.features.user.application.dto.user_dto import UserDTO
from src.features.user.application.mappers.user_mapper import UserMapper
from src.features.user.domain.exceptions.user_exceptions import UserNotFoundError
from uuid import UUID

class GetUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> UserDTO:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with ID '{user_id}' not found.")
        return UserMapper.to_dto(user)
from src.features.user.application.interfaces.repositories.user_repository_interface import IUserRepository
from src.features.user.domain.exceptions.user_exceptions import UserNotFoundError
from uuid import UUID

class DeleteUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> None:
        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise UserNotFoundError(f"User with ID '{user_id}' not found.")
        
        self.user_repository.delete(user_id)

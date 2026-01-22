from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError

class DeleteApiary:
    def __init__(self, apiary_repository: ApiaryRepository):
        self.apiary_repository = apiary_repository

    def execute(self, apiary_id: str) -> None:
        existing_apiary = self.apiary_repository.get_apiary_by_id(apiary_id)
        if not existing_apiary:
            raise ApiaryNotFoundError(f"Apiary with ID '{apiary_id}' not found.")
        
        self.apiary_repository.delete_apiary(apiary_id)

from typing import List
from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper

class GetAllApiaries:
    def __init__(self, apiary_repository: ApiaryRepository):
        self.apiary_repository = apiary_repository

    def execute(self, user_id: str) -> List[ApiaryDto]:
        apiaries = self.apiary_repository.get_all_apiaries_by_user_id(user_id)
        return [ApiaryMapper.to_dto(apiary) for apiary in apiaries]

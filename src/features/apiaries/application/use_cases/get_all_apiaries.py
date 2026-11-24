from typing import List
from src.core.pagination import Page
from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper

class GetAllApiaries:
    def __init__(self, apiary_repository: ApiaryRepository):
        self.apiary_repository = apiary_repository

    def execute(self) -> List[ApiaryDto]:
        apiaries = self.apiary_repository.get_all_apiaries()
        return [ApiaryMapper.to_dto(apiary) for apiary in apiaries]

    def execute_paginated(self, limit: int, offset: int) -> Page[ApiaryDto]:
        page = self.apiary_repository.get_all_apiaries_paginated(limit, offset)
        return Page(
            items=[ApiaryMapper.to_dto(apiary) for apiary in page.items],
            total=page.total,
            limit=page.limit,
            offset=page.offset,
        )

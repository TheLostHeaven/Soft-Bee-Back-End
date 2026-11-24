from typing import List
from uuid import UUID
from src.core.pagination import Page
from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper

class GetApiariesByUserId:
    def __init__(self, apiary_repository: ApiaryRepository):
        self.apiary_repository = apiary_repository

    def execute(self, user_id: UUID) -> List[ApiaryDto]:
        apiaries = self.apiary_repository.get_apiaries_by_user_id(user_id)
        return [ApiaryMapper.to_dto(apiary) for apiary in apiaries]

    def execute_paginated(self, user_id: UUID, limit: int, offset: int) -> Page[ApiaryDto]:
        page = self.apiary_repository.get_apiaries_by_user_id_paginated(user_id, limit, offset)
        return Page(
            items=[ApiaryMapper.to_dto(apiary) for apiary in page.items],
            total=page.total,
            limit=page.limit,
            offset=page.offset,
        )

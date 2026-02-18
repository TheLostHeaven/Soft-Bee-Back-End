from typing import List
from uuid import UUID
from src.features.inventory.application.dto.inventory_summary_dto import (
    ApiaryInventorySummaryDTO,
)
from src.features.apiaries.application.interfaces.repositories.apiary_repository import (
    ApiaryRepository,
)
from src.features.inventory.application.interfaces.repositories.inventory_repository import (
    InventoryRepository,
)
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper
from src.features.inventory.application.mappers.inventory_mapper import InventoryMapper


class GetInventorySummaryUseCase:
    def __init__(
        self,
        apiary_repository: ApiaryRepository,
        inventory_repository: InventoryRepository,
    ):
        self.apiary_repository = apiary_repository
        self.inventory_repository = inventory_repository

    def execute(self, user_id: UUID) -> List[ApiaryInventorySummaryDTO]:
        apiaries = self.apiary_repository.get_apiaries_by_user_id(user_id)
        summary = []

        for apiary in apiaries:
            inventories = self.inventory_repository.get_all(apiary.id)

            apiary_dto = ApiaryMapper.to_dto(apiary)
            inventory_dtos = [InventoryMapper.to_dto(inv) for inv in inventories]

            summary.append(
                ApiaryInventorySummaryDTO(apiary=apiary_dto, inventories=inventory_dtos)
            )

        return summary

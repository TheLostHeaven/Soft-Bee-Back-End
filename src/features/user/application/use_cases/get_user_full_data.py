from uuid import UUID
from typing import List

from src.features.user.application.use_cases.get_user import GetUserUseCase
from src.features.apiaries.application.use_cases.get_apiaries_by_user_id import GetApiariesByUserId
from src.features.beehive.application.use_cases.get_all_beehives_by_apiary_id import GetAllBeehivesByApiaryIdUseCase
from src.features.inventory.application.use_cases.get_inventories_by_apiary_use_case import GetInventoriesByApiaryUseCase
from src.features.inventory.application.mappers.inventory_mapper import InventoryMapper
from src.features.user.application.dto.user_full_data_dto import UserFullDataDTO, ApiaryFullDataDTO

class GetUserFullDataUseCase:
    def __init__(
        self,
        get_user_use_case: GetUserUseCase,
        get_apiaries_use_case: GetApiariesByUserId,
        get_beehives_use_case: GetAllBeehivesByApiaryIdUseCase,
        get_inventories_use_case: GetInventoriesByApiaryUseCase
    ):
        self.get_user_use_case = get_user_use_case
        self.get_apiaries_use_case = get_apiaries_use_case
        self.get_beehives_use_case = get_beehives_use_case
        self.get_inventories_use_case = get_inventories_use_case

    def execute(self, user_id: UUID) -> UserFullDataDTO:
        # 1. Get User
        user_dto = self.get_user_use_case.execute(user_id)
        if not user_dto:
            return None

        # 2. Get Apiaries
        apiaries_dto = self.get_apiaries_use_case.execute(user_id)
        
        full_apiaries: List[ApiaryFullDataDTO] = []
        
        for apiary in apiaries_dto:
            # 3. Get Beehives for each apiary
            beehives = self.get_beehives_use_case.execute(apiary.id)
            
            # 4. Get Inventory for each apiary
            inventory_entities = self.get_inventories_use_case.execute(apiary.id)
            inventory_dtos = [InventoryMapper.to_dto(item) for item in inventory_entities]
            
            # 5. Combine into ApiaryFullDataDTO
            full_apiary = ApiaryFullDataDTO(
                **apiary.model_dump(),
                beehives=beehives,
                inventory=inventory_dtos
            )
            full_apiaries.append(full_apiary)

        return UserFullDataDTO(
            user=user_dto,
            apiaries=full_apiaries
        )

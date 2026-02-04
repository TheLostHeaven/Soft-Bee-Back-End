from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto, CreateApiaryDto
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper
from src.features.apiaries.domain.entities.apiary import Apiary
from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryAlreadyExistsError
from src.features.inventory.application.use_cases.create_inventory_use_case import CreateInventoryUseCase
from src.features.inventory.application.dto.inventory_dto import CreateInventoryDTO


class CreateApiary:
    def __init__(
        self,
        apiary_repository: ApiaryRepository,
        create_inventory_use_case: CreateInventoryUseCase,
    ):
        self.apiary_repository = apiary_repository
        self.create_inventory_use_case = create_inventory_use_case

    def execute(self, create_dto: CreateApiaryDto) -> ApiaryDto:
        # Check if an apiary with the same name already exists for the same user
        existing_apiary = next(
            (
                apiary  
                for apiary in self.apiary_repository.get_all_apiaries()
                if apiary.name == create_dto.name
                and apiary.user_id == create_dto.user_id
            ),
            None,
        )
        if existing_apiary:
            raise ApiaryAlreadyExistsError(
                f"Apiary with name '{create_dto.name}' already exists for this user."
            )

        apiary_entity = ApiaryMapper.from_create_dto_to_entity(create_dto)
        created_apiary = self.apiary_repository.create_apiary(apiary_entity)

        # Create a default inventory for the new apiary
        inventory_dto = CreateInventoryDTO(
            apiary_id=created_apiary.id,
            name="guantes",
            quantity=0,
            unit="unidad",
            description="Ejemplo: guantes de apicultor",
            minimum_stock=0,
        )
        self.create_inventory_use_case.execute(inventory_dto)

        return ApiaryMapper.to_dto(created_apiary)

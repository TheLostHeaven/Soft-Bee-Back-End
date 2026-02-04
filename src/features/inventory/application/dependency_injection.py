from dependency_injector import containers, providers
from src.features.inventory.application.use_cases.create_inventory_use_case import (
    CreateInventoryUseCase,
)
from src.features.inventory.application.use_cases.get_inventories_by_apiary_use_case import (
    GetInventoriesByApiaryUseCase,
)
from src.features.inventory.application.use_cases.update_inventory_use_case import (
    UpdateInventoryUseCase,
)
from src.features.inventory.application.use_cases.delete_inventory_use_case import (
    DeleteInventoryUseCase,
)
from src.features.inventory.infrastructure.repositories.inventory_repository import (
    InventoryRepositoryImpl,
)


class InventoryContainer(containers.DeclarativeContainer):
    db_session = providers.Dependency()

    inventory_repository = providers.Factory(
        InventoryRepositoryImpl, session=db_session
    )

    create_inventory_use_case = providers.Factory(
        CreateInventoryUseCase, repository=inventory_repository
    )
    get_inventories_by_apiary_use_case = providers.Factory(
        GetInventoriesByApiaryUseCase, repository=inventory_repository
    )
    update_inventory_use_case = providers.Factory(
        UpdateInventoryUseCase, repository=inventory_repository
    )
    delete_inventory_use_case = providers.Factory(
        DeleteInventoryUseCase, repository=inventory_repository
    )

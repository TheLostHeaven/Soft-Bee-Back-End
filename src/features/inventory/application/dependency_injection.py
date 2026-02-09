from dependency_injector import containers, providers
from src.features.inventory.infrastructure.datasources.inventory_sql_datasource import (
    InventorySQLDataSource,
)
from src.features.inventory.infrastructure.repositories.inventory_repository_impl import (
    InventoryRepositoryImpl,
)
from src.features.inventory.application.use_cases.create_inventory_use_case import (
    CreateInventoryUseCase,
)
from src.features.inventory.application.use_cases.get_inventories_by_apiary_use_case import (
    GetInventoriesByApiaryUseCase,
)
from src.features.inventory.application.use_cases.get_inventory_summary_use_case import (
    GetInventorySummaryUseCase,
)
from src.features.inventory.application.use_cases.get_low_stock_items_use_case import (
    GetLowStockItemsUseCase,
)
from src.features.inventory.application.use_cases.adjust_inventory_quantity_use_case import (
    AdjustInventoryQuantityUseCase,
)
from src.features.inventory.application.use_cases.search_inventory_items_use_case import (
    SearchInventoryItemsUseCase,
)
from src.features.inventory.application.use_cases.update_inventory_use_case import (
    UpdateInventoryUseCase,
)
from src.features.inventory.application.use_cases.delete_inventory_use_case import (
    DeleteInventoryUseCase,
)
from src.features.inventory.domain.repositories.inventory_repository import InventoryRepository # Import abstract repository


class InventoryContainer(containers.DeclarativeContainer):
    db_session = providers.Dependency()

    inventory_sql_datasource = providers.Factory(
        InventorySQLDataSource,
        db_session=db_session,
    )

    inventory_repository: providers.Provider[InventoryRepository] = providers.Factory(
        InventoryRepositoryImpl,
        datasource=inventory_sql_datasource,
    )

    create_inventory_use_case = providers.Factory(
        CreateInventoryUseCase,
        repository=inventory_repository,
    )

    get_inventories_by_apiary_use_case = providers.Factory(
        GetInventoriesByApiaryUseCase,
        repository=inventory_repository,
    )

    get_inventory_summary_use_case = providers.Factory(
        GetInventorySummaryUseCase,
        repository=inventory_repository,
    )

    get_low_stock_items_use_case = providers.Factory(
        GetLowStockItemsUseCase,
        repository=inventory_repository,
    )

    adjust_inventory_quantity_use_case = providers.Factory(
        AdjustInventoryQuantityUseCase,
        repository=inventory_repository,
    )

    search_inventory_items_use_case = providers.Factory(
        SearchInventoryItemsUseCase,
        repository=inventory_repository,
    )
    
    update_inventory_use_case = providers.Factory(
        UpdateInventoryUseCase,
        repository=inventory_repository,
    )

    delete_inventory_use_case = providers.Factory(
        DeleteInventoryUseCase,
        repository=inventory_repository,
    )
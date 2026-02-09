from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.core.dependencies.containers import MainContainer
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
from src.features.inventory.application.dto.inventory_dto import (
    CreateInventoryDTO,
    UpdateInventoryDTO,
)
from src.features.inventory.application.dto.adjust_inventory_quantity_dto import (
    AdjustInventoryQuantityDTO,
)
from src.features.inventory.application.mappers.inventory_mapper import InventoryMapper
from uuid import UUID


inventory_bp = Blueprint("inventory", __name__, url_prefix="/") # Adjusted url_prefix


@inventory_bp.route("/apiaries/<uuid:apiary_id>/inventory", methods=["GET"]) # Adjusted route path
@inject
def get_inventories(
    apiary_id: UUID,
    get_inventories_use_case: GetInventoriesByApiaryUseCase = Provide[
        MainContainer.inventory_container.get_inventories_by_apiary_use_case
    ],
):
    inventories = get_inventories_use_case.execute(apiary_id)
    dtos = [InventoryMapper.to_dto(inventory) for inventory in inventories]
    return jsonify([dto.dict() for dto in dtos]), 200


@inventory_bp.route("/apiaries/<uuid:apiary_id>/inventory", methods=["POST"]) # Adjusted route path
@inject
def create_inventory(
    apiary_id: UUID,
    create_inventory_use_case: CreateInventoryUseCase = Provide[
        MainContainer.inventory_container.create_inventory_use_case
    ],
):
    data = request.get_json()
    if 'apiary_id' in data:
        del data['apiary_id'] # Remove apiary_id from data to avoid TypeError
    dto = CreateInventoryDTO(apiary_id=apiary_id, **data)
    inventory = create_inventory_use_case.execute(dto)
    return jsonify(InventoryMapper.to_dto(inventory).dict()), 201


from src.features.inventory.domain.exceptions.inventory_exceptions import InventoryNotFoundException

# ... (rest of the imports)

@inventory_bp.route("/inventory/<uuid:inventory_id>", methods=["PUT"]) # Adjusted route path
@inject
def update_inventory(
    inventory_id: UUID,
    update_inventory_use_case: UpdateInventoryUseCase = Provide[
        MainContainer.inventory_container.update_inventory_use_case
    ],
):
    data = request.get_json()
    dto = UpdateInventoryDTO(**data)
    inventory = update_inventory_use_case.execute(inventory_id, dto)
    return jsonify(InventoryMapper.to_dto(inventory).dict()), 200


@inventory_bp.route("/inventory/<uuid:inventory_id>", methods=["DELETE"]) # Adjusted route path
@inject
def delete_inventory(
    inventory_id: UUID,
    delete_inventory_use_case: DeleteInventoryUseCase = Provide[
        MainContainer.inventory_container.delete_inventory_use_case
    ],
):
    delete_inventory_use_case.execute(inventory_id)
    return "", 204

@inventory_bp.errorhandler(InventoryNotFoundException)
def handle_inventory_not_found(e):
    return jsonify({"message": str(e)}), 404


@inventory_bp.route("/apiaries/<uuid:apiary_id>/inventory/summary", methods=["GET"]) # NEW ROUTE
@inject
def get_inventory_summary_endpoint(
    apiary_id: UUID,
    get_inventory_summary_use_case: GetInventorySummaryUseCase = Provide[
        MainContainer.inventory_container.get_inventory_summary_use_case
    ],
):
    summary = get_inventory_summary_use_case.execute(apiary_id)
    return jsonify(summary), 200


@inventory_bp.route("/apiaries/<uuid:apiary_id>/inventory/low-stock", methods=["GET"]) # NEW ROUTE
@inject
def get_low_stock_items_endpoint(
    apiary_id: UUID,
    get_low_stock_items_use_case: GetLowStockItemsUseCase = Provide[
        MainContainer.inventory_container.get_low_stock_items_use_case
    ],
):
    low_stock_items = get_low_stock_items_use_case.execute(apiary_id)
    dtos = [InventoryMapper.to_dto(item) for item in low_stock_items]
    return jsonify([dto.dict() for dto in dtos]), 200


@inventory_bp.route("/inventory/<uuid:inventory_id>/adjust", methods=["PUT"]) # NEW ROUTE
@inject
def adjust_inventory_quantity_endpoint(
    inventory_id: UUID,
    adjust_inventory_quantity_use_case: AdjustInventoryQuantityUseCase = Provide[
        MainContainer.inventory_container.adjust_inventory_quantity_use_case
    ],
):
    data = request.get_json()
    dto = AdjustInventoryQuantityDTO(item_id=inventory_id, amount=data.get("amount")) # Pass inventory_id as item_id
    adjust_inventory_quantity_use_case.execute(dto)
    return "", 200


@inventory_bp.route("/apiaries/<uuid:apiary_id>/inventory/search", methods=["GET"]) # NEW ROUTE
@inject
def search_inventory_items_endpoint(
    apiary_id: UUID,
    search_inventory_items_use_case: SearchInventoryItemsUseCase = Provide[
        MainContainer.inventory_container.search_inventory_items_use_case
    ],
):
    query = request.args.get("query", "")
    items = search_inventory_items_use_case.execute(apiary_id, query)
    dtos = [InventoryMapper.to_dto(item) for item in items]
    return jsonify([dto.dict() for dto in dtos]), 200
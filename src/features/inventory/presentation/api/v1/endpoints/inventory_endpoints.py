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
from src.features.inventory.application.use_cases.adjust_inventory_quantity_use_case import (
    AdjustInventoryQuantityUseCase,
)
from src.features.inventory.application.use_cases.search_inventory_items_use_case import (
    SearchInventoryItemsUseCase,
)
from src.features.inventory.application.use_cases.get_inventory_item_use_case import (
    GetInventoryItemUseCase,
)
from src.features.inventory.application.use_cases.get_inventory_summary_use_case import (
    GetInventorySummaryUseCase,
)
from src.features.inventory.application.use_cases.get_low_stock_items_use_case import (
    GetLowStockItemsUseCase,
)
from src.features.inventory.application.use_cases.record_inventory_exit_use_case import (
    RecordInventoryExitUseCase,
)
from src.features.inventory.application.dto.inventory_dto import (
    CreateInventoryDTO,
    UpdateInventoryDTO,
)
from src.features.inventory.application.dto.adjust_inventory_quantity_dto import (
    AdjustInventoryQuantityDTO,
)
from src.features.inventory.application.dto.record_inventory_exit_dto import (
    RecordInventoryExitDTO,
)
from src.features.inventory.application.mappers.inventory_mapper import InventoryMapper
from uuid import UUID

inventory_bp = Blueprint("inventory", __name__, url_prefix="/api/v1/inventory")


@inventory_bp.route("/<uuid:apiary_id>", methods=["GET"])
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


@inventory_bp.route("/", methods=["POST"])
@inject
def create_inventory(
    create_inventory_use_case: CreateInventoryUseCase = Provide[
        MainContainer.inventory_container.create_inventory_use_case
    ],
):
    data = request.get_json()
    dto = CreateInventoryDTO(**data)
    inventory = create_inventory_use_case.execute(dto)
    return jsonify(InventoryMapper.to_dto(inventory).dict()), 201


@inventory_bp.route("/<uuid:inventory_id>", methods=["GET"])
@inject
def get_inventory_item(
    inventory_id: UUID,
    get_inventory_item_use_case: GetInventoryItemUseCase = Provide[
        MainContainer.inventory_container.get_inventory_item_use_case
    ],
):
    inventory = get_inventory_item_use_case.execute(inventory_id)
    if inventory:
        return jsonify(InventoryMapper.to_dto(inventory).dict()), 200
    return jsonify({"message": "Inventory item not found"}), 404


@inventory_bp.route("/<uuid:inventory_id>", methods=["PUT"])
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


@inventory_bp.route("/<uuid:inventory_id>", methods=["DELETE"])
@inject
def delete_inventory(
    inventory_id: UUID,
    delete_inventory_use_case: DeleteInventoryUseCase = Provide[
        MainContainer.inventory_container.delete_inventory_use_case
    ],
):
    delete_inventory_use_case.execute(inventory_id)
    return "", 204


@inventory_bp.route("/<uuid:inventory_id>/adjust", methods=["PUT"])
@inject
def adjust_inventory_quantity(
    inventory_id: UUID,
    adjust_inventory_quantity_use_case: AdjustInventoryQuantityUseCase = Provide[
        MainContainer.inventory_container.adjust_inventory_quantity_use_case
    ],
):
    data = request.get_json()
    dto = AdjustInventoryQuantityDTO(**data)
    inventory = adjust_inventory_quantity_use_case.execute(inventory_id, dto)
    return jsonify(InventoryMapper.to_dto(inventory).dict()), 200


@inventory_bp.route("/search/<uuid:apiary_id>", methods=["GET"])
@inject
def search_inventory(
    apiary_id: UUID,
    search_inventory_items_use_case: SearchInventoryItemsUseCase = Provide[
        MainContainer.inventory_container.search_inventory_items_use_case
    ],
):
    query = request.args.get("query", "")
    inventories = search_inventory_items_use_case.execute(apiary_id, query)
    dtos = [InventoryMapper.to_dto(inventory) for inventory in inventories]
    return jsonify([dto.dict() for dto in dtos]), 200


@inventory_bp.route("/<uuid:apiary_id>/summary", methods=["GET"])
@inject
def get_inventory_summary(
    apiary_id: UUID,
    get_inventory_summary_use_case: GetInventorySummaryUseCase = Provide[
        MainContainer.inventory_container.get_inventory_summary_use_case
    ],
):
    summary = get_inventory_summary_use_case.execute(apiary_id)
    return jsonify(summary), 200


@inventory_bp.route("/<uuid:apiary_id>/low-stock", methods=["GET"])
@inject
def get_low_stock_items(
    apiary_id: UUID,
    get_low_stock_items_use_case: GetLowStockItemsUseCase = Provide[
        MainContainer.inventory_container.get_low_stock_items_use_case
    ],
):
    low_stock_items = get_low_stock_items_use_case.execute(apiary_id)
    dtos = [InventoryMapper.to_dto(item) for item in low_stock_items]
    return jsonify([dto.dict() for dto in dtos]), 200


@inventory_bp.route("/<uuid:item_id>/exit", methods=["POST"])
@inject
def record_inventory_exit(
    item_id: UUID,
    record_inventory_exit_use_case: RecordInventoryExitUseCase = Provide[
        MainContainer.inventory_container.record_inventory_exit_use_case
    ],
):
    data = request.get_json()
    dto = RecordInventoryExitDTO(item_id=item_id, **data)
    inventory = record_inventory_exit_use_case.execute(dto)
    return jsonify(InventoryMapper.to_dto(inventory).dict()), 200
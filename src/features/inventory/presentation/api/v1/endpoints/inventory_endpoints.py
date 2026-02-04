
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
from src.features.inventory.application.dto.inventory_dto import (
    CreateInventoryDTO,
    UpdateInventoryDTO,
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

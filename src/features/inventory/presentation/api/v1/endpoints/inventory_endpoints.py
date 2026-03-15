
from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from http import HTTPStatus
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
from src.features.inventory.application.use_cases.adjust_inventory_use_case import (
    AdjustInventoryUseCase,
)
from src.features.inventory.application.dto.inventory_dto import (
    CreateInventoryDTO,
    UpdateInventoryDTO,
    AdjustInventoryDTO,
)
from src.features.inventory.application.mappers.inventory_mapper import InventoryMapper
from src.features.inventory.domain.exceptions.inventory_exceptions import (
    InventoryNotFoundError,
    InvalidInventoryAdjustmentError,
)
from uuid import UUID

inventory_bp = Blueprint("inventory", __name__, url_prefix="/api/v1/inventory")


@inventory_bp.route("/summary/<uuid:user_id>", methods=["GET"])
@inject
def get_inventory_summary(
    user_id: UUID,
    get_inventory_summary_use_case: GetInventorySummaryUseCase = Provide[
        MainContainer.inventory_container.get_inventory_summary_use_case
    ],
):
    summary_data = get_inventory_summary_use_case.execute(user_id)
    # The use case already returns DTOs, so we just need to serialize them
    return jsonify([item.model_dump(mode='json') for item in summary_data]), 200


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
    return jsonify([dto.model_dump(mode='json') for dto in dtos]), 200


@inventory_bp.route("/", methods=["POST", "OPTIONS"])
@inject
def create_inventory(
    create_inventory_use_case: CreateInventoryUseCase = Provide[
        MainContainer.inventory_container.create_inventory_use_case
    ],
):
    if request.method == "OPTIONS":
        return "", 204
    data = request.get_json()
    dto = CreateInventoryDTO(**data)
    inventory = create_inventory_use_case.execute(dto)
    return jsonify(InventoryMapper.to_dto(inventory).model_dump(mode='json')), 201


@inventory_bp.route("/movement", methods=["POST", "OPTIONS"])
@inject
def record_movement(
    adjust_use_case: AdjustInventoryUseCase = Provide[
        MainContainer.inventory_container.adjust_inventory_use_case
    ],
):
    """Endpoint para registrar movimientos (entrada/salida)"""
    if request.method == "OPTIONS":
        return "", 204
    try:
        data = request.get_json()
        inv_id = UUID(data.get('inventory_id'))
        qty = int(data.get('quantity'))
        mov_type = data.get('movement_type')
        reason = data.get('reason', 'Ajuste manual')
        notes = data.get('notes')
        
        # Si es salida, la cantidad debe ser negativa para el ajuste
        adjustment = qty if mov_type == 'entry' else -qty
        
        dto = AdjustInventoryDTO(adjustment_amount=adjustment)
        inventory = adjust_use_case.execute(inv_id, dto, reason=reason, notes=notes)
        
        return jsonify(InventoryMapper.to_dto(inventory).model_dump(mode='json')), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@inventory_bp.route("/<uuid:inventory_id>/movements", methods=["GET", "OPTIONS"])
@inject
def get_movements(
    inventory_id: UUID,
    repo = Provide[MainContainer.inventory_container.inventory_repository]
):
    """Endpoint para obtener historial real del producto"""
    if request.method == "OPTIONS":
        return "", 204
    try:
        movements = repo.get_movements(inventory_id)
        return jsonify(movements), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


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
    return jsonify(InventoryMapper.to_dto(inventory).model_dump(mode='json')), 200


@inventory_bp.route("/<uuid:inventory_id>/adjust", methods=["PUT"])
@inject
def adjust_inventory(
    inventory_id: UUID,
    adjust_inventory_use_case: AdjustInventoryUseCase = Provide[
        MainContainer.inventory_container.adjust_inventory_use_case
    ],
):
    try:
        data = request.get_json()
        dto = AdjustInventoryDTO(**data)
        inventory = adjust_inventory_use_case.execute(inventory_id, dto)
        return jsonify(InventoryMapper.to_dto(inventory).model_dump(mode='json')), HTTPStatus.OK
    except InventoryNotFoundError as e:
        return jsonify({"message": str(e)}), HTTPStatus.NOT_FOUND
    except InvalidInventoryAdjustmentError as e:
        return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


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

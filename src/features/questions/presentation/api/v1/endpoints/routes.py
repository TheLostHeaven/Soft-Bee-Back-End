from flask import request, jsonify, current_app
from http import HTTPStatus
from uuid import UUID
from pydantic import ValidationError
from src.features.questions.presentation.api.v1.endpoints import questions_bp
from src.features.questions.presentation.api.v1.schemas.question_schemas import (
    HiveQuestionResponseSchema, UpdateHiveQuestionRequestSchema, AssignQuestionToHiveRequestSchema,
    CreateApiaryQuestionRequestSchema, ApiaryQuestionResponseSchema
)
from src.features.questions.application.dto.question_dto import UpdateHiveQuestionDto
from src.features.auth.presentation.api.v1.dependencies.auth_deps import token_required

# --- APIARY QUESTIONS (El Banco de Preguntas por Apiario) ---

@questions_bp.route("/apiary/<string:apiary_id>", methods=['GET', 'OPTIONS'])
def get_apiary_questions(apiary_id: str):
    if request.method == 'OPTIONS': return '', 204
    """Obtiene todas las preguntas del banco de un apiario específico"""
    try:
        use_case = current_app.container.get_apiary_questions_use_case()
        questions = use_case.execute(UUID(apiary_id))
        return jsonify([ApiaryQuestionResponseSchema.model_validate(q).model_dump(mode='json', by_alias=True) for q in questions]), HTTPStatus.OK
    except ValueError:
        return jsonify({"message": "Invalid Apiary ID format"}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/apiary", methods=['POST', 'OPTIONS'])
def create_apiary_question():
    if request.method == 'OPTIONS': return '', 204
    try:
        data = request.json
        schema = CreateApiaryQuestionRequestSchema(**data)

        use_case = current_app.container.create_apiary_question_use_case()
        new_question = use_case.execute(
            apiary_id=schema.apiary_id,
            question_data=schema.model_dump(exclude_unset=True)
        )

        return jsonify(ApiaryQuestionResponseSchema.model_validate(new_question).model_dump(mode='json', by_alias=True)), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# Alias para POST /api/v1/questions (compatibilidad frontend)
@questions_bp.route("", methods=['POST', 'OPTIONS'])
def create_question_alias():
    return create_apiary_question()

@questions_bp.route("/apiary/<string:id>", methods=['PATCH', 'OPTIONS'])
def update_apiary_question(id: str):
    if request.method == 'OPTIONS': return '', 204
    """Actualiza una pregunta del banco del apiario usando su UUID"""
    try:
        data = request.json
        use_case = current_app.container.update_apiary_question_use_case()
        updated_question = use_case.execute(UUID(id), data)
        
        if not updated_question:
            return jsonify({"message": "Apiary question not found"}), HTTPStatus.NOT_FOUND
            
        return jsonify(ApiaryQuestionResponseSchema.model_validate(updated_question).model_dump(mode='json', by_alias=True)), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# Alias para PATCH /api/v1/questions/<id> (compatibilidad frontend)
@questions_bp.route("/<string:id>", methods=['PATCH', 'PUT', 'OPTIONS'])
def update_question_alias(id: str):
    return update_apiary_question(id)

@questions_bp.route("/apiary/<string:id>", methods=['DELETE', 'OPTIONS'])
def delete_apiary_question(id: str):
    if request.method == 'OPTIONS': return '', 204
    try:
        use_case = current_app.container.delete_apiary_question_use_case()
        success = use_case.execute(UUID(id))
        if not success:
            return jsonify({"message": "Question not found"}), HTTPStatus.NOT_FOUND
        return jsonify({}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# Alias para DELETE /api/v1/questions/<id>
@questions_bp.route("/<string:id>", methods=['DELETE', 'OPTIONS'])
def delete_question_alias(id: str):
    return delete_apiary_question(id)

@questions_bp.route("/templates", methods=['GET', 'OPTIONS'])
def get_question_templates():
    if request.method == 'OPTIONS': return '', 204
    try:
        use_case = current_app.container.get_default_questions_use_case()
        templates = use_case.execute()
        return jsonify(templates), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/load_defaults/<string:apiary_id>", methods=['POST', 'OPTIONS'])
def load_default_questions(apiary_id: str):
    if request.method == 'OPTIONS': return '', 204
    try:
        use_case = current_app.container.initialize_apiary_questions_use_case()
        use_case.execute(UUID(apiary_id))
        return jsonify({"message": "Defaults loaded successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/apiary/<string:apiary_id>/reorder", methods=['PUT', 'OPTIONS'])
def reorder_apiary_questions(apiary_id: str):
    if request.method == 'OPTIONS': return '', 204
    try:
        data = request.json
        order_ids = data.get('order', [])
        
        repo = current_app.container.question_repository()
        for idx, q_id in enumerate(order_ids):
            q = repo.get_apiary_question_by_id(UUID(q_id))
            if q:
                q.display_order = idx + 1
                repo.update_apiary_question(q)
                
        return jsonify({"message": "Reordered successfully"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# --- HIVE QUESTIONS (Asignación a Colmenas) ---

@questions_bp.route("/hive", methods=['POST', 'OPTIONS'])
def assign_question_to_hive():
    if request.method == 'OPTIONS': return '', 204
    try:
        data = request.json
        schema = AssignQuestionToHiveRequestSchema(**data)
        
        use_case = current_app.container.assign_question_to_hive_use_case()
        new_question = use_case.execute(
            hive_id=schema.hive_id,
            apiary_question_id=schema.apiary_question_id,
            display_order=schema.display_order
        )
        
        return jsonify(HiveQuestionResponseSchema.model_validate(new_question).model_dump(mode='json')), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/hive/<string:hive_id>", methods=['GET', 'OPTIONS'])
def get_hive_questions(hive_id: str):
    if request.method == 'OPTIONS': return '', 204
    """Obtiene todas las preguntas de una colmena con los detalles completos del apiario"""
    try:
        use_case = current_app.container.get_hive_questions_use_case()
        questions = use_case.execute(UUID(hive_id))
        return jsonify([HiveQuestionResponseSchema.model_validate(q).model_dump(mode='json') for q in questions]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/hive/<string:id>", methods=['PATCH', 'OPTIONS'])
def update_hive_question(id: str):
    if request.method == 'OPTIONS': return '', 204
    """Actualiza la asignación de una pregunta a una colmena usando su UUID"""
    try:
        data = request.json
        schema = UpdateHiveQuestionRequestSchema(**data)
        update_dto = UpdateHiveQuestionDto(**schema.model_dump(exclude_unset=True))
        
        use_case = current_app.container.update_hive_question_use_case()
        updated_question = use_case.execute(UUID(id), update_dto)
        
        if not updated_question:
            return jsonify({"message": "Hive question assignment not found"}), HTTPStatus.NOT_FOUND
            
        return jsonify(HiveQuestionResponseSchema.model_validate(updated_question).model_dump(mode='json')), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/hive/<string:id>", methods=['DELETE', 'OPTIONS'])
def delete_hive_question(id: str):
    if request.method == 'OPTIONS': return '', 204
    """Elimina la asignación de una pregunta a una colmena usando su UUID"""
    try:
        use_case = current_app.container.delete_hive_question_use_case()
        success = use_case.execute(UUID(id))
        
        if not success:
            return jsonify({"message": "Hive question assignment not found"}), HTTPStatus.NOT_FOUND
            
        return jsonify({}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/hive/<string:hive_id>/sync", methods=['POST', 'OPTIONS'])
def sync_hive_questions(hive_id: str):
    if request.method == 'OPTIONS': return '', 204
    """
    Sincroniza las preguntas de la colmena con las del apiario.
    - Agrega preguntas activas del apiario que aún no estén asignadas a la colmena.
    - Elimina asignaciones cuya pregunta de apiario ya no existe o fue desactivada.
    Retorna el listado actualizado de preguntas de la colmena.
    """
    try:
        from uuid import uuid4
        from src.features.questions.domain.entities.question import HiveQuestion
        from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException

        hive_uuid = UUID(hive_id)

        # Obtener la colmena para conocer su apiary_id
        get_beehive = current_app.container.get_beehive_by_id_use_case()
        try:
            beehive = get_beehive.execute(hive_uuid)
        except BeehiveNotFoundException:
            return jsonify({"message": "Colmena no encontrada"}), HTTPStatus.NOT_FOUND

        question_repo = current_app.container.question_repository()

        # Obtener preguntas activas del apiario
        apiary_questions = question_repo.get_apiary_questions_by_apiary_id(beehive.apiary_id)
        active_apiary_question_ids = {aq.id for aq in apiary_questions if aq.is_active}

        # Obtener preguntas ya asignadas a la colmena
        existing_hive_questions = question_repo.get_hive_questions_by_hive_id(hive_uuid)
        existing_apiary_question_ids = {hq.apiary_question_id for hq in existing_hive_questions}

        # 1. Eliminar asignaciones cuya pregunta del apiario fue desactivada o eliminada
        for hq in existing_hive_questions:
            if hq.apiary_question_id not in active_apiary_question_ids:
                question_repo.delete_hive_question(hq.id)

        # 2. Agregar preguntas activas del apiario que no estén asignadas
        max_order = max((hq.display_order for hq in existing_hive_questions), default=0)
        new_hive_questions = []
        for aq in apiary_questions:
            if aq.is_active and aq.id not in existing_apiary_question_ids:
                max_order += 1
                hq = HiveQuestion(
                    id=uuid4(),
                    hive_id=hive_uuid,
                    apiary_question_id=aq.id,
                    display_order=max_order,
                    is_active=True
                )
                new_hive_questions.append(hq)

        if new_hive_questions:
            question_repo.create_hive_questions_batch(new_hive_questions)

        # Retornar listado actualizado
        updated_questions = question_repo.get_hive_questions_by_hive_id(hive_uuid)
        from src.features.questions.application.mappers.question_mapper import QuestionMapper
        dtos = [QuestionMapper.hive_to_dto(q) for q in updated_questions]

        return jsonify({
            "message": "Sincronización completada",
            "questions": [HiveQuestionResponseSchema.model_validate(q).model_dump(mode='json') for q in dtos],
            "total_questions": len(dtos)
        }), HTTPStatus.OK

    except ValueError:
        return jsonify({"message": "ID de colmena inválido"}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


# --- REPARACIÓN IDEMPOTENTE DE HIVE QUESTIONS ---

@questions_bp.route("/hive/<string:hive_id>/sync-from-apiary", methods=['POST', 'OPTIONS'])
@token_required()
def sync_hive_from_apiary(hive_id: str):
    """
    Reparación idempotente para UNA colmena: crea las HiveQuestion faltantes
    a partir de las ApiaryQuestion activas de su apiario. No duplica las
    preguntas ya asignadas. Sirve para arreglar colmenas que quedaron sin
    preguntas (por ejemplo, creadas por sincronización offline) sin recrearlas.
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException

        hive_uuid = UUID(hive_id)

        # Obtener la colmena para conocer su apiary_id
        get_beehive = current_app.container.get_beehive_by_id_use_case()
        try:
            beehive = get_beehive.execute(hive_uuid)
        except BeehiveNotFoundException:
            return jsonify({"message": "Colmena no encontrada"}), HTTPStatus.NOT_FOUND

        initialize = current_app.container.initialize_hive_questions_use_case()
        hive_questions = initialize.execute(hive_uuid, beehive.apiary_id)

        return jsonify({
            "message": "Sincronización completada",
            "hive_id": hive_id,
            "total_questions": len(hive_questions),
        }), HTTPStatus.OK

    except ValueError:
        return jsonify({"message": "ID de colmena inválido"}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@questions_bp.route("/apiary/<string:apiary_id>/sync-hives", methods=['POST', 'OPTIONS'])
@token_required()
def sync_hives_from_apiary(apiary_id: str):
    """
    Reparación idempotente para TODAS las colmenas de un apiario: crea las
    HiveQuestion faltantes a partir de las ApiaryQuestion activas del apiario.
    """
    if request.method == 'OPTIONS':
        return '', 204

    try:
        apiary_uuid = UUID(apiary_id)
        use_case = current_app.container.sync_apiary_hive_questions_use_case()
        results = use_case.execute(apiary_uuid)

        return jsonify({
            "message": "Sincronización completada",
            "apiary_id": apiary_id,
            "hives_processed": len(results),
            "hives": results,
        }), HTTPStatus.OK

    except ValueError:
        return jsonify({"message": "ID de apiario inválido"}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

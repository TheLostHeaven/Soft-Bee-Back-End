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

# --- APIARY QUESTIONS (El Banco de Preguntas Master) ---

@questions_bp.route("/apiary/<string:apiary_id>", methods=['GET'])
def get_apiary_questions(apiary_id: str):
    try:
        use_case = current_app.container.get_apiary_questions_use_case()
        questions = use_case.execute(UUID(apiary_id))
        return jsonify([ApiaryQuestionResponseSchema.model_validate(q).model_dump() for q in questions]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/apiary", methods=['POST'])
def create_apiary_question():
    try:
        data = request.json
        schema = CreateApiaryQuestionRequestSchema(**data)

        use_case = current_app.container.create_apiary_question_use_case()
        new_question = use_case.execute(
            apiary_id=schema.apiary_id,
            question_data=schema.model_dump(exclude_unset=True)
        )

        return jsonify(ApiaryQuestionResponseSchema.model_validate(new_question).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/apiary/<string:id>", methods=['PATCH'])
def update_apiary_question(id: str):
    """Actualiza una pregunta maestra usando su UUID"""
    try:
        data = request.json
        use_case = current_app.container.update_apiary_question_use_case()
        updated_question = use_case.execute(UUID(id), data)
        
        if not updated_question:
            return jsonify({"message": "Apiary question not found"}), HTTPStatus.NOT_FOUND
            
        return jsonify(ApiaryQuestionResponseSchema.model_validate(updated_question).model_dump()), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# --- HIVE QUESTIONS (Asignación a Colmenas) ---

@questions_bp.route("/hive", methods=['POST'])
def assign_question_to_hive():
    try:
        data = request.json
        schema = AssignQuestionToHiveRequestSchema(**data)
        
        use_case = current_app.container.assign_question_to_hive_use_case()
        new_question = use_case.execute(
            hive_id=schema.hive_id,
            apiary_question_id=schema.apiary_question_id,
            display_order=schema.display_order
        )
        
        return jsonify(HiveQuestionResponseSchema.model_validate(new_question).model_dump()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/hive/<string:hive_id>", methods=['GET'])
def get_hive_questions(hive_id: str):
    try:
        use_case = current_app.container.get_hive_questions_use_case()
        questions = use_case.execute(UUID(hive_id))
        return jsonify([HiveQuestionResponseSchema.model_validate(q).model_dump() for q in questions]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/hive/<string:id>", methods=['PATCH'])
def update_hive_question(id: str):
    """Actualiza la asignación de una pregunta a una colmena usando su UUID"""
    try:
        data = request.json
        schema = UpdateHiveQuestionRequestSchema(**data)
        update_dto = UpdateHiveQuestionDto(**schema.model_dump(exclude_unset=True))
        
        use_case = current_app.container.update_hive_question_use_case()
        updated_question = use_case.execute(UUID(id), update_dto)
        
        if not updated_question:
            return jsonify({"message": "Hive question assignment not found"}), HTTPStatus.NOT_FOUND
            
        return jsonify(HiveQuestionResponseSchema.model_validate(updated_question).model_dump()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/hive/<string:id>", methods=['DELETE'])
def delete_hive_question(id: str):
    """Elimina la asignación de una pregunta a una colmena usando su UUID"""
    try:
        use_case = current_app.container.delete_hive_question_use_case()
        success = use_case.execute(UUID(id))
        
        if not success:
            return jsonify({"message": "Hive question assignment not found"}), HTTPStatus.NOT_FOUND
            
        return jsonify({}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

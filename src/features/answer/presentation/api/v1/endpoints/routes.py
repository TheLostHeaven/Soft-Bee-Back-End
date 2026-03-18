from flask import request, jsonify, current_app, g
from http import HTTPStatus
from uuid import UUID
from pydantic import ValidationError
from src.features.answer.presentation.api.v1.endpoints import answers_bp
from src.features.answer.presentation.api.v1.schemas.answer_schemas import (
    HiveAnswerResponseSchema, CreateAnswerRequestSchema, UpdateAnswerRequestSchema,
    BatchCreateAnswersRequestSchema, BatchCreateAnswersResponseSchema
)

# --- ANSWERS CRUD ---

@answers_bp.route("", methods=['POST', 'OPTIONS'])
def create_answer():
    if request.method == 'OPTIONS': return '', 204
    """Create a single answer"""
    try:
        data = request.json
        schema = CreateAnswerRequestSchema(**data)
        
        # Get user_id from auth context if available
        user_id = getattr(g, 'user_id', None)
        
        use_case = current_app.container.create_answer_use_case()
        answer = use_case.execute(
            hive_question_id=schema.hive_question_id,
            answer=schema.answer,
            score=schema.score,
            user_id=user_id
        )
        
        return jsonify(HiveAnswerResponseSchema.model_validate(answer).model_dump(mode='json')), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@answers_bp.route("/batch", methods=['POST', 'OPTIONS'])
def create_answers_batch():
    if request.method == 'OPTIONS': return '', 204
    """Create multiple answers at once"""
    try:
        data = request.json
        schema = BatchCreateAnswersRequestSchema(**data)
        
        # Get user_id from auth context if available
        user_id = getattr(g, 'user_id', None)
        
        # Convert to list of dicts
        answers_data = [
            {
                "hive_question_id": item.hive_question_id, 
                "answer": item.answer,
                "score": item.score
            } 
            for item in schema.answers
        ]
        
        use_case = current_app.container.create_answers_batch_use_case()
        answers = use_case.execute(answers_data, user_id)
        
        response = BatchCreateAnswersResponseSchema(
            created=len(answers),
            answers=[HiveAnswerResponseSchema.model_validate(a).model_dump(mode='json') for a in answers]
        )
        
        return jsonify(response.model_dump(mode='json')), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@answers_bp.route("/<string:answer_id>", methods=['GET', 'OPTIONS'])
def get_answer(answer_id: str):
    if request.method == 'OPTIONS': return '', 204
    """Get a specific answer by ID"""
    try:
        use_case = current_app.container.get_answer_by_id_use_case()
        answer = use_case.execute(UUID(answer_id))
        
        if not answer:
            return jsonify({"message": "Answer not found"}), HTTPStatus.NOT_FOUND
        
        return jsonify(HiveAnswerResponseSchema.model_validate(answer).model_dump(mode='json')), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@answers_bp.route("/hive/<string:hive_id>", methods=['GET', 'OPTIONS'])
def get_answers_by_hive(hive_id: str):
    if request.method == 'OPTIONS': return '', 204
    """Get all answers for a hive"""
    try:
        # Query params
        limit = request.args.get('limit', type=int)
        latest_only = request.args.get('latest_only', 'false').lower() == 'true'
        
        use_case = current_app.container.get_answers_by_hive_use_case()
        answers = use_case.execute(UUID(hive_id), limit, latest_only)
        
        return jsonify([HiveAnswerResponseSchema.model_validate(a).model_dump(mode='json') for a in answers]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@answers_bp.route("/history/<string:hive_id>/<string:hive_question_id>", methods=['GET', 'OPTIONS'])
def get_answer_history(hive_id: str, hive_question_id: str):
    if request.method == 'OPTIONS': return '', 204
    """Get the history of answers for a specific question"""
    try:
        limit = request.args.get('limit', type=int)
        
        use_case = current_app.container.get_answer_history_use_case()
        answers = use_case.execute(UUID(hive_id), UUID(hive_question_id), limit)
        
        return jsonify([HiveAnswerResponseSchema.model_validate(a).model_dump(mode='json') for a in answers]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@answers_bp.route("/<string:answer_id>", methods=['PATCH', 'OPTIONS'])
def update_answer(answer_id: str):
    if request.method == 'OPTIONS': return '', 204
    """Update an answer"""
    try:
        data = request.json
        schema = UpdateAnswerRequestSchema(**data)
        
        use_case = current_app.container.update_answer_use_case()
        answer = use_case.execute(UUID(answer_id), schema.answer, schema.score)
        
        if not answer:
            return jsonify({"message": "Answer not found"}), HTTPStatus.NOT_FOUND
        
        return jsonify(HiveAnswerResponseSchema.model_validate(answer).model_dump(mode='json')), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@answers_bp.route("/<string:answer_id>", methods=['DELETE', 'OPTIONS'])
def delete_answer(answer_id: str):
    if request.method == 'OPTIONS': return '', 204
    """Delete an answer"""
    try:
        use_case = current_app.container.delete_answer_use_case()
        success = use_case.execute(UUID(answer_id))
        
        if not success:
            return jsonify({"message": "Answer not found"}), HTTPStatus.NOT_FOUND
        
        return jsonify({}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

from flask import request, jsonify, current_app
from http import HTTPStatus
from uuid import UUID
from pydantic import ValidationError
from src.features.questions.presentation.api.v1.endpoints import questions_bp
from src.features.questions.application.dto.question_dto import CreateQuestionDto, UpdateQuestionDto
from src.features.questions.application.use_cases.question_use_cases import QuestionUseCases

@questions_bp.route("/apiary/<uuid:apiary_id>", methods=['GET'])
def get_questions(apiary_id: UUID):
    try:
        use_cases: QuestionUseCases = current_app.container.questions_use_cases()
        questions = use_cases.get_questions_by_apiary(apiary_id)
        return jsonify([q.dict() for q in questions]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("", methods=['POST'])
def create_question():
    try:
        data = request.json
        dto = CreateQuestionDto(**data)
        use_cases: QuestionUseCases = current_app.container.questions_use_cases()
        question = use_cases.create_question(dto)
        return jsonify(question.dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/<uuid:question_id>", methods=['PUT'])
def update_question(question_id: UUID):
    try:
        data = request.json
        dto = UpdateQuestionDto(**data)
        use_cases: QuestionUseCases = current_app.container.questions_use_cases()
        question = use_cases.update_question(question_id, dto)
        if not question:
            return jsonify({"message": "Question not found"}), HTTPStatus.NOT_FOUND
        return jsonify(question.dict()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/<uuid:question_id>", methods=['DELETE'])
def delete_question(question_id: UUID):
    try:
        use_cases: QuestionUseCases = current_app.container.questions_use_cases()
        success = use_cases.delete_question(question_id)
        if not success:
            return jsonify({"message": "Question not found"}), HTTPStatus.NOT_FOUND
        return jsonify({}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/apiary/<uuid:apiary_id>/reorder", methods=['PUT'])
def reorder_questions(apiary_id: UUID):
    try:
        data = request.json
        order_ids = [UUID(id_str) for id_str in data.get('order', [])]
        use_cases: QuestionUseCases = current_app.container.questions_use_cases()
        use_cases.reorder_questions(apiary_id, order_ids)
        return jsonify({"message": "Order updated"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/templates", methods=['GET'])
def get_templates():
    # Aquí podrías devolver preguntas predefinidas
    templates = [
        {
            "question_text": "Nivel de varroa detectado",
            "question_type": "numero",
            "category": "Sanidad",
            "is_required": True,
            "min_value": 0,
            "max_value": 100
        },
        {
            "question_text": "Presencia de la reina",
            "question_type": "opciones",
            "category": "Población",
            "options": ["Vista", "No vista pero hay postura", "No vista y no hay postura"]
        }
    ]
    return jsonify(templates), HTTPStatus.OK

from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from src.features.questions.application.use_cases.create_question import CreateQuestionUseCase
from src.features.questions.application.use_cases.get_question import GetQuestionUseCase
from src.features.questions.application.use_cases.get_apiary_questions import GetApiaryQuestionsUseCase
from src.features.questions.application.use_cases.update_question import UpdateQuestionUseCase
from src.features.questions.application.use_cases.delete_question import DeleteQuestionUseCase
from src.features.questions.presentation.api.v1.schemas.question_schemas import (
    QuestionResponseSchema, CreateQuestionRequestSchema, UpdateQuestionRequestSchema,
    ReorderQuestionsRequestSchema
)
from pydantic import ValidationError
from uuid import UUID
import os
import json

questions_bp = Blueprint('questions_bp', __name__, url_prefix='/api/v1/questions')

@questions_bp.route("", methods=['POST'])
def create_question_endpoint():
    try:
        data = request.json
        create_request = CreateQuestionRequestSchema(**data)
        use_case: CreateQuestionUseCase = current_app.container.create_question_use_case()
        result = use_case.execute(create_request)
        return jsonify(QuestionResponseSchema.from_orm(result).dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ValueError as e:
        return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/<string:question_id>", methods=['GET'])
def get_question_endpoint(question_id: str):
    try:
        use_case: GetQuestionUseCase = current_app.container.get_question_use_case()
        result = use_case.execute(UUID(question_id))
        if result:
            return jsonify(QuestionResponseSchema.from_orm(result).dict()), HTTPStatus.OK
        return jsonify({"message": "Question not found"}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/apiary/<string:apiary_id>", methods=['GET'])
def get_apiary_questions_endpoint(apiary_id: str):
    try:
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        use_case: GetApiaryQuestionsUseCase = current_app.container.get_apiary_questions_use_case()
        results = use_case.execute(UUID(apiary_id), active_only)
        return jsonify([QuestionResponseSchema.from_orm(q).dict() for q in results]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/<string:question_id>", methods=['PUT'])
def update_question_endpoint(question_id: str):
    try:
        data = request.json
        update_request = UpdateQuestionRequestSchema(**data)
        use_case: UpdateQuestionUseCase = current_app.container.update_question_use_case()
        result = use_case.execute(UUID(question_id), update_request)
        return jsonify(QuestionResponseSchema.from_orm(result).dict()), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({"message": "Validation Error", "errors": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY
    except ValueError as e:
        return jsonify({"message": str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/<string:question_id>", methods=['DELETE'])
def delete_question_endpoint(question_id: str):
    try:
        use_case: DeleteQuestionUseCase = current_app.container.delete_question_use_case()
        use_case.execute(UUID(question_id))
        return jsonify({}), HTTPStatus.NO_CONTENT
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/apiary/<string:apiary_id>/reorder", methods=['PUT'])
def reorder_questions_endpoint(apiary_id: str):
    try:
        data = request.json
        reorder_request = ReorderQuestionsRequestSchema(**data)
        # We might need a ReorderQuestionsUseCase
        # For brevity, let's assume we implement it or call repository directly if it's simple
        # But following the pattern, we should have a use case.
        from src.features.questions.application.use_cases.reorder_questions import ReorderQuestionsUseCase
        use_case: ReorderQuestionsUseCase = current_app.container.reorder_questions_use_case()
        use_case.execute(UUID(apiary_id), reorder_request.order)
        return jsonify({"message": "Questions reordered"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/templates", methods=['GET'])
def get_question_templates_endpoint():
    try:
        # Busca el archivo en la raíz del proyecto (fuera de src)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        config_path = os.path.join(base_dir, 'config', 'preguntas_config.json')
        
        if not os.path.exists(config_path):
            config_path = os.path.join(current_app.root_path, 'config', 'preguntas_config.json')

        if not os.path.exists(config_path):
            return jsonify({'error': 'Config file not found'}), HTTPStatus.NOT_FOUND

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return jsonify(config.get("preguntas", [])), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/load_defaults/<string:apiary_id>", methods=['POST'])
def load_default_questions_endpoint(apiary_id: str):
    try:
        from src.features.questions.application.use_cases.load_default_questions import LoadDefaultQuestionsUseCase
        use_case: LoadDefaultQuestionsUseCase = current_app.container.load_default_questions_use_case()
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        config_path = os.path.join(base_dir, 'config', 'preguntas_config.json')
        
        if not os.path.exists(config_path):
            config_path = os.path.join(current_app.root_path, 'config', 'preguntas_config.json')

        if not os.path.exists(config_path):
            return jsonify({'error': 'Config file not found'}), HTTPStatus.NOT_FOUND

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        preguntas = config.get("preguntas", [])
        result_ids = use_case.execute(UUID(apiary_id), preguntas)
        
        return jsonify({
            'message': f'Loaded {len(result_ids)} questions',
            'question_ids': [str(rid) for rid in result_ids]
        }), HTTPStatus.OK
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@questions_bp.route("/beehive/<string:beehive_id>", methods=['GET'])
def get_beehive_questions_endpoint(beehive_id: str):
    try:
        from src.features.beehive.application.use_cases.get_beehive_by_id import GetBeehiveByIdUseCase
        get_beehive_use_case: GetBeehiveByIdUseCase = current_app.container.get_beehive_by_id_use_case()
        beehive = get_beehive_use_case.execute(UUID(beehive_id))
        
        if not beehive:
            return jsonify({"message": "Beehive not found"}), HTTPStatus.NOT_FOUND
            
        apiary_id = beehive.apiary_id
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        use_case: GetApiaryQuestionsUseCase = current_app.container.get_apiary_questions_use_case()
        results = use_case.execute(apiary_id, active_only)
        return jsonify([QuestionResponseSchema.from_orm(q).dict() for q in results]), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

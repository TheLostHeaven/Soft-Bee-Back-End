from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError

from src.features.ai_agent.application.dto.ai_prompt_dto import AIPromptDTO
from src.features.ai_agent.application.use_cases.process_ai_prompt import ProcessAIPromptUseCase
from src.core.dependencies.containers import MainContainer

ai_agent_bp = Blueprint('ai_agent_v1', __name__, url_prefix='/api/v1/ai')

@ai_agent_bp.route('/ask', methods=['POST'])
@inject
def ask_ai(
    process_use_case: ProcessAIPromptUseCase = Provide[MainContainer.process_ai_prompt_use_case]
):
    try:
        # Aquí es donde recibimos el JSON
        json_data = request.json
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        # Pydantic valida el JSON contra nuestro DTO
        prompt_dto = AIPromptDTO(**json_data)
        
        # Ejecutamos el caso de uso
        result = process_use_case.execute(prompt_dto)
        
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

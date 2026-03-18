from flask import Blueprint, request, jsonify, current_app
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError
from uuid import UUID

from src.features.ai_agent.application.dto.ai_prompt_dto import AIPromptDTO
from src.features.ai_agent.application.use_cases.process_ai_prompt import ProcessAIPromptUseCase
from src.core.dependencies.containers import MainContainer

# Maya Bot (Chat IA) - Mantiene su prefijo original /api/v1/ai
ai_agent_bp = Blueprint('ai_agent_v1', __name__, url_prefix='/api/v1/ai')

# Maya Voz (Monitoreo Estructurado) - Nuevo prefijo específico /api/v1/maya
maya_voice_bp = Blueprint('maya_voice_v1', __name__, url_prefix='/api/v1/maya')

print("DEBUG: Cargando módulo ai_agent endpoints y registrando maya_voice_bp")

@ai_agent_bp.route('/ask', methods=['POST'])
@inject
def ask_ai(
    process_use_case: ProcessAIPromptUseCase = Provide[MainContainer.process_ai_prompt_use_case]
):
    """Endpoint para el Chatbot con IA Generativa (Maya Bot)"""
    try:
        json_data = request.json
        if not json_data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        prompt_dto = AIPromptDTO(**json_data)
        result = process_use_case.execute(prompt_dto)
        return jsonify(result), 200
        
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@maya_voice_bp.route('/iniciar-monitoreo', methods=['POST'])
@inject
def iniciar_monitoreo(
    get_questions_use_case = Provide[MainContainer.get_hive_questions_use_case]
):
    """Endpoint para Maya Voz: Carga preguntas estructuradas de la DB"""
    try:
        data = request.json
        hive_id = data.get('hive_id')
        
        if not hive_id:
            return jsonify({"error": "hive_id is required"}), 400
            
        current_app.logger.info(f"Maya Voz: Buscando preguntas para colmena ID: {hive_id}")
        
        # 1. Obtener preguntas asignadas a la colmena (Reutilizando Caso de Uso existente)
        questions = get_questions_use_case.execute(UUID(str(hive_id)))
        
        # 2. Filtrar solo las ACTIVAS (Tanto en la colmena como en el banco general)
        active_questions = [hq for hq in questions if hq.is_active and hq.apiary_question and hq.apiary_question.is_active]
        
        # 3. Serializar usando el ESQUEMA ESTÁNDAR para garantizar consistencia total
        from src.features.questions.presentation.api.v1.schemas.question_schemas import HiveQuestionResponseSchema
        
        serialized_questions = [
            HiveQuestionResponseSchema.model_validate(hq).model_dump(mode='json', by_alias=True) 
            for hq in active_questions
        ]
        
        current_app.logger.info(f"Maya Voz: Se enviarán {len(serialized_questions)} preguntas activas con formato estándar.")
        return jsonify({"preguntas": serialized_questions}), 200
    except Exception as e:
        current_app.logger.error(f"Maya Voz Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@maya_voice_bp.route('/guardar-respuestas', methods=['POST'])
@inject
def guardar_respuestas(
    batch_save_use_case = Provide[MainContainer.create_answers_batch_use_case]
):
    """Endpoint para Maya Voz: Guarda respuestas reutilizando la lógica de Answers Batch"""
    try:
        data = request.json
        # El frontend ahora envía el formato estándar: {"answers": [{"hive_question_id": ..., "answer": ...}]}
        from src.features.answer.presentation.api.v1.schemas.answer_schemas import BatchCreateAnswersRequestSchema
        
        # Validación del esquema estándar
        schema = BatchCreateAnswersRequestSchema(**data)
        
        # Convertir a formato que espera el caso de uso
        answers_data = [item.model_dump() for item in schema.answers]
        
        batch_save_use_case.execute(answers_data)
        
        return jsonify({"status": "success", "message": "Monitoreo guardado exitosamente"}), 201
    except Exception as e:
        current_app.logger.error(f"Maya Voz Error al guardar: {str(e)}")
        return jsonify({"error": str(e)}), 500

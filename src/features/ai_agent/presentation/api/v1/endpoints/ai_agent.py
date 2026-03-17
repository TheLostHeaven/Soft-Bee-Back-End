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
        
        # LOGS SOLICITADOS
        print("DEBUG: Hive ID recibido:", hive_id)
        
        if not hive_id:
            return jsonify({"error": "hive_id is required"}), 400
            
        current_app.logger.info(f"Maya Voz: Buscando preguntas para colmena ID: {hive_id}")
        
        # 1. Obtener preguntas asignadas a la colmena (Reutilizando Caso de Uso existente)
        # Esto ya reutiliza la lógica de /api/v1/questions/hive/{hive_id}
        questions = get_questions_use_case.execute(UUID(str(hive_id)))
        
        # LOGS SOLICITADOS
        print("DEBUG: Preguntas encontradas:", len(questions))
        
        # 2. Filtrar solo las ACTIVAS (Tanto en la colmena como en el banco general)
        active_questions = []
        for hq in questions:
            # hq es HiveQuestionDto
            if hq.is_active and hq.apiary_question and hq.apiary_question.is_active:
                aq = hq.apiary_question
                active_questions.append({
                    "id": str(hq.id), # ID de la relación hive_question para guardar la respuesta
                    "texto": aq.question,
                    "tipo": aq.type,
                    "obligatoria": aq.is_required,
                    "opciones": aq.options.split(',') if aq.options else None,
                    "min": aq.min_value,
                    "max": aq.max_value,
                    "categoria": aq.category
                })
        
        current_app.logger.info(f"Maya Voz: Se enviarán {len(active_questions)} preguntas activas.")
        return jsonify({"preguntas": active_questions}), 200
    except Exception as e:
        current_app.logger.error(f"Maya Voz Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@maya_voice_bp.route('/guardar-respuestas', methods=['POST'])
@inject
def guardar_respuestas(
    batch_save_use_case = Provide[MainContainer.create_answers_batch_use_case]
):
    """Endpoint para Maya Voz: Guarda respuestas en hive_answers"""
    try:
        data = request.json
        respuestas_raw = data.get('respuestas', [])
        
        current_app.logger.info(f"Maya Voz: Recibidas {len(respuestas_raw)} respuestas para guardar.")
        
        answers_data = [{
            "hive_question_id": UUID(r['pregunta_id']),
            "answer": str(r['valor']),
            "score": 0 
        } for r in respuestas_raw]
        
        batch_save_use_case.execute(answers_data)
        
        return jsonify({"status": "success", "message": "Monitoreo guardado exitosamente"}), 201
    except Exception as e:
        current_app.logger.error(f"Maya Voz Error al guardar: {str(e)}")
        return jsonify({"error": str(e)}), 500

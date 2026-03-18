from flask import Blueprint, request, jsonify, current_app
from dependency_injector.wiring import inject, Provide
from pydantic import ValidationError
from uuid import UUID

from src.features.ai_agent.application.dto.ai_prompt_dto import AIPromptDTO
from src.features.ai_agent.application.use_cases.process_ai_prompt import ProcessAIPromptUseCase
from src.core.dependencies.containers import MainContainer

# Blueprint unificado para la feature AI Agent (Maya)
# Usamos un prefijo base /api/v1 para ser consistente con el resto de la app
ai_agent_bp = Blueprint('ai_agent_v1', __name__, url_prefix='/api/v1')

@ai_agent_bp.route('/ai/ask', methods=['POST', 'OPTIONS'])
@inject
def ask_ai(
    process_use_case: ProcessAIPromptUseCase = Provide[MainContainer.process_ai_prompt_use_case]
):
    """Endpoint para el Chatbot con IA Generativa (Maya Bot)"""
    if request.method == 'OPTIONS':
        return '', 204
        
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

@ai_agent_bp.route('/maya/iniciar-monitoreo', methods=['POST', 'OPTIONS'])
@inject
def iniciar_monitoreo(
    get_questions_use_case = Provide[MainContainer.get_hive_questions_use_case],
    beehive_repo = Provide[MainContainer.beehive_repository],
    initialize_hive_questions_use_case = Provide[MainContainer.initialize_hive_questions_use_case]
):
    """Endpoint para Maya Voz: Carga preguntas estructuradas de la DB"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        hive_id = data.get('hive_id')
        if not hive_id:
            return jsonify({"error": "hive_id is required"}), 400
            
        hive_uuid = UUID(str(hive_id))
        current_app.logger.info(f"Maya Voz: Buscando preguntas para colmena ID: {hive_uuid}")
        
        # 1. Obtener la colmena para conocer su apiario
        hive = beehive_repo.get_beehive_by_id(hive_uuid)
        if not hive:
            return jsonify({"error": "Beehive not found"}), 404
            
        # 2. SINCRONIZAR: Asegurar que la colmena tenga las preguntas del apiario actualizadas
        # Esto garantiza que si el usuario añade preguntas "a nivel general", Maya las tome.
        initialize_hive_questions_use_case.execute(hive_uuid, hive.apiary_id)
        
        # 3. Obtener preguntas asignadas a la colmena (ahora ya sincronizadas)
        questions = get_questions_use_case.execute(hive_uuid)
        
        # 4. Filtrar preguntas: Si la pregunta base del apiario está activa, Maya DEBE leerla.
        # Priorizamos el estado 'is_active' de la pregunta del apiario (aq).
        active_questions = []
        for hq in questions:
            if hq.apiary_question and hq.apiary_question.is_active:
                # Si la pregunta base está activa en el apiario, la incluimos
                active_questions.append(hq)
        
        # 5. APLANAR y mapear campos para el frontend (Maya Voz espera estructura plana)
        serialized_questions = []
        for hq in active_questions:
            aq = hq.apiary_question
            
            # Convertir opciones de String (del DB) a List para el frontend
            opciones_list = []
            if aq.options:
                opciones_list = [o.strip() for o in aq.options.split(',') if o.strip() and o.strip() != '{}']
            
            serialized_questions.append({
                "id": str(hq.id), # ID de la relación HiveQuestion para guardar respuestas
                "question_text": aq.question,
                "question_type": aq.type,
                "tipo": aq.type, # Compatibilidad
                "opciones": opciones_list, # Compatibilidad
                "options": aq.options,
                "is_required": aq.is_required,
                "obligatoria": aq.is_required,
                "min": aq.min_value,
                "max": aq.max_value,
                "min_value": aq.min_value,
                "max_value": aq.max_value,
                "category": aq.category,
                "display_order": hq.display_order
            })
        
        current_app.logger.info(f"Maya Voz: Se enviarán {len(serialized_questions)} preguntas activas (sincronizadas).")
        return jsonify({"preguntas": serialized_questions}), 200
    except Exception as e:
        import traceback
        current_app.logger.error(f"Maya Voz Error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@ai_agent_bp.route('/maya/guardar-respuestas', methods=['POST', 'OPTIONS'])
@inject
def guardar_respuestas(
    batch_save_use_case = Provide[MainContainer.create_answers_batch_use_case]
):
    """Endpoint para Maya Voz: Guarda respuestas reutilizando la lógica de Answers Batch"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Extraemos solo las respuestas para validar contra el esquema Batch
        answers_only = {"answers": data.get('answers', [])}
        
        from src.features.answer.presentation.api.v1.schemas.answer_schemas import BatchCreateAnswersRequestSchema
        
        # Validación del esquema estándar
        schema = BatchCreateAnswersRequestSchema(**answers_only)
        
        # Convertir a formato que espera el caso de uso
        answers_data = [item.model_dump() for item in schema.answers]
        
        hive_id = data.get('hive_id')
        if hive_id:
            current_app.logger.info(f"Maya Voz: Guardando {len(answers_data)} respuestas para colmena {hive_id}")
        
        batch_save_use_case.execute(answers_data)
        
        return jsonify({"status": "success", "message": "Monitoreo guardado exitosamente"}), 201
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        current_app.logger.error(f"Maya Voz Error al guardar: {str(e)}")
        return jsonify({"error": str(e)}), 500

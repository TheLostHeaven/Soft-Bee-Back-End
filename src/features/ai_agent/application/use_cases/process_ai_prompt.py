from typing import Dict, Any, Optional, List
from uuid import UUID
import json
import re

from src.features.ai_agent.infrastructure.services.ai_provider_registry import AIProviderRegistry
from src.features.ai_agent.domain.services.session_repository import IAISessionRepository
from src.features.ai_agent.domain.entities.session import ConversationSession, Message
from src.features.ai_agent.application.dto.ai_prompt_dto import AIPromptDTO

class ProcessAIPromptUseCase:
    def __init__(self, 
                 provider_registry: AIProviderRegistry, 
                 session_repository: IAISessionRepository,
                 get_apiary_questions_use_case = None,
                 get_hive_questions_use_case = None,
                 create_answer_use_case = None,
                 get_all_beehives_use_case = None):
        self.provider_registry = provider_registry
        self.session_repository = session_repository
        self.get_apiary_questions_use_case = get_apiary_questions_use_case
        self.get_hive_questions_use_case = get_hive_questions_use_case
        self.create_answer_use_case = create_answer_use_case
        self.get_all_beehives_use_case = get_all_beehives_use_case

    def execute(self, dto: AIPromptDTO) -> Dict[str, Any]:
        # 1. Obtener o crear sesión
        session = self._get_or_create_session(dto.session_id, dto.agent_id)
        
        # 2. Si el usuario pide cerrar, cerramos y limpiamos
        if dto.close_session:
            self.session_repository.delete(session.id)
            return {
                "status": "session_closed",
                "message": "La sesión ha sido finalizada y el contexto limpiado.",
                "session_id": str(session.id)
            }

        # 3. Preparar contexto enriquecido si hay apiary_id
        enriched_context = dto.context or {}
        apiary_id = enriched_context.get('apiary_id')
        
        if apiary_id and self.get_apiary_questions_use_case:
            try:
                apiary_uuid = UUID(str(apiary_id))
                questions = self.get_apiary_questions_use_case.execute(apiary_uuid)
                hives = self.get_all_beehives_use_case.execute(apiary_uuid)
                
                # Formatear información para el modelo
                questions_info = [{"id": str(q.id), "text": q.question, "type": q.type, "category": q.category} for q in questions]
                hives_info = [{"id": str(h.id), "number": h.hive_number} for h in hives]
                
                enriched_context['available_questions'] = questions_info
                enriched_context['available_hives'] = hives_info
                
                # Agregar instrucción de sistema al historial si es una nueva sesión o no está presente
                if not any(m.role == 'system' for m in session.history):
                    system_msg = self._generate_system_instruction(questions_info, hives_info)
                    session.history.insert(0, Message(role="system", content=system_msg))
            except Exception as e:
                print(f"Error enriching context: {e}")

        # 4. Seleccionar el proveedor (OpenAI, Gemini, etc.)
        ai_service = self.provider_registry.get_provider(dto.provider)

        # 5. Añadir el prompt del usuario al historial
        session.add_message("user", dto.prompt)
        
        # 6. Llamar a la IA con todo el historial
        response_content = ai_service.ask(
            dto.prompt, 
            session.history, 
            session.agent_id, 
            dto.provider,
            enriched_context
        )
        
        # 7. Procesar si la IA quiere guardar una respuesta
        processed_response = self._process_save_commands(response_content, enriched_context)
        
        # 8. Añadir respuesta de la IA al historial
        session.add_message("assistant", processed_response)
        
        # 9. Guardar sesión actualizada
        self.session_repository.save(session)
        
        return {
            "status": "success",
            "session_id": str(session.id),
            "agent_id": session.agent_id,
            "provider_used": dto.provider,
            "data": {
                "response": processed_response,
                "is_finished": False
            }
        }

    def _generate_system_instruction(self, questions, hives) -> str:
        hives_str = ", ".join([f"Colmena {h['number']} (ID: {h['id']})" for h in hives])
        questions_str = "\n".join([f"- {q['text']} (Tipo: {q['type']}, ID: {q['id']})" for q in questions])
        
        return f"""Eres Maya, la asistente inteligente de SoftBee. 
Tu objetivo es ayudar al apicultor a monitorear sus apiarios.
Tienes acceso a las siguientes colmenas: {hives_str}.
Y a estas preguntas de monitoreo:
{questions_str}

Si el usuario te da información sobre el estado de una colmena, debes confirmar que la has registrado y generar al final de tu respuesta un bloque especial con este formato:
RECORD_DATA: {{"hive_id": "ID_DE_LA_COLMENA", "answers": [{{"question_id": "ID_DE_LA_PREGUNTA", "answer": "VALOR"}}]}}

IMPORTANTE: El bloque RECORD_DATA debe estar en una sola línea al final.
Solo genera RECORD_DATA si estás seguro de la colmena y la pregunta.
Si falta información, pregunta al apicultor de forma amable."""

    def _process_save_commands(self, response: str, context: Dict) -> str:
        match = re.search(r'RECORD_DATA: (\{.*\})', response)
        if not match:
            return response
            
        try:
            data_json = match.group(1)
            data = json.loads(data_json)
            
            hive_id = data.get('hive_id')
            answers = data.get('answers', [])
            
            if hive_id and answers and self.create_answer_use_case:
                # Necesitamos mapear las preguntas de apiario a las de la colmena específica
                hive_uuid = UUID(hive_id)
                hive_questions = self.get_hive_questions_use_case.execute(hive_uuid)
                
                # Mapa de question_id (apiary_question_id) -> hive_question_id (el UUID de la relación)
                mapping = {str(hq.apiary_question_id): str(hq.id) for hq in hive_questions}
                
                for ans in answers:
                    apiary_q_id = ans.get('question_id')
                    answer_value = ans.get('answer')
                    
                    hive_q_id = mapping.get(apiary_q_id)
                    if hive_q_id:
                        self.create_answer_use_case.execute(
                            hive_question_id=UUID(hive_q_id),
                            answer=str(answer_value),
                            score=0, # Por ahora 0, se podría calcular
                            user_id=None # Se podría pasar desde el contexto si se tiene
                        )
                
                # Limpiar el comando de la respuesta para el usuario
                clean_response = response.replace(match.group(0), "").strip()
                return f"{clean_response}\n\n✅ [Datos registrados en el sistema]"
                
        except Exception as e:
            print(f"Error processing save command: {e}")
            
        return response

    def _get_or_create_session(self, session_id: Optional[UUID], agent_id: str) -> ConversationSession:
        if session_id:
            session = self.session_repository.get_by_id(session_id)
            if session and session.is_active:
                return session
        
        # Crear nueva sesión si no existe o no es válida
        new_session = ConversationSession(agent_id=agent_id)
        self.session_repository.save(new_session)
        return new_session

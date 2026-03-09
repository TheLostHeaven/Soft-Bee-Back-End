from uuid import UUID
from typing import Optional
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import ApiaryQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class UpdateApiaryQuestion:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, apiary_question_id: UUID, update_data: dict) -> Optional[ApiaryQuestionDto]:
        entity = self.question_repository.get_apiary_question_by_id(apiary_question_id)
        if not entity:
            return None
            
        # Actualizar campos permitidos manejando posibles alias del frontend
        entity.category = update_data.get("category", update_data.get("categoria", entity.category))
        entity.question = update_data.get("question", update_data.get("question_text", entity.question))
        entity.type = update_data.get("type", update_data.get("question_type", entity.type))
        entity.is_required = update_data.get("is_required", update_data.get("obligatoria", entity.is_required))
        entity.options = update_data.get("options", update_data.get("opciones", entity.options))
        entity.display_order = update_data.get("display_order", update_data.get("orden", entity.display_order))
        entity.min_value = update_data.get("min_value", update_data.get("min", entity.min_value))
        entity.max_value = update_data.get("max_value", update_data.get("max", entity.max_value))
        entity.depends_on = update_data.get("depends_on", entity.depends_on)
        entity.is_active = update_data.get("is_active", update_data.get("activa", entity.is_active))
        entity.score = update_data.get("score", entity.score)
            
        updated_entity = self.question_repository.update_apiary_question(entity)
        return QuestionMapper.apiary_to_dto(updated_entity)

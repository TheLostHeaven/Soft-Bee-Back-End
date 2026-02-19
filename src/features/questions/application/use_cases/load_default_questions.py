from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import CreateQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper
from uuid import UUID
from typing import List, Dict, Any

class LoadDefaultQuestionsUseCase:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, apiary_id: UUID, default_questions: List[Dict[str, Any]]) -> List[UUID]:
        loaded_ids = []
        
        for i, q_data in enumerate(default_questions):
            external_id = q_data.get('id')
            if not external_id:
                continue
            
            # Check if it already exists
            existing = self.question_repository.get_by_external_id(apiary_id, external_id)
            if existing:
                continue
            
            # Create entity
            dto = CreateQuestionDto(
                apiary_id=apiary_id,
                question_text=q_data.get('pregunta'),
                question_type=q_data.get('tipo'),
                category=q_data.get('categoria'),
                is_required=q_data.get('obligatoria', False),
                display_order=i + 1,
                min_value=q_data.get('min'),
                max_value=q_data.get('max'),
                options=q_data.get('opciones'),
                depends_on=q_data.get('depende_de'),
                is_active=True,
                external_id=external_id
            )
            
            entity = QuestionMapper.from_create_dto_to_entity(dto)
            created = self.question_repository.create(entity)
            loaded_ids.append(created.id)
            
        return loaded_ids

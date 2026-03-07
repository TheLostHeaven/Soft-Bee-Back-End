from typing import List, Optional
from uuid import UUID
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import QuestionDto, CreateQuestionDto, UpdateQuestionDto
from src.features.questions.domain.entities.question import Question

class QuestionUseCases:
    def __init__(self, repository: QuestionRepository):
        self.repository = repository

    def get_questions_by_apiary(self, apiary_id: UUID) -> List[QuestionDto]:
        questions = self.repository.get_by_apiary_id(apiary_id)
        return [self._to_dto(q) for q in questions]

    def create_question(self, dto: CreateQuestionDto) -> QuestionDto:
        question = Question(
            id=None,
            apiary_id=dto.apiary_id,
            question_text=dto.question_text,
            question_type=dto.question_type,
            category=dto.category,
            is_required=dto.is_required,
            display_order=dto.display_order,
            min_value=dto.min_value,
            max_value=dto.max_value,
            options=dto.options
        )
        saved = self.repository.save(question)
        return self._to_dto(saved)

    def update_question(self, question_id: UUID, dto: UpdateQuestionDto) -> Optional[QuestionDto]:
        existing = self.repository.get_by_id(question_id)
        if not existing:
            return None
        
        if dto.question_text is not None: existing.question_text = dto.question_text
        if dto.question_type is not None: existing.question_type = dto.question_type
        if dto.category is not None: existing.category = dto.category
        if dto.is_required is not None: existing.is_required = dto.is_required
        if dto.display_order is not None: existing.display_order = dto.display_order
        if dto.min_value is not None: existing.min_value = dto.min_value
        if dto.max_value is not None: existing.max_value = dto.max_value
        if dto.options is not None: existing.options = dto.options
        if dto.is_active is not None: existing.is_active = dto.is_active

        saved = self.repository.save(existing)
        return self._to_dto(saved)

    def delete_question(self, question_id: UUID) -> bool:
        return self.repository.delete(question_id)

    def reorder_questions(self, apiary_id: UUID, order_ids: List[UUID]) -> bool:
        return self.repository.update_order(apiary_id, order_ids)

    def _to_dto(self, entity: Question) -> QuestionDto:
        return QuestionDto(
            id=entity.id,
            apiary_id=entity.apiary_id,
            question_text=entity.question_text,
            question_type=entity.question_type,
            category=entity.category,
            is_required=entity.is_required,
            display_order=entity.display_order,
            min_value=entity.min_value,
            max_value=entity.max_value,
            options=entity.options,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

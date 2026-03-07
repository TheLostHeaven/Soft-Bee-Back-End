from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.domain.entities.question import Question
from src.features.questions.infrastructure.models.question_model import QuestionModel

class QuestionRepositoryImpl(QuestionRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, question_id: UUID) -> Optional[Question]:
        model = self.db_session.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        return self._to_entity(model) if model else None

    def get_by_apiary_id(self, apiary_id: UUID) -> List[Question]:
        models = self.db_session.query(QuestionModel)\
            .filter(QuestionModel.apiary_id == apiary_id)\
            .order_by(QuestionModel.display_order.asc())\
            .all()
        return [self._to_entity(m) for m in models]

    def save(self, question: Question) -> Question:
        model = self.db_session.query(QuestionModel).filter(QuestionModel.id == question.id).first() if question.id else None
        
        if not model:
            model = QuestionModel(
                apiary_id=question.apiary_id,
                external_id=question.external_id,
                question_text=question.question_text,
                question_type=question.question_type,
                category=question.category,
                is_required=question.is_required,
                display_order=question.display_order,
                min_value=question.min_value,
                max_value=question.max_value,
                options=question.options,
                depends_on=question.depends_on,
                is_active=question.is_active
            )
            self.db_session.add(model)
        else:
            model.question_text = question.question_text
            model.question_type = question.question_type
            model.category = question.category
            model.is_required = question.is_required
            model.display_order = question.display_order
            model.min_value = question.min_value
            model.max_value = question.max_value
            model.options = question.options
            model.is_active = question.is_active

        self.db_session.commit()
        self.db_session.refresh(model)
        return self._to_entity(model)

    def delete(self, question_id: UUID) -> bool:
        model = self.db_session.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        if model:
            self.db_session.delete(model)
            self.db_session.commit()
            return True
        return False

    def update_order(self, apiary_id: UUID, order_ids: List[UUID]) -> bool:
        for index, q_id in enumerate(order_ids):
            self.db_session.query(QuestionModel)\
                .filter(QuestionModel.id == q_id, QuestionModel.apiary_id == apiary_id)\
                .update({"display_order": index})
        self.db_session.commit()
        return True

    def _to_entity(self, model: QuestionModel) -> Question:
        return Question(
            id=model.id,
            apiary_id=model.apiary_id,
            external_id=model.external_id,
            question_text=model.question_text,
            question_type=model.question_type,
            category=model.category,
            is_required=model.is_required,
            display_order=model.display_order,
            min_value=model.min_value,
            max_value=model.max_value,
            options=model.options,
            depends_on=model.depends_on,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

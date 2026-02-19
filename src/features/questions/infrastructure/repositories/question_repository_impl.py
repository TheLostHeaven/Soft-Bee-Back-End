from typing import Optional, List
from sqlalchemy.orm import Session
from src.features.questions.domain.entities.question import Question
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.mappers.question_mapper import QuestionMapper
from src.features.questions.infrastructure.models.question_model import QuestionModel
from datetime import datetime
from uuid import UUID

class QuestionRepositoryImpl(QuestionRepository):
    """Implementation of the question repository with SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_by_id(self, question_id: UUID) -> Optional[Question]:
        model = self.db_session.query(QuestionModel).filter_by(id=question_id).first()
        return QuestionMapper.to_entity(model) if model else None

    def get_by_apiary_id(self, apiary_id: UUID, active_only: bool = True) -> List[Question]:
        query = self.db_session.query(QuestionModel).filter_by(apiary_id=apiary_id)
        if active_only:
            query = query.filter_by(is_active=True)
        models = query.order_by(QuestionModel.display_order).all()
        return [QuestionMapper.to_entity(model) for model in models]

    def get_by_external_id(self, apiary_id: UUID, external_id: str) -> Optional[Question]:
        model = self.db_session.query(QuestionModel).filter_by(
            apiary_id=apiary_id, external_id=external_id
        ).first()
        return QuestionMapper.to_entity(model) if model else None
    
    def create(self, question: Question) -> Question:
        model = QuestionMapper.to_model(question)
        self.db_session.add(model)
        self.db_session.flush()
        self.db_session.refresh(model)
        return QuestionMapper.to_entity(model)
    
    def update(self, question: Question) -> Question:
        model = self.db_session.query(QuestionModel).filter_by(id=question.id).first()
        if not model:
            raise ValueError(f"Question with ID {question.id} not found.")

        model.question_text = question.question_text
        model.question_type = question.question_type
        model.category = question.category
        model.is_required = question.is_required
        model.display_order = question.display_order
        model.min_value = question.min_value
        model.max_value = question.max_value
        model.options = question.options
        model.depends_on = question.depends_on
        model.is_active = question.is_active
        model.external_id = question.external_id
        model.updated_at = datetime.utcnow()
        
        self.db_session.flush()
        self.db_session.refresh(model)
        return QuestionMapper.to_entity(model)

    def delete(self, question_id: UUID) -> None:
        model = self.db_session.query(QuestionModel).filter_by(id=question_id).first()
        if model:
            self.db_session.delete(model)
            self.db_session.flush()
        else:
            raise ValueError(f"Question with ID {question_id} not found.")

    def reorder(self, apiary_id: UUID, new_order: List[UUID]) -> None:
        for index, question_id in enumerate(new_order, 1):
            model = self.db_session.query(QuestionModel).filter_by(
                id=question_id, apiary_id=apiary_id
            ).first()
            if model:
                model.display_order = index
        self.db_session.flush()

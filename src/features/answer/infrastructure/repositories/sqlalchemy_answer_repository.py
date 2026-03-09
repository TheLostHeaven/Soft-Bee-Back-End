from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, and_
from uuid import UUID
from src.features.answer.application.interfaces.repositories.answer_repository import AnswerRepository
from src.features.answer.domain.entities.answer import HiveAnswer
from src.features.answer.infrastructure.models.answer_models import HiveAnswerModel
from src.features.answer.application.mappers.answer_mapper import AnswerMapper
from src.features.questions.infrastructure.models.question_models import HiveQuestionModel, ApiaryQuestionModel

class SQLAlchemyAnswerRepository(AnswerRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, answer: HiveAnswer) -> HiveAnswer:
        model = AnswerMapper.to_model(answer)
        self.db_session.add(model)
        self.db_session.commit()
        self.db_session.refresh(model)
        return AnswerMapper.to_entity(model)

    def create_batch(self, answers: List[HiveAnswer]) -> List[HiveAnswer]:
        models = [AnswerMapper.to_model(a) for a in answers]
        self.db_session.add_all(models)
        self.db_session.commit()
        for model in models:
            self.db_session.refresh(model)
        return [AnswerMapper.to_entity(m) for m in models]

    def get_by_id(self, answer_id: UUID) -> Optional[HiveAnswer]:
        model = self.db_session.query(HiveAnswerModel)\
            .options(
                joinedload(HiveAnswerModel.hive_question)
                .joinedload(HiveQuestionModel.apiary_question)
            )\
            .filter_by(id=answer_id)\
            .first()
        return AnswerMapper.to_entity(model) if model else None

    def get_by_hive_id(self, hive_id: UUID, limit: Optional[int] = None) -> List[HiveAnswer]:
        """Get all answers for a hive by joining with hive_questions"""
        query = self.db_session.query(HiveAnswerModel)\
            .join(HiveQuestionModel, HiveAnswerModel.hive_question_id == HiveQuestionModel.id)\
            .options(
                joinedload(HiveAnswerModel.hive_question)
                .joinedload(HiveQuestionModel.apiary_question)
            )\
            .filter(HiveQuestionModel.hive_id == hive_id)\
            .order_by(desc(HiveAnswerModel.answered_at))
        
        if limit:
            query = query.limit(limit)
        
        models = query.all()
        return [AnswerMapper.to_entity(m) for m in models]

    def get_latest_by_hive_id(self, hive_id: UUID) -> List[HiveAnswer]:
        """Get the latest answer for each question of a hive"""
        from sqlalchemy import func
        
        # Subquery to get the latest answered_at for each question
        subquery = self.db_session.query(
            HiveAnswerModel.hive_question_id,
            func.max(HiveAnswerModel.answered_at).label('max_answered_at')
        ).join(
            HiveQuestionModel, HiveAnswerModel.hive_question_id == HiveQuestionModel.id
        ).filter(
            HiveQuestionModel.hive_id == hive_id
        ).group_by(
            HiveAnswerModel.hive_question_id
        ).subquery()

        # Join with the subquery to get the full answer records
        models = self.db_session.query(HiveAnswerModel)\
            .join(HiveQuestionModel, HiveAnswerModel.hive_question_id == HiveQuestionModel.id)\
            .options(
                joinedload(HiveAnswerModel.hive_question)
                .joinedload(HiveQuestionModel.apiary_question)
            )\
            .join(
                subquery,
                and_(
                    HiveAnswerModel.hive_question_id == subquery.c.hive_question_id,
                    HiveAnswerModel.answered_at == subquery.c.max_answered_at
                )
            )\
            .filter(HiveQuestionModel.hive_id == hive_id)\
            .order_by(HiveAnswerModel.hive_question_id)\
            .all()

        return [AnswerMapper.to_entity(m) for m in models]

    def get_by_hive_and_question(self, hive_id: UUID, hive_question_id: UUID, limit: Optional[int] = None) -> List[HiveAnswer]:
        """Get all answers for a specific question (history)"""
        query = self.db_session.query(HiveAnswerModel)\
            .join(HiveQuestionModel, HiveAnswerModel.hive_question_id == HiveQuestionModel.id)\
            .options(
                joinedload(HiveAnswerModel.hive_question)
                .joinedload(HiveQuestionModel.apiary_question)
            )\
            .filter(
                HiveQuestionModel.hive_id == hive_id,
                HiveAnswerModel.hive_question_id == hive_question_id
            )\
            .order_by(desc(HiveAnswerModel.answered_at))
        
        if limit:
            query = query.limit(limit)
        
        models = query.all()
        return [AnswerMapper.to_entity(m) for m in models]

    def get_latest_by_hive_and_question(self, hive_id: UUID, hive_question_id: UUID) -> Optional[HiveAnswer]:
        """Get the latest answer for a specific question"""
        model = self.db_session.query(HiveAnswerModel)\
            .join(HiveQuestionModel, HiveAnswerModel.hive_question_id == HiveQuestionModel.id)\
            .options(
                joinedload(HiveAnswerModel.hive_question)
                .joinedload(HiveQuestionModel.apiary_question)
            )\
            .filter(
                HiveQuestionModel.hive_id == hive_id,
                HiveAnswerModel.hive_question_id == hive_question_id
            )\
            .order_by(desc(HiveAnswerModel.answered_at))\
            .first()
        return AnswerMapper.to_entity(model) if model else None

    def update(self, answer: HiveAnswer) -> HiveAnswer:
        model = self.db_session.query(HiveAnswerModel).filter_by(id=answer.id).first()
        if model:
            model.answer = answer.answer
            model.score = answer.score
            model.answered_at = answer.answered_at
            self.db_session.commit()
            self.db_session.refresh(model)
            return AnswerMapper.to_entity(model)
        return None

    def delete(self, answer_id: UUID) -> bool:
        model = self.db_session.query(HiveAnswerModel).filter_by(id=answer_id).first()
        if model:
            self.db_session.delete(model)
            self.db_session.commit()
            return True
        return False

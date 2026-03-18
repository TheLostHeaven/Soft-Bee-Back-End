from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.domain.entities.question import ApiaryQuestion, HiveQuestion
from src.features.questions.infrastructure.models.question_models import ApiaryQuestionModel, HiveQuestionModel
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class SQLAlchemyQuestionRepository(QuestionRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    # Apiary Questions
    def create_apiary_question(self, question: ApiaryQuestion) -> ApiaryQuestion:
        model = QuestionMapper.apiary_to_model(question)
        self.db_session.add(model)
        self.db_session.commit()
        return QuestionMapper.apiary_to_entity(model)

    def create_apiary_questions_batch(self, questions: List[ApiaryQuestion]) -> List[ApiaryQuestion]:
        models = [QuestionMapper.apiary_to_model(q) for q in questions]
        self.db_session.add_all(models)
        self.db_session.commit()
        return [QuestionMapper.apiary_to_entity(m) for m in models]

    def get_apiary_questions_by_apiary_id(self, apiary_id: UUID) -> List[ApiaryQuestion]:
        models = self.db_session.query(ApiaryQuestionModel)\
            .filter_by(apiary_id=apiary_id)\
            .order_by(ApiaryQuestionModel.display_order)\
            .all()
        return [QuestionMapper.apiary_to_entity(m) for m in models]

    def get_apiary_question_by_id(self, apiary_question_id: UUID) -> Optional[ApiaryQuestion]:
        model = self.db_session.query(ApiaryQuestionModel)\
            .filter_by(id=apiary_question_id)\
            .first()
        return QuestionMapper.apiary_to_entity(model) if model else None

    def update_apiary_question(self, question: ApiaryQuestion) -> ApiaryQuestion:
        model = self.db_session.query(ApiaryQuestionModel).filter_by(id=question.id).first()
        if model:
            model.category = question.category
            model.question = question.question
            model.type = question.type
            model.is_required = question.is_required
            model.options = question.options
            model.display_order = question.display_order
            model.min_value = question.min_value
            model.max_value = question.max_value
            model.depends_on = question.depends_on
            model.is_active = question.is_active
            model.score = question.score
            self.db_session.commit()
            return QuestionMapper.apiary_to_entity(model)
        return None

    def delete_apiary_question(self, question_id: UUID) -> bool:
        model = self.db_session.query(ApiaryQuestionModel).filter_by(id=question_id).first()
        if model:
            self.db_session.delete(model)
            self.db_session.commit()
            return True
        return False

    # Hive Questions
    def create_hive_question(self, question: HiveQuestion) -> HiveQuestion:
        model = QuestionMapper.hive_to_model(question)
        self.db_session.add(model)
        self.db_session.commit()
        return QuestionMapper.hive_to_entity(model)

    def create_hive_questions_batch(self, questions: List[HiveQuestion]) -> List[HiveQuestion]:
        models = [QuestionMapper.hive_to_model(q) for q in questions]
        self.db_session.add_all(models)
        self.db_session.commit()
        return [QuestionMapper.hive_to_entity(m) for m in models]

    def get_hive_questions_by_hive_id(self, hive_id: UUID) -> List[HiveQuestion]:
        models = self.db_session.query(HiveQuestionModel)\
            .options(joinedload(HiveQuestionModel.apiary_question))\
            .filter_by(hive_id=hive_id)\
            .order_by(HiveQuestionModel.display_order)\
            .all()
        return [QuestionMapper.hive_to_entity(m) for m in models]

    def get_hive_question_by_id(self, hive_question_id: UUID) -> Optional[HiveQuestion]:
        model = self.db_session.query(HiveQuestionModel)\
            .options(joinedload(HiveQuestionModel.apiary_question))\
            .filter_by(id=hive_question_id)\
            .first()
        return QuestionMapper.hive_to_entity(model) if model else None

    def update_hive_question(self, question: HiveQuestion) -> HiveQuestion:
        model = self.db_session.query(HiveQuestionModel).filter_by(id=question.id).first()
        if model:
            model.display_order = question.display_order
            model.is_active = question.is_active
            self.db_session.commit()
            return QuestionMapper.hive_to_entity(model)
        return None

    def delete_hive_question(self, hive_question_id: UUID) -> bool:
        model = self.db_session.query(HiveQuestionModel).filter_by(id=hive_question_id).first()
        if model:
            self.db_session.delete(model)
            self.db_session.commit()
            return True
        return False

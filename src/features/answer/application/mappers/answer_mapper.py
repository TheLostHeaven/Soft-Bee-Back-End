from src.features.answer.domain.entities.answer import HiveAnswer
from src.features.answer.infrastructure.models.answer_models import HiveAnswerModel
from src.features.answer.application.dto.answer_dto import HiveAnswerDto

class AnswerMapper:
    @staticmethod
    def to_entity(model: HiveAnswerModel) -> HiveAnswer:
        if not model:
            return None
        
        # Import here to avoid circular dependency
        hive_question = None
        if hasattr(model, 'hive_question') and model.hive_question:
            from src.features.questions.application.mappers.question_mapper import QuestionMapper
            hive_question = QuestionMapper.hive_to_entity(model.hive_question)
        
        return HiveAnswer(
            id=model.id,
            hive_question_id=model.hive_question_id,
            answer=model.answer,
            score=model.score,
            answered_by=model.answered_by,
            answered_at=model.answered_at,
            updated_at=model.updated_at,
            hive_question=hive_question
        )

    @staticmethod
    def to_model(entity: HiveAnswer) -> HiveAnswerModel:
        if not entity:
            return None
        return HiveAnswerModel(
            id=entity.id,
            hive_question_id=entity.hive_question_id,
            answer=entity.answer,
            score=entity.score,
            answered_by=entity.answered_by,
            answered_at=entity.answered_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_dto(entity: HiveAnswer) -> HiveAnswerDto:
        if not entity:
            return None
        
        hive_question_dto = None
        if entity.hive_question:
            from src.features.questions.application.mappers.question_mapper import QuestionMapper
            hive_question_dto = QuestionMapper.hive_to_dto(entity.hive_question)
        
        return HiveAnswerDto(
            id=entity.id,
            hive_question_id=entity.hive_question_id,
            answer=entity.answer,
            score=entity.score,
            answered_by=entity.answered_by,
            answered_at=entity.answered_at,
            updated_at=entity.updated_at,
            hive_question=hive_question_dto
        )

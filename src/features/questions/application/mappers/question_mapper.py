from src.features.questions.domain.entities.question import ApiaryQuestion, HiveQuestion
from src.features.questions.infrastructure.models.question_models import ApiaryQuestionModel, HiveQuestionModel
from src.features.questions.application.dto.question_dto import ApiaryQuestionDto, HiveQuestionDto

class QuestionMapper:
    @staticmethod
    def apiary_to_entity(model: ApiaryQuestionModel) -> ApiaryQuestion:
        if not model:
            return None
        return ApiaryQuestion(
            id=model.id,
            apiary_id=model.apiary_id,
            question_id=model.question_id,
            category=model.category,
            question=model.question,
            type=model.type,
            display_order=model.display_order,
            is_required=model.is_required,
            options=model.options,
            min_value=model.min_value,
            max_value=model.max_value,
            depends_on=model.depends_on,
            is_active=model.is_active,
            is_system=model.is_system,
            score=model.score,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def apiary_to_model(entity: ApiaryQuestion) -> ApiaryQuestionModel:
        if not entity:
            return None
        return ApiaryQuestionModel(
            id=entity.id,
            apiary_id=entity.apiary_id,
            question_id=entity.question_id,
            category=entity.category,
            question=entity.question,
            type=entity.type,
            display_order=entity.display_order,
            is_required=entity.is_required,
            options=entity.options,
            min_value=entity.min_value,
            max_value=entity.max_value,
            depends_on=entity.depends_on,
            is_active=entity.is_active,
            is_system=entity.is_system,
            score=entity.score,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def apiary_to_dto(entity: ApiaryQuestion) -> ApiaryQuestionDto:
        if not entity:
            return None
        return ApiaryQuestionDto(
            id=entity.id,
            apiary_id=entity.apiary_id,
            question_id=entity.question_id,
            category=entity.category,
            question=entity.question,
            type=entity.type,
            display_order=entity.display_order,
            is_required=entity.is_required,
            options=entity.options,
            min_value=entity.min_value,
            max_value=entity.max_value,
            depends_on=entity.depends_on,
            is_active=entity.is_active,
            is_system=entity.is_system,
            score=entity.score,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def hive_to_entity(model: HiveQuestionModel) -> HiveQuestion:
        if not model:
            return None
        
        apiary_q = None
        if hasattr(model, 'apiary_question') and model.apiary_question:
            apiary_q = QuestionMapper.apiary_to_entity(model.apiary_question)
            
        return HiveQuestion(
            id=model.id,
            hive_id=model.hive_id,
            apiary_question_id=model.apiary_question_id,
            display_order=model.display_order,
            is_active=model.is_active,
            assigned_at=model.assigned_at,
            updated_at=model.updated_at,
            apiary_question=apiary_q
        )

    @staticmethod
    def hive_to_model(entity: HiveQuestion) -> HiveQuestionModel:
        if not entity:
            return None
        return HiveQuestionModel(
            id=entity.id,
            hive_id=entity.hive_id,
            apiary_question_id=entity.apiary_question_id,
            display_order=entity.display_order,
            is_active=entity.is_active,
            assigned_at=entity.assigned_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def hive_to_dto(entity: HiveQuestion) -> HiveQuestionDto:
        if not entity:
            return None
        
        apiary_q_dto = None
        if entity.apiary_question:
            apiary_q_dto = QuestionMapper.apiary_to_dto(entity.apiary_question)
            
        return HiveQuestionDto(
            id=entity.id,
            hive_id=entity.hive_id,
            apiary_question_id=entity.apiary_question_id,
            display_order=entity.display_order,
            is_active=entity.is_active,
            assigned_at=entity.assigned_at,
            updated_at=entity.updated_at,
            apiary_question=apiary_q_dto
        )

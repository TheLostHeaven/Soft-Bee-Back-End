from src.features.questions.domain.entities.question import Question
from src.features.questions.application.dto.question_dto import QuestionDto, CreateQuestionDto
from src.features.questions.infrastructure.models.question_model import QuestionModel
from uuid import uuid4

class QuestionMapper:
    @staticmethod
    def to_entity(model: QuestionModel) -> Question:
        return Question(
            id=model.id,
            apiary_id=model.apiary_id,
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
            external_id=model.external_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: Question) -> QuestionModel:
        return QuestionModel(
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
            depends_on=entity.depends_on,
            is_active=entity.is_active,
            external_id=entity.external_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def to_dto(entity: Question) -> QuestionDto:
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
            depends_on=entity.depends_on,
            is_active=entity.is_active,
            external_id=entity.external_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def from_create_dto_to_entity(dto: CreateQuestionDto) -> Question:
        return Question(
            id=uuid4(),
            apiary_id=dto.apiary_id,
            question_text=dto.question_text,
            question_type=dto.question_type,
            category=dto.category,
            is_required=dto.is_required,
            display_order=dto.display_order,
            min_value=dto.min_value,
            max_value=dto.max_value,
            options=dto.options,
            depends_on=dto.depends_on,
            is_active=dto.is_active,
            external_id=dto.external_id
        )

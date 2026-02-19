from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import QuestionDto, UpdateQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper
from uuid import UUID

class UpdateQuestionUseCase:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, question_id: UUID, dto: UpdateQuestionDto) -> QuestionDto:
        entity = self.question_repository.get_by_id(question_id)
        if not entity:
            raise ValueError(f"Question with ID {question_id} not found.")

        if dto.question_text is not None:
            entity.question_text = dto.question_text
        if dto.question_type is not None:
            entity.question_type = dto.question_type
        if dto.category is not None:
            entity.category = dto.category
        if dto.is_required is not None:
            entity.is_required = dto.is_required
        if dto.display_order is not None:
            entity.display_order = dto.display_order
        if dto.min_value is not None:
            entity.min_value = dto.min_value
        if dto.max_value is not None:
            entity.max_value = dto.max_value
        if dto.options is not None:
            entity.options = dto.options
        if dto.depends_on is not None:
            entity.depends_on = dto.depends_on
        if dto.is_active is not None:
            entity.is_active = dto.is_active
        if dto.external_id is not None:
            entity.external_id = dto.external_id

        # Validations
        if entity.question_type == 'opciones' and (not entity.options or len(entity.options) < 2):
            raise ValueError("Las preguntas de opción múltiple requieren al menos 2 opciones")
        if entity.question_type == 'numero' and (entity.min_value is None or entity.max_value is None):
            raise ValueError("Las preguntas numéricas requieren valores mínimos y máximos")

        updated_entity = self.question_repository.update(entity)
        return QuestionMapper.to_dto(updated_entity)

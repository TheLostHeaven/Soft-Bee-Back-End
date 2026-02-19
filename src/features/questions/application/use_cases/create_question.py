from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.application.dto.question_dto import QuestionDto, CreateQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class CreateQuestionUseCase:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, dto: CreateQuestionDto) -> QuestionDto:
        if dto.question_type == 'opciones' and (not dto.options or len(dto.options) < 2):
            raise ValueError("Las preguntas de opción múltiple requieren al menos 2 opciones")

        if dto.question_type == 'numero' and (dto.min_value is None or dto.max_value is None):
            raise ValueError("Las preguntas numéricas requieren valores mínimos y máximos")

        entity = QuestionMapper.from_create_dto_to_entity(dto)
        created_entity = self.question_repository.create(entity)
        return QuestionMapper.to_dto(created_entity)

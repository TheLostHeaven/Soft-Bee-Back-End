from uuid import UUID, uuid4
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.domain.entities.question import ApiaryQuestion
from src.features.questions.application.dto.question_dto import ApiaryQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class CreateApiaryQuestion:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, apiary_id: UUID, question_data: dict) -> ApiaryQuestionDto:
        new_apiary_q = ApiaryQuestion(
            id=uuid4(),
            apiary_id=apiary_id,
            question_id=question_data.get("question_id", f"custom_{uuid4().hex[:8]}"),
            category=question_data.get("category"),
            question=question_data.get("question"),
            type=question_data.get("type"),
            display_order=question_data.get("display_order", 0),
            is_required=question_data.get("is_required", False),
            options=question_data.get("options"),
            min_value=question_data.get("min_value"),
            max_value=question_data.get("max_value"),
            depends_on=question_data.get("depends_on"),
            is_active=True,
            is_system=False, # Al ser creada por el usuario, no es de sistema
            score=question_data.get("score", 0)
        )
        
        entity = self.question_repository.create_apiary_question(new_apiary_q)
        return QuestionMapper.apiary_to_dto(entity)

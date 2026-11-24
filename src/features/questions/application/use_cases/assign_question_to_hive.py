from uuid import UUID, uuid4
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.domain.entities.question import HiveQuestion
from src.features.questions.application.dto.question_dto import HiveQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class AssignQuestionToHive:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, hive_id: UUID, apiary_question_id: UUID, display_order: int) -> HiveQuestionDto:
        # Si ya existe una asignación para este par colmena/pregunta (por ejemplo,
        # una que fue desactivada con soft-delete), la reactivamos en lugar de
        # crear una nueva fila. Esto evita violar el UniqueConstraint
        # (hive_id, apiary_question_id) y conserva el registro histórico.
        existing = self.question_repository.get_hive_question_by_hive_and_apiary_question(
            hive_id, apiary_question_id
        )
        if existing:
            existing.is_active = True
            existing.display_order = display_order
            updated = self.question_repository.update_hive_question(existing)
            return QuestionMapper.hive_to_dto(updated)

        new_hive_q = HiveQuestion(
            id=uuid4(),
            hive_id=hive_id,
            apiary_question_id=apiary_question_id,
            display_order=display_order,
            is_active=True
        )

        entity = self.question_repository.create_hive_question(new_hive_q)
        return QuestionMapper.hive_to_dto(entity)

from uuid import UUID
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository


class DeleteApiaryQuestion:
    """
    Desactiva (soft-delete) una pregunta del banco del apiario.

    En lugar de eliminar físicamente la fila de `apiary_questions` (lo que
    borraría en cascada todas las `hive_questions` asociadas por el
    ForeignKey con ondelete='CASCADE'), marca `is_active = False`.

    Así la pregunta deja de aparecer en el monitoreo de Maya (que solo trae
    las activas tanto a nivel apiario como colmena) pero se conserva el
    registro y su histórico, y puede reactivarse más adelante.
    """

    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, question_id: UUID) -> bool:
        entity = self.question_repository.get_apiary_question_by_id(question_id)
        if not entity:
            return False

        # Ya está desactivada: la operación es idempotente y exitosa.
        if entity.is_active is False:
            return True

        entity.is_active = False
        updated = self.question_repository.update_apiary_question(entity)
        return updated is not None

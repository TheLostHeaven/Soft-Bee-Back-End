from uuid import UUID
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository


class DeleteHiveQuestion:
    """
    Desactiva (soft-delete) la asignación de una pregunta a una colmena.

    En lugar de eliminar físicamente el registro de `hive_questions`, marca
    `is_active = False`. De esta forma la pregunta deja de aparecer en el
    monitoreo de Maya (que solo trae las activas), pero el registro se conserva
    y puede reactivarse más adelante sin perder el histórico ni la configuración.
    """

    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, hive_question_id: UUID) -> bool:
        entity = self.question_repository.get_hive_question_by_id(hive_question_id)
        if not entity:
            return False

        # Ya está desactivada: no hay nada que hacer, pero la operación es exitosa.
        if entity.is_active is False:
            return True

        entity.is_active = False
        updated = self.question_repository.update_hive_question(entity)
        return updated is not None

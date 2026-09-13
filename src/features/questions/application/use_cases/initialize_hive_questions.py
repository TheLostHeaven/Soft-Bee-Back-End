import logging
from uuid import uuid4, UUID
from typing import List
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.domain.entities.question import HiveQuestion
from src.features.questions.application.dto.question_dto import HiveQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

logger = logging.getLogger(__name__)


class InitializeHiveQuestions:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, hive_id: UUID, apiary_id: UUID) -> List[HiveQuestionDto]:
        """
        Asigna a la colmena todas las ApiaryQuestion ACTIVAS de su apiario,
        convertidas en HiveQuestion con is_active=True.

        Es IDEMPOTENTE: si una HiveQuestion ya existe para la combinación
        colmena + apiary_question, no la duplica. Por eso puede ejecutarse
        de forma segura en cualquier camino de creación de colmena y también
        como reparación de colmenas que quedaron sin preguntas.

        Retorna la lista completa (actualizada) de HiveQuestion de la colmena.
        """
        # 1. Obtener SOLO las preguntas activas del apiario.
        #    (Antes se copiaban todas, incluidas las inactivas, lo que era
        #    inconsistente con el criterio de iniciar-monitoreo y con /sync.)
        apiary_questions = self.question_repository.get_apiary_questions_by_apiary_id(apiary_id)
        active_apiary_questions = [aq for aq in apiary_questions if aq.is_active]

        # 2. Ver qué HiveQuestion ya existen para no duplicar (idempotencia).
        existing_hive_questions = self.question_repository.get_hive_questions_by_hive_id(hive_id)
        existing_apiary_question_ids = {hq.apiary_question_id for hq in existing_hive_questions}

        # 3. Crear solo las faltantes, respetando la restricción única
        #    (hive_id, apiary_question_id).
        new_hive_questions = []
        for aq in active_apiary_questions:
            if aq.id in existing_apiary_question_ids:
                continue
            new_hive_questions.append(
                HiveQuestion(
                    id=uuid4(),
                    hive_id=hive_id,
                    apiary_question_id=aq.id,
                    display_order=aq.display_order,
                    is_active=True,
                )
            )

        # LOGGING TEMPORAL: permite verificar en cada creación (incluido el
        # camino de sincronización offline) cuántas preguntas activas se
        # encontraron y cuántas HiveQuestion se crearon realmente.
        logger.info(
            "[InitializeHiveQuestions] hive_id=%s apiary_id=%s "
            "apiary_questions_activas=%d hive_questions_existentes=%d hive_questions_creadas=%d",
            hive_id, apiary_id,
            len(active_apiary_questions), len(existing_hive_questions), len(new_hive_questions),
        )

        if new_hive_questions:
            self.question_repository.create_hive_questions_batch(new_hive_questions)

        # 4. Devolver el estado final completo de la colmena.
        final_hive_questions = self.question_repository.get_hive_questions_by_hive_id(hive_id)
        return [QuestionMapper.hive_to_dto(e) for e in final_hive_questions]

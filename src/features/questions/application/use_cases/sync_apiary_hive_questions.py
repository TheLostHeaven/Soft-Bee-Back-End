import logging
from uuid import UUID
from typing import Dict, List

from src.features.beehive.application.interfaces.repositories.beehive_repository import IBeehiveRepository
from src.features.questions.application.use_cases.initialize_hive_questions import InitializeHiveQuestions

logger = logging.getLogger(__name__)


class SyncApiaryHiveQuestions:
    """
    Reparación a nivel de apiario: para TODAS las colmenas de un apiario,
    crea las HiveQuestion faltantes a partir de las ApiaryQuestion activas.

    Reutiliza InitializeHiveQuestions (que es idempotente) por cada colmena,
    por lo que no duplica preguntas ya existentes.
    """

    def __init__(
        self,
        beehive_repository: IBeehiveRepository,
        initialize_hive_questions_use_case: InitializeHiveQuestions,
    ):
        self.beehive_repository = beehive_repository
        self.initialize_hive_questions_use_case = initialize_hive_questions_use_case

    def execute(self, apiary_id: UUID) -> List[Dict]:
        beehives = self.beehive_repository.get_all_beehives_by_apiary_id(apiary_id)

        results: List[Dict] = []
        for beehive in beehives:
            hive_questions = self.initialize_hive_questions_use_case.execute(
                beehive.id, apiary_id
            )
            results.append({
                "hive_id": str(beehive.id),
                "total_questions": len(hive_questions),
            })

        logger.info(
            "[SyncApiaryHiveQuestions] apiary_id=%s colmenas_procesadas=%d",
            apiary_id, len(results),
        )
        return results

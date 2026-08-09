from src.features.beehive.application.dto.beehive_dto import CreateBeehiveDTO, BeehiveDTO
from src.features.beehive.application.interfaces.repositories.beehive_repository import IBeehiveRepository
from src.features.beehive.application.mappers.beehive_mapper import BeehiveMapper
from src.features.beehive.domain.exceptions.beehive_exceptions import DuplicateHiveNumberException
from src.features.questions.application.use_cases.initialize_hive_questions import InitializeHiveQuestions


class CreateBeehiveUseCase:
    def __init__(self, repository: IBeehiveRepository, initialize_hive_questions_use_case: InitializeHiveQuestions):
        self.repository = repository
        self.initialize_hive_questions_use_case = initialize_hive_questions_use_case

    def execute(self, beehive_dto: CreateBeehiveDTO) -> BeehiveDTO:
        # Validate that hive_number is not duplicated within the same apiary
        if self.repository.exists_by_apiary_and_number(beehive_dto.apiary_id, beehive_dto.hive_number):
            raise DuplicateHiveNumberException(beehive_dto.hive_number, beehive_dto.apiary_id)

        beehive = self.repository.create_beehive(beehive_dto)
        
        # Initialize questions for the new hive
        self.initialize_hive_questions_use_case.execute(beehive.id, beehive.apiary_id)
        
        return BeehiveMapper.to_dto(beehive)

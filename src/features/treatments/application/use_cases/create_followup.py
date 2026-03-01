import uuid
from src.features.treatments.application.dto.treatment_dto import CreateFollowupDTO, FollowupDTO
from src.features.treatments.application.interfaces.repositories.treatment_repository import TreatmentRepository
from src.features.treatments.application.mappers.treatment_mapper import TreatmentMapper
from src.features.treatments.domain.entities.treatment import TreatmentFollowup

class CreateFollowupUseCase:
    def __init__(self, repository: TreatmentRepository):
        self.repository = repository

    def execute(self, dto: CreateFollowupDTO) -> FollowupDTO:
        followup = TreatmentFollowup(
            followup_id=uuid.uuid4(),
            treatment_id=dto.treatment_id,
            review_date=dto.review_date,
            hive_condition=dto.hive_condition,
            observed_changes=dto.observed_changes,
            partial_results=dto.partial_results,
            infestation_level=dto.infestation_level,
            notes=dto.notes,
            reviewer=dto.reviewer
        )
        saved_followup = self.repository.save_followup(followup)
        return TreatmentMapper.followup_to_dto(saved_followup)

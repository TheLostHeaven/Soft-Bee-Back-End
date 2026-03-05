from uuid import UUID
from typing import Optional
from src.features.treatments.application.dto.treatment_dto import UpdateFollowupDTO, FollowupDTO
from src.features.treatments.application.interfaces.repositories.treatment_repository import TreatmentRepository
from src.features.treatments.application.mappers.treatment_mapper import TreatmentMapper

class UpdateFollowupUseCase:
    def __init__(self, repository: TreatmentRepository):
        self.repository = repository

    def execute(self, followup_id: UUID, dto: UpdateFollowupDTO) -> Optional[FollowupDTO]:
        followup = self.repository.find_followup_by_id(followup_id)
        if not followup:
            return None

        if dto.review_date is not None:
            followup.review_date = dto.review_date
        if dto.hive_condition is not None:
            followup.hive_condition = dto.hive_condition
        if dto.observed_changes is not None:
            followup.observed_changes = dto.observed_changes
        if dto.partial_results is not None:
            followup.partial_results = dto.partial_results
        if dto.infestation_level is not None:
            followup.infestation_level = dto.infestation_level
        if dto.notes is not None:
            followup.notes = dto.notes
        if dto.reviewer is not None:
            followup.reviewer = dto.reviewer

        saved_followup = self.repository.save_followup(followup)
        return TreatmentMapper.followup_to_dto(saved_followup)

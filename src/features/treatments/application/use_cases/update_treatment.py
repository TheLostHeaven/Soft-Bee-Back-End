from uuid import UUID
from typing import Optional
from src.features.treatments.application.dto.treatment_dto import UpdateTreatmentDTO, TreatmentDTO
from src.features.treatments.application.interfaces.repositories.treatment_repository import TreatmentRepository
from src.features.treatments.application.mappers.treatment_mapper import TreatmentMapper

class UpdateTreatmentUseCase:
    def __init__(self, repository: TreatmentRepository):
        self.repository = repository

    def execute(self, id: UUID, dto: UpdateTreatmentDTO) -> Optional[TreatmentDTO]:
        treatment = self.repository.find_by_id(id)
        if not treatment:
            return None

        # Update fields if provided in DTO
        if dto.treatment_type is not None:
            treatment.treatment_type = dto.treatment_type
        if dto.product_name is not None:
            treatment.product_name = dto.product_name
        if dto.start_date is not None:
            treatment.start_date = dto.start_date
        if dto.active_ingredient is not None:
            treatment.active_ingredient = dto.active_ingredient
        if dto.target_disease is not None:
            treatment.target_disease = dto.target_disease
        if dto.estimated_duration_days is not None:
            treatment.estimated_duration_days = dto.estimated_duration_days
        if dto.end_date is not None:
            treatment.end_date = dto.end_date
        if dto.application_method is not None:
            treatment.application_method = dto.application_method
        if dto.dosage_applied is not None:
            treatment.dosage_applied = dto.dosage_applied
        if dto.dosage_unit is not None:
            treatment.dosage_unit = dto.dosage_unit
        if dto.batch_number is not None:
            treatment.batch_number = dto.batch_number
        if dto.supplier is not None:
            treatment.supplier = dto.supplier
        if dto.expiry_date is not None:
            treatment.expiry_date = dto.expiry_date
        if dto.status is not None:
            treatment.status = dto.status
        if dto.final_result is not None:
            treatment.final_result = dto.final_result
        if dto.final_hive_condition is not None:
            treatment.final_hive_condition = dto.final_hive_condition
        if dto.requires_repeat is not None:
            treatment.requires_repeat = dto.requires_repeat
        if dto.future_recommendations is not None:
            treatment.future_recommendations = dto.future_recommendations
        if dto.applied_by is not None:
            treatment.applied_by = dto.applied_by

        saved_treatment = self.repository.save(treatment)
        return TreatmentMapper.to_dto(saved_treatment)

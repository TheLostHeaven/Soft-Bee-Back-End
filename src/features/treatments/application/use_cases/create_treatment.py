import uuid
from src.features.treatments.application.dto.treatment_dto import CreateTreatmentDTO, TreatmentDTO
from src.features.treatments.application.interfaces.repositories.treatment_repository import TreatmentRepository
from src.features.treatments.application.mappers.treatment_mapper import TreatmentMapper
from src.features.treatments.domain.entities.treatment import Treatment

class CreateTreatmentUseCase:
    def __init__(self, repository: TreatmentRepository):
        self.repository = repository

    def execute(self, dto: CreateTreatmentDTO) -> TreatmentDTO:
        treatment = Treatment(
            id=uuid.uuid4(),
            hive_id=dto.hive_id,
            treatment_type=dto.treatment_type,
            product_name=dto.product_name,
            start_date=dto.start_date,
            active_ingredient=dto.active_ingredient,
            target_disease=dto.target_disease,
            estimated_duration_days=dto.estimated_duration_days,
            end_date=dto.end_date,
            application_method=dto.application_method,
            dosage_applied=dto.dosage_applied,
            dosage_unit=dto.dosage_unit,
            batch_number=dto.batch_number,
            supplier=dto.supplier,
            expiry_date=dto.expiry_date,
            applied_by=dto.applied_by
        )
        saved_treatment = self.repository.save(treatment)
        return TreatmentMapper.to_dto(saved_treatment)

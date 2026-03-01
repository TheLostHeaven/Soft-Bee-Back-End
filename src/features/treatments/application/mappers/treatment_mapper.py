from src.features.treatments.domain.entities.treatment import Treatment, TreatmentFollowup
from src.features.treatments.application.dto.treatment_dto import TreatmentDTO, FollowupDTO

class TreatmentMapper:
    @staticmethod
    def to_dto(entity: Treatment) -> TreatmentDTO:
        return TreatmentDTO(
            id=entity.id,
            hive_id=entity.hive_id,
            treatment_type=entity.treatment_type,
            product_name=entity.product_name,
            start_date=entity.start_date,
            active_ingredient=entity.active_ingredient,
            target_disease=entity.target_disease,
            estimated_duration_days=entity.estimated_duration_days,
            end_date=entity.end_date,
            application_method=entity.application_method,
            dosage_applied=entity.dosage_applied,
            dosage_unit=entity.dosage_unit,
            batch_number=entity.batch_number,
            supplier=entity.supplier,
            expiry_date=entity.expiry_date,
            status=entity.status,
            final_result=entity.final_result,
            final_hive_condition=entity.final_hive_condition,
            requires_repeat=entity.requires_repeat,
            future_recommendations=entity.future_recommendations,
            applied_by=entity.applied_by,
            registration_date=entity.registration_date,
            update_date=entity.update_date,
            followups=[TreatmentMapper.followup_to_dto(f) for f in entity.followups]
        )

    @staticmethod
    def followup_to_dto(entity: TreatmentFollowup) -> FollowupDTO:
        return FollowupDTO(
            followup_id=entity.followup_id,
            treatment_id=entity.treatment_id,
            review_date=entity.review_date,
            hive_condition=entity.hive_condition,
            observed_changes=entity.observed_changes,
            partial_results=entity.partial_results,
            infestation_level=entity.infestation_level,
            notes=entity.notes,
            reviewer=entity.reviewer,
            registration_date=entity.registration_date
        )

from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
from src.features.treatments.application.interfaces.repositories.treatment_repository import TreatmentRepository
from src.features.treatments.domain.entities.treatment import Treatment, TreatmentFollowup
from src.features.treatments.infrastructure.models.treatment_model import TreatmentModel, TreatmentFollowupModel

class TreatmentRepositoryImpl(TreatmentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def find_by_id(self, id: UUID) -> Optional[Treatment]:
        model = self.db_session.query(TreatmentModel).filter(TreatmentModel.id == id).first()
        return self._to_treatment_entity(model) if model else None

    def find_by_hive_id(self, hive_id: UUID) -> List[Treatment]:
        models = self.db_session.query(TreatmentModel).filter(TreatmentModel.hive_id == hive_id).all()
        return [self._to_treatment_entity(model) for model in models]

    def save(self, treatment: Treatment) -> Treatment:
        model = self.db_session.query(TreatmentModel).filter(TreatmentModel.id == treatment.id).first()
        
        if not model:
            model = TreatmentModel(
                id=treatment.id,
                hive_id=treatment.hive_id,
                treatment_type=treatment.treatment_type,
                product_name=treatment.product_name,
                active_ingredient=treatment.active_ingredient,
                target_disease=treatment.target_disease,
                start_date=treatment.start_date,
                estimated_duration_days=treatment.estimated_duration_days,
                end_date=treatment.end_date,
                application_method=treatment.application_method,
                dosage_applied=treatment.dosage_applied,
                dosage_unit=treatment.dosage_unit,
                batch_number=treatment.batch_number,
                supplier=treatment.supplier,
                expiry_date=treatment.expiry_date,
                status=treatment.status,
                final_result=treatment.final_result,
                final_hive_condition=treatment.final_hive_condition,
                requires_repeat=treatment.requires_repeat,
                future_recommendations=treatment.future_recommendations,
                applied_by=treatment.applied_by
            )
            self.db_session.add(model)
        else:
            model.treatment_type = treatment.treatment_type
            model.product_name = treatment.product_name
            model.active_ingredient = treatment.active_ingredient
            model.target_disease = treatment.target_disease
            model.start_date = treatment.start_date
            model.estimated_duration_days = treatment.estimated_duration_days
            model.end_date = treatment.end_date
            model.application_method = treatment.application_method
            model.dosage_applied = treatment.dosage_applied
            model.dosage_unit = treatment.dosage_unit
            model.batch_number = treatment.batch_number
            model.supplier = treatment.supplier
            model.expiry_date = treatment.expiry_date
            model.status = treatment.status
            model.final_result = treatment.final_result
            model.final_hive_condition = treatment.final_hive_condition
            model.requires_repeat = treatment.requires_repeat
            model.future_recommendations = treatment.future_recommendations
            model.applied_by = treatment.applied_by

        self.db_session.commit()
        self.db_session.refresh(model)
        return self._to_treatment_entity(model)

    def delete(self, id: UUID) -> bool:
        model = self.db_session.query(TreatmentModel).filter(TreatmentModel.id == id).first()
        if model:
            self.db_session.delete(model)
            self.db_session.commit()
            return True
        return False

    def save_followup(self, followup: TreatmentFollowup) -> TreatmentFollowup:
        model = self.db_session.query(TreatmentFollowupModel).filter(TreatmentFollowupModel.followup_id == followup.followup_id).first()
        
        if not model:
            model = TreatmentFollowupModel(
                followup_id=followup.followup_id,
                treatment_id=followup.treatment_id,
                review_date=followup.review_date,
                hive_condition=followup.hive_condition,
                observed_changes=followup.observed_changes,
                partial_results=followup.partial_results,
                infestation_level=followup.infestation_level,
                notes=followup.notes,
                reviewer=followup.reviewer
            )
            self.db_session.add(model)
        else:
            model.review_date = followup.review_date
            model.hive_condition = followup.hive_condition
            model.observed_changes = followup.observed_changes
            model.partial_results = followup.partial_results
            model.infestation_level = followup.infestation_level
            model.notes = followup.notes
            model.reviewer = followup.reviewer

        self.db_session.commit()
        self.db_session.refresh(model)
        return self._to_followup_entity(model)

    def find_followup_by_id(self, followup_id: UUID) -> Optional[TreatmentFollowup]:
        model = self.db_session.query(TreatmentFollowupModel).filter(TreatmentFollowupModel.followup_id == followup_id).first()
        return self._to_followup_entity(model) if model else None

    def delete_followup(self, followup_id: UUID) -> bool:
        model = self.db_session.query(TreatmentFollowupModel).filter(TreatmentFollowupModel.followup_id == followup_id).first()
        if model:
            self.db_session.delete(model)
            self.db_session.commit()
            return True
        return False

    def _to_treatment_entity(self, model: TreatmentModel) -> Treatment:
        followups = [self._to_followup_entity(f) for f in model.followups]
        return Treatment(
            id=model.id,
            hive_id=model.hive_id,
            treatment_type=model.treatment_type,
            product_name=model.product_name,
            active_ingredient=model.active_ingredient,
            target_disease=model.target_disease,
            start_date=model.start_date,
            estimated_duration_days=model.estimated_duration_days,
            end_date=model.end_date,
            application_method=model.application_method,
            dosage_applied=model.dosage_applied,
            dosage_unit=model.dosage_unit,
            batch_number=model.batch_number,
            supplier=model.supplier,
            expiry_date=model.expiry_date,
            status=model.status,
            final_result=model.final_result,
            final_hive_condition=model.final_hive_condition,
            requires_repeat=model.requires_repeat,
            future_recommendations=model.future_recommendations,
            applied_by=model.applied_by,
            registration_date=model.registration_date,
            update_date=model.update_date,
            followups=followups
        )

    def _to_followup_entity(self, model: TreatmentFollowupModel) -> TreatmentFollowup:
        return TreatmentFollowup(
            followup_id=model.followup_id,
            treatment_id=model.treatment_id,
            review_date=model.review_date,
            hive_condition=model.hive_condition,
            observed_changes=model.observed_changes,
            partial_results=model.partial_results,
            infestation_level=model.infestation_level,
            notes=model.notes,
            reviewer=model.reviewer,
            registration_date=model.registration_date
        )

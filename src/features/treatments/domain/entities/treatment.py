from datetime import datetime, date
from typing import Optional, List
from uuid import UUID

class TreatmentFollowup:
    def __init__(
        self,
        followup_id: UUID,
        treatment_id: UUID,
        review_date: date,
        hive_condition: Optional[str] = None,
        observed_changes: Optional[str] = None,
        partial_results: Optional[str] = None,
        infestation_level: Optional[str] = None,
        notes: Optional[str] = None,
        reviewer: Optional[str] = None,
        registration_date: Optional[datetime] = None,
    ):
        self.followup_id = followup_id
        self.treatment_id = treatment_id
        self.review_date = review_date
        self.hive_condition = hive_condition
        self.observed_changes = observed_changes
        self.partial_results = partial_results
        self.infestation_level = infestation_level
        self.notes = notes
        self.reviewer = reviewer
        self.registration_date = registration_date

class Treatment:
    def __init__(
        self,
        id: UUID,
        hive_id: UUID,
        treatment_type: str,
        product_name: str,
        start_date: date,
        active_ingredient: Optional[str] = None,
        target_disease: Optional[str] = None,
        estimated_duration_days: Optional[int] = None,
        end_date: Optional[date] = None,
        application_method: Optional[str] = None,
        dosage_applied: Optional[str] = None,
        dosage_unit: Optional[str] = None,
        batch_number: Optional[str] = None,
        supplier: Optional[str] = None,
        expiry_date: Optional[date] = None,
        status: str = 'active',
        final_result: Optional[str] = None,
        final_hive_condition: Optional[str] = None,
        requires_repeat: bool = False,
        future_recommendations: Optional[str] = None,
        applied_by: Optional[str] = None,
        registration_date: Optional[datetime] = None,
        update_date: Optional[datetime] = None,
        followups: List[TreatmentFollowup] = None
    ):
        self.id = id
        self.hive_id = hive_id
        self.treatment_type = treatment_type
        self.product_name = product_name
        self.start_date = start_date
        self.active_ingredient = active_ingredient
        self.target_disease = target_disease
        self.estimated_duration_days = estimated_duration_days
        self.end_date = end_date
        self.application_method = application_method
        self.dosage_applied = dosage_applied
        self.dosage_unit = dosage_unit
        self.batch_number = batch_number
        self.supplier = supplier
        self.expiry_date = expiry_date
        self.status = status
        self.final_result = final_result
        self.final_hive_condition = final_hive_condition
        self.requires_repeat = requires_repeat
        self.future_recommendations = future_recommendations
        self.applied_by = applied_by
        self.registration_date = registration_date
        self.update_date = update_date
        self.followups = followups or []

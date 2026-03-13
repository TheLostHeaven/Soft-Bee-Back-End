from datetime import datetime
from typing import Optional
from uuid import UUID


class Beehive:
    def __init__(
        self,
        id: UUID,
        apiary_id: UUID,
        hive_number: int,
        activity_level: Optional[str],
        bee_population: Optional[str],
        food_frames: Optional[int],
        brood_frames: Optional[int],
        hive_status: Optional[str],
        health_status: Optional[str],
        has_production_chamber: Optional[str],
        observations: Optional[str],
        treatments: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.apiary_id = apiary_id
        self.hive_number = hive_number
        self.activity_level = activity_level
        self.bee_population = bee_population
        self.food_frames = food_frames
        self.brood_frames = brood_frames
        self.hive_status = hive_status
        self.health_status = health_status
        self.has_production_chamber = has_production_chamber
        self.observations = observations
        self.treatments = treatments
        self.created_at = created_at
        self.updated_at = updated_at

from datetime import datetime
from typing import Optional
from uuid import UUID


class Beehive:
    def __init__(
        self,
        beehive_id: UUID,
        apiary_id: UUID,
        beehive_number: Optional[int] = None,
        activity_level: Optional[str] = None,
        bee_population: Optional[str] = None,
        food_frames: Optional[int] = None,
        brood_frames: Optional[int] = None,
        hive_status: Optional[str] = None,
        health_status: Optional[str] = None,
        has_production_chamber: Optional[str] = None,
        observations: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.beehive_id = beehive_id
        self.apiary_id = apiary_id
        self.beehive_number = beehive_number
        self.activity_level = activity_level
        self.bee_population = bee_population
        self.food_frames = food_frames
        self.brood_frames = brood_frames
        self.hive_status = hive_status
        self.health_status = health_status
        self.has_production_chamber = has_production_chamber
        self.observations = observations
        self.created_at = created_at
        self.updated_at = updated_at

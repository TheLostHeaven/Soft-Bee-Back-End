from src.features.beehive.domain.entities.beehive import Beehive
from src.features.beehive.application.dto.beehive_dto import BeehiveDTO
from src.features.beehive.domain.enums.beehive_enums import ActivityLevel, BeePopulation, HiveStatus, HealthStatus, HasProductionChamber


class BeehiveMapper:
    @staticmethod
    def to_dto(beehive: Beehive) -> BeehiveDTO:
        return BeehiveDTO(
            beehive_id=beehive.beehive_id,
            apiary_id=beehive.apiary_id,
            beehive_number=beehive.beehive_number,
            activity_level=beehive.activity_level,
            bee_population=beehive.bee_population,
            food_frames=beehive.food_frames,
            brood_frames=beehive.brood_frames,
            hive_status=beehive.hive_status,
            health_status=beehive.health_status,
            has_production_chamber=beehive.has_production_chamber,
            observations=beehive.observations,
            created_at=beehive.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=beehive.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

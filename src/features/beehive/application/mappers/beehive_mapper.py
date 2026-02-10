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
            activity_level=ActivityLevel(beehive.activity_level) if beehive.activity_level else None,
            bee_population=BeePopulation(beehive.bee_population) if beehive.bee_population else None,
            food_frames=beehive.food_frames,
            brood_frames=beehive.brood_frames,
            hive_status=HiveStatus(beehive.hive_status) if beehive.hive_status else None,
            health_status=HealthStatus(beehive.health_status) if beehive.health_status else None,
            has_production_chamber=HasProductionChamber(beehive.has_production_chamber) if beehive.has_production_chamber else None,
            observations=beehive.observations,
            created_at=beehive.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=beehive.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        )

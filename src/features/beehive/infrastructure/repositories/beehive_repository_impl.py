from typing import List, Optional
from sqlalchemy.orm import Session
from src.features.beehive.application.dto.beehive_dto import CreateBeehiveDTO, UpdateBeehiveDTO
from src.features.beehive.application.interfaces.repositories.beehive_repository import IBeehiveRepository
from src.features.beehive.domain.entities.beehive import Beehive
from src.features.beehive.infrastructure.models.beehive_model import BeehiveModel
from src.features.apiaries.infrastructure.models.apiary_model import ApiaryModel
from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException
from sqlalchemy.exc import IntegrityError
from uuid import UUID


class BeehiveRepositoryImpl(IBeehiveRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_beehive(self, beehive_dto: CreateBeehiveDTO) -> Beehive:
        new_beehive = BeehiveModel(**beehive_dto.model_dump())
        self.db_session.add(new_beehive)
        self.db_session.flush()  # Flush to get the ID

        # Update beehives_count in the related apiary
        apiary = self.db_session.query(ApiaryModel).filter(ApiaryModel.id == beehive_dto.apiary_id).first()
        if apiary:
            apiary.beehives_count = (apiary.beehives_count or 0) + 1
        
        self.db_session.commit()
        self.db_session.refresh(new_beehive)
        
        return self._to_entity(new_beehive)

    def get_beehive_by_id(self, id: UUID) -> Optional[Beehive]:
        beehive = self.db_session.query(BeehiveModel).filter(BeehiveModel.id == id).first()
        return self._to_entity(beehive) if beehive else None

    def get_all_beehives_by_apiary_id(self, apiary_id: UUID) -> List[Beehive]:
        beehives = self.db_session.query(BeehiveModel).filter(BeehiveModel.apiary_id == apiary_id).all()
        return [self._to_entity(beehive) for beehive in beehives]

    def update_beehive(self, id: UUID, beehive_dto: UpdateBeehiveDTO) -> Beehive:
        beehive = self.db_session.query(BeehiveModel).filter(BeehiveModel.id == id).first()
        if not beehive:
            raise BeehiveNotFoundException(id)

        update_data = beehive_dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(beehive, key, value)
        
        self.db_session.commit()
        self.db_session.refresh(beehive)
        
        return self._to_entity(beehive)

    def delete_beehive(self, id: UUID) -> bool:
        beehive = self.db_session.query(BeehiveModel).filter(BeehiveModel.id == id).first()
        if not beehive:
            raise BeehiveNotFoundException(id)
        
        apiary_id = beehive.apiary_id
        self.db_session.delete(beehive)

        # Update beehives_count in the related apiary
        apiary = self.db_session.query(ApiaryModel).filter(ApiaryModel.id == apiary_id).first()
        if apiary:
            apiary.beehives_count = (apiary.beehives_count or 1) - 1

        self.db_session.commit()
        return True

    def _to_entity(self, model: BeehiveModel) -> Beehive:
        if not model:
            return None
        return Beehive(
            id=model.id,
            apiary_id=model.apiary_id,
            activity_level=model.activity_level,
            bee_population=model.bee_population,
            food_frames=model.food_frames,
            brood_frames=model.brood_frames,
            hive_status=model.hive_status,
            health_status=model.health_status,
            has_production_chamber=model.has_production_chamber,
            observations=model.observations,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

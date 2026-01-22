from typing import Optional, List
from sqlalchemy.orm import Session
from src.features.apiaries.domain.entities.apiary import Apiary
from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper
from src.features.apiaries.infrastructure.models.apiary_model import ApiaryModel
import datetime

class ApiaryRepositoryImpl(ApiaryRepository):
    """Implementation of the apiary repository with SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_all_apiaries(self) -> List[Apiary]:
        apiary_models = self.db_session.query(ApiaryModel).all()
        return [ApiaryMapper.to_entity(model) for model in apiary_models]

    def get_apiary_by_id(self, apiary_id: int) -> Optional[Apiary]:
        
        apiary_model = self.db_session.query(ApiaryModel).filter_by(id=apiary_id).first()
        return ApiaryMapper.to_entity(apiary_model) if apiary_model else None
    
    def create_apiary(self, apiary: Apiary) -> Apiary:
        apiary_model = ApiaryMapper.to_model(apiary)
        self.db_session.add(apiary_model)
        self.db_session.flush()
        self.db_session.refresh(apiary_model)
        return ApiaryMapper.to_entity(apiary_model)
    
    def update_apiary(self, apiary: Apiary) -> Apiary:
            
        existing_apiary_model = self.db_session.query(ApiaryModel).filter_by(id=apiary.id).first()
        
        if not existing_apiary_model:
            raise ValueError(f"Apiary with ID {apiary.id} not found.")

        existing_apiary_model.name = apiary.name
        existing_apiary_model.location = apiary.location
        existing_apiary_model.user_id = apiary.user_id
        existing_apiary_model.beehives_count = apiary.beehives_count
        existing_apiary_model.treatments = apiary.treatments
        existing_apiary_model.updated_at = datetime.datetime.utcnow()
        
        self.db_session.flush()
        self.db_session.refresh(existing_apiary_model)
        return ApiaryMapper.to_entity(existing_apiary_model)

    def delete_apiary(self, apiary_id: int) -> None:
            
        apiary_model = self.db_session.query(ApiaryModel).filter_by(id=apiary_id).first()
        if apiary_model:
            self.db_session.delete(apiary_model)
            self.db_session.flush()
        else:
            raise ValueError(f"Apiary with ID {apiary_id} not found.")

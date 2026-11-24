from typing import Optional, List
from sqlalchemy.orm import Session
from src.features.apiaries.domain.entities.apiary import Apiary
from src.features.apiaries.application.interfaces.repositories.apiary_repository import ApiaryRepository
from src.features.apiaries.application.mappers.apiary_mapper import ApiaryMapper
from src.features.apiaries.infrastructure.models.apiary_model import ApiaryModel
from src.core.pagination import Page
import datetime
from uuid import UUID

class ApiaryRepositoryImpl(ApiaryRepository):
    """Implementation of the apiary repository with SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_all_apiaries(self) -> List[Apiary]:
        apiary_models = self.db_session.query(ApiaryModel).all()
        return [ApiaryMapper.to_entity(model) for model in apiary_models]

    def get_apiary_by_id(self, apiary_id: UUID) -> Optional[Apiary]:
        
        apiary_model = self.db_session.query(ApiaryModel).filter_by(id=apiary_id).first()
        return ApiaryMapper.to_entity(apiary_model) if apiary_model else None

    def get_apiaries_by_user_id(self, user_id: UUID) -> List[Apiary]:
        apiary_models = (
            self.db_session.query(ApiaryModel)
            .filter_by(user_id=user_id)
            .order_by(ApiaryModel.created_at, ApiaryModel.id)
            .all()
        )
        return [ApiaryMapper.to_entity(model) for model in apiary_models]
    
    def get_all_apiaries_paginated(self, limit: int, offset: int) -> Page[Apiary]:
        query = self.db_session.query(ApiaryModel)
        return self._paginate(query, limit, offset)

    def get_apiaries_by_user_id_paginated(self, user_id: UUID, limit: int, offset: int) -> Page[Apiary]:
        query = self.db_session.query(ApiaryModel).filter_by(user_id=user_id)
        return self._paginate(query, limit, offset)

    def _paginate(self, query, limit: int, offset: int) -> Page[Apiary]:
        total = query.count()
        # Stable ordering (id as tie-breaker) so pages never overlap or skip rows
        models = (
            query.order_by(ApiaryModel.created_at, ApiaryModel.id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return Page(
            items=[ApiaryMapper.to_entity(model) for model in models],
            total=total,
            limit=limit,
            offset=offset,
        )

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

    def delete_apiary(self, apiary_id: UUID) -> None:
            
        apiary_model = self.db_session.query(ApiaryModel).filter_by(id=apiary_id).first()
        if apiary_model:
            self.db_session.delete(apiary_model)
            self.db_session.flush()
        else:
            raise ValueError(f"Apiary with ID {apiary_id} not found.")

from src.features.apiaries.domain.entities.apiary import Apiary
from src.features.apiaries.infrastructure.models.apiary_model import ApiaryModel
from src.features.apiaries.application.dto.apiary_dto import ApiaryDto, CreateApiaryDto, UpdateApiaryDto
from uuid import UUID

class ApiaryMapper:
    """Maps between Apiary entity, ApiaryModel, and ApiaryDto"""

    @staticmethod
    def to_entity(apiary_model: ApiaryModel) -> Apiary:
        """Converts an ApiaryModel to an Apiary entity"""
        if not apiary_model:
            return None
        
        return Apiary(
            id=apiary_model.id,
            name=apiary_model.name,
            location=apiary_model.location,
            user_id=apiary_model.user_id,
            beehives_count=apiary_model.beehives_count,
            treatments=apiary_model.treatments,
            created_at=apiary_model.created_at,
            updated_at=apiary_model.updated_at
        )

    @staticmethod
    def to_model(apiary_entity: Apiary) -> ApiaryModel:
        """Converts an Apiary entity to an ApiaryModel"""
        if not apiary_entity:
            return None
            
        return ApiaryModel(
            id=apiary_entity.id if apiary_entity.id else None,
            name=apiary_entity.name,
            location=apiary_entity.location,
            user_id=apiary_entity.user_id,
            beehives_count=apiary_entity.beehives_count,
            treatments=apiary_entity.treatments,
            created_at=apiary_entity.created_at,
            updated_at=apiary_entity.updated_at
        )

    @staticmethod
    def to_dto(apiary_entity: Apiary) -> ApiaryDto:
        """Converts an Apiary entity to an ApiaryDto"""
        if not apiary_entity:
            return None
        
        return ApiaryDto(
            id=apiary_entity.id,
            name=apiary_entity.name,
            location=apiary_entity.location,
            user_id=str(apiary_entity.user_id),
            beehives_count=apiary_entity.beehives_count,
            treatments=apiary_entity.treatments,
            created_at=apiary_entity.created_at,
            updated_at=apiary_entity.updated_at
        )

    @staticmethod
    def from_create_dto_to_entity(create_dto: CreateApiaryDto, apiary_id: UUID = None) -> Apiary:
        """Converts CreateApiaryDto to an Apiary entity"""
        return Apiary(
            id=apiary_id,
            user_id=create_dto.user_id,
            name=create_dto.name,
            location=create_dto.location,
            beehives_count=create_dto.beehives_count,
            treatments=create_dto.treatments
        )

    @staticmethod
    def from_update_dto_to_entity(update_dto: UpdateApiaryDto, existing_entity: Apiary) -> Apiary:
        """Updates an existing Apiary entity with data from UpdateApiaryDto"""
        if not existing_entity:
            raise ValueError("Existing Apiary entity cannot be None for update.")
            
        existing_entity.name = update_dto.name if update_dto.name is not None else existing_entity.name
        existing_entity.location = update_dto.location if update_dto.location is not None else existing_entity.location
        existing_entity.beehives_count = update_dto.beehives_count if update_dto.beehives_count is not None else existing_entity.beehives_count
        existing_entity.treatments = update_dto.treatments if update_dto.treatments is not None else existing_entity.treatments
        # user_id is not updatable via this DTO based on current DTO structure
        return existing_entity

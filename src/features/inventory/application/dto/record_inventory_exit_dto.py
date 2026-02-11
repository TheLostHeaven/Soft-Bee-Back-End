from pydantic import BaseModel, Field
from uuid import UUID

class RecordInventoryExitDTO(BaseModel):
    item_id: UUID
    quantity: int = Field(..., gt=0)
    person: str = Field(..., min_length=1)

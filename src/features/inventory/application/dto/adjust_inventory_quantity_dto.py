from pydantic import BaseModel

class AdjustInventoryQuantityDTO(BaseModel):
    amount: int
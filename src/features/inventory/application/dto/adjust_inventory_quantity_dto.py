from pydantic import BaseModel


class AdjustInventoryQuantityDTO(BaseModel):
    item_id: int
    amount: int

class InventoryError(Exception):
    """Base exception for inventory-related errors."""
    pass

class InventoryNotFoundError(InventoryError):
    """Raised when an inventory item is not found."""
    def __init__(self, inventory_id: str):
        self.inventory_id = inventory_id
        super().__init__(f"Inventory item with ID '{inventory_id}' not found.")

class InvalidInventoryAdjustmentError(InventoryError):
    """Raised when an adjustment would result in a negative quantity."""
    def __init__(self, message: str = "Invalid adjustment amount."):
        self.message = message
        super().__init__(self.message)

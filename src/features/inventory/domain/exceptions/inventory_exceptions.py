class InventoryNotFoundException(Exception):
    """Custom exception raised when an inventory item is not found."""
    def __init__(self, message="Inventory not found"):
        self.message = message
        super().__init__(self.message)

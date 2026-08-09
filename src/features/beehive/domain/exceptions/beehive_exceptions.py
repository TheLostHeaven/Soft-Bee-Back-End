from uuid import UUID

class BeehiveException(Exception):
    """Base class for exceptions in the beehive feature."""
    pass


class BeehiveNotFoundException(BeehiveException):
    """Raised when a beehive is not found."""
    def __init__(self, id: UUID):
        self.id = id
        super().__init__(f"Beehive with id {id} not found.")


class DuplicateHiveNumberException(BeehiveException):
    """Raised when a hive number already exists in the same apiary."""
    def __init__(self, hive_number: int, apiary_id):
        self.hive_number = hive_number
        self.apiary_id = apiary_id
        super().__init__(
            f"Hive number {hive_number} already exists in apiary {apiary_id}."
        )

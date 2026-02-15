from uuid import UUID

class BeehiveException(Exception):
    """Base class for exceptions in the beehive feature."""
    pass


class BeehiveNotFoundException(BeehiveException):
    """Raised when a beehive is not found."""
    def __init__(self, id: UUID):
        self.id = id
        super().__init__(f"Beehive with id {id} not found.")

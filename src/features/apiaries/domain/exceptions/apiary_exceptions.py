class ApiaryNotFoundError(Exception):
    def __init__(self, message="Apiary not found"):
        self.message = message
        super().__init__(self.message)

class ApiaryAlreadyExistsError(Exception):
    def __init__(self, message="Apiary with this name already exists"):
        self.message = message
        super().__init__(self.message)

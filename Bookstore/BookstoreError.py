class BookStoreError(Exception):
    def __init__(self, message, status):
        super().__init__()
        self.message = message
        self.status = status

    def __str__(self):
        return self.message, self.status

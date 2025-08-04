class ValidationError(Exception):
    def __init__(self, message, table_name, back_name, field_name = None):
        super().__init__(message)
        self.message = message
        self.table_name = table_name
        self.back_name = back_name
        self.field_name = field_name
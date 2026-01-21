class BaseAppException(Exception):
    pass

class UserExistError(BaseAppException):
    pass

class UserNotFoundError(BaseAppException):
    pass

class WrongPasswordError(BaseAppException):
    pass

class InvalidTokenError(BaseAppException):
    pass

class InvalidMessagesError(BaseAppException):
    pass

class ExpiredTokenError(BaseAppException):
    pass

class NoPermissionError(BaseAppException):
    pass

class NoWritePermissionError(NoPermissionError):
    def __init__(self, message: dict):
        super().__init__()
        self.error_message = message

class NoReadPermissionError(NoPermissionError):
    pass
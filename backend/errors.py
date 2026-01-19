class UserExistError(BaseException):
    pass

class UserNotFoundError(BaseException):
    pass

class WrongPasswordError(BaseException):
    pass

class InvalidTokenError(BaseException):
    pass

class InvalidMessagesError(BaseException):
    pass

class ExpiredTokenError(BaseException):
    pass

class NoPermissionError(BaseException):
    pass

class NoWritePermissionError(NoPermissionError):
    def __init__(self, message: dict):
        super().__init__()
        self.error_message = message

class NoReadPermissionError(NoPermissionError):
    pass
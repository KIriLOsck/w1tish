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
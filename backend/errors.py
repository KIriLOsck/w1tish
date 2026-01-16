class UserExistError(BaseException):
    pass

class UserNotFoundError(BaseException):
    pass

class WrongPasswordError(BaseException):
    pass

class InvalidRefreshToken(BaseException):
    pass

class InvalidAccessToken(BaseException):
    pass
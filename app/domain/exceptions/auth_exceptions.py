class AuthException(Exception):
    """Base domain exception for authentication errors"""
    pass


class InvalidCredentialsException(AuthException):
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message)


class UserAlreadyExistsException(AuthException):
    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(message)


class OrganizationAlreadyExistsException(AuthException):
    def __init__(self, message: str = "Organization with this slug already exists"):
        super().__init__(message)


class UserNotFoundException(AuthException):
    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class OrganizationNotFoundException(AuthException):
    def __init__(self, message: str = "Organization not found"):
        super().__init__(message)


class InvalidTokenException(AuthException):
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)


class TokenRevokedException(AuthException):
    def __init__(self, message: str = "Token has been revoked"):
        super().__init__(message)


class PermissionDeniedException(AuthException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)

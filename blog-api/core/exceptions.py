class DomainError(Exception):
    """Базовый тип ошибки."""

class InvalidCredentialsError(DomainError):
    """Неверный email или пароль."""

class InvalidTokenError(DomainError):
    """Токен отсутствует, невалиден или истёк."""

class EmailAlreadyExistsError(DomainError):
    """Email уже занят."""
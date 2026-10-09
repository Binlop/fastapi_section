from core.exceptions import NotFoundError

class UserNotFoundError(NotFoundError):
    model_name = "Post"
from core.exceptions import NotFoundError, PermissionDeniedError

class PostNotFoundError(NotFoundError):
    model_name = "Post"

class PostAccessDeniedError(PermissionDeniedError):
    def __init__(self, post_id: int, user_id: int):
        self.post_id = post_id
        self.user_id = user_id
        super().__init__(f"User {user_id} cannot edit post {post_id}")

class CommentNotFoundError(NotFoundError):
    model_name = "Comment"

class CommentAccessDeniedError(PermissionDeniedError):
    def __init__(self, comment_id: int, user_id: int):
        self.comment_id = comment_id
        self.user_id = user_id
        super().__init__(f"User {user_id} cannot modify comment {comment_id}")
from db.uow import UnitOfWork
from posts.repository import PostRepository, CommentRepository
from posts.domain import PostReadCommand, PostCreateCommand, PostUpdateCommand, CommentCreateCommand
from posts.exceptions import PostNotFoundError, PostAccessDeniedError, CommentNotFoundError, CommentAccessDeniedError
from posts.models import Post, Comment
from auth.models import User

class PostService:
    def __init__(self, uow: UnitOfWork):
        self.post_repository = PostRepository(uow=uow)

    async def get_post_or_404(self, post_id: int) -> PostReadCommand:
        post = await self.post_repository.get_post_by_id(post_id)
        if post is None:
            raise PostNotFoundError(post_id)
        return post

    async def create_post(self, data: PostCreateCommand) -> Post:
        post = await self.post_repository.create_post(data)
        return post
    
    async def update_post(self, data: PostUpdateCommand, user: User) -> Post:
        post = await self.post_repository.get_post_by_id(data.id)
        if post is None:
            raise PostNotFoundError(data.id)
        if post.author_id != user.id:
            raise PostAccessDeniedError(data.id, user.id)
        if data.title is not None:
            post.title = data.title
        if data.content is not None:
            post.content = data.content
        return post

    async def delete_post(self, post_id: int, user: User) -> None:
        post = await self.post_repository.get_post_by_id(post_id)
        if post is None:
            raise PostNotFoundError(post_id)
        if post.author_id != user.id:
            raise PostAccessDeniedError(post_id, user.id)
        await self.post_repository.uow.db.delete(post)

class CommentService:
    def __init__(self, uow: UnitOfWork):
        self.comment_repository = CommentRepository(uow=uow)

    async def create_comment(self, data: CommentCreateCommand) -> Comment:
        comment = await self.comment_repository.create_comment(data)
        return comment

    async def delete_comment(self, comment_id, user: User) -> Comment:
        comment = await self.comment_repository.get_comment_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundError(comment_id)
        if comment.author_id != user.id:
            raise CommentAccessDeniedError(comment_id, user.id)
        await self.comment_repository.uow.db.delete(comment)
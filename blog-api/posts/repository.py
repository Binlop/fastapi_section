from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.uow import UnitOfWork
from posts.models import Post, Comment
from posts.domain import PostCreateCommand, CommentCreateCommand

class PostRepository:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_published_posts(self, limit: int = 10, offset: int = 0) -> list[Post]:
        stmt = (select(Post)
                .options(selectinload(Post.author))
                .order_by(Post.id.desc())
                .limit(limit).offset(offset))
        result = await self.uow.db.scalars(stmt)
        return list(result.all())

    async def get_post_by_id(self, post_id: int):
        stmt = (select(Post)
                .options(selectinload(Post.author))
                .where(Post.id == post_id))
        return await self.uow.db.scalar(stmt)

    async def create_post(self, data: PostCreateCommand) -> Post:
        post = Post(
            title=data.title,
            content=data.content,
            author_id=data.author_id
        )
        self.uow.db.add(post)
        await self.uow.db.flush()
        return post

class CommentRepository:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_comment_by_id(self, comment_id: int):
        stmt = (select(Comment)
                .options(selectinload(Comment.author))
                .where(Comment.id == comment_id))
        return await self.uow.db.scalar(stmt)

    async def get_comments_by_post(self, post_id: int, limit: int = 10, offset: int = 0) -> list[Comment]:
        stmt = (select(Comment)
                .options(
                    selectinload(Comment.author),
                    selectinload(Comment.post),
                    )
                .where(Comment.post_id == post_id)
                .order_by(Comment.id.desc())
                .limit(limit).offset(offset)
                )
        result = await self.uow.db.scalars(stmt)
        return list(result.all())
    
    async def create_comment(self, data: CommentCreateCommand) -> Comment:
        comment = Comment(
            text=data.text,
            post_id=data.post_id,
            author_id=data.author_id
        )
        self.uow.db.add(comment)
        await self.uow.db.flush()
        return comment

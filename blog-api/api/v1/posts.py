import structlog
log = structlog.get_logger(__name__)

from fastapi import APIRouter, status
from ws.manager import manager
from posts.schemas import PostCreate, PostRead, PostUpdate, CommentRead, CommentCreate
from posts.domain import PostCreateCommand, PostUpdateCommand, CommentCreateCommand
from api.deps import PaginationDep, UserDep
from posts.deps import PostRepoDep, PostServiceDep, CommentRepoDep, CommentServiceDep


router = APIRouter(prefix='/posts', tags=['Posts'])

class PostView:

    @router.get('/', response_model=list[PostRead])
    async def get_posts(repo: PostRepoDep, pagination: PaginationDep):
        posts = await repo.get_published_posts(limit=pagination.limit, offset=pagination.offset)
        return posts

    @router.get('/{post_id}', response_model=PostRead)
    async def get_post(post_id: int, service: PostServiceDep):
        return await service.get_post_or_404(post_id=post_id)

    @router.post("/", response_model=PostCreate, status_code=status.HTTP_201_CREATED)
    async def create_post(user: UserDep, data: PostCreate, service: PostServiceDep):
        cmd = PostCreateCommand(title=data.title, content=data.content, author_id=user.id)
        post = await service.create_post(cmd)
        log.info("post_created", post_id=post.id)
        return post

    @router.patch('/{post_id}', response_model=PostRead, status_code=status.HTTP_200_OK)
    async def update_post(post_id: int, user: UserDep, data: PostUpdate, service: PostServiceDep):
        cmd = PostUpdateCommand(id=post_id, title=data.title, content=data.content, author_id=data.author_id)
        post = await service.update_post(data=cmd, user=user)
        log.info("post_updated", post_id=post.id)
        return post

    @router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_post(post_id: int, user: UserDep, service: PostServiceDep):
        await service.delete_post(post_id=post_id, user=user)

class CommentView:

    @router.get('/{post_id}/comments', response_model=list[CommentRead])
    async def get_comments(post_id: int, repo: CommentRepoDep, pagination: PaginationDep):
        posts = await repo.get_comments_by_post(post_id=post_id, limit=pagination.limit, offset=pagination.offset)
        return posts

    @router.post("/{post_id}/comments", response_model=CommentCreate, status_code=status.HTTP_201_CREATED)
    async def create_comment(post_id: int, user: UserDep, data: CommentCreate, service: CommentServiceDep):
        cmd = CommentCreateCommand(text=data.text, post_id=post_id, author_id=user.id)
        comment = await service.create_comment(cmd)
        await manager.broadcast_to_post({
            "type": "new_comment",
            "text": comment.text,
            "author": user.username,
        })
        return comment

    @router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_comment(post_id: int, comment_id: int, user: UserDep, service: CommentServiceDep):
        await service.delete_comment(comment_id=comment_id, user=user)
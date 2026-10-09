from typing import Annotated
from fastapi import Depends
from db.uow import UnitOfWork
from posts.repository import PostRepository, CommentRepository
from posts.service import PostService, CommentService
from api.deps import get_uow

def get_post_repository(uow: UnitOfWork = Depends(get_uow)) -> PostRepository:
    return PostRepository(uow)

def get_post_service(uow: UnitOfWork = Depends(get_uow)) -> PostService:
    return PostService(uow)

def get_comment_repository(uow: UnitOfWork = Depends(get_uow)) -> CommentRepository:
    return CommentRepository(uow)

def get_comment_service(uow: UnitOfWork = Depends(get_uow)) -> CommentService:
    return CommentService(uow)

PostRepoDep = Annotated[PostRepository, Depends(get_post_repository)]
PostServiceDep = Annotated[PostService, Depends(get_post_service)]
CommentRepoDep = Annotated[CommentRepository, Depends(get_comment_repository)]
CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]
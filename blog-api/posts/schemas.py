from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class PostAuthor(BaseModel):
    id: int
    username: str

class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Заголовок поста")
    content: str = Field(..., min_length=10, description="Текст поста")

class PostCreate(PostBase):
    author_id: int

class PostRead(PostBase):
    id: int
    created_at: datetime | None = None
    author: PostAuthor

    model_config = ConfigDict(from_attributes=True)

class PostUpdate(PostBase):
    author_id: int

class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Текст комментария")
    post_id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)

class CommentRead(CommentCreate):
    text: str = Field(..., min_length=1, max_length=1000, description="Текст комментария")
    post_id: int
    author_id: int
    author: PostAuthor
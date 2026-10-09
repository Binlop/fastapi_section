from dataclasses import dataclass

@dataclass(frozen=True)
class PostAuthor:
    username: str

@dataclass(frozen=True)
class PostReadCommand:
    id: int
    title: str
    content: str
    author: PostAuthor

@dataclass(frozen=True)
class PostCreateCommand:
    title: str
    content: str
    author_id: int

@dataclass(frozen=True)
class PostUpdateCommand:
    id: int
    title: str
    content: str
    author_id: int

@dataclass(frozen=True)
class CommentCreateCommand:
    text: str
    post_id: int
    author_id: int

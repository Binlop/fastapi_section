posts: list[dict] = [
    {
        "id": 1,
        "title": "Первый пост о FastAPI",
        "content": "FastAPI — это современный фреймворк для создания API...",
        "author_id": 1,
    },
    {
        "id": 2,
        "title": "Зачем нужен Pydantic",
        "content": "Pydantic автоматически проверяет типы входящих данных...",
        "author_id": 1,
    },
    {
        "id": 3,
        "title": "Асинхронность в Python",
        "content": "async/await позволяют обрабатывать тысячи запросов одновременно...",
        "author_id": 2,
    },
]
next_post_id = 4

users = []
next_user_id = 1
from fastapi import APIRouter, HTTPException, Response
import storage as storage

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/')
async def get_posts():
    return storage.posts

@router.get('/{post_id}')
async def get_post(post_id: int):
    for post in storage.posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Пост не найден")

@router.post("/", status_code=201)
async def create_post(title: str, content: str, author_id: int):
    post = {
        "id": storage.next_post_id,
        "title": title,
        "content": content,
        "author_id": author_id,
    }
    storage.posts.append(post)
    storage.next_post_id += 1
    return post

@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int):
    for i, post in enumerate(storage.posts):
        if post["id"] == post_id:
            storage.posts.pop(i)
            # Для статуса 204 обязательно возвращаем пустой Response, 
            # чтобы FastAPI не пытался отправить клиенту "null"
            return Response(status_code=204)
            
    raise HTTPException(status_code=404, detail="Пост не найден")
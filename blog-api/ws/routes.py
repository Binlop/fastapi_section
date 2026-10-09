from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from ws.manager import manager
from ws.deps import post_id

router = APIRouter()

@router.websocket("/ws/posts/{post_id}/comments")
async def post_comments_ws(post_id: post_id, websocket: WebSocket) -> None:
    await manager.connect(websocket, post_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.broadcast_to_post(post_id, 
            {
                "type": "message",
                "text": data,
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket, post_id)
        # await manager.broadcast(f"[post {post_id}] кто-то отключился")
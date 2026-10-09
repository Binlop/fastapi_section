from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        self.posts: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, post_id: int, ):
        await websocket.accept()
        self.posts[post_id].append(websocket)

    def disconnect(self, websocket: WebSocket, post_id: int):
        if websocket in self.posts[post_id]:
            self.posts[post_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, post_id: int, message: str):
        post_connections = self.posts[post_id]
        for connection in post_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

    async def broadcast_to_post(self, post_id: int, message: dict) -> None:
        post_connections = self.posts[post_id]
        for connection in post_connections:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

manager = ConnectionManager()
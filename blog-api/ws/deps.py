from fastapi import Depends, WebSocket
from typing import Annotated

def get_post_id(websocket: WebSocket) -> int:
    return int(websocket.path_params['post_id'])

post_id = Annotated[int, Depends(get_post_id)]
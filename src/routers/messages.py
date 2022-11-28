from fastapi import (
    APIRouter, 
    Depends,
    status,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    )

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.schemas import GetMessage, Message
from models.models import messages
from utils.utils import get_current_user
from config.database import conn
from fastapi.responses import Response, HTMLResponse
import json
from typing import List

class SocketManager:
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user: str):
        await websocket.accept()
        self.active_connections.append((websocket, user))

    def disconnect(self, websocket: WebSocket, user: str):
        self.active_connections.remove((websocket, user))

    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection[0].send_json(data)    

manager = SocketManager()

messageRouter = APIRouter(
    prefix='/api/messages',
    tags=["messages"],
    dependencies=[Depends(get_current_user)]
)

@messageRouter.websocket("/ws/{chat_id}")
async def chat(websocket: WebSocket, token: str, chat_id: int):
    user = await get_current_user(token)
    if user.username:
        await manager.connect(websocket, token)
        response = {
            "username": user.username,
            "status": "got connected"
        }
        await manager.broadcast(response)
        try:
            while True:
                data = await websocket.receive_json()
                conn.execute(messages.insert().values(
                    message_text=data.get("message"),
                    user_id=user.user_id,
                    chatroom_id=chat_id
                ))
                response = {
                    "username": user.username,
                    "message": data.get("message")
                }
                await manager.broadcast(response)
        except Exception as e:
            print(e)
            manager.disconnect(websocket, token)
            response['status'] = "left"
            await manager.broadcast(response)




@messageRouter.post("", status_code=status.HTTP_201_CREATED, response_class=Response)
async def create_new_message(message: Message):
    conn.execute(messages.insert().values(
        message_text=message.message_text,
        user_id=message.user_id,
        chatroom_id=message.chatroom_id
    ))

# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var ws = new WebSocket("ws://localhost:8000/api/messages/ws");
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """
# @messageRouter.get("/asdf")
# async def get():
#     return HTMLResponse(html)



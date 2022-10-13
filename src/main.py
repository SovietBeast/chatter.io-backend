from datetime import timedelta
import imp
from fastapi import FastAPI, HTTPException, status, Depends, WebSocket
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.database import conn
from models.models import *
from schemas.schemas import *
from utils.utils import *
from sqlalchemy import or_
from jose.exceptions import JWTError
from routers import authorization, users, chatrooms, messages


app = FastAPI()
app.include_router(authorization.authRouter)
app.include_router(users.userRouter)
app.include_router(chatrooms.chatRouter)
app.include_router(messages.messageRouter)
onlineUsers = []


@app.get("/")
async def test_get():
    res = {}
    res['detail'] = 'It just works with auto deploy on main push ;)'
    return res

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text("ELOSZKA")
    
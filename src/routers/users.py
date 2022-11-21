from fastapi import (
    APIRouter, 
    Depends, 
    )
from schemas.schemas import (
    TokenData,
    GetUser,
    UserChatrooms,
    GetUserChatrooms,
    GetChatroom
    )
from models.models import users, users_chat, chatrooms
from utils.utils import get_current_user, decode_user_token
from config.database import conn
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response

userRouter = APIRouter(
    prefix='/api/users',
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@userRouter.get("/", response_model=list[GetUser])
async def get_all_user():
    return conn.execute(users.select()).fetchall()

@userRouter.get("/self")
async def get_user_self(token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    payload = decode_user_token(token)
    token_data = TokenData(username=payload.get("username"), user_id = payload.get("user_id"))
    return token_data

@userRouter.post("/add/chatroom", response_class=Response)
async def add_user_to_chatroom(chatroom_id: int, token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    usr_object = await get_current_user(token)
    us = UserChatrooms(user_id=usr_object.user_id, chat_id=chatroom_id)    
    conn.execute(users_chat.insert().values(
        user_id=us.user_id, 
        chat_id=us.chat_id
    ))


@userRouter.get("/get/chatrooms", response_model=list[GetChatroom])
async def get_user_chatrooms(token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    usr_object =  await get_current_user(token)
    user_chats_object =  conn.execute(users_chat.select().where(users_chat.c.user_id == usr_object.user_id)).fetchall()
    ret = []
    for chat in user_chats_object:
        print(chat)
        ret.append(dict(conn.execute(chatrooms.select().where(chatrooms.c.chatroom_id == chat.chat_id)).fetchone()))
    return ret


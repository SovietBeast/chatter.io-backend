from http.client import responses
from fastapi import (
    APIRouter, 
    Depends,
    HTTPException, 
    status
    )
from models.models import (
    chatrooms, 
    messages, 
    users_chat,
    users
    )
from schemas.schemas import Chatroom, GetChatroom, GetMessage, GetUser
from utils.utils import get_current_user
from config.database import conn
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer

chatRouter = APIRouter(
    prefix='/api/chatrooms',
    tags=["chatrooms"],
    dependencies=[Depends(get_current_user)]
)


@chatRouter.get("", response_model=list[GetChatroom])
async def get_all_chatrooms():
    return conn.execute(chatrooms.select()).fetchall()

@chatRouter.get("/public", response_model=list[GetChatroom])
async def get_public_chatrooms():
    return conn.execute(chatrooms.select().where(chatrooms.c.private == 'f')).fetchall()

@chatRouter.get("/{id}", response_model=GetChatroom)
async def get_chatroom_by_id(id: int):
    result = conn.execute(chatrooms.select().where(chatrooms.c.chatroom_id == id)).fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chatroom not found")
    return result

@chatRouter.post("", status_code=status.HTTP_201_CREATED, response_class=Response)
async def create_new_chatroom(chat: Chatroom, token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    if len(chat.name) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chatroom name must not be empty!")
    user = await get_current_user(token)
    created_chat = conn.execute(chatrooms.insert().values(
        user_id = user.user_id,
        name=chat.name,
        private=chat.private,
    ))

    conn.execute(users_chat.insert().values(
        user_id=user.user_id,
        chat_id=created_chat.inserted_primary_key[0]
     ))

    
@chatRouter.get("/{chatroom_id}/messages", response_model=list[GetMessage])
async def get_all_messages_for_chatroom_id(chatroom_id: int):
    chat_messages = conn.execute(messages.select().where(messages.c.chatroom_id == chatroom_id)).fetchall()
    messages_list = []
    for m in chat_messages:
        user = conn.execute(users.select().where(users.c.user_id == m.user_id)).fetchone()
        mess = GetMessage(message_id=m.message_id, message_text=m.message_text, user_id=m.user_id, chatroom_id=m.chatroom_id, username=user.username)
        messages_list.append(mess)
    return messages_list


@chatRouter.get("/{chatroom_id}/users", response_model=list[GetUser])
async def get_all_users_in_chatroom(chatroom_id: int):
    chat_users = conn.execute(users_chat.select().where(users_chat.c.chat_id == chatroom_id)).fetchall()
    print(chat_users)
    users_list = []
    for u in chat_users:
        us = conn.execute(users.select().where(users.c.user_id == u.user_id)).fetchone()
        user = GetUser(user_id=us.user_id, username=us.username, email=us.email)
        users_list.append(user)
    return users_list
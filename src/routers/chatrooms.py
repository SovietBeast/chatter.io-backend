from fastapi import (
    APIRouter, 
    Depends,
    HTTPException, 
    status
    )
from schemas.schemas import Chatroom, GetChatroom, GetMessage
from models.models import chatrooms, messages
from utils.utils import get_current_user
from config.database import conn

chatRouter = APIRouter(
    prefix='/api/chatrooms',
    tags=["chatrooms"],
    dependencies=[Depends(get_current_user)]
)


@chatRouter.get("/", response_model=list[GetChatroom])
async def get_all_chatrooms():
    return conn.execute(chatrooms.select()).fetchall()

@chatRouter.get("/{id}", response_model=GetChatroom)
async def get_chatroom_by_id(id: int):
    result = conn.execute(chatrooms.select().where(chatrooms.c.chatroom_id == id)).fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chatroom not found")
    return result

@chatRouter.post("/", response_model=GetChatroom, status_code=status.HTTP_201_CREATED)
async def create_new_chatroom(chat: Chatroom):
    insertedChat = conn.execute(chatrooms.insert().values(
        name=chat.name,
        private=chat.private,
        passcode=chat.passcode
    ))
    chat = dict(chat)
    
    chat['chatroom_id'] = insertedChat.inserted_primary_key[0]
    return chat

    
@chatRouter.get("/{chatroom_id}/messages", response_model=list[GetMessage])
async def get_all_messages_for_chatroom_id(chatroom_id: int):
    return conn.execute(messages.select().where(messages.c.chatroom_id == chatroom_id)).fetchall()
from http.client import responses
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
from fastapi.responses import Response

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

@chatRouter.post("/", status_code=status.HTTP_201_CREATED, response_class=Response)
async def create_new_chatroom(chat: Chatroom):
    if len(chat.name) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chatroom name must not be empty!")
    conn.execute(chatrooms.insert().values(
        name=chat.name,
        private=chat.private,
        passcode=chat.passcode
    ))

    
@chatRouter.get("/{chatroom_id}/messages", response_model=list[GetMessage])
async def get_all_messages_for_chatroom_id(chatroom_id: int):
    return conn.execute(messages.select().where(messages.c.chatroom_id == chatroom_id)).fetchall()
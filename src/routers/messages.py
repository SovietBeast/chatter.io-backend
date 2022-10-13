from fastapi import (
    APIRouter, 
    Depends,
    status
    )
from schemas.schemas import GetMessage, Message
from models.models import messages
from utils.utils import get_current_user
from config.database import conn

messageRouter = APIRouter(
    prefix='/api/messages',
    tags=["messages"],
    dependencies=[Depends(get_current_user)]
)

@messageRouter.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_message(message: Message):
    insertedMessage = conn.execute(messages.insert().values(
        message_text=message.message_text,
        user_id=message.user_id,
        chatroom_id=message.chatroom_id
    ))

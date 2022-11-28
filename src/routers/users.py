from fastapi import (
    APIRouter, 
    Depends, 
    status,
    HTTPException
    )
from schemas.schemas import (
    TokenData,
    GetUser,
    UserChatrooms,
    GetUserChatrooms,
    GetChatroom,
    UserChatroom
    )
from models.models import users, users_chat, chatrooms
from utils.utils import get_current_user, decode_user_token
from config.database import conn
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import Response
from sqlalchemy import and_

userRouter = APIRouter(
    prefix='/api/users',
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@userRouter.get("/", response_model=list[GetUser])
async def get_all_user():
    return conn.execute(users.select()).fetchall()

@userRouter.get("/self", response_model=GetUser)
async def get_user_self(token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    payload = decode_user_token(token)
    return conn.execute(users.select().where(users.c.user_id == payload.get("user_id"))).fetchone()


@userRouter.post("/add/chatroom",status_code=status.HTTP_201_CREATED, response_class=Response)
async def add_user_to_chatroom(userchat: UserChatroom, token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    user_admin = await get_current_user(token)
    chat_list =  conn.execute(chatrooms.select().where(chatrooms.c.user_id == user_admin.user_id)).fetchall()
    user_to_add_not_admin = conn.execute(users.select().where(users.c.username == userchat.user)).fetchone()
    users_chat_list = conn.execute(users_chat.select().where(users_chat.c.user_id == user_to_add_not_admin.user_id)).fetchall()
    ids = [x[0] for x in chat_list]
    if userchat.chatroom_id in ids:
        user_to_add = conn.execute(users.select().where(users.c.username == userchat.user)).fetchone()
        #us = UserChatrooms(user_id=user_to_add.user_id, chat_id=userchat.chatroom_id) 
        for uc_id in users_chat_list:
            if user_to_add.user_id == uc_id[1] and userchat.chatroom_id == uc_id[2]:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User already in chatroom")
            if  user_to_add_not_admin.user_id == uc_id[1] and userchat.chatroom_id == uc_id[2]:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User already in chatroom")
        conn.execute(users_chat.insert().values(
            user_id=user_to_add.user_id,
            chat_id=userchat.chatroom_id
        ))
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only chatroom owner is able to do that")



@userRouter.get("/mychats", response_model=list[GetChatroom])
async def get_mychats(token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    user_admin = await get_current_user(token)
    chat_list =  conn.execute(chatrooms.select().where(chatrooms.c.user_id == user_admin.user_id)).fetchall()
    return chat_list


@userRouter.get("/get/chatrooms", response_model=list[GetChatroom])
async def get_user_chatrooms(token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    usr_object =  await get_current_user(token)
    #user_chats_object =  conn.execute(users_chat.select().where(users_chat.c.user_id == usr_object.user_id and users_chat.c.chat_id == usr_object.chat_id)).fetchall()
    test = conn.execute(chatrooms.select().join(users_chat, isouter=True)).fetchall()
    return test
    # print(test)
    # ret = []
    # for chat in user_chats_object:
    #     ret.append(dict(conn.execute(chatrooms.select().where(chatrooms.c.chatroom_id == chat.chat_id)).fetchone()))
    # public_chats = conn.execute(chatrooms.select().where(chatrooms.c.private == 'f')).fetchall()
    # for public in public_chats:
    #     ret.append(dict(public))
    # return ret


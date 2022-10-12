from datetime import timedelta
from fastapi import FastAPI, HTTPException, status, Depends, WebSocket
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.database import conn
from models.models import chatrooms, users, messages
from schemas.schemas import Chatroom, GetChatroom, User, GetUser, Message, GetMessage, Token
from utils.utils import hashPassword, createAccessToken, verifyPassword, TOKEN_EXPIRE_TIME
from sqlalchemy import or_

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="api/login")
app = FastAPI()
onlineUsers = []


@app.get("/")
async def test_get():
    res = {}
    res['detail'] = 'It just works with auto deploy on main push ;)'
    return res

@app.get("/api/chatrooms", response_model=list[GetChatroom])
async def get_all_chatrooms():
    return conn.execute(chatrooms.select()).fetchall()

@app.get("/api/chatrooms/{id}", response_model=GetChatroom)
async def get_chatroom_by_id(id: int):
    result = conn.execute(chatrooms.select().where(chatrooms.c.chatroom_id == id)).fetchone()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chatroom not found")
    return result

@app.post("/api/chatrooms", response_model=GetChatroom)
async def create_new_chatroom(chat: Chatroom):
    insertedChat = conn.execute(chatrooms.insert().values(
        name=chat.name,
        private=chat.private,
        passcode=chat.passcode
    ))
    chat = dict(chat)
    
    chat['chatroom_id'] = insertedChat.inserted_primary_key[0]
    return chat

@app.post("/api/register", response_model=GetUser)
async def create_new_user(data: User):
    user = conn.execute(users.select().where(or_(users.c.username == data.username, users.c.email == data.email))).fetchone()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already taken")
    else:    
        conn.execute(users.insert().values(
            username=data.username,
            email=data.email,
            password=hashPassword(data.password)
        ))
        user = conn.execute(users.select().where(users.c.username == data.username)).fetchone()
        resp = dict(data)
        resp["user_id"] = user.user_id 
        return resp

@app.get("/api/users", response_model=list[GetUser])
async def get_all_user():
    return conn.execute(users.select()).fetchall()

@app.post("/api/login", response_model=Token)
async def login(data: OAuth2PasswordRequestForm = Depends()):
    user = conn.execute(users.select().where(users.c.username == data.username)).fetchone()
    if user:
        if verifyPassword(data.password, user.password):
            data = {
                "username": user.username,
                "user_id": user.user_id
            }
            access_token = createAccessToken(data, timedelta(minutes=TOKEN_EXPIRE_TIME))
            return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid username or password",
        headers={"WWW-authenticate": "Bearer"}
        )

@app.get("/api/chatroom/messages/{chatroom_id}", response_model=list[GetMessage])
async def get_all_messages_for_chatroom_id(chatroom_id: int):
    return conn.execute(messages.select().where(messages.c.chatroom_id == chatroom_id)).fetchall()

@app.post("/api/messages", response_model=GetMessage)
async def create_new_message(message: Message):
    insertedMessage = conn.execute(messages.insert().values(
        message_text=message.message_text,
        user_id=message.user_id,
        chatroom_id=message.chatroom_id
    ))
    message = dict(message)
    message['message_id'] = insertedMessage.inserted_primary_key[0]
    return message




# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_text("ELOSZKA")
    
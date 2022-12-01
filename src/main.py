from datetime import timedelta
from fastapi import FastAPI, HTTPException, status, Depends, WebSocket
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.database import conn
from models.models import *
from schemas.schemas import *
from utils.utils import *
from sqlalchemy import or_
from jose.exceptions import JWTError
from routers import authorization, users, chatrooms, messages
from fastapi.middleware.cors import CORSMiddleware

onlineUsers = []

app = FastAPI()
app.include_router(authorization.authRouter)
app.include_router(users.userRouter)
app.include_router(chatrooms.chatRouter)
app.include_router(messages.messageRouter)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    "https://chatter-io.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

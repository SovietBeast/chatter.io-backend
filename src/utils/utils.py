import os
from jose import jwt
from jose.exceptions import JWTError
from models.models import *
from schemas.schemas import *
from typing import Optional, Union, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, HTTPException, status, Depends, WebSocket
from config.database import conn


TOKEN_EXPIRE_TIME = 30 #minutes
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.urandom(16)
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="api/login")


# configure "engine" to hashing password 
passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str) -> str:
    return passwordContext.hash(password)

def verifyPassword(password: str, hashedPassword: str) -> bool:
    return passwordContext.verify(password, hashedPassword)

def createAccessToken(data: dict, expireTimeDelta: Optional[timedelta]):
    if expireTimeDelta:
        expire = datetime.utcnow() + expireTimeDelta
    else:
        expire = datetime.utcnow() + timedelta(TOKEN_EXPIRE_TIME)
    data.update({"exp": expire})
    jwtToken = jwt.encode(data, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return jwtToken

def decode_user_token(token: str):
    token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    return token

async def get_current_user(token: str = Depends(oauth2Scheme)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_user_token(token)
        username: str = payload.get("username")
        user_id: int = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id = user_id)
    except JWTError:
        raise credentials_exception
    
    user = conn.execute(users.select().where(users.c.username == token_data.username)).fetchone()
    if user is None:
        raise credentials_exception
    return user


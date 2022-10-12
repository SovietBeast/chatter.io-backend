import os
from jose import jwt
from typing import Optional, Union, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext

TOKEN_EXPIRE_TIME = 30 #minutes
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.urandom(16)

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

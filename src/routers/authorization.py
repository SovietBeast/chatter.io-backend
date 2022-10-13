from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException,
    status
    )
from schemas.schemas import (
    Token, 
    User,
    GetUser
    )
from models.models import users
from utils.utils import (
    get_current_user, 
    hashPassword, 
    verifyPassword, 
    createAccessToken,
    TOKEN_EXPIRE_TIME
    )

from sqlalchemy import or_
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from config.database import conn

authRouter = APIRouter(
    prefix='/api',
    tags=["auth"]
)


@authRouter.post("/register", status_code=status.HTTP_201_CREATED)
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

@authRouter.post("/login", response_model=Token)
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
from fastapi import (
    APIRouter, 
    Depends, 
    )
from schemas.schemas import (
    TokenData,
    GetUser
    )
from models.models import users
from utils.utils import get_current_user, decode_user_token
from config.database import conn
from fastapi.security import OAuth2PasswordBearer

userRouter = APIRouter(
    prefix='/api/users',
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@userRouter.get("/", response_model=list[GetUser])
async def get_all_user():
    return conn.execute(users.select()).fetchall()

@userRouter.get("/self")
async def get_user_self(token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/login"))):
    payload = decode_user_token(token)
    token_data = TokenData(username=payload.get("username"), user_id = payload.get("user_id"))
    return token_data


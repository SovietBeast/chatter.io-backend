from fastapi import (
    APIRouter, 
    Depends, 
    )
from schemas.schemas import (
    User,
    GetUser
    )
from models.models import users
from utils.utils import get_current_user
from config.database import conn

userRouter = APIRouter(
    prefix='/api/users',
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)

@userRouter.get("/", response_model=list[GetUser])
async def get_all_user():
    return conn.execute(users.select()).fetchall()

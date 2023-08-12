from datetime import datetime, timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.params import Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import async_sessionmaker

from the_remember.src.api.auth.logics import get_current_user, verify_password, get_password_hash
from the_remember.src.api.users.db_model import UserORM
from the_remember.src.api.users.dto import UserDTO, CreateUserDTO
from the_remember.src.config.config import CONFIG

user_app = APIRouter()


@user_app.get("/me/", response_model=UserDTO)
async def read_users_me(
    current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    return current_user


# @user_app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[UserDTO, Depends(get_current_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]

@user_app.post("/create", response_model=UserDTO, status_code=201)
async def create_user(
        new_user: CreateUserDTO
):
    async_session = async_sessionmaker(CONFIG.engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            res = await session.execute(insert(UserORM).returning(UserORM), [
                new_user.model_dump(exclude={'password'})
                | {'hashed_password': get_password_hash(new_user.password)}
            ])
            return UserDTO.model_validate(next(res)[0])

from datetime import datetime, timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from the_remember.src.api.auth.logics import get_current_user
from the_remember.src.api.users.dto import UserDTO

user_app = APIRouter()


@user_app.get("/users/me/", response_model=UserDTO)
async def read_users_me(
    current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    return current_user


@user_app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
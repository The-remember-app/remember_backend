
from datetime import datetime, timedelta
from typing import Annotated, Literal

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from the_remember.src.api.auth.dto import Token
from the_remember.src.api.auth.logics import authenticate_user, create_access_token, get_db_session
from the_remember.src.config.config import CONFIG
# from the_remember.src.db_models.fake_db import fake_users_db

auth_app = APIRouter()


@auth_app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    user = await authenticate_user(form_data.username, form_data.password, db_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_app.post("/healthcheck", response_model=Literal['ok'])
async def login_for_access_token():
    return 'ok'
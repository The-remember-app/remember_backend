from datetime import datetime, timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from the_remember.src.api.auth.dto import TokenData
from the_remember.src.api.users.db_model import UserORM
from the_remember.src.api.users.dto import UserInDbDTO, UserDTO
from the_remember.src.config.config import CONFIG
# from the_remember.src.db_models.fake_db import fake_users_db

async def get_db_session():
    async_session = async_sessionmaker(CONFIG.engine, expire_on_commit=False)
    async with async_session() as session:
        if True:
        # async with session.begin():
            try:
                yield session
            finally:
                pass

async def get_db_write_session(
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with db_session.begin():
        yield db_session


def verify_password(plain_password, hashed_password):
    return CONFIG.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return CONFIG.pwd_context.hash(password)






async def authenticate_user( username: str, password: str, db_session: AsyncSession):
    user = await get_user(username, db_session)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, CONFIG.SECRET_KEY, algorithm=CONFIG.ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(CONFIG.oauth2_scheme)],
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CONFIG.SECRET_KEY, algorithms=[CONFIG.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username, db_session=db_session)
    if user is None:
        raise credentials_exception
    return user





async def get_user(username: str, db_session: AsyncSession):
    res = await db_session.execute(
        select(UserORM).where(UserORM.username == username)
    )
    return UserInDbDTO.model_validate(next(res)[0])
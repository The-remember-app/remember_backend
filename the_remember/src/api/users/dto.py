from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    name: str
    surname: str

    created_at: datetime
    updated_at: datetime


class UserInDbDTO(UserDTO):
    hashed_password: str

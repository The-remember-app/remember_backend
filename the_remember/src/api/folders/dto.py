from __future__ import annotations

from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, Field


# from pydantic.types import


class FolderDTO(BaseModel,  extra='ignore', from_attributes=True):
    # model_config = ConfigDict()

    id: UUID
    name: str
    user_id: UUID
    root_folder_id: UUID | None = None
    sub_folders: list[FolderDTO] | None = None  #  Field(default_factory=lambda : list())

    created_at: datetime
    updated_at: datetime


class CreateFolderDTO(BaseModel):
    name: str
    root_folder_id: UUID | None = None

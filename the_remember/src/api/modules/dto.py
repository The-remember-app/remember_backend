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


class ModuleDTO(BaseModel, extra='ignore', from_attributes=True):
    # model_config = ConfigDict()

    id: UUID
    name: str
    author_id: UUID
    root_folder_id: UUID | None

    created_at: datetime
    updated_at: datetime


class CreateModuleDTO(BaseModel):
    name: str
    root_folder_id: UUID | None


class PersonalizeModuleDTO(ModuleDTO):
    user_id: UUID

    is_reverse_definition_write: bool
    standard_and_reverse_write: bool
    is_reverse_definition_choice: bool
    standard_and_reverse_choice: bool


    personal_created_at: datetime
    personal_updated_at: datetime

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


class TermDTO(BaseModel, extra='ignore', from_attributes=True):
    # model_config = ConfigDict()

    id: UUID
    term: str
    definition: str
    module_id: UUID


    created_at: datetime
    updated_at: datetime


class CreateTermDTO(BaseModel):
    term: str
    definition: str
    module_id: UUID


class PersonalizeTermDTO(TermDTO):
    user_id: UUID
    term_id: UUID

    choose_error_counter: int
    write_error_counter: int
    choice_neg_error_counter: int

    personal_created_at: datetime
    personal_updated_at: datetime

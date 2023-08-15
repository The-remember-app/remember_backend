from __future__ import annotations

from abc import ABC
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


class _AbstractSentenceDTO(BaseModel, ABC, extra='ignore', from_attributes=True):
    sentence: str
    translate: str


class CreateSentenceDTO(_AbstractSentenceDTO):
    term_id: UUID


class SentenceDTO(CreateSentenceDTO):
    # model_config = ConfigDict()

    id: UUID

    created_at: datetime
    updated_at: datetime


class CreateSentenceAsTreeDTO(_AbstractSentenceDTO):
    term_id: UUID | None = None



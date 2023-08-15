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

from the_remember.src.api.sentences.dto import CreateSentenceAsTreeDTO


# from pydantic.types import


class _AbstractTermDTO(BaseModel, ABC, extra='ignore', from_attributes=True):
    term: str
    definition: str
    transcription: str | None = None


class CreateTermDTO(_AbstractTermDTO):
    module_id: UUID


class TermDTO(CreateTermDTO):
    # model_config = ConfigDict()

    id: UUID
    module_id: UUID

    created_at: datetime
    updated_at: datetime


class CreateTermAsTreeDTO(_AbstractTermDTO):
    module_id: UUID | None = None
    sub_sentences: list[CreateSentenceAsTreeDTO | None] | None = None


class _AbstractPersonalizeTermDTO(BaseModel, ABC, extra='ignore', from_attributes=True):
    user_id: UUID

    choose_error_counter: int
    write_error_counter: int
    choice_neg_error_counter: int

    personal_created_at: datetime
    personal_updated_at: datetime


class PersonalizeTermDTO(TermDTO, _AbstractPersonalizeTermDTO):
    pass


class OnlyPersonalizePartTermDTO(_AbstractPersonalizeTermDTO):
    term_id: UUID
    module_id: UUID

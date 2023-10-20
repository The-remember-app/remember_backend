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
from the_remember.src.api.terms.enums import AddInfoTypeEnum, WatchLearnTypeEnum
from the_remember.src.utils.post_db import OrmBaseModel


class _AbstractTermDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    term: str
    definition: str


class _AbstractPersonalizeTermDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    user_id: UUID

    choose_error_counter: int
    write_error_counter: int
    choice_neg_error_counter: int
    watch_count: int

    personal_created_at: datetime
    personal_updated_at: datetime


class _AbstractAdditionalTermInfoDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    text_data: str | None
    adding_text_data: str | None = None
    dialect_or_area: str | None = None
    add_info_type: AddInfoTypeEnum = AddInfoTypeEnum.usual_term

    parent_add_info_id: UUID | None = None


class _AbstractLearnMarks(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    # user_id: UUID
    term_id: UUID

    start_watch: datetime
    end_watch: datetime
    is_learnt: bool
    is_learn_iter_start: bool
    watch_type: WatchLearnTypeEnum

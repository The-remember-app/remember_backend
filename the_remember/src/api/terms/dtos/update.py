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
from the_remember.src.api.terms.dtos.abstract import _AbstractTermDTO, _AbstractPersonalizeTermDTO, \
    _AbstractAdditionalTermInfoDTO
from the_remember.src.api.terms.dtos.create import CreateTermDTO, CreateAdditionalTermInfoDTO, \
    CreateAdditionalTermInfoAsTreeDTO
from the_remember.src.api.terms.enums import AddInfoTypeEnum
from the_remember.src.utils.post_db import OrmBaseModel


# from pydantic.types import


class UpdateOnlyPersonalizePartTermDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    term_id: UUID
    module_id: UUID

    choose_error_counter: int
    write_error_counter: int
    choice_neg_error_counter: int
    watch_count: int

    personal_updated_at: datetime
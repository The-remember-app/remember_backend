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
    _AbstractAdditionalTermInfoDTO, _AbstractLearnMarks
from the_remember.src.api.terms.dtos.create import CreateTermDTO, CreateAdditionalTermInfoDTO, \
    CreateAdditionalTermInfoAsTreeDTO
from the_remember.src.api.terms.enums import AddInfoTypeEnum
from the_remember.src.utils.post_db import OrmBaseModel


# from pydantic.types import


class TermDTO(CreateTermDTO):
    # model_config = ConfigDict()

    id: UUID
    module_id: UUID

    created_at: datetime
    updated_at: datetime


class PersonalizeTermDTO(TermDTO, _AbstractPersonalizeTermDTO):
    pass


class OnlyPersonalizePartTermDTO(_AbstractPersonalizeTermDTO):
    term_id: UUID
    module_id: UUID


class AdditionalTermInfoDTO(CreateAdditionalTermInfoDTO):
    id: UUID

    created_at: datetime
    updated_at: datetime


class TermWithAddInfoDTO(TermDTO):
    term_additional_info_entities: list[AdditionalTermInfoDTO] = []


class PersonalizeTermWithAddInfoDTO(TermWithAddInfoDTO, _AbstractPersonalizeTermDTO):
    pass


class TermAsTreeDTO(TermDTO):
    term_additional_info_entities: list[AdditionalTermInfoDTO] = []
    personalize: OnlyPersonalizePartTermDTO | None = None


class LearnMarkDTO(_AbstractLearnMarks):
    id: UUID
    user_id: UUID

    created_at: datetime
    updated_at: datetime
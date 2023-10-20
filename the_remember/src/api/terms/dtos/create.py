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
from the_remember.src.api.terms.enums import AddInfoTypeEnum
from the_remember.src.utils.post_db import OrmBaseModel


# from pydantic.types import


class CreateTermDTO(_AbstractTermDTO):
    module_id: UUID



class CreateAdditionalTermInfoDTO(_AbstractAdditionalTermInfoDTO):
    term_id: UUID


class CreateAdditionalTermInfoAsTreeDTO(_AbstractAdditionalTermInfoDTO):
    term_id: UUID | None = None
    sub_add_info_entities: list[CreateAdditionalTermInfoAsTreeDTO] | None = None



class CreateTermAsTreeDTO(_AbstractTermDTO):
    module_id: UUID | None = None
    sub_sentences: list[CreateSentenceAsTreeDTO | None] | None = None
    term_additional_info_entities: list[CreateAdditionalTermInfoAsTreeDTO] | None = None


class CreateLearnMarkDTO(_AbstractLearnMarks):
    # id: UUID | None = None
    pass
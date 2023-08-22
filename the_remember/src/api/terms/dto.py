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
from the_remember.src.api.terms.enums import AddInfoTypeEnum
from the_remember.src.utils.post_db import OrmBaseModel


# from pydantic.types import


class _AbstractTermDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    term: str
    definition: str


class CreateTermDTO(_AbstractTermDTO):
    module_id: UUID


class TermDTO(CreateTermDTO):
    # model_config = ConfigDict()

    id: UUID
    module_id: UUID

    created_at: datetime
    updated_at: datetime


class _AbstractPersonalizeTermDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
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


class _AbstractAdditionalTermInfoDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    text_data: str | None
    adding_text_data: str | None = None
    dialect_or_area: str | None = None
    add_info_type: AddInfoTypeEnum = AddInfoTypeEnum.usual_term

    parent_add_info_id: UUID | None = None


class CreateAdditionalTermInfoDTO(_AbstractAdditionalTermInfoDTO):
    term_id: UUID


class AdditionalTermInfoDTO(CreateAdditionalTermInfoDTO):
    id: UUID

    created_at: datetime
    updated_at: datetime


class CreateAdditionalTermInfoAsTreeDTO(_AbstractAdditionalTermInfoDTO):
    term_id: UUID | None = None
    sub_add_info_entities: list[CreateAdditionalTermInfoAsTreeDTO] | None = None


class CreateTermAsTreeDTO(_AbstractTermDTO):
    module_id: UUID | None = None
    sub_sentences: list[CreateSentenceAsTreeDTO | None] | None = None
    term_additional_info_entities: list[CreateAdditionalTermInfoAsTreeDTO] | None = None


class TermWithAddInfoDTO(TermDTO):
    term_additional_info_entities: list[AdditionalTermInfoDTO] = []


class PersonalizeTermWithAddInfoDTO(TermWithAddInfoDTO, _AbstractPersonalizeTermDTO):
    pass


class TermAsTreeDTO(TermDTO):
    term_additional_info_entities: list[AdditionalTermInfoDTO] = []
    personalize: OnlyPersonalizePartTermDTO | None = None


class UpdateOnlyPersonalizePartTermDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    term_id: UUID

    choose_error_counter: int
    write_error_counter: int
    choice_neg_error_counter: int

    personal_updated_at: datetime


class DeleteOnlyPersonalizePartTermDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    term_id: UUID
    user_id: UUID
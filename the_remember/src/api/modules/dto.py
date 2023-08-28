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

from the_remember.src.api.terms.dto import CreateTermDTO, CreateTermAsTreeDTO, TermDTO
from the_remember.src.utils.post_db import OrmBaseModel


# from pydantic.types import

class CreateModuleDTO(OrmBaseModel, extra='ignore', from_attributes=True):
    name: str
    description: str | None = ""
    root_folder_id: UUID | None = None


class ModuleDTO(CreateModuleDTO):
    id: UUID
    author_id: UUID

    created_at: datetime
    updated_at: datetime


class ModuleWithNestedEntitiesDTO(ModuleDTO):
    sub_terms: list[TermDTO | None] | None = None


class _AbstractPersonalizeModuleDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    user_id: UUID

    is_reverse_definition_write: bool
    standard_and_reverse_write: bool
    is_reverse_definition_choice: bool
    standard_and_reverse_choice: bool
    max_iteration_len: int
    min_iteration_len: int
    min_watch_count: int
    known_term_part: int
    choices_count: int
    is_learnt:bool


    personal_created_at: datetime
    personal_updated_at: datetime


class PersonalizeModuleDTO(ModuleDTO, _AbstractPersonalizeModuleDTO):
    pass


class OnlyPersonalizePartModuleDTO(_AbstractPersonalizeModuleDTO):
    module_id: UUID


class CreateModuleAsTreeDTO(CreateModuleDTO):
    id: UUID | None = None
    sub_terms: list[CreateTermAsTreeDTO] = []


class UpdateOnlyPersonalizePartModuleDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    module_id: UUID

    is_reverse_definition_write: bool
    standard_and_reverse_write: bool
    is_reverse_definition_choice: bool
    standard_and_reverse_choice: bool
    max_iteration_len: int
    min_iteration_len: int
    min_watch_count: int
    known_term_part: int
    choices_count: int
    is_learnt:bool

    personal_updated_at: datetime


class DeleteOnlyPersonalizePartModuleDTO(OrmBaseModel, ABC, extra='ignore', from_attributes=True):
    module_id: UUID
    user_id: UUID


'''
lie (lay, lain)
wear   wear (wore, worn)
de scribe      describe

alter — изменять, модицифировать что-то
The writers had to alter the script after the actress got sick – Сценаристам пришлось изменить сценарий после того, как актриса заболела

The tailor altered my shirt by making it shorter – Портной подправил мою рубашку, сделав ее короче
'''

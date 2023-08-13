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


# from pydantic.types import

class CreateModuleDTO(BaseModel, extra='ignore', from_attributes=True):
    name: str
    root_folder_id: UUID | None = None


class ModuleDTO(CreateModuleDTO):
    id: UUID
    author_id: UUID

    created_at: datetime
    updated_at: datetime


class ModuleWithNestedEntitiesDTO(ModuleDTO):
    sub_terms: list[TermDTO | None] | None = None


class _AbstractPersonalizeModuleDTO(BaseModel, ABC, extra='ignore', from_attributes=True):
    user_id: UUID

    is_reverse_definition_write: bool
    standard_and_reverse_write: bool
    is_reverse_definition_choice: bool
    standard_and_reverse_choice: bool

    personal_created_at: datetime
    personal_updated_at: datetime


class PersonalizeModuleDTO(ModuleDTO, _AbstractPersonalizeModuleDTO):
    pass


class OnlyPersonalizePartModuleDTO(_AbstractPersonalizeModuleDTO):
    module_id: UUID


class CreateModuleAsTreeDTO(CreateModuleDTO):
    id: UUID | None = None
    sub_terms: list[CreateTermAsTreeDTO] = []

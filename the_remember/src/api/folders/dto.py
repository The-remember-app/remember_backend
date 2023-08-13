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
from pydantic.functional_validators import AfterValidator, BeforeValidator, field_validator

from the_remember.src.api.modules.dto import CreateModuleAsTreeDTO, ModuleDTO, ModuleWithNestedEntitiesDTO
from the_remember.src.utils.validators import relation_validator


# from pydantic.types import


# RelFolderDTO = Annotated[FolderDTO | None, BeforeValidator(relation_validator)]

class CreateFolderDTO(BaseModel, extra='ignore', from_attributes=True):
    name: str
    root_folder_id: UUID | None = None


class FolderDTO(CreateFolderDTO):
    # model_config = ConfigDict()

    id: UUID
    user_id: UUID

    created_at: datetime
    updated_at: datetime

    # @field_validator('root_folder_entity', mode='before')
    # @classmethod
    # def test(cls, v):
    #     print("@@@@@@@@@@@@@@@!!!!!!!!!!-----------", type(v), v)
    #     if isinstance(v, str):
    #         return None
    #     return v


class FolderWithNestedEntitiesDTO(FolderDTO):
    sub_folders: list[FolderWithNestedEntitiesDTO | None] | None = None  # Field(default_factory=lambda : list())
    sub_modules: list[ModuleWithNestedEntitiesDTO | None] | None = None


class FolderWithRootEntityDTO(FolderDTO):
    root_folder_entity: FolderWithRootEntityDTO | None = None


# RelFolderDTO = Annotated[FolderDTO | None, BeforeValidator(relation_validator)]
# ListRelFolderDTO = Annotated[list[RelFolderDTO], BeforeValidator(relation_validator)]
#
# FolderDTO.model_rebuild()


class CreateFolderAsTreeDTO(CreateFolderDTO):
    id: UUID | None = None
    sub_folders: list[CreateFolderAsTreeDTO] = []
    sub_modules: list[CreateModuleAsTreeDTO] = []

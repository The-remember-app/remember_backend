from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from the_remember.src.api.auth.logics import get_db_session, get_current_user, get_db_write_session
from the_remember.src.api.folders.db_model import FolderORM
from the_remember.src.api.folders.dto import CreateFolderDTO, FolderDTO, CreateFolderAsTreeDTO, \
    FolderWithNestedEntitiesDTO, FolderWithRootEntityDTO
from the_remember.src.api.modules.db_model import ModuleORM
from the_remember.src.api.modules.dto import CreateModuleAsTreeDTO
from the_remember.src.api.terms.db_model import TermORM
from the_remember.src.api.terms.dto import CreateTermDTO, CreateTermAsTreeDTO
from the_remember.src.api.users.dto import UserDTO
from the_remember.src.config.config import CONFIG


def recourse_tree_to_db_models(
        obj: CreateFolderAsTreeDTO | CreateModuleAsTreeDTO | CreateTermAsTreeDTO,
        current_user: UserDTO,
        __deep: int = 0
) -> FolderORM | ModuleORM | TermORM:
    if isinstance(obj, CreateFolderAsTreeDTO):
        return FolderORM(
            **(obj.model_dump(
                exclude_unset=True,
                exclude_defaults=True,
                exclude_none=False
            ) | dict(
                user_id=current_user.id,
                sub_folders=[recourse_tree_to_db_models(i, current_user, __deep=__deep + 1) for i in obj.sub_folders],
                sub_modules=[recourse_tree_to_db_models(i, current_user, __deep=__deep + 1) for i in obj.sub_modules],
            ))
        )

    elif isinstance(obj, CreateModuleAsTreeDTO):
        return ModuleORM(
            **(obj.model_dump(
                exclude_unset=True,
                exclude_defaults=True,
                exclude_none=False
            ) | dict(
                author_id=current_user.id,
                sub_terms=[recourse_tree_to_db_models(i, current_user, __deep=__deep + 1) for i in obj.sub_terms],

            ))
        )
    elif isinstance(obj, CreateTermAsTreeDTO):
        return TermORM(
            **(obj.model_dump(
                exclude_unset=True,
                exclude_defaults=True,
                exclude_none=False
            ) | dict(

            ))
        )
    else:
        raise NotImplementedError()

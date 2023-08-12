from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from the_remember.src.api.auth.logics import get_db_session, get_current_user, get_db_write_session
from the_remember.src.api.modules.db_model import ModuleORM, PersonalizeModuleORM
from the_remember.src.api.modules.dto import ModuleDTO, CreateModuleDTO, PersonalizeModuleDTO
from the_remember.src.api.users.dto import UserDTO
from the_remember.src.config.config import CONFIG

module_app = APIRouter()


@module_app.post("/create", response_model=ModuleDTO, status_code=201)
async def create_module(
        new_module: CreateModuleDTO,
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]

):
    res = await db_session.execute(insert(ModuleORM).returning(ModuleORM), [
        new_module.model_dump() | {'author_id': current_user.id}
    ])
    data_ = list(res)
    data__ = data_[0]
    data = data__[0]
    # await db_session.commit()
    # data1 = res.raw.return_defaults
    return ModuleDTO.model_validate(data)


@module_app.get("/all", response_model=list[PersonalizeModuleDTO])
async def get_all_module(
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(PersonalizeModuleORM)
        .join(PersonalizeModuleORM.module_entity)
        .add_columns(ModuleORM)
        .where(PersonalizeModuleORM.user_id == current_user.id)
    )

    data = list(res)
    return [PersonalizeModuleDTO.model_validate(i[0].module_entity.__dict__ | i[0].__dict__) for i in data]


@module_app.get("/{module_id}", response_model=PersonalizeModuleDTO)
async def get_one_module(
        module_id: UUID,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(PersonalizeModuleORM)
        .join(PersonalizeModuleORM.module_entity)
        .add_columns(ModuleORM)
        .where((PersonalizeModuleORM.user_id == current_user.id)
               & (PersonalizeModuleORM.module_id == module_id))

    )

    data = list(res)
    return PersonalizeModuleDTO.model_validate(data[0][0].module_entity.__dict__ | data[0][0].__dict__)

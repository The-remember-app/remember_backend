import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert


from the_remember.src.api.auth.logics import get_db_session, get_current_user, get_db_write_session
from the_remember.src.api.modules.db_model import ModuleORM, PersonalizeModuleORM
from the_remember.src.api.modules.dto import ModuleDTO, CreateModuleDTO, PersonalizeModuleDTO, \
    OnlyPersonalizePartModuleDTO, UpdateOnlyPersonalizePartModuleDTO, DeleteOnlyPersonalizePartModuleDTO
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


@module_app.put("/personalize/create_or_update", response_model=list[OnlyPersonalizePartModuleDTO], status_code=200)
async def update_personalize_module(
        update_modules: list[UpdateOnlyPersonalizePartModuleDTO],
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]

):
    index = [PersonalizeModuleORM.module_id, PersonalizeModuleORM.user_id]
    vals = [
        {'personal_update_at': datetime.datetime.utcnow()}
        | update_module.model_dump()
        | {'user_id': current_user.id}
        for update_module in update_modules
    ]
    if bool(vals) is False:
        return []
    vals_key = frozenset(vals[0].keys())
    query = ((_query := (pg_insert(PersonalizeModuleORM)
                         .values(vals)))
             .on_conflict_do_update(
        index_elements=index,
        set_={i.key: i for i in _query.excluded._all_columns if i.key in vals_key}
    )
             .returning(PersonalizeModuleORM)
             )

    data = list(await db_session.execute(query))
    return [OnlyPersonalizePartModuleDTO.model_validate(i[0]) for i in data]


@module_app.delete("/personalize/delete", response_model=list[DeleteOnlyPersonalizePartModuleDTO], status_code=200)
async def delete_personalize_module(
        delete_module_ids: list[UUID],
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    query = (delete(PersonalizeModuleORM)
             .where((PersonalizeModuleORM.user_id == current_user.id)
                    & (PersonalizeModuleORM.module_id.in_(delete_module_ids)))
             .returning(PersonalizeModuleORM.module_id, PersonalizeModuleORM.user_id)
             )

    data = list(await db_session.execute( query ))
    return [DeleteOnlyPersonalizePartModuleDTO.model_validate(i) for i in data]

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
import sqlalchemy as sa
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from the_remember.src.api.auth.logics import get_db_session, get_current_user, get_db_write_session
from the_remember.src.api.modules.db_model import ModuleORM
from the_remember.src.api.terms.db_model import TermORM, PersonalizeTermORM
from the_remember.src.api.terms.dto import TermDTO, CreateTermDTO, PersonalizeTermDTO
from the_remember.src.api.users.dto import UserDTO
from the_remember.src.config.config import CONFIG

term_app = APIRouter()


@term_app.post("/create", response_model=TermDTO, status_code=201)
async def create_folder(
        new_term: CreateTermDTO,
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]

):
    res = await db_session.execute(
        insert(TermORM)
        .from_select(
            [TermORM.module_id, TermORM.term, TermORM.definition],
            select(
                ModuleORM.id,
                sa.text("'" + str(new_term.term) + "'"),
                sa.text("'" + str(new_term.definition) + "'")
            )
            .where(
                (ModuleORM.id == new_term.module_id)
                & (ModuleORM.author_id == current_user.id)))
        .returning(TermORM)
    )

    # res = await db_session.execute(insert(TermORM).returning(TermORM), [
    #     new_term.model_dump()
    # ])
    data_ = list(res)
    data__ = data_[0]
    data = data__[0]
    # await db_session.commit()
    # data1 = res.raw.return_defaults
    return TermDTO.model_validate(data)


@term_app.get("/all", response_model=list[PersonalizeTermDTO])
async def get_all_folders(
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(PersonalizeTermORM)
        .join(PersonalizeTermORM.term_entity)
        .add_columns(TermORM)
        .where(PersonalizeTermORM.user_id == current_user.id)
    )

    data = list(res)
    return [PersonalizeTermDTO.model_validate(i[0].term_entity.__dict__ | i[0].__dict__) for i in data]


@term_app.get("/{term_id}", response_model=PersonalizeTermDTO)
async def get_one_folder(
        term_id: UUID,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(PersonalizeTermORM)
        .join(PersonalizeTermORM.term_entity)
        .add_columns(TermORM)
        .where((PersonalizeTermORM.user_id == current_user.id)
               & (PersonalizeTermORM.term_id == term_id))

    )

    data = list(res)
    return PersonalizeTermDTO.model_validate(data[0][0].term_entity.__dict__ | data[0][0].__dict__)

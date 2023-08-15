from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
import sqlalchemy as sa
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from the_remember.src.api.auth.logics import get_db_session, get_current_user, get_db_write_session
from the_remember.src.api.modules.db_model import ModuleORM
from the_remember.src.api.sentences.db_model import SentenceORM
from the_remember.src.api.sentences.dto import SentenceDTO, CreateSentenceDTO
from the_remember.src.api.terms.db_model import TermORM, PersonalizeTermORM

from the_remember.src.api.users.dto import UserDTO
from the_remember.src.config.config import CONFIG

sentence_app = APIRouter()


@sentence_app.post("/create", response_model=SentenceDTO, status_code=201)
async def create_term(
        new_sentence: CreateSentenceDTO,
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]

):
    res = await db_session.execute(
        insert(SentenceORM)
        .from_select(
            [SentenceORM.term_id, SentenceORM.sentence, SentenceORM.translate],
            select(
                TermORM.id,
                sa.text("'" + str(new_sentence.sentence) + "'"),
                sa.text("'" + str(new_sentence.translate) + "'")
            ).join(
                TermORM.module_entity,

            )
            .where(
                (TermORM.id == new_sentence.term_id)
                & (ModuleORM.id == TermORM.module_id)
                & (ModuleORM.author_id == current_user.id)))
        .returning(SentenceORM)
    )

    # res = await db_session.execute(insert(TermORM).returning(TermORM), [
    #     new_term.model_dump()
    # ])
    data_ = list(res)
    data__ = data_[0]
    data = data__[0]
    # await db_session.commit()
    # data1 = res.raw.return_defaults
    return SentenceDTO.model_validate(data)


@sentence_app.get("/all", response_model=list[SentenceDTO])
async def get_all_term(
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(SentenceORM)
        .join(SentenceORM.term_entity)
        .join(
            PersonalizeTermORM,
            (PersonalizeTermORM.user_id == current_user.id)
            & (SentenceORM.term_id == PersonalizeTermORM.term_id)
        )
        .where(PersonalizeTermORM.user_id == current_user.id)
    )

    data = list(res)
    return [SentenceDTO.model_validate(i[0]) for i in data]


@sentence_app.get("/{sentence_id}", response_model=SentenceDTO)
async def get_one_term(
        sentence_id: UUID,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(SentenceORM)
        .join(
            PersonalizeTermORM,
            (PersonalizeTermORM.user_id == current_user.id)
            & (SentenceORM.term_id == PersonalizeTermORM.term_id)
        )
        .where((PersonalizeTermORM.user_id == current_user.id)
               & (SentenceORM.id == sentence_id))

    )

    data = list(res)
    return SentenceDTO.model_validate(data[0][0])

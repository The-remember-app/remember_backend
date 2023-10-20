import datetime
from pprint import pprint
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert, insert

from the_remember.src.api.auth.logics import get_current_user, get_db_write_session
from the_remember.src.api.terms.db_model import PersonalizeTermORM, LearnTermDatetimeMarkORM
from the_remember.src.api.terms.dtos.create import CreateLearnMarkDTO
from the_remember.src.api.terms.dtos.dto import  LearnMarkDTO
from the_remember.src.api.users.dto import UserDTO

term_marks_app = APIRouter()


@term_marks_app.post("/create", response_model=list[LearnMarkDTO], status_code=201)
async def create_mark(
        new_marks: list[CreateLearnMarkDTO],
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]

):
    res = await db_session.execute(
        insert(LearnTermDatetimeMarkORM)
        .returning(LearnTermDatetimeMarkORM), [
        new_marks.model_dump() | {'user_id': current_user.id}
    ])
    data = list(res)
    # data__ = data_
    # data = data__[0]
    # await db_session.commit()
    # data1 = res.raw.return_defaults
    return [LearnTermDatetimeMarkORM.model_validate(i[0])
            for i in data]



@term_marks_app.get("/module/{module_id}/all",
                    response_model=list[LearnMarkDTO])
async def get_marks_from_module(
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

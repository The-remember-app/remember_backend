from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
import sqlalchemy as sa
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from the_remember.src.api.auth.logics import get_db_session, get_current_user, get_db_write_session
from the_remember.src.api.modules.db_model import ModuleORM
from the_remember.src.api.terms.db_model import TermORM, PersonalizeTermORM, AdditionalTermInfoORM
from the_remember.src.api.terms.dtos.dto import TermDTO, CreateTermDTO, PersonalizeTermDTO, PersonalizeTermWithAddInfoDTO, \
    AdditionalTermInfoDTO
from the_remember.src.api.terms.views.laerning_marks import term_marks_app
from the_remember.src.api.terms.views.personalize import personal_term_app
from the_remember.src.api.users.dto import UserDTO

term_app = APIRouter()
term_app.include_router(personal_term_app, prefix='/personalize')
term_app.include_router(term_marks_app, prefix='/personalize/marks')



@term_app.post("/create", response_model=TermDTO, status_code=201)
async def create_term(
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
async def get_all_term(
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


@term_app.get("/add_info/all", response_model=list[AdditionalTermInfoDTO])
async def get_all_add_term_info(
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(AdditionalTermInfoORM)
        .join(AdditionalTermInfoORM.term_entity)
        .join(TermORM.personalized_term_entities)
        # .add_columns(TermORM)
        .where(PersonalizeTermORM.user_id == current_user.id)
    )

    data = list(res)
    return [AdditionalTermInfoDTO.model_validate(i[0]) for i in data]



@term_app.get("/from_module/{module_id}", response_model=list[PersonalizeTermWithAddInfoDTO])
async def get_all_term(
        module_id: UUID,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    query = (sa.text(  # language=PostgreSQL
        """
        select t.*, pt.*, json_agg(
            json_build_object(
            'id', aiot.id,
            'text_data', aiot.text_data,
            'adding_text_data', aiot.adding_text_data,
            'dialect_or_area', aiot.dialect_or_area,
            'add_info_type', aiot.add_info_type,
            'term_id', aiot.term_id,
            'parent_add_info_id', aiot.parent_add_info_id,
            'created_at', aiot.created_at,
            'updated_at', aiot.updated_at
            )
            ) term_additional_info_entities
            from add_info_of_term aiot
            join public.term t on t.id = aiot.term_id 
                and t.module_id = :module_id
            join public.personalize_term pt 
                on aiot.term_id = pt.term_id 
                and pt.user_id = :user_id 
            group by pt.user_id,  pt.module_id, pt.term_id,  t.id
        -- join public.personalize_term pt on af.id = pt.term_id
        -- where pt.user_id = :user_id
    """).bindparams(module_id=module_id, user_id=current_user.id)
             # .columns(*[i for i in sa.inspect(TermORM).column_attrs], *[i for i in sa.inspect(PersonalizeTermORM).column_attrs])
             # .columns()
             )
    # query = query.columns(*[i for i in sa.inspect(TermORM).column_attrs]).cte('st')
    # query = select()
    res1 = list((await db_session.execute(query)))

    # res = await db_session.execute(
    #     select(PersonalizeTermORM)
    #     .join(PersonalizeTermORM.term_entity)
    #     .join(TermORM.term_additional_info_entities)
    #     .add_columns(TermORM)
    #     .add_columns(AdditionalTermInfoORM)
    #     .where((PersonalizeTermORM.user_id == current_user.id)
    #            & (TermORM.module_id == module_id))
    # )

    # data = list(res)
    # return [PersonalizeTermWithAddInfoDTO.model_validate(
    #     i[0].__dict__ | i[1].__dict__ | {'term_additional_info_entities': list(i[2])}) for i in data]
    return [PersonalizeTermWithAddInfoDTO.model_validate(i) for i in res1]


@term_app.get("/{term_id}", response_model=PersonalizeTermDTO)
async def get_one_term(
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






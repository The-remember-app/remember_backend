import datetime
from pprint import pprint
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert


from the_remember.src.api.auth.logics import get_current_user, get_db_write_session
from the_remember.src.api.terms.db_model import PersonalizeTermORM
from the_remember.src.api.terms.dtos.delete import DeleteOnlyPersonalizePartTermDTO
from the_remember.src.api.terms.dtos.dto import OnlyPersonalizePartTermDTO
from the_remember.src.api.terms.dtos.update import UpdateOnlyPersonalizePartTermDTO
from the_remember.src.api.users.dto import UserDTO

personal_term_app = APIRouter()



@personal_term_app.post("/create", response_model=list[OnlyPersonalizePartTermDTO], status_code=201)
async def update_personalize_term(
        create_marks: list[UpdateOnlyPersonalizePartTermDTO],
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]

):
    index = [PersonalizeTermORM.user_id, PersonalizeTermORM.term_id, PersonalizeTermORM.module_id]
    vals = [
        {'personal_updated_at': datetime.datetime.utcnow()}
        | update_term.model_dump(exclude_defaults=True)
        | {'user_id': current_user.id}
        for update_term in update_terms
    ]
    pprint(update_terms)
    if bool(vals) is False:
        return []
    print(vals[0])
    vals_key = set(vals[0].keys()) - {i.key for i in index}
    print(vals_key)
    query = ((_query := (pg_insert(PersonalizeTermORM)
                         .values(vals)))
             .on_conflict_do_update(
        index_elements=index,
        set_={i.key: i for i in _query.excluded._all_columns if i.key in vals_key}
    )
             .returning(PersonalizeTermORM)
             )
    print({i.key: i for i in _query.excluded._all_columns if i.key in vals_key})
    data = list(await db_session.execute(query))
    return [OnlyPersonalizePartTermDTO.model_validate(i[0]) for i in data]


@personal_term_app.delete("/delete", response_model=list[DeleteOnlyPersonalizePartTermDTO], status_code=200)
async def delete_personalize_terme(
        delete_term_ids: list[UUID],
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    query = (delete(PersonalizeTermORM)
             .where((PersonalizeTermORM.user_id == current_user.id)
                    & (PersonalizeTermORM.term_id.in_(delete_term_ids)))
             .returning(PersonalizeTermORM.term_id, PersonalizeTermORM.user_id)
             )

    data = list(await db_session.execute( query ))
    return [DeleteOnlyPersonalizePartTermDTO.model_validate(i) for i in data]
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from the_remember.src.api.auth.logics import get_db_session, get_current_user, get_db_write_session
from the_remember.src.api.folders.db_model import FolderORM
from the_remember.src.api.folders.dto import CreateFolderDTO, FolderDTO
from the_remember.src.api.users.dto import UserDTO
from the_remember.src.config.config import CONFIG

folder_app = APIRouter()


@folder_app.post("/create", response_model=FolderDTO, status_code=201)
async def create_folder(
        new_folder: CreateFolderDTO,
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]

):
    if True:
        res = await db_session.execute(insert(FolderORM).returning(FolderORM),
                                       [
                                           new_folder.model_dump() | {'user_id': current_user.id}
                                       ])
        data_ = list(res)
        data__ = data_[0]
        data = data__[0]
        # await db_session.commit()
        # data1 = res.raw.return_defaults
        return FolderDTO.model_validate(data)


@folder_app.get("/all", response_model=list[FolderDTO])
async def get_all_folders(
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(FolderORM).where(FolderORM.user_id == current_user.id)
    )

    data = list(res)
    return [FolderDTO.model_validate(i[0]) for i in data]


@folder_app.get("/{folder_id}", response_model=FolderDTO)
async def get_one_folder(
        folder_id: UUID,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(FolderORM).where((FolderORM.user_id == current_user.id)
                                & (FolderORM.id == folder_id))
    )

    data = list(res)
    return FolderDTO.model_validate(data[0][0])

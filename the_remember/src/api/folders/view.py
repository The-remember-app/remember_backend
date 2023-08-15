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
from the_remember.src.api.folders.logic import recourse_tree_to_db_models
from the_remember.src.api.modules.db_model import ModuleORM
from the_remember.src.api.modules.dto import CreateModuleAsTreeDTO
from the_remember.src.api.terms.db_model import TermORM
from the_remember.src.api.terms.dto import CreateTermDTO, CreateTermAsTreeDTO
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
        res = await db_session.execute(
            insert(FolderORM)
            .returning(FolderORM),
            [new_folder.model_dump() | {'user_id': current_user.id}]
        )
        data_ = list(res)
        data__ = data_[0]
        data = data__[0]
        return FolderDTO.model_validate(data)


@folder_app.post("/create/as_tree", response_model=list[str], status_code=201)
async def create_folder_as_tree(
        new_folders: list[CreateFolderAsTreeDTO],
        db_session: Annotated[AsyncSession, Depends(get_db_write_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]

):
    db_session.add_all(
        [recourse_tree_to_db_models(i, current_user) for i in new_folders]
    )
    await db_session.commit()
    return ['ok']


@folder_app.get("/all", response_model=list[FolderDTO])
async def get_all_folders(
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    # res1 = await  db_session.execute(select(FolderORM)
    #                                  .where(FolderORM.id == 'd39f35a7-6c13-4685-972b-1cebb82ea937'))
    # print(res1)

    res = await db_session.execute(
        select(FolderORM)
        # .join(FolderORM.root_folder_entity)
        .where(FolderORM.user_id == current_user.id)
    )

    # var = FolderORM.root_folder_entity

    data = list(res)
    data1 = [i[0] for i in data]
    return [FolderDTO.model_validate(i) for i in data1]


@folder_app.get("/all/as_tree", response_model=list[FolderWithNestedEntitiesDTO])
async def get_all_folders_as_tree(
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(FolderORM)
        .where(FolderORM.user_id == current_user.id)
    )

    data = list(res)
    data1 = [i[0] for i in data if (
        await i[0].awaitable_attrs.sub_folders,
        [
            [await iii.awaitable_attrs.sub_terms
             for iii in await ii.awaitable_attrs.sub_terms]
            for ii in await i[0].awaitable_attrs.sub_modules]
    ) or True]

    return [FolderWithNestedEntitiesDTO.model_validate(i) for i in data1]


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
    res2 = data[0][0]
    return FolderDTO.model_validate(res2)


@folder_app.get("/{folder_id}/with_parent", response_model=FolderWithRootEntityDTO)
async def get_one_folder_with_parents(
        folder_id: UUID,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(FolderORM).where((FolderORM.user_id == current_user.id)
                                & (FolderORM.id == folder_id))
    )

    data = list(res)
    res2 = data[0][0]
    res3 = res2
    print(res3)
    while isinstance(res3, FolderORM):
        res3 = await res3.awaitable_attrs.root_folder_entity
    return FolderWithRootEntityDTO.model_validate(res2)


@folder_app.get("/{folder_id}/as_tree", response_model=FolderWithNestedEntitiesDTO)
async def get_one_folder_as_tree(
        folder_id: UUID,
        db_session: Annotated[AsyncSession, Depends(get_db_session)],
        current_user: Annotated[UserDTO, Depends(get_current_user)]
):
    res = await db_session.execute(
        select(FolderORM).where((FolderORM.user_id == current_user.id)
                                & (FolderORM.id == folder_id))
    )

    data = list(res)
    res2 = data[0][0]
    sub_folders = [res2]

    while bool(sub_folders):
        next_sub_folders = []
        for i in sub_folders:
            next_sub_folders += [ii for ii in await i.awaitable_attrs.sub_folders]
            [[await iii.awaitable_attrs.sub_terms
              for iii in await ii.awaitable_attrs.sub_terms]
             for ii in await i.awaitable_attrs.sub_modules]
        sub_folders = next_sub_folders[:]
    return FolderWithNestedEntitiesDTO.model_validate(res2)

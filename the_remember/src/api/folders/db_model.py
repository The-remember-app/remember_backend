from __future__ import annotations

import asyncio
import datetime
from typing import List
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import UUID as pUUID

from the_remember.src.utils.db import AbstractDbEntity




class FolderORM(AbstractDbEntity):
    __tablename__ = "folder"

    id: Mapped[UUID] = mapped_column(primary_key=True, type_=postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"))
    name: Mapped[str]
    author_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id", ondelete='set null',  name='folder__user_id__fk',), type_=postgresql.UUID(as_uuid=True))
    root_folder_id: Mapped[UUID | None] = mapped_column(ForeignKey("folder.id", ondelete='CASCADE',  name='folder__root_folder_id__fk',), type_=postgresql.UUID(as_uuid=True))

    # root_folder: Mapped[FolderORM | None] = relationship(back_populates="sub_folders", remote_side=[root_folder_id])
    sub_folders: Mapped[list[FolderORM]] = relationship("FolderORM", back_populates="root_folder_entity")
    sub_modules: Mapped[list["ModuleORM"]] = relationship("ModuleORM",  back_populates='root_folder_entity')
    root_folder_entity: Mapped[FolderORM] = relationship("FolderORM", back_populates='sub_folders',  remote_side=[id])
    personalize_folders: Mapped[list[PersonalizeFolderORM]] = relationship("PersonalizeFolderORM", back_populates='folder_entity',)

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())



class PersonalizeFolderORM(AbstractDbEntity):
    __tablename__ = "personalize_folder"

    folder_id: Mapped[UUID] = mapped_column(ForeignKey("folder.id", name='personalize_folder__folder_id__fk', ondelete='CASCADE'), type_=postgresql.UUID(as_uuid=True),
                                            primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", name='personalize_folder__user_id__fk',  ondelete='CASCADE'), type_=postgresql.UUID(as_uuid=True), primary_key=True)
    root_folder_id: Mapped[UUID | None] = mapped_column(type_=postgresql.UUID(as_uuid=True),)

    ForeignKeyConstraint([user_id, root_folder_id], ['personalize_folder.user_id', 'personalize_folder.folder_id'], name='personalize_folder__to_root_personalize_folder__fk', ondelete='CASCADE')


    personal_created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    personal_updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


    folder_entity: Mapped[FolderORM] = relationship(FolderORM, back_populates='personalize_folders',  )
    # root_folder_entity: Mapped[FolderORM | None] = relationship(FolderORM, )
    root_personalize_folder_entity: Mapped[PersonalizeFolderORM | None] = relationship('PersonalizeFolderORM', back_populates='sub_personalize_folder_entities',  remote_side=[folder_id, user_id]  )
    sub_personalize_folder_entities: Mapped[list[PersonalizeFolderORM | None]] = relationship('PersonalizeFolderORM', back_populates='root_personalize_folder_entity',  )
    sub_personalize_modules: Mapped[list["PersonalizeModuleORM"]] = relationship("PersonalizeModuleORM", back_populates='root_personalize_folder_entity',)
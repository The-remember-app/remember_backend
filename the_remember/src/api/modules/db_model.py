from __future__ import annotations

import asyncio
import datetime
from typing import List
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
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

from the_remember.src.api.folders.db_model import PersonalizeFolderORM, FolderORM
from the_remember.src.utils.db import AbstractDbEntity


class ModuleORM(AbstractDbEntity):
    __tablename__ = "module"

    id: Mapped[UUID] = mapped_column(primary_key=True, type_=postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"))
    name: Mapped[str]
    description: Mapped[str | None]
    author_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id", ondelete='set null',  name='module__user_id__fk',), type_=postgresql.UUID(as_uuid=True))
    root_folder_id: Mapped[UUID | None] = mapped_column(ForeignKey("folder.id", ondelete='set null',  name='module__root_folder_id__fk',), type_=postgresql.UUID(as_uuid=True))

    sub_terms:   Mapped[list["TermORM"]] = relationship("TermORM", back_populates='module_entity')
    personalize_modules: Mapped[list[PersonalizeModuleORM]] = relationship("PersonalizeModuleORM", back_populates='module_entity',)
    root_folder_entity: Mapped[FolderORM] = relationship(FolderORM, back_populates='sub_modules')

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


class PersonalizeModuleORM(AbstractDbEntity):
    __tablename__ = "personalize_module"

    module_id: Mapped[UUID] = mapped_column(ForeignKey("module.id", ondelete='CASCADE',  name='personalize_module__module_id__fk',), type_=postgresql.UUID(as_uuid=True),
                                            primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete='CASCADE',  name='personalize_module__user_id__fk',), type_=postgresql.UUID(as_uuid=True), primary_key=True)
    root_folder_id: Mapped[UUID | None] = mapped_column(type_=postgresql.UUID(as_uuid=True),)

    ForeignKeyConstraint([user_id, root_folder_id], ['personalize_folder.user_id', 'personalize_folder.folder_id'], name='personalize_module__to_root_personalize_folder__fk',
                         ondelete='CASCADE')

    is_reverse_definition_write: Mapped[bool] = mapped_column(server_default=sa.text("true"))
    standard_and_reverse_write: Mapped[bool] = mapped_column(server_default=sa.text("false"))
    is_reverse_definition_choice: Mapped[bool] = mapped_column(server_default=sa.text("false"))
    standard_and_reverse_choice: Mapped[bool] = mapped_column(server_default=sa.text("false"))
    max_iteration_len: Mapped[int] = mapped_column(server_default=sa.text("10"))
    min_iteration_len: Mapped[int] = mapped_column(server_default=sa.text("4"))
    min_watch_count: Mapped[int] = mapped_column(server_default=sa.text("5"))
    known_term_part: Mapped[int] = mapped_column(server_default=sa.text("30"))
    choices_count: Mapped[int] = mapped_column(server_default=sa.text("4"))
    # PrimaryKeyConstraint(module_id, user_id)

    personal_created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    personal_updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


    # root_folder_entity: Mapped[FolderORM] = relationship(FolderORM,)
    module_entity: Mapped[ModuleORM] = relationship(ModuleORM, back_populates='personalize_modules')
    root_personalize_folder_entity: Mapped[PersonalizeFolderORM | None] = relationship('PersonalizeFolderORM', back_populates='sub_personalize_modules',)
    personalize_terms: Mapped[list["PersonalizeModuleORM"]] = relationship("PersonalizeTermORM", back_populates='personalize_module_entity',)


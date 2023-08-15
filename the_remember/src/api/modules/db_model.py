from __future__ import annotations

import asyncio
import datetime
from typing import List
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
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


class ModuleORM(AbstractDbEntity):
    __tablename__ = "module"

    id: Mapped[UUID] = mapped_column(primary_key=True, type_=postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"))
    name: Mapped[str]
    description: Mapped[str | None]
    author_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), type_=postgresql.UUID(as_uuid=True))
    root_folder_id: Mapped[UUID | None] = mapped_column(ForeignKey("folder.id"), type_=postgresql.UUID(as_uuid=True))

    sub_terms:   Mapped[list["TermORM"]] = relationship("TermORM", back_populates='module_entity')

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


class PersonalizeModuleORM(AbstractDbEntity):
    __tablename__ = "personalize_module"

    module_id: Mapped[UUID] = mapped_column(ForeignKey("module.id"), type_=postgresql.UUID(as_uuid=True),
                                            primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), type_=postgresql.UUID(as_uuid=True), primary_key=True)

    is_reverse_definition_write: Mapped[bool] = mapped_column(server_default=sa.text("true"))
    standard_and_reverse_write: Mapped[bool] = mapped_column(server_default=sa.text("false"))
    is_reverse_definition_choice: Mapped[bool] = mapped_column(server_default=sa.text("false"))
    standard_and_reverse_choice: Mapped[bool] = mapped_column(server_default=sa.text("false"))
    # PrimaryKeyConstraint(module_id, user_id)

    personal_created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    personal_updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


    module_entity: Mapped[ModuleORM] = relationship()

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

from the_remember.src.utils.db import AbstractDbEntity


class TermORM(AbstractDbEntity):
    __tablename__ = "term"

    id: Mapped[UUID] = mapped_column(primary_key=True, type_=postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"))
    term: Mapped[str]
    definition: Mapped[str]
    module_id: Mapped[UUID] = mapped_column(ForeignKey("module.id"), type_=postgresql.UUID(as_uuid=True))


    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


class PersonalizeTermORM(AbstractDbEntity):
    __tablename__ = "personalize_term"


    module_id: Mapped[UUID] = mapped_column(ForeignKey("module.id"), type_=postgresql.UUID(as_uuid=True),
                                            primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), type_=postgresql.UUID(as_uuid=True), primary_key=True)

    term_id: Mapped[UUID] = mapped_column(ForeignKey("term.id"), type_=postgresql.UUID(as_uuid=True),
                                            primary_key=True)

    choose_error_counter: Mapped[int] = mapped_column(server_default=sa.text("0"))
    write_error_counter: Mapped[int] = mapped_column(server_default=sa.text("0"))
    choice_neg_error_counter: Mapped[int] = mapped_column(server_default=sa.text("0"))


    ForeignKeyConstraint([module_id, user_id], ['personalize_module.module_id', 'personalize_module.user_id'])

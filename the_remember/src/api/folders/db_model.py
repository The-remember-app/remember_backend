from __future__ import annotations

import asyncio
import datetime
from typing import List
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import ForeignKey
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
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), type_=postgresql.UUID(as_uuid=True))
    root_folder_id: Mapped[UUID | None] = mapped_column(ForeignKey("folder.id"), type_=postgresql.UUID(as_uuid=True))

    # root_folder: Mapped[FolderORM | None] = relationship(back_populates="sub_folders", remote_side=[root_folder_id])
    # sub_folders: Mapped[list[FolderORM]] = relationship()

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


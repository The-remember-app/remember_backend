from __future__ import annotations

import asyncio
import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import select
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

    id: Mapped[pUUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[pUUID] = mapped_column(ForeignKey("user.id"))
    root_folder_id: Mapped[pUUID | None] = mapped_column(ForeignKey("folder.id"))
    sub_folders: Mapped[list[FolderORM]] = relationship()

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())

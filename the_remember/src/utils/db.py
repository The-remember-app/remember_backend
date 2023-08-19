from __future__ import annotations

import asyncio
import datetime
import enum
from abc import ABC
from typing import List, Any

from pydantic import BaseModel
# from pydantic.main import Model
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


class AbstractDbEntity(AsyncAttrs, DeclarativeBase):
    pass


class AbstractPydanticEnum(str, enum.Enum):
    """
    by
    str as name or value
    of
    enum
    fields
    >>> SomeEnum['red']
    < SomeEnum.RED: 1 >
    >>> SomeEnum('red')
    < SomeEnum.RED: 1 >
    """

    # ===== methods for Pydantic validations =====
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, var: object):
        if isinstance(var, str):
            # noinspection PyArgumentList
            return cls(var)
        elif issubclass(var.__class__, cls):
            return var
        else:
            raise ValueError(f'Value must "str", not {var.__class__}')



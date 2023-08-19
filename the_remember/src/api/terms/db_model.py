from __future__ import annotations

import asyncio
import datetime
from typing import List
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint, Column
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
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from the_remember.src.api.modules.db_model import ModuleORM, PersonalizeModuleORM
from the_remember.src.api.terms.enums import AddInfoTypeEnum
from the_remember.src.utils.db import AbstractDbEntity


class TermORM(AbstractDbEntity):
    __tablename__ = "term"

    id: Mapped[UUID] = mapped_column(primary_key=True, type_=postgresql.UUID(as_uuid=True),
                                     server_default=sa.text("uuid_generate_v4()"))
    term: Mapped[str]
    definition: Mapped[str]
    # transcription: Mapped[str | None]
    module_id: Mapped[UUID] = mapped_column(ForeignKey("module.id", ondelete='CASCADE', name='term__module_id__fk',), type_=postgresql.UUID(as_uuid=True))

    module_entity: Mapped[ModuleORM] = relationship(ModuleORM, back_populates='sub_terms')
    sub_sentences: Mapped[list["SentenceORM"]] = relationship("SentenceORM", back_populates='term_entity')
    term_additional_info_entities: Mapped[list[AdditionalTermInfoORM]] = relationship("AdditionalTermInfoORM", back_populates='term_entity')
    personalized_term_entities: Mapped[list[PersonalizeTermORM]] = relationship("PersonalizeTermORM", back_populates='term_entity')

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


class AdditionalTermInfoORM(AbstractDbEntity):
    __tablename__ = "add_info_of_term"

    id: Mapped[UUID] = mapped_column(primary_key=True, type_=postgresql.UUID(as_uuid=True),
                                     server_default=sa.text("uuid_generate_v4()"))
    text_data: Mapped[str | None]
    adding_text_data: Mapped[str | None]
    dialect_or_area: Mapped[str | None]
    add_info_type: Mapped[AddInfoTypeEnum] = mapped_column(  type_=PgEnum(AddInfoTypeEnum, name='add_info_type__enum', create_type=True))

    term_id: Mapped[UUID] = mapped_column(ForeignKey("term.id", ondelete='CASCADE', name='add_info_of_term__term_id__fk',), type_=postgresql.UUID(as_uuid=True))
    parent_add_info_id: Mapped[UUID | None] = mapped_column(ForeignKey("add_info_of_term.id", ondelete='set null', name='add_info_of_term__parent_add_info_term_id__fk',), type_=postgresql.UUID(as_uuid=True))

    sub_add_info_entities: Mapped[list[AdditionalTermInfoORM]] = relationship("AdditionalTermInfoORM", back_populates="parent_add_info_entity")
    parent_add_info_entity: Mapped[AdditionalTermInfoORM | None] = relationship("AdditionalTermInfoORM", back_populates='sub_add_info_entities', remote_side=[id])
    term_entity: Mapped[TermORM] = relationship(TermORM, back_populates='term_additional_info_entities')


    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())


class PersonalizeTermORM(AbstractDbEntity):
    __tablename__ = "personalize_term"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete='CASCADE', name='personalize_term__user_id__fk', ), type_=postgresql.UUID(as_uuid=True), primary_key=True)
    term_id: Mapped[UUID] = mapped_column(ForeignKey("term.id", ondelete='CASCADE', name='personalize_term__term_id__fk', ), type_=postgresql.UUID(as_uuid=True),
                                          primary_key=True)

    module_id: Mapped[UUID] = mapped_column(ForeignKey("module.id", ondelete='CASCADE', name='personalize_term__module_id__fk', ), type_=postgresql.UUID(as_uuid=True),)

    ForeignKeyConstraint([module_id, user_id], ['personalize_module.module_id', 'personalize_module.user_id'], name='personalize_term__to_personalize_module__fk', ondelete='CASCADE')

    choose_error_counter: Mapped[int] = mapped_column(server_default=sa.text("0"))
    write_error_counter: Mapped[int] = mapped_column(server_default=sa.text("0"))
    choice_neg_error_counter: Mapped[int] = mapped_column(server_default=sa.text("0"))

    personal_created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    personal_updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(),
                                                                   server_onupdate=func.now())


    module_entity: Mapped[ModuleORM] = relationship(ModuleORM)
    term_entity: Mapped[TermORM] = relationship(TermORM, back_populates='personalized_term_entities')
    personalize_module_entity: Mapped[PersonalizeModuleORM | None] = relationship('PersonalizeModuleORM', back_populates='personalize_terms',)


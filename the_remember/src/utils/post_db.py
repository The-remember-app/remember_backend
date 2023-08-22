import typing
from abc import ABC
from typing import Any

from pydantic import BaseModel
from sqlalchemy import inspect
# from pydantic.main import Model
from sqlalchemy.orm import InstrumentedAttribute, Relationship, ColumnProperty

from the_remember.src.api.modules.db_model import ModuleORM, PersonalizeModuleORM
from the_remember.src.api.sentences.db_model import SentenceORM
from the_remember.src.api.terms.db_model import TermORM, PersonalizeTermORM, AdditionalTermInfoORM
from the_remember.src.api.users.db_model import UserORM

from the_remember.src.api.folders.db_model import FolderORM, PersonalizeFolderORM

Model = typing.TypeVar('Model', bound='BaseModel')

__db_models__ = [
    FolderORM, UserORM, PersonalizeFolderORM,
    ModuleORM, PersonalizeModuleORM,
    TermORM, PersonalizeTermORM,
    SentenceORM, AdditionalTermInfoORM
]

from the_remember.src.utils.db import AbstractDbEntity

orm_to_dto_mask: dict[ColumnProperty | Relationship, dict[str, bool]] = {
    i: {k: True for k in inspect(i).column_attrs}
       | {k: False for k in inspect(i).relationships}
 for i in __db_models__
}


class OrmBaseModel(BaseModel, ABC, extra='ignore', from_attributes=True):

    @classmethod
    def model_validate(cls: type[Model],
                       obj: Any,
                       *,
                       strict: bool | None = None,
                       from_attributes: bool | None = None,
                       context: dict[str, Any] | None = None,
                       ) -> Model:
        if isinstance(obj, AbstractDbEntity):
            return cls(**{k.key: getattr(obj, k.key) for k, v in orm_to_dto_mask[obj.__class__].items() if v})

        return super().model_validate(obj, strict=strict, from_attributes=from_attributes, context=context)

from abc import abstractmethod
from datetime import datetime
from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, declarative_base

from core.db.models.helpers import get_id_column_orm, get_url_id_column_orm, get_created_at_column_orm

Base = declarative_base()


class URLDerivedModel(Base):
    __abstract__ = True
    id: Mapped[int] = get_id_column_orm()
    url_id: Mapped[int] = get_url_id_column_orm()
    created_at: Mapped[datetime] = get_created_at_column_orm()


class StringMapModel(Base):
    __abstract__ = True
    id: Mapped[int] = get_id_column_orm()
    name: Mapped[str] = sa.Column(sa.Text, nullable=False)


class FamilyModel(URLDerivedModel):
    __abstract__ = True

    @property
    @abstractmethod
    def type(self) -> Enum:
        pass

    @property
    @abstractmethod
    def url(self) -> "URL":
        pass

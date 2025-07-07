from datetime import datetime
from enum import Enum
from typing import TypeVar, Type

from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy import Enum as SAEnum

def get_id_column_orm() -> Mapped[int]:
    return mapped_column(
        primary_key=True,
        index=True
    )

def get_created_at_column_orm() -> Mapped[datetime]:
    return mapped_column(
        nullable=False,
        default=sa.func.current_timestamp()
    )

def get_url_id_column_orm() -> Mapped[int]:
    return mapped_column(
        sa.ForeignKey('urls.id'),
        nullable=False
    )

EnumType = TypeVar("EnumType", bound=Enum)

def get_enum_column_orm(
    enum_class: Type[EnumType],
    enum_name: str,
    nullable: bool = False
) -> Mapped[EnumType]:
    return mapped_column(
        SAEnum(
            enum_class,
            name=enum_name,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=nullable
    )


def get_single_url_relationship(back_populates_name: str) -> Mapped["URL"]:
    return sa.orm.relationship("URL", back_populates=back_populates_name, uselist=False)


url_relationship_kwargs = dict(
    cascade="all, delete-orphan",
    back_populates="url"
)

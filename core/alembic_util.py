from typing import Optional

import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import Mapped, relationship


def get_created_at_column_ddl(name: str = "created_at") -> sa.Column:
    return sa.Column(
        name,
        sa.DateTime(),
        nullable=False,
        server_default=sa.func.current_timestamp()
    )

def get_updated_at_column_ddl(name: str = "updated_at") -> sa.Column:
    return sa.Column(
        name,
        sa.DateTime(),
        nullable=False,
        server_default=sa.func.current_timestamp(),
        server_onupdate=sa.func.current_timestamp()
    )

def get_id_column_ddl() -> sa.Column:
    return sa.Column(
        'id',
        sa.Integer(),
        primary_key=True,
        index=True
    )

def get_url_id_column_ddl() -> sa.Column:
    return sa.Column(
        'url_id',
        sa.Integer(),
        sa.ForeignKey('urls.id'),
        nullable=False
    )

def get_enum_column_ddl(column_name: str, enum_name: str, values: list[str]) -> sa.Column:
    return sa.Column(
        column_name,
        sa.Enum(*values, name=enum_name),
        nullable=False
    )

def create_url_table(
    table_name: str,
    additional_columns: list[sa.Column],
    unique_constraint_values: Optional[list[str]] = None,
) -> sa.Table:
    constraints = []

    if unique_constraint_values:
        constraints.append(sa.UniqueConstraint(*unique_constraint_values))

    return op.create_table(
        table_name,
        get_id_column_ddl(),
        get_url_id_column_ddl(),
        *additional_columns,
        get_created_at_column_ddl(),
        *constraints
    )

def drop_enum(enum_name: str) -> None:
    op.execute(f"DROP TYPE IF EXISTS {enum_name}")
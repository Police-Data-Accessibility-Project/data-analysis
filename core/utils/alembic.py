from typing import Optional

import sqlalchemy as sa
from alembic import op


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

def switch_enum_type(
        table_name,
        column_name,
        enum_name,
        new_enum_values,
        drop_old_enum=True,
        check_constraints_to_drop: list[str] = None,
):
    """
    Switches an ENUM type in a PostgreSQL column by:
    1. Renaming the old enum type.
    2. Creating the new enum type with the same name.
    3. Updating the column to use the new enum type.
    4. Dropping the old enum type.

    :param table_name: Name of the table containing the ENUM column.
    :param column_name: Name of the column using the ENUM type.
    :param enum_name: Name of the ENUM type in PostgreSQL.
    :param new_enum_values: List of new ENUM values.
    :param drop_old_enum: Whether to drop the old ENUM type.
    """

    # 1. Drop check constraints that reference the enum
    if check_constraints_to_drop is not None:
        for constraint in check_constraints_to_drop:
            op.execute(f'ALTER TABLE "{table_name}" DROP CONSTRAINT IF EXISTS "{constraint}"')


    # Rename old enum type
    old_enum_temp_name = f"{enum_name}_old"
    op.execute(f'ALTER TYPE "{enum_name}" RENAME TO "{old_enum_temp_name}"')

    # Create new enum type with the updated values
    new_enum_type = sa.Enum(*new_enum_values, name=enum_name)
    new_enum_type.create(op.get_bind())

    # Alter the column type to use the new enum type
    op.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" TYPE "{enum_name}" USING "{column_name}"::text::{enum_name}')

    # Drop the old enum type
    if drop_old_enum:
        op.execute(f'DROP TYPE "{old_enum_temp_name}"')

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
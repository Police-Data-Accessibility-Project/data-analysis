"""Add html_bag_of_tags

Revision ID: ac504e6eaf7c
Revises: 4eee471c227f
Create Date: 2025-05-27 08:15:16.586896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.utils.alembic import create_url_table, get_enum_column_ddl, drop_enum

# revision identifiers, used by Alembic.
revision: str = 'ac504e6eaf7c'
down_revision: Union[str, None] = '4eee471c227f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = "html_bag_of_tags"
ENUM_NAME = "html_bag_of_tags_type"

def upgrade() -> None:
    """Upgrade schema."""
    create_url_table(
        table_name=TABLE_NAME,
        additional_columns=[
            get_enum_column_ddl(
                column_name='type',
                enum_name=ENUM_NAME,
                values=[
                    "all_tags",
                ]
            ),
            sa.Column('tag_id', sa.Integer(), sa.ForeignKey('html_tags.id'), nullable=True),
            sa.Column('count', sa.Integer(), nullable=False)
        ],
        unique_constraint_values=['url_id', 'type', 'tag_id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)
    drop_enum(ENUM_NAME)

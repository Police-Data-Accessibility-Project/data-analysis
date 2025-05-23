"""Add html_bag_of_words table

Revision ID: e0d8efdd34e4
Revises: 772cdef9d097
Create Date: 2025-05-22 09:46:15.522406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.alembic_util import create_url_table, get_enum_column_ddl, drop_enum

# revision identifiers, used by Alembic.
revision: str = 'e0d8efdd34e4'
down_revision: Union[str, None] = '772cdef9d097'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = 'html_bag_of_words'
ENUM_NAME = 'html_bag_of_words_type'

def upgrade() -> None:
    """Upgrade schema."""
    create_url_table(
        table_name=TABLE_NAME,
        additional_columns=[
            get_enum_column_ddl(
                column_name='type',
                enum_name=ENUM_NAME,
                values=[
                    "all_words",
                    "all_tags",
                    "locations",
                    "persons",
                    "common_nouns",
                    "proper_nouns",
                    "verbs",
                    "adjectives",
                    "adverbs"
                ]
            ),
            sa.Column('term', sa.Text(), nullable=True),
            sa.Column('count', sa.Integer(), nullable=False)
        ],
        unique_constraint_values=['url_id', 'type', 'term']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)

    drop_enum(ENUM_NAME)

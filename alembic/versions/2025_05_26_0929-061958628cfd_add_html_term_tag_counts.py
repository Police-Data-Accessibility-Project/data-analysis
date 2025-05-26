"""Add html_term_tag_counts

Revision ID: 061958628cfd
Revises: 6fed3587a37f
Create Date: 2025-05-26 09:29:49.100301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.utils.alembic import create_url_table, get_enum_column_ddl, drop_enum, get_id_column_ddl

# revision identifiers, used by Alembic.
revision: str = '061958628cfd'
down_revision: Union[str, None] = '6fed3587a37f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TERM_TAG_COUNTS_TABLE_NAME = 'html_term_tag_counts'
HTML_TAGS_TABLE_NAME = 'html_tags'
HTML_TERMS_TABLE_NAME = 'html_terms'
ENUM_NAME = 'html_term_tag_counts_type'

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        HTML_TAGS_TABLE_NAME,
        get_id_column_ddl(),
        sa.Column('name', sa.Text(), nullable=False),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        HTML_TERMS_TABLE_NAME,
        get_id_column_ddl(),
        sa.Column('name', sa.Text(), nullable=False),
        sa.UniqueConstraint('name')
    )

    create_url_table(
        table_name=TERM_TAG_COUNTS_TABLE_NAME,
        additional_columns=[
            get_enum_column_ddl(
                column_name='type',
                enum_name=ENUM_NAME,
                values=[
                    "all_words",
                ]
            ),
            sa.Column(
                'tag_id',
                sa.Integer(),
                sa.ForeignKey(f"{HTML_TAGS_TABLE_NAME}.id"),
                nullable=True
            ),
            sa.Column(
                'term_id',
                sa.Integer(),
                sa.ForeignKey(f"{HTML_TERMS_TABLE_NAME}.id"),
                nullable=True
            ),
            sa.Column('count', sa.Integer(), nullable=False)
        ],
        unique_constraint_values=['url_id', 'type', 'tag_id', 'term_id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    for table in [TERM_TAG_COUNTS_TABLE_NAME, HTML_TAGS_TABLE_NAME, HTML_TERMS_TABLE_NAME]:
        op.drop_table(table)

    drop_enum(ENUM_NAME)

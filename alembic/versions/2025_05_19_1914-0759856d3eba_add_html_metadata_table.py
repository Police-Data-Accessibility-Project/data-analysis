"""Add html_metadata table

Revision ID: 0759856d3eba
Revises: 39568445bf9b
Create Date: 2025-05-19 19:14:50.075873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.utils.alembic import get_id_column_ddl, get_url_id_column_ddl, get_created_at_column_ddl, get_enum_column_ddl

# revision identifiers, used by Alembic.
revision: str = '0759856d3eba'
down_revision: Union[str, None] = '39568445bf9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'html_metadata',
        get_id_column_ddl(),
        get_url_id_column_ddl(),
        get_enum_column_ddl(
            column_name='type',
            enum_name='html_metadata_type',
            values=['title', 'description', 'keywords', 'author']
        ),
        get_created_at_column_ddl(),
        sa.Column('value', sa.Text(), nullable=True),
        sa.UniqueConstraint('url_id', 'type')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('html_metadata')

    op.execute("""
        DROP TYPE IF EXISTS html_metadata_type;
    """)

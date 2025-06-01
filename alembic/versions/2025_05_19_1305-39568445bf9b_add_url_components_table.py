"""Add url_components table

Revision ID: 39568445bf9b
Revises: eafeb21ce65a
Create Date: 2025-05-19 13:05:39.275865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.utils.alembic import get_id_column_ddl, get_url_id_column_ddl, get_enum_column_ddl, get_created_at_column_ddl

# revision identifiers, used by Alembic.
revision: str = '39568445bf9b'
down_revision: Union[str, None] = 'eafeb21ce65a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'url_components',
        get_id_column_ddl(),
        get_url_id_column_ddl(),
        get_created_at_column_ddl(),
        get_enum_column_ddl(
            column_name='type',
            enum_name='url_component_type',
            values=[
                'scheme',
                'domain',
                'suffix',
                'subdomain',
                'path',
                'fragment',
                'query_params',
                'file_format'
            ]
        ),
        sa.Column('value', sa.Text(), nullable=True),
        sa.UniqueConstraint('url_id', 'type')
    ),


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('url_components')

    op.execute("""
        DROP TYPE IF EXISTS url_component_type;
    """)

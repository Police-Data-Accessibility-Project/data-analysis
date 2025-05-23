"""Add url_compressed_html table

Revision ID: b6cd7ff31ae5
Revises: 0759856d3eba
Create Date: 2025-05-20 07:24:18.194270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.utils.alembic import create_url_table

# revision identifiers, used by Alembic.
revision: str = 'b6cd7ff31ae5'
down_revision: Union[str, None] = '0759856d3eba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    create_url_table(
        table_name='url_compressed_html',
        additional_columns=[
            sa.Column('compressed_html', sa.LargeBinary(), nullable=False)
        ],
        unique_constraint_values=['url_id']
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('url_compressed_html')

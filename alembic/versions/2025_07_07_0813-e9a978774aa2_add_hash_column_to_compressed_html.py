"""Add hash column to compressed html

Revision ID: e9a978774aa2
Revises: ac504e6eaf7c
Create Date: 2025-07-07 08:13:31.855198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9a978774aa2'
down_revision: Union[str, None] = 'ac504e6eaf7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = 'url_compressed_html'
COLUMN_NAME = 'hash'

def upgrade() -> None:
    """Upgrade schema."""
    # Add column
    op.add_column(
        TABLE_NAME,
        sa.Column(COLUMN_NAME, sa.String(), nullable=True)
    )
    # Create hashes

    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.execute(f"UPDATE {TABLE_NAME} SET {COLUMN_NAME} = encode(digest(compressed_html, 'sha256'), 'hex');")

    # Remove allow null
    op.alter_column(
        TABLE_NAME,
        COLUMN_NAME,
        nullable=False
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(TABLE_NAME, COLUMN_NAME)

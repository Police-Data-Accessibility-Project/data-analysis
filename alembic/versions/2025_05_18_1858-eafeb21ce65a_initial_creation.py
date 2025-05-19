"""Initial creation

Revision ID: eafeb21ce65a
Revises: 
Create Date: 2025-05-18 18:58:08.778527

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

from core.alembic_util import get_id_column_ddl, get_created_at_column_ddl, get_url_id_column_ddl, get_enum_column_ddl

# revision identifiers, used by Alembic.
revision: str = 'eafeb21ce65a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


error_type = sa.Enum('scrape', 'parse', name='error_type')

def upgrade() -> None:
    """Upgrade schema."""
    # Create url table
    op.create_table(
        'urls',
        get_id_column_ddl(),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('response_code', sa.Integer(), nullable=True),
        get_created_at_column_ddl(),
        sa.UniqueConstraint('url'),
    )

    # Create url_error
    op.create_table(
        'url_errors',
        get_id_column_ddl(),
        get_url_id_column_ddl(),
        sa.Column('error_type', error_type, nullable=False),
        sa.Column('error', sa.Text(), nullable=False),
        get_created_at_column_ddl(),
    )

    # Create url_full_html
    op.create_table(
        'url_full_html',
        get_id_column_ddl(),
        get_url_id_column_ddl(),
        sa.Column('html', sa.Text(), nullable=False),
        get_created_at_column_ddl(),
        get_created_at_column_ddl("updated_at"),
        sa.UniqueConstraint('url_id'),
    )

    # Create trigger function for updated at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Add trigger for updated at
    op.execute("""
        CREATE TRIGGER update_updated_at
        BEFORE UPDATE
        ON url_full_html
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at();
    """)




def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('url_full_html')
    op.drop_table('url_errors')
    op.drop_table('urls')

    op.execute("""
        DROP FUNCTION IF EXISTS update_updated_at;
    """)

    op.execute("""
        DROP TYPE IF EXISTS error_type;
    """)
"""Add url_html_content_metrics table

Revision ID: 772cdef9d097
Revises: b6cd7ff31ae5
Create Date: 2025-05-20 16:45:21.459195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.utils.alembic import create_url_table, get_enum_column_ddl

# revision identifiers, used by Alembic.
revision: str = '772cdef9d097'
down_revision: Union[str, None] = 'b6cd7ff31ae5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = 'html_content_metrics'

def upgrade() -> None:
    """Upgrade schema."""
    create_url_table(
        table_name=TABLE_NAME,
        additional_columns=[
            get_enum_column_ddl(
                column_name='type',
                enum_name='html_content_metric_type',
                values=[
                    "proper_nouns",
                    "location_names",
                    "organization_names",
                    "people_names",
                    "legal_terms",
                    "dates_and_times",
                    "emails",
                    "external_links",
                    "internal_links",
                    "words",
                    "characters",
                ]
            ),
            sa.Column('value', sa.Integer(), nullable=False)
        ],
        unique_constraint_values=['url_id', 'type']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)

    op.execute("""
        DROP TYPE IF EXISTS html_content_metric_type;
    """)

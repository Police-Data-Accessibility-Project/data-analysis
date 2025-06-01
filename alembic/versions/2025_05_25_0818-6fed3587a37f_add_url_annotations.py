"""Add URL annotations

Revision ID: 6fed3587a37f
Revises: e0d8efdd34e4
Create Date: 2025-05-25 08:18:58.837835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.utils.alembic import create_url_table, get_enum_column_ddl, drop_enum

# revision identifiers, used by Alembic.
revision: str = '6fed3587a37f'
down_revision: Union[str, None] = 'e0d8efdd34e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = 'url_annotations'
RECORD_TYPE_NAME = 'url_annotations_fine_record_type'
COARSE_RECORD_TYPE_NAME = 'url_annotations_coarse_record_type'

def upgrade() -> None:
    """Upgrade schema."""
    create_url_table(
        table_name=TABLE_NAME,
        additional_columns=[
            sa.Column('relevant', sa.Boolean(), nullable=False),
            get_enum_column_ddl(
                column_name="record_type_fine",
                enum_name=RECORD_TYPE_NAME,
                values=[
                    "Policies & Contracts",
                    "Not Criminal Justice Related",
                    "Media Bulletins",
                    "Poor Data Source",
                    "Resources",
                    "Personnel Records",
                    "Contact Info & Agency Meta",
                    "Misc Police Activity",
                    "Arrest Records",
                    "Dispatch Logs",
                    "Wanted Persons",
                    "List of Data Sources",
                    "Complaints & Misconduct",
                    "Daily Activity Logs",
                    "Training & Hiring Info",
                    "Annual & Monthly Reports",
                    "Calls for Service",
                    "Officer Involved Shootings",
                    "Crime Maps & Reports",
                    "Court Cases",
                    "Records Request Info",
                    "Accident Reports",
                    "Incident Reports",
                    "Dispatch Recordings",
                    "Geographic",
                    "Sex Offender Registry",
                    "Crime Statistics",
                    "Field Contacts",
                    "Surveys",
                    "Use of Force Reports",
                    "Incarceration Records",
                    "Citations",
                    "Booking Reports",
                    "Stops",
                    "Other",
                    "Vehicle Pursuits",
                    "Budgets & Finances",
                ]
            ),
            get_enum_column_ddl(
                column_name="record_type_coarse",
                enum_name=COARSE_RECORD_TYPE_NAME,
                values=[
                    "Info About Agencies",
                    "Not Criminal Justice Related",
                    "Agency-Published Resources",
                    "Poor Data Source",
                    "Info About Officers",
                    "Police & Public Interactions",
                    "Jails & Courts Specific",
                    "Other",
                ],
            )
        ],
        unique_constraint_values=['url_id']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(TABLE_NAME)
    drop_enum(RECORD_TYPE_NAME)
    drop_enum(COARSE_RECORD_TYPE_NAME)

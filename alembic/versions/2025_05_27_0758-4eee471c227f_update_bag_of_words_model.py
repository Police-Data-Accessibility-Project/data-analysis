"""Update bag of words model

Revision ID: 4eee471c227f
Revises: 061958628cfd
Create Date: 2025-05-27 07:58:34.705625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from core.utils.alembic import switch_enum_type

# revision identifiers, used by Alembic.
revision: str = '4eee471c227f'
down_revision: Union[str, None] = '061958628cfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE_NAME = 'html_bag_of_words'
ENUM_NAME = 'html_bag_of_words_type'
CONSTRAINT_NAME = 'html_bag_of_words_url_id_type_term_key'

def upgrade() -> None:
    """Upgrade schema."""
    # Drop unique constraint
    op.drop_constraint(
        CONSTRAINT_NAME,
        TABLE_NAME,
        type_='unique'
    )

    # Add term_id column that is a foreign key to html_terms table
    op.add_column(
        TABLE_NAME,
        sa.Column(
            'term_id',
            sa.Integer(),
            sa.ForeignKey('html_terms.id'),
            nullable=True
        )
    )
    # Drop term column
    op.drop_column(TABLE_NAME, 'term')

    # Re-add unique constraint
    op.create_unique_constraint(
        CONSTRAINT_NAME,
        TABLE_NAME,
        ['url_id', 'type', 'term_id']
    )

    # Update enums
    switch_enum_type(
        table_name=TABLE_NAME,
        column_name='type',
        enum_name=ENUM_NAME,
        new_enum_values=[
            "all_words",
            "locations",
            "persons",
            "common_nouns",
            "proper_nouns",
            "verbs",
            "adjectives",
            "adverbs"
        ]
    )




def downgrade() -> None:
    """Downgrade schema."""

    # Drop unique constraint
    op.drop_constraint(
        CONSTRAINT_NAME,
        TABLE_NAME,
        type_='unique'
    )

    # Drop term_id column
    op.drop_column(TABLE_NAME, 'term_id')

    # Add term column
    op.add_column(
        TABLE_NAME,
        sa.Column(
            'term',
            sa.String(),
            nullable=False
        )
    )

    # Re-add unique constraint
    op.create_unique_constraint(
        CONSTRAINT_NAME,
        TABLE_NAME,
        ['url_id', 'type', 'term']
    )

    # Update enums
    switch_enum_type(
        table_name=TABLE_NAME,
        column_name='type',
        enum_name=ENUM_NAME,
        new_enum_values=[
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
    )


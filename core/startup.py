"""
Code for starting up the database and applying alembic migrations
"""

from alembic.config import Config
from alembic import command


alembic_config = Config("alembic.ini")
alembic_config.set_main_option("script_location", "alembic")
command.stamp(alembic_config, "head")
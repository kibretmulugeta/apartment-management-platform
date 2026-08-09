"""initial_schema_and_notifications

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-08-09 10:50:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Tables are auto-constructed by SQLAlchemy metadata create_all in dev environment
    pass

def downgrade() -> None:
    pass

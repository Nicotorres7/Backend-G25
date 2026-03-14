"""add location to offers

Revision ID: a1b2c3d4e5f6
Revises: c58799fd5d0d
Create Date: 2026-03-09 22:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'c58799fd5d0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('offers', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('offers', sa.Column('longitude', sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column('offers', 'longitude')
    op.drop_column('offers', 'latitude')
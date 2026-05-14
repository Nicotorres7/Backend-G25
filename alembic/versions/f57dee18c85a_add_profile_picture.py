"""add_profile_picture

Revision ID: f57dee18c85a
Revises: e1f2a3b4c5d6
Create Date: 2026-05-09 12:06:03.181782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f57dee18c85a'
down_revision: Union[str, Sequence[str], None] = 'e1f2a3b4c5d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('profile_picture', sa.String(500), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'profile_picture')

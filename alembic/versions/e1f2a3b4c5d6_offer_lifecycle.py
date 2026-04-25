"""offer lifecycle columns

Revision ID: e1f2a3b4c5d6
Revises: 656f06f81c5e
Create Date: 2026-04-14 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'e1f2a3b4c5d6'
down_revision = '656f06f81c5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('offers', sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('offers', sa.Column('closed_early', sa.Boolean(), nullable=False, server_default=sa.false()))

    op.add_column('applications', sa.Column('is_completed', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column('applications', sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('applications', sa.Column('rating', sa.Float(), nullable=True))
    op.add_column('applications', sa.Column('rating_feedback', sa.Text(), nullable=True))
    op.add_column('applications', sa.Column('rating_punctuality', sa.Float(), nullable=True))
    op.add_column('applications', sa.Column('rating_quality', sa.Float(), nullable=True))
    op.add_column('applications', sa.Column('rating_attitude', sa.Float(), nullable=True))
    op.add_column('applications', sa.Column('rated_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('applications', 'rated_at')
    op.drop_column('applications', 'rating_attitude')
    op.drop_column('applications', 'rating_quality')
    op.drop_column('applications', 'rating_punctuality')
    op.drop_column('applications', 'rating_feedback')
    op.drop_column('applications', 'rating')
    op.drop_column('applications', 'completed_at')
    op.drop_column('applications', 'is_completed')
    op.drop_column('offers', 'closed_early')
    op.drop_column('offers', 'closed_at')

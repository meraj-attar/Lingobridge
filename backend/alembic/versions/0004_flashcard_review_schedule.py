"""Add optional spaced-repetition metadata without changing existing review states.

Revision ID: 0004
Revises: 0003
"""
from alembic import op
import sqlalchemy as sa

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    # Handle fresh 0001 installations and upgrades equally. All fields are nullable
    # to preserve existing 'known'/'revise' cards with no fabricated review history.
    columns = {item['name'] for item in sa.inspect(op.get_bind()).get_columns('flashcard_states')}
    for name, type_ in (
        ('due_at', sa.DateTime(timezone=True)),
        ('last_reviewed_at', sa.DateTime(timezone=True)),
        ('interval_days', sa.Integer()),
        ('repetitions', sa.Integer()),
    ):
        if name not in columns:
            op.add_column('flashcard_states', sa.Column(name, type_, nullable=True))


def downgrade():
    raise RuntimeError('Review history is not removed by a destructive downgrade')

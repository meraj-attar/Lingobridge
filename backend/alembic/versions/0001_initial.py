"""Initial relational LingoBridge schema. Additive migration; does not drop unrelated tables.

Revision ID: 0001
Revises:
"""
from alembic import op
from app.db import Base
from app import models
revision='0001'
down_revision=None
branch_labels=None
depends_on=None

def upgrade():
    # The project starts with a new database. checkfirst preserves pre-existing tables;
    # future changes must receive explicit new versioned migrations.
    # Freeze revision 0001 table set: newly introduced models belong to later
    # migrations. Otherwise an empty database would create revision 0002
    # tables here and revision 0002 would fail with duplicate-table errors.
    future={'course_enrollments','flashcard_states','quiz_sessions'}
    initial=[table for table in Base.metadata.sorted_tables if table.name not in future]
    Base.metadata.create_all(bind=op.get_bind(),tables=initial,checkfirst=True)

def downgrade():
    raise RuntimeError('Destructive downgrade is intentionally disabled')

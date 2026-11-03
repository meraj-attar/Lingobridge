"""Add per-course enrollment, flashcard revision, and quiz sessions without touching existing data.

Revision ID: 0002
Revises: 0001
"""
from alembic import op
import sqlalchemy as sa
revision='0002'
down_revision='0001'
branch_labels=None
depends_on=None

def upgrade():
    op.create_table('course_enrollments',
        sa.Column('id',sa.String(70),primary_key=True),
        sa.Column('user_id',sa.String(70),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False),
        sa.Column('course_id',sa.String(70),sa.ForeignKey('courses.id',ondelete='RESTRICT'),nullable=False),
        sa.Column('enrolled_at',sa.DateTime(timezone=True),nullable=False),
        sa.Column('last_accessed_at',sa.DateTime(timezone=True),nullable=False),
        sa.UniqueConstraint('user_id','course_id'))
    op.create_index('ix_course_enrollments_user_id','course_enrollments',['user_id'])
    op.create_index('ix_course_enrollments_course_id','course_enrollments',['course_id'])
    op.create_table('flashcard_states',
        sa.Column('user_id',sa.String(70),sa.ForeignKey('users.id',ondelete='CASCADE'),primary_key=True),
        sa.Column('vocabulary_id',sa.String(70),sa.ForeignKey('vocabulary_items.id',ondelete='CASCADE'),primary_key=True),
        sa.Column('state',sa.String(12),nullable=False),
        sa.Column('updated_at',sa.DateTime(timezone=True),nullable=False))
    op.create_table('quiz_sessions',
        sa.Column('id',sa.String(70),primary_key=True),
        sa.Column('user_id',sa.String(70),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False),
        sa.Column('lesson_id',sa.String(70),sa.ForeignKey('lessons.id',ondelete='CASCADE'),nullable=False),
        sa.Column('expires_at',sa.DateTime(timezone=True),nullable=False),
        sa.Column('consumed_at',sa.DateTime(timezone=True)))
    op.create_index('ix_quiz_sessions_user_id','quiz_sessions',['user_id'])

def downgrade():
    raise RuntimeError('Destructive downgrade is deliberately disabled')

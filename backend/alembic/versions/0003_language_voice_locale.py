"""Optional per-language pronunciation locale; additive and data-preserving.

Revision ID: 0003
Revises: 0002
"""
from alembic import op
import sqlalchemy as sa

revision='0003'
down_revision='0002'
branch_labels=None
depends_on=None

_LOCALES={'en':'en-US','hi':'hi-IN','mr':'mr-IN','gu':'gu-IN','bn':'bn-IN','ta':'ta-IN','te':'te-IN','kn':'kn-IN','ur':'ur-PK','es':'es-ES'}

def upgrade():
    # 0001 materializes current metadata on a brand-new database, so the
    # column may already exist on a fresh install. Older DBs still need it.
    if 'tts_locale' not in {col['name'] for col in sa.inspect(op.get_bind()).get_columns('languages')}:
        op.add_column('languages',sa.Column('tts_locale',sa.String(20),nullable=True))
    # Backfill only unspecified locales; never change a prior administrator override.
    languages=sa.table('languages',sa.column('code',sa.String()),sa.column('tts_locale',sa.String()))
    for lang,locale in _LOCALES.items():
        op.execute(languages.update().where(languages.c.code==lang,languages.c.tts_locale.is_(None)).values(tts_locale=locale))

def downgrade():
    raise RuntimeError('Non-destructive downgrade policy: do not remove the languages.tts_locale column')

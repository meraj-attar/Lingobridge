"""Read-only verification of the configured PostgreSQL installation (no schema changes)."""
from sqlalchemy import select,func,text,inspect
from .db import engine,SessionLocal
from . import models as m

def main():
    if engine.dialect.name != 'postgresql':
        raise SystemExit('Configured DATABASE_URL is not PostgreSQL; no PostgreSQL verification performed')
    with engine.connect() as connection:
        assert connection.scalar(text('SELECT 1')) == 1
        version=connection.scalar(text('SHOW server_version'))
        installed=set(inspect(connection).get_table_names())
        expected={'users','roles','languages','course_levels','courses','modules','lessons','course_enrollments','flashcard_states','quiz_sessions','quiz_questions','quiz_options'}
        if not expected<=installed:raise RuntimeError('Missing schema tables: '+str(expected-installed))
    with SessionLocal() as db:
        codes={x.code for x in db.scalars(select(m.Language)).all()}
        levels={x.code for x in db.scalars(select(m.Level)).all()}
        required_languages={'en','hi','mr','gu','bn','ta','te','kn','ur','es'}
        if not required_languages<=codes or not {'A1','A2','B1','B2','C1','C2'}<=levels:
            raise RuntimeError('Missing curriculum language or level seed')
        for code in sorted(required_languages):
            for level in ('a1','a2','b1','b2','c1','c2'):
                count=db.scalar(select(func.count()).select_from(m.Lesson).where(m.Lesson.language_id=='lang-'+code,m.Lesson.level_id=='lvl-'+level))
                minimum=3 if code in {'gu','bn','ta','te','kn','ur','es'} else 3
                if count<minimum:raise RuntimeError(f'Insufficient seed for {code} {level}: {count}')
    print('PostgreSQL connection OK; server:',version)
    print('Schema tables and 60 language/level course paths present across 10 languages.')
    print('Note: this is a read-only smoke test, not a full PostgreSQL test suite.')
if __name__=='__main__': main()

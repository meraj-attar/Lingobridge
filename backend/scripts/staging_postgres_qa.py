"""READ-ONLY preservation snapshots and PostgreSQL structure inspection.

Database URL MUST name an isolated database containing `_qa` or `_staging`.
Never points at the production LingoBridge database. Compare snapshots before
and after Alembic upgrade / seed using --compare <previous.json>.
"""
import argparse
import hashlib
import json
import re
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from sqlalchemy import inspect, text
from sqlalchemy.engine import make_url
from app.db import engine

HISTORY = ('users','student_languages','course_enrollments','lesson_progress',
           'quiz_attempts','flashcard_states','daily_activity','bookmarks','user_achievements')
CURRICULUM = ('languages','course_levels','courses','modules','lessons',
              'vocabulary_items','quiz_questions','quiz_options','achievements')
ADDED_FLASHCARD_COLUMNS={'due_at','last_reviewed_at','interval_days','repetitions'}


def safety_check():
    url=make_url(str(engine.url))
    if url.get_backend_name() != 'postgresql':
        raise RuntimeError('This script verifies actual PostgreSQL, not SQLite')
    db=(url.database or '').lower()
    if not re.fullmatch(r'[a-z0-9_]+',db) or not re.search(r'(?:_qa|_staging)(?:_[a-z0-9]+)?$',db):
        raise RuntimeError('REFUSED: database name must end _qa or _staging (optional _suffix). Production is forbidden.')
    return db


def stable_string(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),default=lambda x:x.isoformat() if isinstance(x,(datetime,date)) else str(x) if isinstance(x,Decimal) else repr(x))


def snapshot(conn,include_curriculum=False):
    insp=inspect(conn)
    tables=set(insp.get_table_names())
    result={}
    for table in HISTORY+(CURRICULUM if include_curriculum else ()):
        if table not in tables:
            result[table]={'exists':False,'rows':None,'sha256':None}
            continue
        columns=[c['name'] for c in insp.get_columns(table)
                 if not (table=='flashcard_states' and c['name'] in ADDED_FLASHCARD_COLUMNS)]
        if not columns:raise RuntimeError('Unexpected empty table')
        # All identifiers are hardcoded table/column identifiers; data stays read-only.
        quoted=', '.join('"'+c.replace('"','""')+'"' for c in columns)
        data=conn.execute(text(f'SELECT {quoted} FROM "{table}"')).mappings().all()
        rendered=sorted(stable_string(dict(row)) for row in data)
        digest=hashlib.sha256(('\n'.join(rendered)).encode('utf-8')).hexdigest()
        result[table]={'exists':True,'rows':len(data),'sha256':digest,'columns':columns}
    return result


def inspect_schema(conn):
    inspector=inspect(conn)
    names=set(inspector.get_table_names())
    errors=[]
    required={'users','quiz_attempts','lesson_progress','student_languages',
              'course_enrollments','flashcard_states','vocabulary_items','languages'}
    if required-names:errors.append('Missing tables: '+', '.join(sorted(required-names)))
    try:
        columns={col['name'] for col in inspector.get_columns('flashcard_states')}
        if not ADDED_FLASHCARD_COLUMNS<=columns:
            errors.append('Missing 0004 review columns')
        language_cols={col['name'] for col in inspector.get_columns('languages')}
        if 'tts_locale' not in language_cols:errors.append('Missing 0003 locale column')
    except Exception as e:errors.append('Unable to inspect required tables')
    fk_count=0; index_count=0; unique_count=0
    for name in names:
        fk_count+=len(inspector.get_foreign_keys(name))
        index_count+=len(inspector.get_indexes(name))
        unique_count+=len(inspector.get_unique_constraints(name))
    if fk_count==0 or index_count==0 or unique_count==0:
        errors.append('Expected foreign keys/indexes/unique constraints not found')
    unvalidated=conn.execute(text("SELECT conname FROM pg_constraint WHERE convalidated = false AND contype IN ('f','c')")).scalars().all()
    if unvalidated:errors.append('Unvalidated FK/check constraints: '+', '.join(unvalidated))
    revision=conn.execute(text('SELECT version_num FROM alembic_version')).scalar_one_or_none()
    if revision!='0004':errors.append('Expected revision 0004, found '+str(revision))
    return {'revision':revision,'foreign_keys':fk_count,'indexes':index_count,
            'unique_constraints':unique_count,'unvalidated_constraints':unvalidated,
            'errors':errors,'pass':not errors}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--compare',type=Path)
    parser.add_argument('--include-curriculum',action='store_true',help='For seed idempotency AFTER migration')
    parser.add_argument('--inspect',action='store_true',help='Inspect constraints, indexes and Alembic head AFTER upgrade')
    args=parser.parse_args()
    db=safety_check()
    with engine.connect() as conn:
        data={'database':db,'read_only':True,'snapshot':snapshot(conn,args.include_curriculum)}
        if args.inspect:data['schema']=inspect_schema(conn)
    if args.compare:
        before=json.loads(args.compare.read_text())['snapshot']
        data['unchanged']= before==data['snapshot']
        changed=[name for name in set(before)|set(data['snapshot']) if before.get(name)!=data['snapshot'].get(name)]
        data['changed_tables']=sorted(changed)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('STAGING POSTGRESQL',db,'SNAPSHOT',sum(v['rows'] or 0 for v in data['snapshot'].values()),'rows')
    if args.compare:print('PRESERVED',data['unchanged'],'CHANGED',data['changed_tables'])
    if args.inspect:print('SCHEMA',json.dumps(data['schema']))
    if args.compare and not data['unchanged']:raise SystemExit(1)
    if args.inspect and not data['schema']['pass']:raise SystemExit(1)


if __name__=='__main__':main()

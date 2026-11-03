"""Real Alembic SQLite additive migration preserving existing example records.

PostgreSQL must be checked separately on a backed-up staging clone.
"""
import os
import subprocess
import sys
from pathlib import Path
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import Session
import test_integration  # sets the isolated test DATABASE_URL before importing app.db
from app.db import Base
from app import models as m


def test_0004_preserves_existing_rows_and_identifiers(tmp_path):
    path=tmp_path/'previous_release.sqlite3'
    url='sqlite:///'+str(path)
    engine=create_engine(url)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add(m.Role(code='student',label='Student'))
        db.add(m.Language(id='lang-en',code='en',name='English',native_name='English'))
        db.add(m.Level(id='lvl-a1',code='A1',name='Beginner'))
        db.flush()
        db.add(m.User(id='existing-user',email='person@example.com',full_name='Existing Learner',password_hash='pbkdf2_sha256$390000$protected-sample',role='student',xp=200,streak=5))
        db.add(m.Course(id='course-en-a1',language_id='lang-en',level_id='lvl-a1',title='A1'))
        db.flush()
        db.add(m.Module(id='module-en-a1',course_id='course-en-a1',title='Start',sort_order=1))
        db.flush()
        db.add(m.Lesson(id='lesson-original',module_id='module-en-a1',language_id='lang-en',level_id='lvl-a1',title='Existing'))
        db.flush()
        db.add(m.Vocabulary(id='word-original',lesson_id='lesson-original',word='hello',translation='greeting'))
        db.add(m.Progress(id='progress-original',user_id='existing-user',lesson_id='lesson-original',status='completed'))
        db.add(m.QuizAttempt(id='attempt-original',user_id='existing-user',lesson_id='lesson-original',score=1,total_questions=1,percentage=100,passed=True,answers=[{'question_id':'keep-original'}]))
        db.flush()
        db.add(m.FlashcardState(user_id='existing-user',vocabulary_id='word-original',state='known'))
        db.commit()
    # Emulate a real revision 0003 database, where 0004 columns did not yet exist.
    with engine.begin() as connection:
        for col in ('due_at','last_reviewed_at','interval_days','repetitions'):
            connection.exec_driver_sql(f'ALTER TABLE flashcard_states DROP COLUMN {col}')
    assert 'due_at' not in {x['name'] for x in inspect(engine).get_columns('flashcard_states')}
    backend=Path(__file__).resolve().parents[1]
    env={**os.environ,'DATABASE_URL':url}
    for command in (['stamp','0003'], ['upgrade','head']):
        result=subprocess.run([sys.executable,'-m','alembic','-c','alembic.ini',*command],cwd=backend,env=env,capture_output=True,text=True,timeout=35)
        assert result.returncode==0,result.stderr
    assert {'due_at','last_reviewed_at','interval_days','repetitions'} <= {x['name'] for x in inspect(engine).get_columns('flashcard_states')}
    with Session(engine) as db:
        user=db.get(m.User,'existing-user')
        assert user.email=='person@example.com' and user.password_hash=='pbkdf2_sha256$390000$protected-sample' and user.xp==200
        assert db.get(m.Progress,'progress-original').status=='completed'
        assert db.get(m.QuizAttempt,'attempt-original').answers==[{'question_id':'keep-original'}]
        review=db.get(m.FlashcardState,('existing-user','word-original'))
        assert review.state=='known' and review.due_at is None and review.repetitions is None
    engine.dispose()

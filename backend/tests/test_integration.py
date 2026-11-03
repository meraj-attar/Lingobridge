import os, tempfile
from pathlib import Path
TEST_DB=Path(tempfile.gettempdir())/'lingobridge_pytest_integration.sqlite3'
if TEST_DB.exists(): TEST_DB.unlink()
os.environ['DATABASE_URL']='sqlite:///'+str(TEST_DB)
os.environ['JWT_SECRET']='integration-test-secret-key-not-for-production-use-34567890'
from fastapi.testclient import TestClient
from app.db import Base,engine,SessionLocal
from app import models as m
from app.seed import seed
from app.security import hash_password
from app.main import app
from sqlalchemy import select
import pytest

Base.metadata.create_all(bind=engine)
seed()

@pytest.fixture
def client():
    with TestClient(app) as c: yield c

def register(c,email='learner@example.com'):
    r=c.post('/api/auth/register',json={'full_name':'Learner One','email':email,'password':'SafePassword123!'})
    assert r.status_code==201,r.text
    c.headers['X-CSRF-Token']=r.json()['csrf']
    return r.json()

def login(c,email,password):
    r=c.post('/api/auth/login',json={'email':email,'password':password})
    assert r.status_code==200,r.text
    c.headers['X-CSRF-Token']=r.json()['csrf']
    return r.json()

def enroll_in_course(client, cid='course-en-a1'):
    r=client.post(f'/api/courses/{cid}/enroll')
    assert r.status_code==200,r.text
    return r.json()

def ticket_for(client, lid):
    r=client.post(f'/api/lessons/{lid}/quiz-session')
    assert r.status_code==200,r.text
    return r.json()['attempt_token']

def make_admin():
    with SessionLocal.begin() as db:
        if not db.get(m.User,'test-admin'):
            db.add(m.User(id='test-admin',email='admin@example.com',full_name='Admin',password_hash=hash_password('AdminPassword123!'),role='admin'))

def test_languages_and_seed(client):
    ls=client.get('/api/languages').json()
    assert {x['code'] for x in ls}=={'en','hi','mr','gu','bn','ta','te','kn','ur','es'}
    lessons=client.get('/api/lessons').json()
    assert all(any(x['language_id']==lid for x in lessons) for lid in ('lang-en','lang-hi','lang-mr','lang-gu','lang-bn','lang-ta','lang-te','lang-kn','lang-ur','lang-es'))
    assert any(x['level_id']=='lvl-c1' for x in lessons)
    assert all('quiz' not in str(x) for x in lessons)

def test_registration_and_protection(client):
    assert client.get('/api/auth/me').status_code==401
    register(client)
    assert client.get('/api/auth/me').json()['user']['role']=='student'
    assert client.get('/api/admin/stats').status_code==403
    assert client.post('/api/auth/register',json={'full_name':'Another','email':'learner@example.com','password':'Password1234'}).status_code==409
    assert client.post('/api/auth/logout').status_code==200
    assert client.get('/api/auth/me').status_code==401
    assert client.post('/api/auth/login',json={'email':'learner@example.com','password':'wrong'}).status_code==401
    login(client,'learner@example.com','SafePassword123!')
    assert client.get('/api/auth/me').status_code==200

def test_csrf_student_scoring_and_persistence(client):
    login(client,'learner@example.com','SafePassword123!')
    assert client.post('/api/enrollments',json={'language_id':'lang-en'},headers={'X-CSRF-Token':''}).status_code==403
    en=client.post('/api/enrollments',json={'language_id':'lang-en'});assert en.status_code==200,en.text
    assert client.post('/api/enrollments',json={'language_id':'lang-en'}).status_code==200
    enroll_in_course(client)
    lesson=client.get('/api/lessons/les-en-1');assert lesson.status_code==200
    quiz=lesson.json()['quiz_questions']
    assert len(quiz)>0 and all('is_correct' not in o for q in quiz for o in q['options'])
    assert all('answer_text' not in q for q in quiz)
    # Keys are test fixtures only, resolved server-side from the trusted test DB.
    with SessionLocal() as db:
        answers=[]
        for q in quiz:
            option=db.scalar(select(m.Option).where(m.Option.question_id==q['id'],m.Option.is_correct==True))
            answers.append({'question_id':q['id'],'option_id':option.id})
    token=ticket_for(client,'les-en-1')
    assert client.post('/api/lessons/les-en-1/submit',json={'answers':answers[:-1],'attempt_token':token}).status_code==400
    assert client.post('/api/lessons/les-en-1/submit',json={'answers':[{'question_id':a['question_id'],'option_id':'hacked'} for a in answers],'attempt_token':token}).status_code==400
    scored=client.post('/api/lessons/les-en-1/submit',json={'answers':answers,'attempt_token':token})
    assert scored.status_code==200,scored.text
    assert scored.json()['percentage']==100 and scored.json()['passed']
    p=client.get('/api/progress').json()
    assert p['lesson_progress'][0]['status']=='completed' and p['quiz_attempts'][0]['percentage']==100
    assert p['xp']>=10 and p['streak']==1
    assert client.get('/api/activity').json()['achievements']
    assert client.post('/api/auth/logout').status_code==200
    login(client,'learner@example.com','SafePassword123!')
    assert client.get('/api/progress').json()['quiz_attempts'][0]['percentage']==100

def test_profile_bookmark_and_four_exercise_types(client):
    login(client,'learner@example.com','SafePassword123!')
    assert client.patch('/api/profile',json={'native_language_id':'lang-hi','target_language_id':'lang-mr','daily_goal':20}).json()['daily_goal']==20
    assert client.post('/api/bookmarks/les-en-1').status_code==200
    assert len(client.get('/api/bookmarks').json())==1
    assert client.delete('/api/bookmarks/les-en-1').status_code==200
    enroll_in_course(client,'course-en-a2')
    lesson=client.get('/api/lessons/les-en-a2-1').json()
    types={q['question_type'] for q in lesson['quiz_questions']}
    assert types=={'mcq','fill_blank','matching','arrangement'}
    assert all('answer_text' not in q for q in lesson['quiz_questions'])
    assert 'pairs' not in str(lesson['quiz_questions'])
    assert client.post('/api/enrollments',json={'language_id':'lang-en'}).status_code==200
    with SessionLocal() as db:
        ans=[]
        for q in lesson['quiz_questions']:
            if q['question_type']=='mcq':
                opt=db.scalar(select(m.Option).where(m.Option.question_id==q['id'],m.Option.is_correct==True))
                ans.append({'question_id':q['id'],'option_id':opt.id})
            else:
                model=db.get(m.Question,q['id'])
                value=model.answer_text
                if model.question_type=='matching':value='|'.join(f'{x}:{y}' for x,y in model.meta['pairs'])
                ans.append({'question_id':q['id'],'text':value})
    result=client.post('/api/lessons/les-en-a2-1/submit',json={'answers':ans,'attempt_token':ticket_for(client,'les-en-a2-1')})
    assert result.status_code==200,result.text
    assert result.json()['score']==4

def test_admin_allows_crud_and_account_control(client):
    make_admin()
    login(client,'admin@example.com','AdminPassword123!')
    s=client.get('/api/admin/stats');assert s.status_code==200 and s.json()['total_students']>=1
    assert len(client.get('/api/admin/students').json())>=2
    result=client.post('/api/admin/manage/languages',json={'code':'xx','name':'Test Language','native_name':'Test'})
    assert result.status_code==201,result.text
    lid=result.json()['id']
    assert client.patch('/api/admin/manage/languages/'+lid,json={'name':'Changed Language'}).json()['name']=='Changed Language'
    assert client.delete('/api/admin/manage/languages/'+lid).status_code==200
    student=next(u for u in client.get('/api/admin/students').json() if u['email']=='learner@example.com')
    assert client.patch('/api/admin/students/'+student['id'],json={'is_active':False}).status_code==200
    assert client.patch('/api/admin/students/'+student['id'],json={'is_active':True}).status_code==200
    assert client.get('/api/lessons/les-en-1?include_answers=true').json()['quiz_questions'][0]['options'][0].get('is_correct') is not None
    result=client.post('/api/admin/lessons/les-en-1/vocabulary',json={'word':'Test','translation':'Test word'})
    assert result.status_code==201,result.text
    assert client.delete('/api/admin/manage/vocabulary/'+result.json()['id']).status_code==200
    res=client.post('/api/admin/lessons/les-en-1/questions',json={'question_text':'What is correct?','options':[{'option_text':'Yes','is_correct':True},{'option_text':'No','is_correct':False}]})
    assert res.status_code==201,res.text
    assert client.delete('/api/admin/manage/questions/'+res.json()['id']).status_code==200

def test_multiuser_isolation_and_csrf(client):
    register(client,'other@example.com')
    assert client.get('/api/progress').json()['quiz_attempts']==[]
    assert client.get('/api/bookmarks').json()==[]
    assert client.get('/api/admin/manage/languages').status_code==403
    assert client.get('/api/lessons/les-en-1?include_answers=true').status_code==403
    enroll_in_course(client)
    assert client.get('/api/lessons/les-en-1?include_answers=true').json()['quiz_questions'][0]['options'][0].get('is_correct') is None
    assert client.post('/api/enrollments',json={'language_id':'lang-en'},headers={'X-CSRF-Token':'wrong'}).status_code==403

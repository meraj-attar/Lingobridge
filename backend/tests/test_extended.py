# Additional independent persistence and media-authorization checks.
from test_integration import app,SessionLocal,m,make_admin
from fastapi.testclient import TestClient

def admin(c):
    make_admin()
    r=c.post('/api/auth/login',json={'email':'admin@example.com','password':'AdminPassword123!'})
    assert r.status_code==200,r.text
    c.headers['X-CSRF-Token']=r.json()['csrf']

def test_server_api_and_admin_module_management():
    with TestClient(app) as c:
        assert c.get('/api/health').json()['status']=='ok'
        admin(c)
        extra=c.post('/api/admin/manage/modules',json={'course_id':'course-en-a1','title':'Second learning unit','sort_order':2})
        assert extra.status_code==201,extra.text
        res=c.get('/api/courses/course-en-a1/modules');assert any(x['title']=='Second learning unit' for x in res.json())
        assert c.patch('/api/admin/manage/modules/'+extra.json()['id'],json={'title':'Revised unit'}).status_code==200
        assert c.delete('/api/admin/manage/modules/'+extra.json()['id']).status_code==200

def test_seed_idempotent():
    from app.seed import seed
    from sqlalchemy import select,func
    with SessionLocal() as db:before=db.scalar(select(func.count()).select_from(m.Lesson))
    seed()
    with SessionLocal() as db:assert before==db.scalar(select(func.count()).select_from(m.Lesson))


def test_timed_quiz_requires_unexpired_server_session():
    from test_integration import register,enroll_in_course
    from app.security import SECRET
    import jwt
    from datetime import datetime, timezone, timedelta
    from sqlalchemy import select
    with SessionLocal.begin() as db:
        q = db.scalar(select(m.Question).where(m.Question.lesson_id == 'les-en-1'))
        q.time_limit_seconds = 30
    try:
        with TestClient(app) as c:
            register(c,'timed@example.com')
            assert c.post('/api/enrollments',json={'language_id':'lang-en'}).status_code==200
            enroll_in_course(c)
            quiz=c.get('/api/lessons/les-en-1').json()['quiz_questions']
            answers=[]
            with SessionLocal() as db:
                for q in quiz:
                    opt=db.scalar(select(m.Option).where(m.Option.question_id==q['id'],m.Option.is_correct==True))
                    answers.append({'question_id':q['id'],'option_id':opt.id})
            assert c.post('/api/lessons/les-en-1/submit',json={'answers':answers}).status_code==403
            ticket=c.post('/api/lessons/les-en-1/quiz-session')
            assert ticket.status_code==200 and ticket.json()['limit_seconds']==30
            assert c.post('/api/lessons/les-en-1/submit',json={'answers':answers,'attempt_token':ticket.json()['attempt_token']}).status_code==200
            expired=jwt.encode({'sub':c.get('/api/auth/me').json()['user']['id'],'lesson':'les-en-1','type':'quiz', 'iss':'lingobridge','exp':datetime.now(timezone.utc)-timedelta(seconds=1)},SECRET,algorithm='HS256')
            assert c.post('/api/lessons/les-en-1/submit',json={'answers':answers,'attempt_token':expired}).status_code==403
    finally:
        with SessionLocal.begin() as db:
            q=db.scalar(select(m.Question).where(m.Question.lesson_id=='les-en-1'))
            q.time_limit_seconds=None

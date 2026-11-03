"""Password policy and cascade-guard regressions. Uses disposable fixtures only."""
from sqlalchemy import select
from fastapi.testclient import TestClient
from app import models as m
from app.password_policy import password_errors
from test_integration import app, SessionLocal, register, login, make_admin


def test_password_policy_and_legacy_login():
    assert password_errors('password123')
    assert password_errors('AAAAAAAA123!')
    assert not password_errors('StrongPassword123!')
    with TestClient(app) as c:
        invalid=c.post('/api/auth/register',json={'full_name':'Test User','email':'weak-pwd@example.com','password':'Password1234'})
        assert invalid.status_code==422
        response=c.post('/api/auth/register',json={'full_name':'Test User','email':'strong-pwd@example.com','password':'StrongPassword123!'})
        assert response.status_code==201
        c.headers['X-CSRF-Token']=response.json()['csrf']
        assert c.post('/api/auth/logout').status_code==200
        assert c.post('/api/auth/login',json={'email':'strong-pwd@example.com','password':'StrongPassword123!'}).status_code==200


def test_archive_language_with_student_enrollments():
    with TestClient(app) as c:
        register(c,'history-language-test@example.com')
        enrollment=c.post('/api/enrollments',json={'language_id':'lang-gu'})
        assert enrollment.status_code==200
        make_admin();login(c,'admin@example.com','AdminPassword123!')
        response=c.delete('/api/admin/manage/languages/lang-gu')
        assert response.status_code==200 and response.json()['archived']
        with SessionLocal() as db:
            assert not db.get(m.Language,'lang-gu').is_active
            assert db.scalar(select(m.Enrollment).where(m.Enrollment.language_id=='lang-gu')) is not None
        # Restore the shared disposable test fixture, never modify user DB.
        with SessionLocal.begin() as db: db.get(m.Language,'lang-gu').is_active=True


def test_flashcard_review_prevents_lesson_delete():
    with TestClient(app) as c:
        register(c,'card-lesson-test@example.com')
        assert c.post('/api/courses/course-en-a1/enroll').status_code==200
        word='v-les-en-1-1'
        with SessionLocal() as db:
            word=db.scalar(select(m.Vocabulary.id).where(m.Vocabulary.lesson_id=='les-en-1'))
        assert c.put('/api/flashcards/'+word,json={'state':'known'}).status_code==200
        make_admin();login(c,'admin@example.com','AdminPassword123!')
        response=c.delete('/api/admin/manage/lessons/les-en-1')
        assert response.status_code==409
        with SessionLocal() as db:
            assert db.get(m.Lesson,'les-en-1') is not None
            assert db.scalar(select(m.FlashcardState).where(m.FlashcardState.vocabulary_id==word)) is not None


def test_single_correct_mcq_option_cannot_be_doubled():
    with TestClient(app) as c:
        make_admin();login(c,'admin@example.com','AdminPassword123!')
        question=c.post('/api/admin/lessons/les-en-1/questions',json={
            'question_text':'Single correct integrity check?',
            'options':[{'option_text':'Yes','is_correct':True},{'option_text':'No','is_correct':False}]
        })
        assert question.status_code==201,question.text
        q=question.json()
        correct=next(x for x in q['options'] if x['is_correct'])
        wrong=next(x for x in q['options'] if not x['is_correct'])
        assert c.patch('/api/admin/manage/options/'+wrong['id'],json={'is_correct':True}).status_code==409
        assert c.patch('/api/admin/manage/options/'+correct['id'],json={'is_correct':False}).status_code==409
        assert c.delete('/api/admin/manage/options/'+correct['id']).status_code==409
        with SessionLocal() as db:
            assert sum(bool(o.is_correct) for o in db.scalars(select(m.Option).where(m.Option.question_id==q['id'])))==1
        assert c.delete('/api/admin/manage/questions/'+q['id']).status_code==200



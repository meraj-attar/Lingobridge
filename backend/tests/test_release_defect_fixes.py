"""Release regression tests, using only the disposable SQLite fixture in test_integration."""
import pytest
from sqlalchemy import select
from test_integration import app, SessionLocal, make_admin, login
from app import models as m
from app.video_urls import validate_video_url
from fastapi.testclient import TestClient


def admin_client():
    c=TestClient(app)
    make_admin()
    login(c,'admin@example.com','AdminPassword123!')
    return c


def mcq(c, n):
    result=c.post('/api/admin/lessons/les-en-1/questions',json={
        'question_text':f'Release regression MCQ: {n} options?',
        'question_type':'mcq',
        'options':[{'option_text':f'Choice {i}','is_correct':i==0} for i in range(n)]})
    assert result.status_code==201, result.text
    return result.json()


def options_from_db(qid):
    with SessionLocal() as db:
        return [(x.id,x.option_text,x.is_correct) for x in db.scalars(select(m.Option).where(m.Option.question_id==qid).order_by(m.Option.id)).all()]


def test_delete_from_three_allowed_but_two_rejected_and_state_preserved():
    with admin_client() as c:
        q=mcq(c,3)
        wrong=next(o for o in q['options'] if not o['is_correct'])
        assert c.delete('/api/admin/manage/options/'+wrong['id']).status_code==200
        previous=options_from_db(q['id'])
        assert len(previous)==2 and sum(x[2] for x in previous)==1
        second=next(x for x in previous if not x[2])
        res=c.delete('/api/admin/manage/options/'+second[0])
        assert res.status_code==409 and 'at least two' in res.json()['detail']
        assert options_from_db(q['id'])==previous
        correct=next(x for x in previous if x[2])
        assert c.delete('/api/admin/manage/options/'+correct[0]).status_code==409
        assert options_from_db(q['id'])==previous


def test_legacy_one_option_cannot_be_deleted_but_can_be_repaired():
    with admin_client() as c:
        q=mcq(c,2)
        with SessionLocal.begin() as db:
            db.delete(db.get(m.Option,next(o['id'] for o in q['options'] if not o['is_correct'])))
        previous=options_from_db(q['id'])
        assert len(previous)==1
        assert c.delete('/api/admin/manage/options/'+previous[0][0]).status_code==409
        assert options_from_db(q['id'])==previous
        response=c.post('/api/admin/manage/options',json={'question_id':q['id'],'option_text':'Repair missing choice','is_correct':False})
        assert response.status_code==201,response.text
        assert len(options_from_db(q['id']))==2


def test_add_eighth_allowed_ninth_rejected_and_no_db_change():
    with admin_client() as c:
        q=mcq(c,7)
        eighth=c.post('/api/admin/manage/options',json={'question_id':q['id'],'option_text':'Eighth choice','is_correct':False})
        assert eighth.status_code==201,eighth.text
        before=options_from_db(q['id']);assert len(before)==8
        extra=c.post('/api/admin/manage/options',json={'question_id':q['id'],'option_text':'Ninth choice','is_correct':False})
        assert extra.status_code==409 and 'eight' in extra.json()['detail']
        assert before==options_from_db(q['id'])
        assert sum(x[2] for x in before)==1


@pytest.mark.parametrize('count', [0,1,9,10])
def test_bulk_question_validation_rejects_invalid_counts(count):
    with admin_client() as c:
        previous_count=None
        with SessionLocal() as db:
            previous_count=len(db.scalars(select(m.Question).where(m.Question.lesson_id=='les-en-1')).all())
        response=c.post('/api/admin/lessons/les-en-1/questions',json={
            'question_text': 'Reject invalid bulk option count',
            'options':[{'option_text':f'Option {i}','is_correct':i==0} for i in range(count)]})
        assert response.status_code==400,response.text
        with SessionLocal() as db:
            assert len(db.scalars(select(m.Question).where(m.Question.lesson_id=='les-en-1')).all())==previous_count


def test_bulk_create_two_eight_and_exactly_one_correct():
    with admin_client() as c:
        for n in (2,8):
            q=mcq(c,n)
            assert len(options_from_db(q['id']))==n
            assert sum(x[2] for x in options_from_db(q['id']))==1
        r=c.post('/api/admin/lessons/les-en-1/questions',json={'question_text':'No correct option','options':[{'option_text':'A','is_correct':False},{'option_text':'B','is_correct':False}]})
        assert r.status_code==400
        r=c.post('/api/admin/lessons/les-en-1/questions',json={'question_text':'Two correct options','options':[{'option_text':'A','is_correct':True},{'option_text':'B','is_correct':True}]})
        assert r.status_code==400


def test_admin_full_question_editor_cannot_save_wrong_number_or_correct_count():
    with admin_client() as c:
        q=mcq(c,2)
        for opts in ([{'option_text':'One','is_correct':True}],
                     [{'option_text':str(i),'is_correct':i==0} for i in range(9)],
                     [{'option_text':'A','is_correct':True},{'option_text':'B','is_correct':True}]):
            before=options_from_db(q['id'])
            r=c.put('/api/admin/questions/'+q['id'],json={'question_text':'Changing question', 'options':opts})
            assert r.status_code==400,r.text
            assert options_from_db(q['id'])==before


def test_option_update_blank_or_second_correct_rejected():
    with admin_client() as c:
        q=mcq(c,3)
        correct=next(o for o in q['options'] if o['is_correct'])
        wrong=next(o for o in q['options'] if not o['is_correct'])
        original=options_from_db(q['id'])
        for body in ({'option_text':' '},{'is_correct':True},{'question_id':'unrelated'}):
            response=c.patch('/api/admin/manage/options/'+wrong['id'],json=body)
            assert response.status_code in (409,422,400),response.text
            assert options_from_db(q['id'])==original
        assert c.patch('/api/admin/manage/options/'+correct['id'],json={'is_correct':False}).status_code==409
        assert c.patch('/api/admin/manage/options/'+wrong['id'],json={'option_text':'Updated distractor'}).status_code==200


VALID=[
 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
 'https://youtu.be/dQw4w9WgXcQ',
 'https://www.youtube.com/embed/dQw4w9WgXcQ',
 'https://youtube.com/shorts/dQw4w9WgXcQ',
 'https://m.youtube.com/watch?v=dQw4w9WgXcQ&t=12',
 'https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ',
 'https://www.youtube.com/live/dQw4w9WgXcQ',
]
INVALID=[
 'javascript:alert(1)','data:text/html,<script>alert(1)</script>',
 'file:///etc/passwd','ftp://www.youtube.com/watch?v=dQw4w9WgXcQ',
 'http://www.youtube.com/watch?v=dQw4w9WgXcQ',
 'https://www.youtube.com.evil.tld/watch?v=dQw4w9WgXcQ',
 'https://evil.tld/www.youtube.com/watch?v=dQw4w9WgXcQ',
 'https://www.youtube.com@evil.tld/watch?v=dQw4w9WgXcQ',
 'https://person:password@www.youtube.com/watch?v=dQw4w9WgXcQ',
 'https://www.youtube.com:444/watch?v=dQw4w9WgXcQ',
 'https://www.youtube.com:443/watch?v=dQw4w9WgXcQ',
 'https://www.youtube.com/watch?v=bad',
 'https://youtu.be/dQw4w9WgXcQ/more',
 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&v=dQw4w9WgXcQ',
 'https://youtube.com/', 'https://youtube.com/watch',
 'https://youtube.com/redirect?q=evil',
 'https://www.youtube.com/watch?v=dQw4w9WgXcQ#fragment',
 'https://www.youtube.com\\@evil.com/watch?v=dQw4w9WgXcQ',
 'https://youtube.com/watch?v=dQw4w9WgXcQ\n',
 'not-a-url', ' ', None, 100,
]

@pytest.mark.parametrize('value', VALID)
def test_valid_url_supported_by_service(value):
    assert validate_video_url(value)==value

@pytest.mark.parametrize('value',INVALID)
def test_unsafe_urls_rejected_by_service(value):
    with pytest.raises(ValueError):validate_video_url(value)

@pytest.mark.parametrize('value', INVALID)
def test_unsafe_lesson_updates_rejected_no_change(value):
    with admin_client() as c:
        lesson_id='les-en-1'
        with SessionLocal() as db: old=db.get(m.Lesson,lesson_id).video_url
        r=c.patch('/api/admin/manage/lessons/'+lesson_id,json={'video_url':value})
        assert r.status_code==422,(value,r.status_code,r.text)
        with SessionLocal() as db: assert db.get(m.Lesson,lesson_id).video_url==old


def test_lesson_create_and_clear_video_url():
    with admin_client() as c:
        with SessionLocal() as db:
            existing=db.get(m.Lesson,'les-en-1')
            module_id=existing.module_id
        base={'module_id':module_id,'language_id':'lang-en','level_id':'lvl-a1',
              'title':'Release QA video link check', 'lesson_order':999,'content':'Test content'}
        for bad in (INVALID[0],INVALID[5]):
            r=c.post('/api/admin/manage/lessons',json={**base,'video_url':bad})
            assert r.status_code==422,r.text
        good=c.post('/api/admin/manage/lessons',json={**base,'video_url':VALID[0]})
        assert good.status_code==201,good.text
        ident=good.json()['id']
        empty=c.patch('/api/admin/manage/lessons/'+ident,json={'video_url':''})
        assert empty.status_code==200 and empty.json()['video_url']==''
        with SessionLocal() as db: assert db.get(m.Lesson,ident).video_url==''
        assert c.delete('/api/admin/manage/lessons/'+ident).status_code==200


def test_student_cannot_mutate_admin_mcq_or_video():
    with TestClient(app) as c:
        assert c.post('/api/admin/manage/options',json={'question_id':'any','option_text':'x','is_correct':False}).status_code==401
        assert c.patch('/api/admin/manage/lessons/les-en-1',json={'video_url':VALID[0]}).status_code==401

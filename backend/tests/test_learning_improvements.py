"""Regression checks for new additive features and safe historical record handling."""
from datetime import date, timedelta, datetime, timezone
from types import SimpleNamespace
from sqlalchemy import select
from fastapi.testclient import TestClient
from test_integration import app, SessionLocal, m, register, enroll_in_course, login, make_admin
from app.learning_metrics import active_streak, schedule_review, review_due
from app.quality_audit import audit


def test_streak_calculation_is_date_accurate():
    today=date(2026,10,29)
    days=[SimpleNamespace(day=(today-timedelta(days=x)).isoformat(),minutes=10,xp=0) for x in (1,2,4)]
    assert active_streak(days,today)==2  # yesterday and day before
    days.append(SimpleNamespace(day=today.isoformat(),minutes=2,xp=0))
    assert active_streak(days,today)==3
    assert active_streak([],today)==0
    assert active_streak([SimpleNamespace(day=(today-timedelta(days=4)).isoformat(),minutes=10,xp=0)],today)==0


def test_spaced_review_schedule_and_old_card_compatibility():
    old=SimpleNamespace(state='known',due_at=None,repetitions=None,interval_days=None)
    assert review_due(old)  # old state retained; no fabricated review event
    base=datetime(2026,10,29,tzinfo=timezone.utc)
    for number,days in enumerate((1,3,7,14),start=1):
        schedule_review(old,'known',base)
        assert old.repetitions==number and old.interval_days==days
        assert not review_due(old,base)
        assert review_due(old,base+timedelta(days=days))
    schedule_review(old,'revise',base)
    assert old.repetitions==0 and old.state=='revise' and not review_due(old,base) and review_due(old,base+timedelta(days=1))


def test_language_structural_audit_and_hindi_duplicate_option_repair():
    with SessionLocal() as db:
        result=audit(db)
        assert not result['issues'],result['issues'][:5]
        assert len(result['languages'])==10
        q=db.get(m.Question,'q-hi-3-5')
        options=db.scalars(select(m.Option).where(m.Option.question_id==q.id)).all()
        assert len(options)==4
        assert sum(o.is_correct for o in options)==1
        assert {o.id for o in options}.isdisjoint({o.id for o in db.scalars(select(m.Option).where(m.Option.question_id=='q-hi-3-3'))})


def test_recommendations_are_enrollment_scoped_and_revisions_are_persistent():
    with TestClient(app) as c:
        register(c,'review-feature@example.com')
        assert c.get('/api/recommendations').json()=={'lessons':[],'review_due':0,'review_total':0}
        enroll_in_course(c,'course-ur-a1')
        suggestions=c.get('/api/recommendations')
        assert suggestions.status_code==200
        data=suggestions.json()
        assert len(data['lessons'])==3
        assert all(x['language_id']=='lang-ur' and x['reason'] for x in data['lessons'])
        assert data['review_total']>=3 and data['review_due']==data['review_total']
        word=c.get('/api/lessons/'+data['lessons'][0]['lesson_id']).json()['vocabulary_items'][0]
        saved=c.put('/api/flashcards/'+word['id'],json={'state':'known'})
        assert saved.status_code==200
        assert saved.json()['due_at'] and saved.json()['interval_days']==1
        assert not saved.json()['due']
        assert c.get('/api/recommendations').json()['review_due']==data['review_due']-1
        assert c.get('/api/flashcards').json()[0]['state']=='known'
        assert c.post('/api/auth/logout').status_code==200
        login(c,'review-feature@example.com','SafePassword123!')
        assert c.get('/api/flashcards').json()[0]['due_at']==saved.json()['due_at']


def test_streak_updates_with_activity_and_not_after_inactive_gap():
    with TestClient(app) as c:
        data=register(c,'streak-feature@example.com')
        assert c.get('/api/activity').json()['streak']==0
        assert c.post('/api/activity',json={'minutes':0}).status_code==400
        assert c.post('/api/activity',json={'minutes':3}).status_code==200
        assert c.get('/api/activity').json()['streak']==1
        assert c.get('/api/progress').json()['streak']==1
        with SessionLocal.begin() as db:
            user=db.get(m.User,data['user']['id'])
            user.streak=500  # Simulated stale legacy counter must not drive the UI.
        assert c.get('/api/activity').json()['streak']==1
        assert c.get('/api/auth/me').json()['user']['streak']==500  # stored field preserved


def test_admin_cannot_destroy_attempted_question_or_lesson():
    with TestClient(app) as c:
        user=register(c,'history-guard@example.com')
        enroll_in_course(c)
        q=c.get('/api/lessons/les-en-1').json()['quiz_questions'][0]
        with SessionLocal.begin() as db:
            db.add(m.QuizAttempt(id='history-guard-attempt',user_id=user['user']['id'],lesson_id='les-en-1',score=1,total_questions=1,percentage=100,passed=True,
                answers=[{'question_id':q['id'],'option_id':q['options'][0]['id']}]))
        try:
            make_admin()
            login(c,'admin@example.com','AdminPassword123!')
            assert c.delete(f'/api/admin/manage/questions/{q["id"]}').status_code==409
            assert c.delete('/api/admin/manage/lessons/les-en-1').status_code==409
            assert c.patch(f'/api/admin/manage/questions/{q["id"]}',json={'question_text':'Change'}).status_code==409
        finally:
            with SessionLocal.begin() as db:
                db.delete(db.get(m.QuizAttempt,'history-guard-attempt'))



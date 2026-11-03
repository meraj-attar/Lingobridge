"""Real FastAPI + SQLAlchemy regression tests for independent course learning.

Runs against SQLite for speed. PostgreSQL integration is separately required.
"""
from sqlalchemy import select, func
from fastapi.testclient import TestClient
from test_integration import app, SessionLocal, m, make_admin, register, login, enroll_in_course, ticket_for


def test_all_languages_and_cefr_bands_have_content():
    with TestClient(app) as c, SessionLocal() as db:
        for language in ('en','hi','mr','gu','bn','ta','te','kn','ur','es'):
            for band in ('a1','a2','b1','b2','c1','c2'):
                lessons=db.scalars(select(m.Lesson).where(m.Lesson.language_id==f'lang-{language}',m.Lesson.level_id==f'lvl-{band}')).all()
                assert len(lessons)>=3,(language,band)
                assert all(l.content and l.grammar_notes and l.module_id for l in lessons)
                for lesson in lessons:
                    vocab=db.scalars(select(m.Vocabulary).where(m.Vocabulary.lesson_id==lesson.id)).all()
                    assert vocab and all(v.word and v.translation for v in vocab)
                # One full quiz containing all exercise types for each level.
                assert any({q.question_type for q in db.scalars(select(m.Question).where(m.Question.lesson_id==les.id))} == {'mcq','fill_blank','matching','arrangement'} for les in lessons)
        for language in ('gu','bn','ta','te','kn','ur','es'):
            for band in ('a1','a2','b1','b2','c1','c2'):
                balanced=db.scalars(select(m.Lesson).where(m.Lesson.language_id==f'lang-{language}',m.Lesson.level_id==f'lvl-{band}')).all()
                assert len(balanced)==3,(language,band,len(balanced))
                for lesson in balanced:
                    kinds={q.question_type for q in db.scalars(select(m.Question).where(m.Question.lesson_id==lesson.id))}
                    assert kinds=={'mcq','fill_blank','matching','arrangement'},(language,band,lesson.id,kinds)
                    assert len(db.scalars(select(m.Vocabulary).where(m.Vocabulary.lesson_id==lesson.id)).all())==3
        assert any('\u0900'<=ch<='\u097f' for ch in db.get(m.Lesson,'les-hi-a2-1').content)
        assert any('\u0900'<=ch<='\u097f' for ch in db.get(m.Lesson,'les-mr-a2-1').content)


def test_course_enrollment_is_independent_and_progress_is_correct():
    with TestClient(app) as c:
        register(c,'course-learner@example.com')
        assert c.post('/api/enrollments',json={'language_id':'lang-en'}).status_code==200
        assert c.get('/api/lessons/les-en-1').status_code==403
        assert c.post('/api/lessons/les-en-1/quiz-session').status_code==403
        listing=c.get('/api/courses?language_id=lang-en').json()
        assert len(listing)==6 and not any(x['enrolled'] for x in listing)
        assert c.post('/api/courses/does-not-exist/enroll').status_code==404
        course=enroll_in_course(c,'course-en-a1')
        assert course['enrolled'] and course['lesson_count']>=3
        assert enroll_in_course(c,'course-en-a1')['enrolled']
        assert len(c.get('/api/courses/enrolled/me').json())==1
        assert c.get('/api/lessons/les-en-1').status_code==200
        assert c.get('/api/lessons/les-en-a2-1').status_code==403
        modules=c.get('/api/courses/course-en-a1/modules').json()
        assert modules and modules[0]['lessons']
        assert [l['lesson_order'] for l in modules[0]['lessons']]==sorted(l['lesson_order'] for l in modules[0]['lessons'])
        lesson=c.get('/api/lessons/les-en-1').json()
        answers=[]
        with SessionLocal() as db:
            for q in lesson['quiz_questions']:
                opt=db.scalar(select(m.Option).where(m.Option.question_id==q['id'],m.Option.is_correct==True))
                answers.append({'question_id':q['id'],'option_id':opt.id})
        ticket=ticket_for(c,'les-en-1')
        score=c.post('/api/lessons/les-en-1/submit',json={'answers':answers,'attempt_token':ticket})
        assert score.status_code==200,score.text
        assert score.json()['passed']
        assert c.post('/api/lessons/les-en-1/submit',json={'answers':answers,'attempt_token':ticket}).status_code==403
        course=c.get('/api/courses/enrolled/me').json()[0]
        assert course['completed_lessons']==1 and course['progress_percent']>0
        activity=c.get('/api/activity').json()
        assert activity['today_minutes']>0 and activity['daily_goal_percent']>0
        c.post('/api/auth/logout')
        login(c,'course-learner@example.com','SafePassword123!')
        assert c.get('/api/courses/enrolled/me').json()[0]['completed_lessons']==1
        assert c.get('/api/progress').json()['quiz_attempts'][0]['score']==len(answers)


def test_flashcard_known_revise_states_persist_and_are_isolated():
    with TestClient(app) as c:
        register(c,'flash-learner@example.com')
        enroll_in_course(c)
        detail=c.get('/api/lessons/les-en-1').json()
        word=detail['vocabulary_items'][0]['id']
        assert c.put('/api/flashcards/'+word,json={'state':'other'}).status_code==400
        assert c.put('/api/flashcards/'+word,json={'state':'known'}).json()['state']=='known'
        assert c.put('/api/flashcards/'+word,json={'state':'revise'}).json()['state']=='revise'
        assert c.get('/api/flashcards').json()[0]['state']=='revise'
        c.post('/api/auth/logout')
        login(c,'flash-learner@example.com','SafePassword123!')
        assert c.get('/api/flashcards').json()[0]['vocabulary_id']==word
        register(c,'flash-second@example.com')
        assert c.get('/api/flashcards').json()==[]
        assert c.put('/api/flashcards/'+word,json={'state':'known'}).status_code==403
        enroll_in_course(c)
        assert c.put('/api/flashcards/'+word,json={'state':'known'}).status_code==200
        assert c.get('/api/flashcards').json()[0]['state']=='known'


def test_admin_content_validation_and_all_four_question_types():
    with TestClient(app) as c:
        make_admin();login(c,'admin@example.com','AdminPassword123!')
        new_course=c.post('/api/admin/manage/courses',json={'language_id':'lang-mr','level_id':'lvl-b2','title':'Applied Marathi','is_published':True})
        assert new_course.status_code==201,new_course.text
        course_id=new_course.json()['id']
        module=c.post('/api/admin/manage/modules',json={'course_id':course_id,'title':'First Unit','sort_order':1})
        assert module.status_code==201,module.text
        mod_id=module.json()['id']
        assert c.post('/api/admin/manage/lessons',json={'module_id':mod_id,'language_id':'lang-en','level_id':'lvl-b2','title':'Incorrect parent','lesson_order':1}).status_code==400
        lesson=c.post('/api/admin/manage/lessons',json={'module_id':mod_id,'language_id':'lang-mr','level_id':'lvl-b2','title':'संवाद','content':'दैनंदिन संवाद','grammar_notes':'मात्र जोडशब्द','lesson_order':1})
        assert lesson.status_code==201,lesson.text
        lid=lesson.json()['id']
        vocab=c.post(f'/api/admin/lessons/{lid}/vocabulary',json={'word':'मात्र','translation':'however','example_sentence':'माझे मत मात्र वेगळे आहे.'})
        assert vocab.status_code==201,vocab.text
        assert c.patch('/api/admin/manage/vocabulary/'+vocab.json()['id'],json={'translation':'nevertheless'}).json()['translation']=='nevertheless'
        fixtures=[
            {'question_text':'Choose the correct sentence','question_type':'mcq','options':[{'option_text':'माझे मत वेगळे आहे','is_correct':True},{'option_text':'माझे वेगळे मत आहे नाही','is_correct':False}]},
            {'question_text':'Complete this sentence','question_type':'fill_blank','answer_text':'माझे','meta':{'prompt':'_____ मत वेगळे आहे.'}},
            {'question_text':'Match the words','question_type':'matching','meta':{'pairs':[['मात्र','however'],['मत','opinion']]}},
            {'question_text':'Arrange these tokens','question_type':'arrangement','answer_text':'माझे मत वेगळे आहे','meta':{'tokens':['माझे','मत','वेगळे','आहे']}}
        ]
        for data in fixtures:
            r=c.post(f'/api/admin/lessons/{lid}/questions',json=data)
            assert r.status_code==201,(data['question_type'],r.text)
            qid=r.json()['id']
            if data['question_type']=='mcq':
                edited=c.put('/api/admin/questions/'+qid,json={**data,'question_text':'Updated multiple choice'})
                assert edited.status_code==200,edited.text
            if data['question_type']=='matching':
                assert c.put('/api/admin/questions/'+qid,json={**data,'meta':{'pairs':[['invalid']]}}).status_code==400
        assert len(c.get('/api/lessons/'+lid+'?include_answers=true').json()['quiz_questions'])==4
        assert c.get('/api/admin/stats').status_code==200
        assert c.delete('/api/admin/manage/vocabulary/'+vocab.json()['id']).status_code==200
        # Clean dependent rows to allow the module and course to be removed.
        assert c.delete('/api/admin/manage/lessons/'+lid).status_code==200
        assert c.delete('/api/admin/manage/modules/'+mod_id).status_code==200
        assert c.delete('/api/admin/manage/courses/'+course_id).status_code==200


def test_quiz_answer_material_remains_server_only():
    with TestClient(app) as c:
        register(c,'answer-learner@example.com')
        enroll_in_course(c,'course-hi-b2')
        l=c.get('/api/lessons/les-hi-b2-1').json()
        for q in l['quiz_questions']:
            assert 'answer_text' not in q and 'explanation' not in q
            assert all('is_correct' not in opt for opt in q['options'])
            assert 'pairs' not in q['meta']
        assert c.get('/api/admin/manage/questions').status_code==403
        assert c.get('/api/admin/students').status_code==403


def test_all_seven_new_languages_are_available_through_student_api():
    with TestClient(app) as c:
        register(c, 'ten-language-learner@example.com')
        for language in ('gu', 'bn', 'ta', 'te', 'kn', 'ur', 'es'):
            enrolled = c.post(f'/api/courses/course-{language}-a1/enroll')
            assert enrolled.status_code == 200, (language, enrolled.text)
            modules = c.get(f'/api/courses/course-{language}-a1/modules')
            assert modules.status_code == 200 and modules.json(), language
            lesson_id = modules.json()[0]['lessons'][0]['id']
            detail = c.get(f'/api/lessons/{lesson_id}')
            assert detail.status_code == 200, (language, detail.text)
            payload = detail.json()
            assert len(payload['vocabulary_items']) == 3
            assert {q['question_type'] for q in payload['quiz_questions']} == {
                'mcq', 'fill_blank', 'matching', 'arrangement'
            }

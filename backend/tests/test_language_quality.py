"""Ten-language structural and API regressions.

These checks do not replace human linguistic review.
"""
from collections import Counter
from sqlalchemy import select, func
from fastapi.testclient import TestClient
from test_integration import app, SessionLocal, m, seed, register, enroll_in_course
from app.content_quality import (
    check_authored_words, check_extension_words, CURRICULA, PROMPTS,
    alternatives, extension_alternatives, repair_previous_seed,
)
from app.seed import LANGS as SEED_LANGS

SCRIPTS={
    'hi':(0x0900,0x097f), 'mr':(0x0900,0x097f),
    'gu':(0x0a80,0x0aff), 'bn':(0x0980,0x09ff),
    'ta':(0x0b80,0x0bff), 'te':(0x0c00,0x0c7f),
    'kn':(0x0c80,0x0cff), 'ur':(0x0600,0x06ff),
}
LANGS=('en','hi','mr','gu','bn','ta','te','kn','ur','es')
BANDS=('a1','a2','b1','b2','c1','c2')

def test_ten_languages_native_scripts_and_seed_structure():
    assert not check_authored_words(),check_authored_words()
    assert not check_extension_words(),check_extension_words()
    assert set(SEED_LANGS)==set(LANGS)
    with SessionLocal() as db:
        for code in LANGS:
            language=db.get(m.Language,'lang-'+code)
            assert language
            for band in BANDS:
                course=db.get(m.Course,f'course-{code}-{band}')
                assert course and course.language_id==language.id
                module=db.get(m.Module,f'module-{code}-{band}')
                assert module and module.course_id==course.id
                lessons=db.scalars(select(m.Lesson).where(m.Lesson.module_id==module.id)).all()
                assert len(lessons)>=3,(code,band)
                for lesson in lessons:
                    assert lesson.language_id==language.id and lesson.level_id==course.level_id
                    assert lesson.content and lesson.grammar_notes
                    words=db.scalars(select(m.Vocabulary).where(m.Vocabulary.lesson_id==lesson.id)).all()
                    assert words and all(w.word and w.translation for w in words)
                    questions=db.scalars(select(m.Question).where(m.Question.lesson_id==lesson.id)).all()
                    assert questions
                    if lesson.id.find('-balanced-')>=0:
                        assert {q.question_type for q in questions}=={'mcq','fill_blank','matching','arrangement'}
                        assert len(words)==3
                        assert all(w.translation!='Grammar focus' for w in words)
                        mcq=next(q for q in questions if q.question_type=='mcq')
                        opts=db.scalars(select(m.Option).where(m.Option.question_id==mcq.id)).all()
                        assert len(set(o.option_text for o in opts))==4
                        assert sum(o.is_correct for o in opts)==1
                        assert mcq.question_text.startswith(PROMPTS[code][0])
                        example=next(w.word for w in words if ' ' in w.word)
                        if code in SCRIPTS:
                            lo,hi=SCRIPTS[code]
                            assert any(lo<=ord(c)<=hi for c in example),(code,band,lesson.id)
                        if code=='es':assert any(c.isalpha() for c in example)


def test_all_ten_languages_access_lessons_via_api():
    with TestClient(app) as client:
        register(client,'ten-language-api@example.com')
        languages=client.get('/api/languages').json()
        assert {l['code'] for l in languages}==set(LANGS)
        for code in LANGS:
            courses=client.get('/api/courses',params={'language_id':'lang-'+code})
            assert courses.status_code==200 and len(courses.json())==6,(code,courses.text)
            enrollment=enroll_in_course(client,f'course-{code}-a1')
            assert enrollment['enrolled']
            modules=client.get(f'/api/courses/course-{code}-a1/modules')
            assert modules.status_code==200 and modules.json()[0]['lessons']
            lid=modules.json()[0]['lessons'][0]['id']
            detail=client.get(f'/api/lessons/{lid}')
            assert detail.status_code==200,(code,detail.text)
            result=detail.json()
            assert result['languages']['code']==code
            assert result['vocabulary_items']
            assert result['quiz_questions']
            assert all('is_correct' not in opt for q in result['quiz_questions'] for opt in q['options'])
            assert client.post(f'/api/lessons/{lid}/quiz-session').status_code==200


def test_guarded_repairs_preserve_admin_edits_and_are_idempotent():
    # Database was seeded in test_integration; verify the safe repair is a no-op
    # when the current seed has already been applied.
    with SessionLocal.begin() as db:
        word=db.get(m.Vocabulary,'v-les-gu-a1-balanced-1-3')
        previous=word.word
        word.word='Instructor-approved override'
    try:
        seed()
        with SessionLocal() as db:
            assert db.get(m.Vocabulary,'v-les-gu-a1-balanced-1-3').word=='Instructor-approved override'
    finally:
        with SessionLocal.begin() as db:
            db.get(m.Vocabulary,'v-les-gu-a1-balanced-1-3').word=previous


def test_repair_keeps_prior_quiz_option_when_student_attempt_exists():
    with SessionLocal.begin() as db:
        lid='les-gu-a1-balanced-1'
        first=db.get(m.Option,'o-q-'+lid+'-1')
        previous=first.option_text
        # Restore only the exact old auto-generated distractor for this test.
        phrase=CURRICULA['gu']['A1'][0][1]
        first.option_text=' '.join(reversed(phrase.split()))
        attempt=m.QuizAttempt(id='qa-quality-safety',user_id=db.scalar(select(m.User.id).where(m.User.email=='ten-language-api@example.com')),
            lesson_id=lid,score=0,total_questions=1,percentage=0,passed=False,answers=[])
        db.add(attempt)
    try:
        with SessionLocal.begin() as db:
            counts=repair_previous_seed(db)
            assert counts['skipped_attempted']>=1
        with SessionLocal() as db:
            assert db.get(m.Option,'o-q-'+lid+'-1').option_text==' '.join(reversed(phrase.split()))
    finally:
        with SessionLocal.begin() as db:
            db.delete(db.get(m.QuizAttempt,'qa-quality-safety'))
            db.get(m.Option,'o-q-'+lid+'-1').option_text=previous


def test_native_catalogue_titles_and_guarded_correction():
    with SessionLocal() as db:
        for code in LANGS:
            course=db.get(m.Course,'course-'+code+'-a1')
            lang=db.get(m.Language,'lang-'+code)
            assert lang.native_name in course.title
            assert course.description
        assert 'વિચારું છું' in db.get(m.Lesson,'les-gu-b2-balanced-1').content

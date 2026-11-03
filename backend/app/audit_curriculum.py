"""Read-only curriculum coverage report for the configured database.

Usage: python -m app.audit_curriculum
Does not assert linguistic correctness on client devices.
"""
import json
from sqlalchemy import select,func
from .db import SessionLocal
from . import models as m
from .seed import LANGS

LEVELS=('A1','A2','B1','B2','C1','C2')

def audit(db):
    result={}
    for code in LANGS:
        language=db.scalar(select(m.Language).where(m.Language.code==code))
        if language is None:
            result[code]={'error':'language missing'}
            continue
        levels={}
        for level in LEVELS:
            level_obj=db.scalar(select(m.Level).where(m.Level.code==level))
            courses=db.scalars(select(m.Course).where(m.Course.language_id==language.id,m.Course.level_id==level_obj.id)).all() if level_obj else []
            modules=db.scalars(select(m.Module).where(m.Module.course_id.in_([c.id for c in courses]))).all() if courses else []
            lessons=db.scalars(select(m.Lesson).where(m.Lesson.module_id.in_([mod.id for mod in modules]))).all() if modules else []
            lesson_ids=[l.id for l in lessons]
            vocabulary=db.scalars(select(m.Vocabulary).where(m.Vocabulary.lesson_id.in_(lesson_ids))).all() if lesson_ids else []
            questions=db.scalars(select(m.Question).where(m.Question.lesson_id.in_(lesson_ids))).all() if lesson_ids else []
            levels[level]={
                'courses':len(courses),'modules':len(modules),
                'lessons':len(lessons),'vocabulary':len(vocabulary),'questions':len(questions),
                'lessons_missing_vocabulary':len(set(lesson_ids)-{w.lesson_id for w in vocabulary}),
                'lessons_missing_questions':len(set(lesson_ids)-{q.lesson_id for q in questions}),
            }
        result[code]={'native_name':language.native_name,'levels':levels}
    return result

if __name__=='__main__':
    with SessionLocal() as db:
        print(json.dumps(audit(db),ensure_ascii=False,indent=2))

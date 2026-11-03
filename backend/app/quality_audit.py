"""Read-only structural curriculum audit.

Designed to find omissions, NOT to certify nuanced grammar or translation accuracy.
Run with DATABASE_URL pointing to a restored/staging database, never production seed.
"""
import json
from collections import Counter
from sqlalchemy import select
from . import models as m
from .db import SessionLocal
from .seed import LANGS


def audit(db):
    languages = {}
    issues = []
    for code in LANGS:
        lang=db.scalar(select(m.Language).where(m.Language.code==code))
        if not lang:
            issues.append({'language':code,'object':'language','id':code,'issue':'language_missing'})
            languages[code]={'courses':0,'modules':0,'lessons':0,'vocabulary':0,'questions':0}
            continue
        total=Counter()
        courses=db.scalars(select(m.Course).where(m.Course.language_id==lang.id)).all()
        total['courses']=len(courses)
        for course in courses:
            modules=db.scalars(select(m.Module).where(m.Module.course_id==course.id)).all()
            if not modules:issues.append({'language':code,'object':'course','id':course.id,'issue':'no_modules'})
            total['modules']+=len(modules)
            for module in modules:
                lessons=db.scalars(select(m.Lesson).where(m.Lesson.module_id==module.id)).all()
                if not lessons:issues.append({'language':code,'object':'module','id':module.id,'issue':'no_lessons'})
                total['lessons']+=len(lessons)
                for lesson in lessons:
                    if lesson.language_id!=course.language_id or lesson.level_id!=course.level_id:
                        issues.append({'language':code,'object':'lesson','id':lesson.id,'issue':'incorrect_course_mapping'})
                    if not lesson.content or not lesson.grammar_notes:
                        issues.append({'language':code,'object':'lesson','id':lesson.id,'issue':'missing_content_or_grammar'})
                    vocab=db.scalars(select(m.Vocabulary).where(m.Vocabulary.lesson_id==lesson.id)).all()
                    questions=db.scalars(select(m.Question).where(m.Question.lesson_id==lesson.id)).all()
                    total['vocabulary']+=len(vocab)
                    total['questions']+=len(questions)
                    if not vocab or not questions:
                        issues.append({'language':code,'object':'lesson','id':lesson.id,'issue':'missing_vocabulary_or_quiz'})
                    for v in vocab:
                        if not (v.word and v.word.strip() and v.translation and v.translation.strip() and v.example_sentence and v.example_sentence.strip()):
                            issues.append({'language':code,'object':'vocabulary','id':v.id,'issue':'missing_word_translation_or_example'})
                    for q in questions:
                        if not (q.question_text or '').strip():
                            issues.append({'language':code,'object':'question','id':q.id,'issue':'empty_question'})
                        opts=db.scalars(select(m.Option).where(m.Option.question_id==q.id)).all()
                        if q.question_type=='mcq':
                            if len(opts)<2 or sum(o.is_correct for o in opts)!=1 or len({o.option_text.strip() for o in opts}) != len(opts):
                                issues.append({'language':code,'object':'question','id':q.id,'issue':'invalid_mcq_options'})
                        elif q.question_type=='fill_blank':
                            if not q.answer_text or not (q.meta or {}).get('prompt','').count('_____')==1:
                                issues.append({'language':code,'object':'question','id':q.id,'issue':'invalid_fill_blank'})
                        elif q.question_type=='arrangement':
                            if ' '.join((q.meta or {}).get('tokens',[])).strip()!= (q.answer_text or '').strip():
                                issues.append({'language':code,'object':'question','id':q.id,'issue':'incorrect_arrangement_answer'})
                        elif q.question_type=='matching':
                            pairs=(q.meta or {}).get('pairs',[])
                            if len(pairs)<2 or len({str(p[0]) for p in pairs})!=len(pairs) or len({str(p[1]) for p in pairs})!=len(pairs):
                                issues.append({'language':code,'object':'question','id':q.id,'issue':'invalid_matching_pairs'})
                        else:
                            issues.append({'language':code,'object':'question','id':q.id,'issue':'unknown_exercise_type'})
        languages[code]=dict(total)
    return {'languages':languages,'issues':issues,'issue_count':len(issues),'disclaimer':'Structural review only; professional/native-speaker copy-edit remains necessary.'}


if __name__=='__main__':
    with SessionLocal() as db:
        print(json.dumps(audit(db),indent=2,ensure_ascii=False))

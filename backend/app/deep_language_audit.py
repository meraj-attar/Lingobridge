"""Independent ten-language script, content/answer and accessibility audit.

Passes are mechanical ONLY; native speakers must still check idioms and meaning.
"""
import json
from collections import defaultdict
from sqlalchemy import select
from .db import SessionLocal
from . import models as m
from .seed import LANGS

SCRIPT_RANGES = {
    'hi':(0x0900,0x097f), 'mr':(0x0900,0x097f),
    'gu':(0x0a80,0x0aff), 'bn':(0x0980,0x09ff),
    'ta':(0x0b80,0x0bff), 'te':(0x0c00,0x0c7f),
    'kn':(0x0c80,0x0cff), 'ur':(0x0600,0x06ff),
}


def has_native_script(value, code):
    if code not in SCRIPT_RANGES: return True
    low, high = SCRIPT_RANGES[code]
    return any(low<=ord(ch)<=high for ch in (value or ''))


def audit(db):
    issues=[]; counts=defaultdict(lambda: {'vocabulary':0,'questions':0,'no_native_script':0,'lesson_count':0})
    for code in LANGS:
        lang=db.scalar(select(m.Language).where(m.Language.code==code))
        if not lang:
            issues.append({'code':code,'id':'','issue':'missing_language'}); continue
        lessons=db.scalars(select(m.Lesson).where(m.Lesson.language_id==lang.id)).all()
        counts[code]['lesson_count']=len(lessons)
        for lesson in lessons:
            voc=db.scalars(select(m.Vocabulary).where(m.Vocabulary.lesson_id==lesson.id)).all()
            quizzes=db.scalars(select(m.Question).where(m.Question.lesson_id==lesson.id)).all()
            for item in voc:
                counts[code]['vocabulary'] += 1
                if not has_native_script(item.word,code):
                    counts[code]['no_native_script'] += 1
                    issues.append({'code':code,'id':item.id,'issue':'vocabulary_lacks_native_script',
                                   'word':item.word})
                if not item.example_translation or not item.example_translation.strip():
                    issues.append({'code':code,'id':item.id,'issue':'missing_example_translation'})
                for field in ('word','translation','example_sentence','example_translation'):
                    if '\ufffd' in (getattr(item,field) or ''):
                        issues.append({'code':code,'id':item.id,'issue':'replacement_character_'+field})
            for question in quizzes:
                counts[code]['questions']+=1
                if question.question_type == 'mcq':
                    options=db.scalars(select(m.Option).where(m.Option.question_id==question.id)).all()
                    if len(options)<2 or sum(bool(o.is_correct) for o in options)!=1:
                        issues.append({'code':code,'id':question.id,'issue':'mcq_invalid_answer'})
                if '\ufffd' in (question.question_text or ''):
                    issues.append({'code':code,'id':question.id,'issue':'replacement_character_quiz'})
    return {'languages':dict(counts),'issue_count':len(issues),'issues':issues,
            'native_speaker_validation':'NOT PERFORMED',
            'urdu_direction_expected':'rtl',
            'note':'No proof of grammar, semantics, or regional style.'}


if __name__=='__main__':
    with SessionLocal() as db:
        print(json.dumps(audit(db),indent=2,ensure_ascii=False))

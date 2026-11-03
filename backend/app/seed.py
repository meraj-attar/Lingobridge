"""Idempotent starter curriculum. Never overwrites admin-edited rows or user progress."""
import json
from pathlib import Path
from sqlalchemy import select
from .db import SessionLocal
from .models import Role, Language, Level, Course, Module, Lesson, Vocabulary, Question, Option, Achievement
from .curriculum_extension import UNITS
from .additional_curriculum import LANGUAGES as ADDITIONAL_LANGUAGES, CURRICULA as ADDITIONAL_CURRICULA
from .content_quality import (EXTRA_WORDS, PROMPTS, alternatives, repair_previous_seed,
                              EXTENSION_WORDS, EXTENSION_PROMPT, extension_meaning, extension_alternatives, repair_extension_seed, balanced_native_fields, NATIVE_CATALOG, repair_catalogue, repair_reviewed_phrases, NATIVE_DESCRIPTIONS, balanced_objectives, BASE_LEXEMES, BASE_MEANINGS, repair_base_seed)
# Existing legacy locale data remains populated for schema compatibility.
LEGACY_LANGUAGE_LOCALES = {
    'en':'en-US', 'hi':'hi-IN', 'mr':'mr-IN', 'gu':'gu-IN', 'bn':'bn-IN',
    'ta':'ta-IN', 'te':'te-IN', 'kn':'kn-IN', 'ur':'ur-PK', 'es':'es-ES',
}

DATA=Path(__file__).resolve().parents[1]/'data'/'legacy_seed.json'
LANGS={
'en': {'name':'English','native_name':'English','flag':'🇬🇧','color':'#2563EB','description':'Learn practical English for everyday, academic and professional communication.'},
'hi': {'name':'Hindi','native_name':'हिन्दी','flag':'🇮🇳','color':'#EA580C','description':'Learn Hindi using authentic Devanagari examples.'},
'mr': {'name':'Marathi','native_name':'मराठी','flag':'🇮🇳','color':'#15803D','description':'Learn conversational Marathi, reading and grammar.'},
**ADDITIONAL_LANGUAGES,
}
# Level-specific original instructional material; no duplicated language-name-only lessons.
CURRICULUM={
'en': [
('A2','Shopping & Requests','Could I have a receipt, please?','Could I have a receipt, please?','Making polite requests','Could I have a receipt, please?','Give me a receipt.','I have receipt.','Receipts please had.'),
('B1','Explaining Experiences','I have been learning English for two years.','I have been learning English for two years.','Present perfect continuous','I have been learning English for two years.','I learning English since two years.','I learned English tomorrow.','I have learn English for two year.'),
('B2','Discussing Possibilities','If I had more time, I would read more.','If I had more time, I would read more.','Second conditional','If I had more time, I would read more.','If I have more time, I would read more.','If I had more time, I will reading.','If I had time, I reading.'),
('C1','Academic Argumentation','Although the evidence is limited, the hypothesis remains plausible.','Although the evidence is limited, the hypothesis remains plausible.','Concessive clauses','Although the evidence is limited, the hypothesis remains plausible.','Because evidence limited, hypothesis proved.','Evidence limited therefore certainly true.','Although the evidence are limited, hypotheses remain proof.'),
('C2','Nuanced Professional Speech','The proposal is compelling, albeit not without limitations.','The proposal is compelling, albeit not without limitations.','Concessive register and nuance','The proposal is compelling, albeit not without limitations.','The proposal is perfect without limitations.','Albeit proposal without compel.','Proposal compelling except never limitations.')],
'hi': [
('A2','बाज़ार में विनम्र अनुरोध','कृपया मुझे रसीद दीजिए।','कृपया मुझे रसीद दीजिए।','विनम्र अनुरोध में कृपया और दीजिए','कृपया मुझे रसीद दीजिए।','मुझे रसीद दिया।','रसीद कृपया मैं।','रसीद दीजिए था।'),
('B1','अपने अनुभव बताना','मैं दो साल से हिंदी सीख रहा हूँ।','मैं दो साल से हिंदी सीख रहा हूँ।','से के साथ जारी क्रिया','मैं दो साल से हिंदी सीख रहा हूँ।','मैं दो साल पर हिंदी सीख।','मैं कल दो साल हिंदी सीखा।','मुझे दो साल हिंदी सीखें।'),
('B2','कल्पना और संभावना','अगर मेरे पास समय होता, तो मैं और पढ़ता।','अगर मेरे पास समय होता, तो मैं और पढ़ता।','अगर...तो का काल्पनिक प्रयोग','अगर मेरे पास समय होता, तो मैं और पढ़ता।','अगर समय होगा, तो मैं पढ़ता था।','अगर मेरे समय, तो पढ़ना।','अगर पास समय होता मैं पढ़ने होंगे।'),
('C1','तर्क और प्रमाण','यद्यपि प्रमाण सीमित हैं, यह विचार विचारणीय है।','यद्यपि प्रमाण सीमित हैं, यह विचार विचारणीय है।','यद्यपि के साथ विरोधाभासी विचार','यद्यपि प्रमाण सीमित हैं, यह विचार विचारणीय है।','यद्यपि प्रमाण सीमित है यह निश्चित सिद्ध।','प्रमाण नहीं इसलिए सच है।','यद्यपि यह विचार बिना प्रमाण निश्चित।'),
('C2','सूक्ष्म औपचारिक अभिव्यक्ति','प्रस्ताव प्रभावशाली है, तथापि उसकी कुछ सीमाएँ हैं।','प्रस्ताव प्रभावशाली है, तथापि उसकी कुछ सीमाएँ हैं।','तथापि द्वारा संतुलित निष्कर्ष','प्रस्ताव प्रभावशाली है, तथापि उसकी कुछ सीमाएँ हैं।','प्रस्ताव पूर्ण है और कोई सीमा नहीं।','प्रस्ताव तथापि सीमाएँ बिना प्रभाव।','सीमाएँ प्रभावशाली प्रस्ताव तथापि है कुछ।')],
'mr': [
('A1','ओळख आणि अभिवादन','नमस्कार, माझे नाव मीरा आहे.','नमस्कार, माझे नाव मीरा आहे.','माझे नाव... आहे','नमस्कार, माझे नाव मीरा आहे.','नमस्कार, मी नाव मीरा आहे.','माझे मीरा नाव नाही आहे.','नमस्कार माझे नाव मीरा होते.'),
('A1','कुटुंब आणि नाती','ही माझी बहीण आहे.','ही माझी बहीण आहे.','माझा, माझी, माझे यांचा वापर','ही माझी बहीण आहे.','हा माझी बहीण आहे.','ही माझा बहीण आहे.','माझी हा बहीण आहे.'),
('A1','संख्या आणि वेळ','आता तीन वाजले आहेत.','आता तीन वाजले आहेत.','वेळ सांगताना वाजले','आता तीन वाजले आहेत.','आता तीन वाजला आहे.','तीन आता वाजत आहेत.','आता तीन होती आहेत.'),
('A1','अन्न आणि विनंती','मला पाणी पाहिजे.','मला पाणी पाहिजे.','मला ... पाहिजे','मला पाणी पाहिजे.','मी पाणी पाहिजे.','मला पाणी पाहिजेत.','पाणी मला आहे पाहिजे.'),
('A1','दिशा विचारणे','रेल्वे स्थानक कुठे आहे?','रेल्वे स्थानक कुठे आहे?','कुठे हा प्रश्नार्थक शब्द','रेल्वे स्थानक कुठे आहे?','रेल्वे स्थानक कोण आहे?','कुठे स्थानक आहे का रेल्वे?','रेल्वे कुठे स्थानक होते?'),
('A2','दुकानात विनंती','कृपया मला पावती द्या.','कृपया मला पावती द्या.','विनंतीत कृपया आणि द्या','कृपया मला पावती द्या.','कृपया मी पावती द्या.','पावती मला देतो कृपया.','कृपया पावती दिले. '),
('B1','अनुभव सांगणे','मी दोन वर्षांपासून मराठी शिकत आहे.','मी दोन वर्षांपासून मराठी शिकत आहे.','पासून वापरून कालावधी दाखवा','मी दोन वर्षांपासून मराठी शिकत आहे.','मी दोन वर्षांवर मराठी शिकत.','मी उद्या दोन वर्ष मराठी शिकलो.','मी मराठी दोन वर्ष शिकणार होतो काल.'),
('B2','कल्पना मांडणे','माझ्याकडे वेळ असता तर मी अधिक वाचले असते.','माझ्याकडे वेळ असता तर मी अधिक वाचले असते.','असता तर वापरून अट व्यक्त करा','माझ्याकडे वेळ असता तर मी अधिक वाचले असते.','माझ्याकडे वेळ आहे तर मी वाचले काल.','वेळ तर असता माझे वाचन.','माझ्याकडे वेळ असता मी अधिक वाचतो उद्या.'),
('C1','तर्क आणि पुरावे','पुरावे मर्यादित असले तरी हा विचार महत्त्वाचा आहे.','पुरावे मर्यादित असले तरी हा विचार महत्त्वाचा आहे.','असले तरी विरोध दर्शवतो','पुरावे मर्यादित असले तरी हा विचार महत्त्वाचा आहे.','पुरावे मर्यादित म्हणजे विचार सिद्ध आहे.','पुरावे नाही म्हणजे निश्चित खरे.','पुरावे असले तरी विचार मर्यादितच सिद्ध.'),
('C2','सूक्ष्म औपचारिक भाषा','हा प्रस्ताव प्रभावी असला तरी त्याला काही मर्यादा आहेत.','हा प्रस्ताव प्रभावी असला तरी त्याला काही मर्यादा आहेत.','असला तरी वापरून संतुलित अभिप्राय','हा प्रस्ताव प्रभावी असला तरी त्याला काही मर्यादा आहेत.','हा प्रस्ताव परिपूर्ण आहे, मर्यादा नाहीत.','प्रस्ताव प्रभावी म्हणून मर्यादा अस्तित्वात नाहीत.','त्याला काही प्रस्ताव प्रभावी मर्यादा तर आहेत.')]
}

def put(db, model, **fields):
    obj=db.get(model,fields['id'] if 'id' in fields else fields['code'])
    if obj is None:
        db.add(model(**fields))
        db.flush()

def seed():
    with SessionLocal.begin() as db:
        raw=json.loads(DATA.read_text(encoding='utf-8'))
        for code in ('student','admin'): put(db,Role,code=code,label=code.title())
        for code, info in LANGS.items(): put(db,Language,id='lang-'+code,code=code,tts_locale=LEGACY_LANGUAGE_LOCALES[code],**{**info,'description':NATIVE_DESCRIPTIONS.get(code,info['description'])})
        for level in raw['levels']: put(db,Level,**level)
        for code in LANGS:
            for level in raw['levels']:
                ci='course-'+code+'-'+level['code'].lower()
                mi='module-'+code+'-'+level['code'].lower()
                put(db,Course,id=ci,language_id='lang-'+code,level_id=level['id'],title=f"{LANGS[code]['native_name']} — {level['code']}",description=NATIVE_CATALOG[code][0].format(band=level['code']))
                put(db,Module,id=mi,course_id=ci,title=NATIVE_CATALOG[code][1],sort_order=1)
        for l in raw['lessons']:
            if l['language_id'] not in ('lang-en','lang-hi'):continue
            payload={k:v for k,v in l.items() if k not in ('quiz','vocabulary')}
            payload['module_id']='module-'+l['language_id'][5:]+'-a1'
            put(db,Lesson,**payload)
            for v in l.get('vocabulary',[]):put(db,Vocabulary,lesson_id=l['id'],**v)
            for q in l.get('quiz',[]):
                put(db,Question,id=q['id'],lesson_id=l['id'],question_text=q['question_text'],explanation=q.get('explanation',''))
                for o in q['options']:
                    # Legacy Hindi q-hi-3-5 reused IDs from q-hi-3-3. Keep the
                    # earlier IDs intact; add stable noncolliding IDs for this
                    # question rather than moving/overwriting historical answers.
                    prior=db.get(Option,o['id'])
                    ident=o['id'] if prior is None or prior.question_id==q['id'] else f"{o['id']}-{q['id']}"
                    put(db,Option,question_id=q['id'],**{**o,'id':ident})
        for code,entries in CURRICULUM.items():
            for i,(lvl,title,phrase,example,grammar,correct,wrong1,wrong2,wrong3) in enumerate(entries):
                idx=sum(1 for e in entries[:i] if e[0]==lvl)+1
                lid=f'les-{code}-{lvl.lower()}-{idx}'
                put(db,Lesson,id=lid,module_id=f'module-{code}-{lvl.lower()}',language_id=f'lang-{code}',level_id=f'lvl-{lvl.lower()}',title=title,description=f'Use {LANGS[code]["name"]} in realistic situations: {title}.',content=f'### {title}\nRead this model expression aloud:\n\n**{phrase}**\n\nIdentify word order, politeness and grammatical agreement. Practise saying the full sentence and comparing it to the alternatives.',grammar_notes=grammar,objectives=[f'Understand: {phrase}','Recognise appropriate sentence structure','Apply the grammar point in conversation'],duration_minutes=12,lesson_order=idx)
                for j,(word,translation) in enumerate(((phrase,BASE_MEANINGS[code][i]),BASE_LEXEMES[code][i])):
                    put(db,Vocabulary,id=f'v-{lid}-{j}',lesson_id=lid,word=word,translation=translation,example_sentence=example,example_translation=BASE_MEANINGS[code][i])
                options=[correct,wrong1,wrong2,wrong3]
                qid='q-'+lid
                put(db,Question,id=qid,lesson_id=lid,question_text=f'Choose the correctly formed sentence for: {title}',explanation=f'Correct structure: {grammar}')
                for j,v in enumerate(options):put(db,Option,id=f'o-{qid}-{j}',question_id=qid,option_text=v,is_correct=(j==0))
                # Three additional interactive, server-graded exercise types.
                for typ,answer,meta in [('fill_blank',correct.split(' ')[0],{'prompt':'_____ '+' '.join(correct.split(' ')[1:])}),('matching','1:1',{'pairs':[['1',phrase],['2',title]]}),('arrangement',correct,{'tokens':correct.split(' ')})]:
                    put(db,Question,id=f'{qid}-{typ}',lesson_id=lid,question_type=typ,question_text={'fill_blank':'Complete the model sentence','matching':'Match the numbered items with their meaning','arrangement':'Arrange the words into the correct sentence'}[typ],answer_text=answer,meta=meta,explanation=grammar)
        # Expanded authored units: add only missing records; never overwrite admin edits or student data.
        for lang, levels in UNITS.items():
            for band, units in levels.items():
                # Existing seeded items occupy order 1; extension begins at 2.
                for n,(title,phrase,grammar,gloss) in enumerate(units,start=2 if band!='A1' else 6):
                    slug=f'les-{lang}-{band.lower()}-extension-{n}'
                    tokens=phrase.strip().split()
                    first=tokens[0]
                    ix=n-(6 if band=='A1' else 2)
                    wrong=extension_alternatives(lang,band,ix)
                    put(db,Lesson,id=slug,module_id=f'module-{lang}-{band.lower()}',language_id=f'lang-{lang}',level_id=f'lvl-{band.lower()}',
                        title=title,description=f'Contextual practice: {title}',
                        content=f'## {title}\n\n**Model expression:** {phrase}\n\n**Usage:** {grammar}\n\nRead the expression aloud, notice the word order and practise adapting it to your own situation.',
                        grammar_notes=grammar,objectives=[f'Understand the expression: {phrase}','Explain the grammar pattern','Use the expression in a short conversation'],
                        duration_minutes=15,lesson_order=n)
                    word,english,hindi=gloss.split(' | ')
                    for j,(w,t) in enumerate(((word,english+ ' / '+hindi),(phrase,extension_meaning(lang,band,ix,phrase)),EXTENSION_WORDS[lang][band][ix])):
                        put(db,Vocabulary,id=f'v-{slug}-{j}',lesson_id=slug,word=w,translation=t,example_sentence=phrase,example_translation=title)
                    qid='q-'+slug
                    put(db,Question,id=qid,lesson_id=slug,question_type='mcq',question_text=f'{EXTENSION_PROMPT[lang]} {title}',explanation=grammar)
                    for j,op_text in enumerate([phrase,*wrong]):
                        put(db,Option,id=f'o-{qid}-{j}',question_id=qid,option_text=op_text,is_correct=j==0)
                    for kind,text,answer,meta in (
                        ('fill_blank','Fill in the missing first word',first,{'prompt':'_____ '+' '.join(tokens[1:])}),
                        ('matching','Match each expression with its meaning',None,{'pairs':[[word,english],[phrase,title]]}),
                        ('arrangement','Rearrange the sentence into its original order',phrase,{'tokens':tokens}),
                    ):
                        put(db,Question,id=f'{qid}-{kind}',lesson_id=slug,question_type=kind,question_text=text,answer_text=answer,meta=meta,explanation=grammar)
        # Balanced starter curricula: 3 authored units in every CEFR band for each new language.
        # Existing language content and learner progress are not overwritten.
        for code, bands in ADDITIONAL_CURRICULA.items():
            for band, units in bands.items():
                for order, (title, phrase, meaning, grammar, vocab_word, vocab_meaning) in enumerate(units, start=1):
                    lesson_id = f"les-{code}-{band.lower()}-balanced-{order}"
                    native_title, native_description, content = balanced_native_fields(code, band, order-1)
                    put(db, Lesson, id=lesson_id, module_id=f"module-{code}-{band.lower()}",
                        language_id=f"lang-{code}", level_id=f"lvl-{band.lower()}", title=native_title,
                        description=native_description,
                        content=content, grammar_notes=grammar,
                        objectives=balanced_objectives(code,meaning),
                        duration_minutes=15, lesson_order=order, is_published=True)
                    extra_word, extra_meaning = EXTRA_WORDS[code][band][order-1]
                    vocabulary = [
                        (vocab_word, vocab_meaning, phrase),
                        (phrase, meaning, phrase),
                        (extra_word, extra_meaning, phrase),
                    ]
                    for v_index, (word, translation, example) in enumerate(vocabulary, start=1):
                        put(db, Vocabulary, id=f"v-{lesson_id}-{v_index}", lesson_id=lesson_id,
                            word=word, translation=translation, example_sentence=example,
                            example_translation=meaning)

                    question_id = f"q-{lesson_id}"
                    tokens = phrase.split()
                    wrong_options = alternatives(code, band, order-1)
                    put(db, Question, id=question_id, lesson_id=lesson_id, question_type="mcq",
                        question_text=f"{PROMPTS[code][0]} {meaning}",
                        explanation=grammar)
                    for option_index, option_text in enumerate([phrase, *wrong_options]):
                        put(db, Option, id=f"o-{question_id}-{option_index}", question_id=question_id,
                            option_text=option_text, is_correct=(option_index == 0))

                    exercises = [
                        ("fill_blank", PROMPTS[code][1], tokens[0], {"prompt": "_____ " + " ".join(tokens[1:])}),
                        ("matching", PROMPTS[code][2], None, {"pairs": [[phrase, meaning], [vocab_word, vocab_meaning]]}),
                        ("arrangement", PROMPTS[code][3], phrase, {"tokens": tokens}),
                    ]
                    for kind, prompt, answer, meta in exercises:
                        put(db, Question, id=f"{question_id}-{kind}", lesson_id=lesson_id,
                            question_type=kind, question_text=prompt, answer_text=answer,
                            meta=meta, explanation=grammar)

        repair_previous_seed(db)  # Only unchanged generated seed fields; preserves admin edits and learner attempts.
        repair_extension_seed(db)
        repair_base_seed(db,CURRICULUM)
        repair_catalogue(db,LANGS)
        repair_reviewed_phrases(db)
        for code,title,desc,threshold in [('first_quiz','First Steps','Complete your first quiz',1),('five_quizzes','Getting Started','Complete five quizzes',5),('twenty_quizzes','Dedicated Learner','Complete twenty quizzes',20)]:
            put(db,Achievement,code=code,title=title,description=desc,threshold=threshold)

def info_title(code,level): return f'{LANGS[code]["name"]} — {level}'
if __name__=='__main__':
    seed();print('Seed completed without overwriting existing records')

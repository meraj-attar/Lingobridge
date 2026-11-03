"""Reviewed seed-level fixes, with guarded updates for installations seeded earlier.

Never rewrite administrator edits or student assessments. No deletions or resets.
The English meanings remain intentionally bilingual learning aids.
"""
from sqlalchemy import select, update
from .additional_curriculum import CURRICULA
from . import models as m

# An additional *attested word in the actual lesson example*, not an unrelated
# grammar note. Indexed by language, CEFR band, and the three published units.
EXTRA_WORDS = {
 'gu': {
  'A1': [('નામ','name'),('મારી','my (feminine)'),('જોઈએ','needed / wanted')],
  'A2': [('સવારે','in the morning'),('ગઈકાલે','yesterday'),('કાલે','tomorrow')],
  'B1': [('થોડો','a little'),('વરસાદ','rain'),('શીખી','learning')],
  'B2': [('યોગ્ય','appropriate / valid'),('સમય','time'),('સુધારો','improvement')],
  'C1': [('દલીલ','argument'),('અસર','impact'),('બંને','both')],
  'C2': [('નિષ્કર્ષ','conclusion'),('ચિંતાઓને','concerns'),('મર્યાદાઓ','limitations')]},
 'bn': {
  'A1': [('নাম','name'),('আমার','my'),('চাই','want / need')],
  'A2': [('সকালে','in the morning'),('গতকাল','yesterday'),('আগামীকাল','tomorrow')],
  'B1': [('উচিত','should'),('বৃষ্টি','rain'),('শিখছি','I am learning')],
  'B2': [('বক্তব্য','statement / point'),('সময়','time'),('উন্নতি','improvement')],
  'C1': [('যুক্তিটি','the argument'),('প্রভাব','impact'),('দুটি','two')],
  'C2': [('পরিধি','scope'),('উদ্বেগ','concern'),('সীমাবদ্ধতাগুলি','the limitations')]},
 'ta': {
  'A1': [('பெயர்','name'),('என்','my'),('வேண்டும்','want / need')],
  'A2': [('காலையில்','in the morning'),('நேற்று','yesterday'),('நாளை','tomorrow')],
  'B1': [('பயிற்சி','practice'),('மழை','rain'),('தமிழ்','Tamil')],
  'B2': [('கருத்து','opinion'),('நேரம்','time'),('அறிக்கை','report')],
  'C1': [('வாதம்','argument'),('தாக்கத்தை','impact'),('இரு','two')],
  'C2': [('முடிவு','conclusion'),('கவலைகளைப்','concerns'),('கண்ணோட்டம்','perspective')]},
 'te': {
  'A1': [('పేరు','name'),('నా','my'),('కావాలి','want / need')],
  'A2': [('ఉదయం','morning'),('నిన్న','yesterday'),('రేపు','tomorrow')],
  'B1': [('సాధన','practice'),('వర్షం','rain'),('తెలుగు','Telugu')],
  'B2': [('అభిప్రాయం','opinion'),('సమయం','time'),('నివేదిక','report')],
  'C1': [('వాదన','argument'),('ప్రభావాన్ని','impact'),('రెండు','two')],
  'C2': [('నిర్ణయం','conclusion / decision'),('ఆందోళనలను','concerns'),('పరిమితులను','limitations')]},
 'kn': {
  'A1': [('ಹೆಸರು','name'),('ನನ್ನ','my'),('ಬೇಕು','want / need')],
  'A2': [('ಬೆಳಿಗ್ಗೆ','in the morning'),('ನಿನ್ನೆ','yesterday'),('ನಾಳೆ','tomorrow')],
  'B1': [('ಅಭ್ಯಾಸ','practice'),('ಮಳೆ','rain'),('ಕನ್ನಡ','Kannada')],
  'B2': [('ಅಭಿಪ್ರಾಯ','opinion'),('ಸಮಯವಿದ್ದರೆ','if there were time'),('ವರದಿಯು','the report')],
  'C1': [('ವಾದವು','the argument'),('ಪರಿಣಾಮವನ್ನು','impact'),('ವಿಧಾನಗಳು','approaches')],
  'C2': [('ತೀರ್ಮಾನ','conclusion'),('ಕಳವಳಗಳನ್ನು','concerns'),('ಮಿತಿಗಳನ್ನು','limitations')]},
 'ur': {
  'A1': [('نام','name'),('بہن','sister'),('پانی','water')],
  'A2': [('صبح','morning'),('بازار','market'),('سفر','journey / travel')],
  'B1': [('مشق','practice'),('بارش','rain'),('سیکھ','learn')],
  'B2': [('رائے','opinion'),('وقت','time'),('رپورٹ','report')],
  'C1': [('دلیل','argument'),('اثرات','effects / impact'),('دونوں','both')],
  'C2': [('نتیجہ','conclusion'),('خدشات','concerns'),('حدود','limitations')]},
 'es': {
  'A1': [('llamo','I am called'),('hermana','sister'),('favor','favor')],
  'A2': [('mañana','morning / tomorrow'),('mercado','market'),('viajar','to travel')],
  'B1': [('practicar','to practise'),('lloviendo','raining'),('aprendiendo','learning')],
  'B2': [('punto','point'),('tiempo','time'),('informe','report')],
  'C1': [('argumento','argument'),('propuesta','proposal'),('enfoques','approaches')],
  'C2': [('alcance','scope'),('comité','committee'),('limitaciones','limitations')]}
}

PROMPTS = {
 'gu': ('આ અંગ્રેજી અર્થ માટે યોગ્ય ગુજરાતી વાક્ય પસંદ કરો:', 'ખાલી જગ્યા ભરો', 'વાક્યોને તેમના અર્થ સાથે જોડો', 'શબ્દોને સાચા ક્રમમાં ગોઠવો'),
 'bn': ('এই ইংরেজি অর্থের জন্য সঠিক বাংলা বাক্যটি বেছে নিন:', 'শূন্যস্থান পূরণ করুন', 'বাক্যের সঙ্গে অর্থ মেলান', 'শব্দগুলো সঠিক ক্রমে সাজান'),
 'ta': ('இந்த ஆங்கிலப் பொருளுக்கு ஏற்ற தமிழ்ச் சொற்றொடரைத் தேர்ந்தெடுக்கவும்:', 'விடுபட்ட சொல்லை நிரப்பவும்', 'சொற்றொடர்களைப் பொருளுடன் பொருத்தவும்', 'சொற்களைச் சரியான வரிசையில் அமைக்கவும்'),
 'te': ('ఈ ఆంగ్ల అర్థానికి సరైన తెలుగు వాక్యాన్ని ఎంచుకోండి:', 'ఖాళీని పూరించండి', 'వాక్యాలను వాటి అర్థాలతో జతచేయండి', 'పదాలను సరైన క్రమంలో అమర్చండి'),
 'kn': ('ಈ ಇಂಗ್ಲಿಷ್ ಅರ್ಥಕ್ಕೆ ಸರಿಯಾದ ಕನ್ನಡ ವಾಕ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ:', 'ಖಾಲಿ ಜಾಗವನ್ನು ತುಂಬಿರಿ', 'ವಾಕ್ಯಗಳನ್ನು ಅವುಗಳ ಅರ್ಥಗಳೊಂದಿಗೆ ಹೊಂದಿಸಿ', 'ಪದಗಳನ್ನು ಸರಿಯಾದ ಕ್ರಮದಲ್ಲಿ ಜೋಡಿಸಿ'),
 'ur': ('اس انگریزی معنی کے لیے درست اردو جملہ منتخب کریں:', 'خالی جگہ پُر کریں', 'جملوں کو ان کے معنی سے ملائیں', 'الفاظ کو درست ترتیب میں لگائیں'),
 'es': ('Elige la oración en español que corresponda a este significado en inglés:', 'Completa el espacio en blanco', 'Relaciona las expresiones con su significado', 'Ordena las palabras correctamente'),
}


def alternatives(code, band, i):
    """Three different grammatical sentences from the same authored curriculum.

    No artificial word reversal, whitespace-only or fabricated grammar errors.
    """
    rows=CURRICULA[code][band]
    others=[row[1] for j,row in enumerate(rows) if j!=i]
    next_band=list(CURRICULA[code])[ (list(CURRICULA[code]).index(band)+1) % len(CURRICULA[code]) ]
    others.append(CURRICULA[code][next_band][i][1])
    return others


def repair_previous_seed(db):
    """Compare-and-swap updates to unchanged seed records only.

    Options are left alone if a learner has already attempted that lesson,
    preserving the interpretation of recorded responses. Admin edits win.
    Returns counts for visibility in the CLI and tests.
    """
    counts={'vocabulary':0,'questions':0,'options':0,'skipped_attempted':0}
    for code,bands in CURRICULA.items():
        for band, units in bands.items():
            for idx,(title,phrase,meaning,grammar,word,gloss) in enumerate(units):
                lid=f'les-{code}-{band.lower()}-balanced-{idx+1}'
                vocab_id=f'v-{lid}-3'
                extra_word,extra_meaning=EXTRA_WORDS[code][band][idx]
                # Guard by old field values. No changes to admin-updated fields.
                old=db.get(m.Vocabulary,vocab_id)
                if old and old.word==grammar and old.translation=='Grammar focus':
                    old.word=extra_word
                    old.translation=extra_meaning
                    counts['vocabulary']+=1
                qid=f'q-{lid}'
                quiz=db.get(m.Question,qid)
                if quiz and quiz.question_text==f'Which expression means: {meaning}':
                    quiz.question_text=f'{PROMPTS[code][0]} {meaning}'
                    counts['questions']+=1
                for kind,old_prompt,new_prompt in (
                    ('fill_blank','Complete the expression',PROMPTS[code][1]),
                    ('matching','Match the expression with its meaning',PROMPTS[code][2]),
                    ('arrangement','Arrange the words into the original expression',PROMPTS[code][3])):
                    q=db.get(m.Question,f'{qid}-{kind}')
                    if q and q.question_text==old_prompt:
                        q.question_text=new_prompt
                        counts['questions']+=1
                attempted=db.scalar(select(m.QuizAttempt.id).where(m.QuizAttempt.lesson_id==lid).limit(1))
                if attempted:
                    counts['skipped_attempted']+=1
                    continue
                tokens=phrase.split()
                old_wrong=[' '.join(reversed(tokens)),phrase.replace(' ', '  ', 1),phrase+' '+tokens[0]]
                for j,(before,after) in enumerate(zip(old_wrong,alternatives(code,band,idx)),start=1):
                    option=db.get(m.Option,f'o-{qid}-{j}')
                    if option and option.option_text==before and not option.is_correct:
                        option.option_text=after
                        counts['options']+=1
    return counts


def check_authored_words():
    """Mechanical proof that each added word appears in its target-language sentence."""
    errors=[]
    for code,bands in CURRICULA.items():
        for band,rows in bands.items():
            for index,row in enumerate(rows):
                word,_=EXTRA_WORDS[code][band][index]
                if word not in row[1]:errors.append(f'{code} {band} {index+1}: {word!r} missing')
    return errors

# Original English/Hindi/Marathi extension also used a grammar note as a word
# and a whitespace-only MCQ answer. Use real target-language expressions.
from .curriculum_extension import UNITS
EXTENSION_WORDS={
 'en':{
  'A1':[('name','name'),('Where','question word for a location')],
  'A2':[('grandparents','grandparents'),('tomorrow','the day after today')],
  'B1':[('should','used to give advice'),('lights','lights')],
  'B2':[('differently','in another way'),('students','students')],
  'C1':[('policy','policy'),('public','relating to the public')],
  'C2':[('conclusion','conclusion'),('committee','committee')]},
 'hi':{
  'A1':[('नाम','name'),('कहाँ','where')],
  'A2':[('दादा-दादी','grandparents'),('कल','tomorrow')],
  'B1':[('जाना','to go'),('पढ़','to study / read')],
  'B2':[('समझता','understand'),('विद्यार्थी','students')],
  'C1':[('चिंताओं','concerns'),('बदलाव','change')],
  'C2':[('निष्कर्ष','conclusion'),('समिति','committee')]},
 'mr':{
  'A1':[('नाव','name'),('कुठे','where')],
  'A2':[('आजी-आजोबांना','grandparents'),('उद्या','tomorrow')],
  'B1':[('जावे','should go'),('अभ्यास','study')],
  'B2':[('मुद्दा','point'),('विद्यार्थ्यांना','students')],
  'C1':[('चिंतांनंतरही','despite concerns'),('बदल','change')],
  'C2':[('निष्कर्ष','conclusion'),('समितीने','the committee')]}
}
EXTENSION_MEANINGS={
 'hi':{
  'A1':['Hello, my name is Asha.','Where is the library?'],
  'A2':['I met my grandparents last Sunday.','We are going by train tomorrow.'],
  'B1':['You should visit the museum because it is interesting.','While I was studying, the power went out.'],
  'B2':['I understand your point, but my perspective is different.','The survey suggests that students prefer short lessons.'],
  'C1':['Despite these concerns, the policy needs reassessment.','Overall, the findings indicate a gradual shift in public opinion.'],
  'C2':['This conclusion is reasonable, although its implications are contentious.','It is my duty to acknowledge the committee’s objections.']},
 'mr':{
  'A1':['Hello, my name is Asha.','Where is the library?'],
  'A2':['I visited my grandparents last Sunday.','We are going by train tomorrow.'],
  'B1':['You should visit the museum because it is very interesting.','The power went out while I was studying.'],
  'B2':['I understand your point, but my opinion differs.','The survey suggests that students like short lessons.'],
  'C1':['Despite these concerns, the policy should be considered further.','The findings indicate a gradual change in public opinion.'],
  'C2':['This conclusion is defensible, but its effects remain debatable.','It is necessary to acknowledge the committee’s objections.']},
}
EXTENSION_PROMPT={
 'en':'Choose the expression from the lesson:',
 'hi':'इस पाठ में सिखाया गया वाक्य चुनें:',
 'mr':'या धड्यात शिकवलेले वाक्य निवडा:',
}

def extension_meaning(code,band,index,phrase):
    return phrase if code=='en' else EXTENSION_MEANINGS[code][band][index]

def extension_alternatives(code,band,index):
    levels=list(UNITS[code])
    units=UNITS[code][band]
    following=UNITS[code][levels[(levels.index(band)+1)%len(levels)]]
    return [units[1-index][1],following[0][1],following[1][1]]

def repair_extension_seed(db):
    stats={'vocabulary':0,'options':0,'skipped_attempted':0}
    for code,bands in UNITS.items():
        for band,units in bands.items():
            for idx,(title,phrase,grammar,gloss) in enumerate(units):
                order=(6 if band=='A1' else 2)+idx
                lid=f'les-{code}-{band.lower()}-extension-{order}'
                word,english,hindi=gloss.split(' | ')
                extra,extra_meaning=EXTENSION_WORDS[code][band][idx]
                meaning=extension_meaning(code,band,idx,phrase)
                for j,old_word,old_trans,new_word,new_trans in (
                    (1,phrase,english,phrase,meaning),
                    (2,grammar,'Grammar focus',extra,extra_meaning),
                ):
                    vocab=db.get(m.Vocabulary,f'v-{lid}-{j}')
                    if vocab and vocab.word==old_word and vocab.translation==old_trans:
                        vocab.word=new_word
                        vocab.translation=new_trans
                        stats['vocabulary']+=1
                qid='q-'+lid
                q=db.get(m.Question,qid)
                old_prompt=f'Select the expression with the correct word order for: {title}'
                if q and q.question_text==old_prompt:
                    q.question_text=f'{EXTENSION_PROMPT[code]} {title}'
                if db.scalar(select(m.QuizAttempt.id).where(m.QuizAttempt.lesson_id==lid).limit(1)):
                    stats['skipped_attempted']+=1
                    continue
                tokens=phrase.split()
                old_answers=[' '.join(reversed(tokens)),phrase+' '+tokens[0],phrase.replace(' ', '  ')+tokens[0]]
                for j,(old,new) in enumerate(zip(old_answers,extension_alternatives(code,band,idx)),start=1):
                    option=db.get(m.Option,f'o-{qid}-{j}')
                    if option and option.option_text==old and not option.is_correct:
                        option.option_text=new
                        stats['options']+=1
    return stats


def check_extension_words():
    return [(code,band,i,word) for code,bands in UNITS.items() for band,rows in bands.items()
            for i,row in enumerate(rows) for word,_ in [EXTENSION_WORDS[code][band][i]] if word not in row[1]]

# Catalog copy is native-language text; CEFR band codes remain international.
NATIVE_CATALOG={
 'en':('Learn vocabulary, grammar and conversation at {band} level.','Core lessons'),
 'hi':('{band} स्तर पर हिन्दी शब्दावली, व्याकरण और संवाद सीखें।','मुख्य पाठ'),
 'mr':('{band} स्तरावर मराठी शब्दसंग्रह, व्याकरण आणि संवाद शिका.','मुख्य धडे'),
 'gu':('{band} સ્તરે ગુજરાતી શબ્દભંડોળ, વ્યાકરણ અને સંવાદ શીખો.','મુખ્ય પાઠ'),
 'bn':('{band} স্তরে বাংলা শব্দভান্ডার, ব্যাকরণ ও কথোপকথন শিখুন।','মূল পাঠ'),
 'ta':('{band} நிலையில் தமிழ் சொற்கள், இலக்கணம் மற்றும் உரையாடலைக் கற்றுக்கொள்ளுங்கள்.','முக்கிய பாடங்கள்'),
 'te':('{band} స్థాయిలో తెలుగు పదజాలం, వ్యాకరణం, సంభాషణ నేర్చుకోండి.','ప్రధాన పాఠాలు'),
 'kn':('{band} ಹಂತದಲ್ಲಿ ಕನ್ನಡ ಪದಸಂಪತ್ತು, ವ್ಯಾಕರಣ ಮತ್ತು ಸಂಭಾಷಣೆ ಕಲಿಯಿರಿ.','ಮುಖ್ಯ ಪಾಠಗಳು'),
 'ur':('{band} سطح پر اردو الفاظ، قواعد اور گفتگو سیکھیے۔','اہم اسباق'),
 'es':('Aprende vocabulario, gramática y conversación en español en el nivel {band}.','Lecciones principales'),
}

LESSON_TITLES={
 'gu':('અભિવાદન અને પરિચય','કુટુંબ','ભોજન અને વિનંતીઓ','દૈનિક દિનચર્યા','ગઈકાલની વાત','આયોજન','સલાહ આપવી','કારણ સમજાવવું','અનુભવ વર્ણવવો','વિનમ્ર અસહમતિ','કાલ્પનિક પરિસ્થિતિઓ','માહિતી રજૂ કરવી','પુરાવાનું મૂલ્યાંકન','ઔપચારિક ભલામણ','વિચારોનું સંકલન','સૂક્ષ્મ સ્પષ્ટીકરણ','રાજદ્વારી જવાબ','સુવ્યવસ્થિત દલીલ'),
 'bn':('অভিবাদন ও পরিচয়','পরিবার','খাবার ও অনুরোধ','দৈনন্দিন রুটিন','গতকালের ঘটনা','পরিকল্পনা করা','পরামর্শ দেওয়া','কারণ ব্যাখ্যা করা','অভিজ্ঞতা বর্ণনা করা','বিনীত দ্বিমত','কাল্পনিক পরিস্থিতি','তথ্য উপস্থাপন','প্রমাণ মূল্যায়ন','আনুষ্ঠানিক সুপারিশ','ধারণার সমন্বয়','সূক্ষ্ম শর্ত','কূটনৈতিক জবাব','পরিশীলিত যুক্তি'),
 'ta':('வாழ்த்துகளும் அறிமுகமும்','குடும்பம்','உணவும் கோரிக்கைகளும்','தினசரி வழக்கம்','நேற்றைய நிகழ்வுகள்','திட்டமிடுதல்','ஆலோசனை வழங்குதல்','காரணம் விளக்குதல்','அனுபவத்தை விவரித்தல்','மரியாதையான கருத்து வேறுபாடு','கற்பனைச் சூழல்கள்','தகவல் வழங்குதல்','ஆதாரங்களை மதிப்பிடுதல்','முறையான பரிந்துரை','கருத்துகளை ஒருங்கிணைத்தல்','நுணுக்கமான விளக்கம்','பண்பான பதில்','செம்மையான வாதம்'),
 'te':('శుభాకాంక్షలు మరియు పరిచయాలు','కుటుంబం','ఆహారం మరియు అభ్యర్థనలు','దైనందిన జీవితం','నిన్నటి సంఘటనలు','ప్రణాళికలు రూపొందించడం','సలహా ఇవ్వడం','కారణాన్ని వివరించడం','అనుభవాన్ని వివరించడం','మర్యాదపూర్వక విభేదం','ఊహాజనిత పరిస్థితులు','సమాచారాన్ని తెలియజేయడం','ఆధారాలను విశ్లేషించడం','అధికారిక సిఫార్సు','ఆలోచనల సమన్వయం','సూక్ష్మ వివరణ','దౌత్యపూర్వక సమాధానం','సమగ్ర వాదన'),
 'kn':('ಶುಭಾಶಯಗಳು ಮತ್ತು ಪರಿಚಯಗಳು','ಕುಟುಂಬ','ಆಹಾರ ಮತ್ತು ವಿನಂತಿಗಳು','ದಿನಚರಿ','ನಿನ್ನೆಯ ಘಟನೆಗಳು','ಯೋಜನೆ ರೂಪಿಸುವುದು','ಸಲಹೆ ನೀಡುವುದು','ಕಾರಣ ವಿವರಿಸುವುದು','ಅನುಭವ ವಿವರಿಸುವುದು','ವಿನಯಪೂರ್ವಕ ಭಿನ್ನಾಭಿಪ್ರಾಯ','ಕಾಲ್ಪನಿಕ ಪರಿಸ್ಥಿತಿಗಳು','ಮಾಹಿತಿ ನೀಡುವುದು','ಸಾಕ್ಷ್ಯ ಮೌಲ್ಯಮಾಪನ','ಔಪಚಾರಿಕ ಶಿಫಾರಸು','ವಿಚಾರಗಳ ಸಂಯೋಜನೆ','ಸೂಕ್ಷ್ಮ ಸ್ಪಷ್ಟೀಕರಣ','ರಾಜತಾಂತ್ರಿಕ ಪ್ರತಿಕ್ರಿಯೆ','ಪರಿಷ್ಕೃತ ವಾದ'),
 'ur':('سلام دعا اور تعارف','خاندان','کھانا اور درخواستیں','روزمرہ معمولات','کل کے واقعات','منصوبہ بندی','مشورہ دینا','وجہ بیان کرنا','تجربہ بیان کرنا','شائستہ اختلاف','فرضی صورتِ حال','معلومات بیان کرنا','شواہد کا جائزہ','رسمی سفارش','خیالات کا امتزاج','باریک نکتہ','سفارتی جواب','مدلل استدلال'),
 'es':('Saludos y presentaciones','La familia','Comida y peticiones','Rutina diaria','Ayer','Planes futuros','Dar consejos','Explicar las causas','Describir experiencias','Discrepar con respeto','Situaciones hipotéticas','Comunicar información','Evaluar pruebas','Recomendaciones formales','Sintetizar ideas','Matizar afirmaciones','Respuesta diplomática','Argumentación precisa'),
}
# Localized field labels with intentional English reference meanings and grammar
# notes; teacher explanations are bilingual rather than mislabelled as translation.
LESSON_LABELS={
 'gu':('ગુજરાતી વાક્ય','અંગ્રેજી અર્થ','વ્યાકરણનો નિયમ','વાક્યને મોટેથી વાંચો અને તમારા જીવનનું ઉદાહરણ બનાવો.'),
 'bn':('বাংলা বাক্য','ইংরেজি অর্থ','ব্যাকরণের নিয়ম','বাক্যটি জোরে পড়ুন এবং নিজের উদাহরণ তৈরি করুন।'),
 'ta':('தமிழ் வாக்கியம்','ஆங்கிலப் பொருள்','இலக்கணக் குறிப்பு','வாக்கியத்தை உரக்கப் படித்து உங்கள் சொந்த எடுத்துக்காட்டை உருவாக்குங்கள்.'),
 'te':('తెలుగు వాక్యం','ఆంగ్ల అర్థం','వ్యాకరణ సూచన','వాక్యాన్ని బిగ్గరగా చదివి మీ సొంత ఉదాహరణను రూపొందించండి.'),
 'kn':('ಕನ್ನಡ ವಾಕ್ಯ','ಇಂಗ್ಲಿಷ್ ಅರ್ಥ','ವ್ಯಾಕರಣ ಸೂಚನೆ','ವಾಕ್ಯವನ್ನು ಗಟ್ಟಿಯಾಗಿ ಓದಿ ನಿಮ್ಮದೇ ಉದಾಹರಣೆಯನ್ನು ರಚಿಸಿ.'),
 'ur':('اردو جملہ','انگریزی معنی','گرامر کا اصول','جملہ بلند آواز سے پڑھیں اور اپنی مثال بنائیں۔'),
 'es':('Oración en español','Significado en inglés','Nota gramatical','Lee la oración en voz alta y crea tu propio ejemplo.'),
}

def balanced_native_fields(code,band,index):
    title,phrase,meaning,grammar,*_=CURRICULA[code][band][index]
    native=LESSON_TITLES[code][(list(CURRICULA[code]).index(band)*3)+index]
    label_example,label_meaning,label_grammar,practice=LESSON_LABELS[code]
    content=(f'## {native}\n\n**{label_example}:** {phrase}\n\n'
             f'**{label_meaning}:** {meaning}\n\n**{label_grammar}:** {grammar}\n\n{practice}')
    return native,f'{native} — {meaning}',content


def repair_catalogue(db,langs):
    """Only update unchanged originally seeded course/module/language copy."""
    counts={'courses':0,'modules':0,'lessons':0}
    for code,info in langs.items():
        language=db.get(m.Language,'lang-'+code)
        if language and language.description==info['description'] and code in NATIVE_DESCRIPTIONS:
            language.description=NATIVE_DESCRIPTIONS[code]
        for band in ('A1','A2','B1','B2','C1','C2'):
            course=db.get(m.Course,f'course-{code}-{band.lower()}')
            module=db.get(m.Module,f'module-{code}-{band.lower()}')
            native_name=info['native_name']
            if course:
                old_title=f"{info['name']} — {dict(A1='Beginner',A2='Elementary',B1='Intermediate',B2='Upper Intermediate',C1='Advanced',C2='Mastery').get(band,band)}"
                # Level name comes from the DB; guard against custom renaming.
                lvl=db.get(m.Level,f'lvl-{band.lower()}')
                if lvl:old_title=f"{info['name']} — {lvl.name}"
                old_desc=f"{lvl.name} {info['name']} course" if lvl else None
                if course.title==old_title:
                    course.title=f'{native_name} — {band}'
                    counts['courses']+=1
                if old_desc and course.description==old_desc:
                    course.description=NATIVE_CATALOG[code][0].format(band=band)
            if module:
                lvl=db.get(m.Level,f'lvl-{band.lower()}')
                if lvl and module.title==f'{lvl.name} foundations':
                    module.title=NATIVE_CATALOG[code][1]
                    counts['modules']+=1
    for code,bands in CURRICULA.items():
        for band,units in bands.items():
            for index,(old_title,phrase,meaning,grammar,*_) in enumerate(units):
                lid=f'les-{code}-{band.lower()}-balanced-{index+1}'
                obj=db.get(m.Lesson,lid)
                if not obj:continue
                native,description,content=balanced_native_fields(code,band,index)
                if obj.title==old_title:
                    obj.title=native
                    counts['lessons']+=1
                old_description=f'{old_title}: practise {langs[code]["name"]} in a practical context.'
                if obj.description==old_description:obj.description=description
                old_content=(f'## {old_title}\n\n**Target-language example:** {phrase}\n\n'
                            f'**English meaning:** {meaning}\n\n**Usage note:** {grammar}\n\n'
                            'Read the example aloud, identify the key structure, and adapt it to a similar real-life situation.')
                if obj.content==old_content:obj.content=content
                old_objectives=[f'Understand: {meaning}',f'Recognise: {grammar}','Use the expression in a short conversation']
                if obj.objectives==old_objectives:obj.objectives=balanced_objectives(code,meaning)
    return counts

# Specific reviewed grammatical correction. Only seeded rows without student
# attempts are adjusted, including question meta and recorded sentence text.
# This avoids changing the historical meaning of submitted assessment answers.
SEED_PHRASE_CORRECTIONS={
    'gu':('તમારો મુદ્દો યોગ્ય છે, પરંતુ હું થોડું અલગ વિચારો છું.',
          'તમારો મુદ્દો યોગ્ય છે, પરંતુ હું થોડું અલગ વિચારું છું.'),
}

def repair_reviewed_phrases(db):
    stats={'corrected':0,'skipped_attempts':0}
    for code,(old,new) in SEED_PHRASE_CORRECTIONS.items():
        # Only the known generated units use this phrase.
        owned=f'les-{code}-b2-balanced-1'
        # Other seeded questions may cite the phrase as a distractor.
        affected=[owned,f'les-{code}-b1-balanced-1']
        for lesson_id in affected:
            if db.scalar(select(m.QuizAttempt.id).where(m.QuizAttempt.lesson_id==lesson_id).limit(1)):
                stats['skipped_attempts']+=1
                continue
            lesson=db.get(m.Lesson,lesson_id)
            if lesson_id==owned and lesson and old in lesson.content:
                title,_,meaning,grammar,*_=CURRICULA[code]['B2'][0]
                old_english=(f'## {title}\n\n**Target-language example:** {old}\n\n'
                             f'**English meaning:** {meaning}\n\n**Usage note:** {grammar}\n\n'
                             'Read the example aloud, identify the key structure, and adapt it to a similar real-life situation.')
                native,desc,new_body=balanced_native_fields(code,'B2',0)
                old_native=new_body.replace(new,old)
                if lesson.content in (old_english,old_native):
                    lesson.content=lesson.content.replace(old,new)
                    stats['corrected']+=1
            for word in db.scalars(select(m.Vocabulary).where(m.Vocabulary.lesson_id==lesson_id)).all():
                if word.word==old:word.word=new;stats['corrected']+=1
                if word.example_sentence==old:word.example_sentence=new;stats['corrected']+=1
            for question in db.scalars(select(m.Question).where(m.Question.lesson_id==lesson_id)).all():
                if question.answer_text==old:question.answer_text=new;stats['corrected']+=1
                if question.meta:
                    meta=__import__('copy').deepcopy(question.meta)
                    if isinstance(meta.get('prompt'),str):meta['prompt']=meta['prompt'].replace(old,new)
                    if 'pairs' in meta:meta['pairs']=[[new if v==old else v for v in pair] for pair in meta['pairs']]
                    if 'tokens' in meta and ' '.join(meta['tokens'])==old:meta['tokens']=new.split()
                    if meta!=question.meta:question.meta=meta;stats['corrected']+=1
                for option in db.scalars(select(m.Option).where(m.Option.question_id==question.id)):
                    if option.option_text==old:option.option_text=new;stats['corrected']+=1
    return stats

NATIVE_DESCRIPTIONS={
 'hi':'देवनागरी लिपि, रोज़मर्रा की बातचीत और हिन्दी व्याकरण सीखें।',
 'mr':'मराठी लिपी, दैनंदिन संभाषण आणि व्याकरण शिका.',
 'gu':'ગુજરાતી લિપિ, રોજિંદો સંવાદ અને વ્યાકરણ શીખો.',
 'bn':'বাংলা লিপি, দৈনন্দিন কথোপকথন ও ব্যাকরণ শিখুন।',
 'ta':'தமிழ் எழுத்து, அன்றாட உரையாடல் மற்றும் இலக்கணத்தைக் கற்றுக்கொள்ளுங்கள்.',
 'te':'తెలుగు లిపి, రోజువారీ సంభాషణలు మరియు వ్యాకరణం నేర్చుకోండి.',
 'kn':'ಕನ್ನಡ ಲಿಪಿ, ದಿನನಿತ್ಯದ ಸಂಭಾಷಣೆ ಮತ್ತು ವ್ಯಾಕರಣ ಕಲಿಯಿರಿ.',
 'ur':'اردو رسم الخط، روزمرہ گفتگو اور قواعد سیکھیے۔',
 'es':'Aprende vocabulario, gramática y conversación en español.',
}
OBJECTIVE_COPY={
 'gu':('આ વાક્યનો અર્થ સમજો:', 'વાક્યની રચના ઓળખો.', 'સંવાદમાં વાક્યનો ઉપયોગ કરો.'),
 'bn':('এই বাক্যের অর্থ বুঝুন:', 'বাক্যের গঠন চিনুন।', 'কথোপকথনে বাক্যটি ব্যবহার করুন।'),
 'ta':('இந்த வாக்கியத்தின் பொருளைப் புரிந்துகொள்ளுங்கள்:', 'வாக்கிய அமைப்பைக் கண்டறியுங்கள்.', 'உரையாடலில் வாக்கியத்தைப் பயன்படுத்துங்கள்.'),
 'te':('ఈ వాక్య అర్థాన్ని తెలుసుకోండి:', 'వాక్య నిర్మాణాన్ని గుర్తించండి.', 'సంభాషణలో వాక్యాన్ని ఉపయోగించండి.'),
 'kn':('ಈ ವಾಕ್ಯದ ಅರ್ಥವನ್ನು ತಿಳಿಯಿರಿ:', 'ವಾಕ್ಯ ರಚನೆಯನ್ನು ಗುರುತಿಸಿ.', 'ಸಂಭಾಷಣೆಯಲ್ಲಿ ವಾಕ್ಯವನ್ನು ಬಳಸಿ.'),
 'ur':('اس جملے کا مطلب سمجھیں:', 'جملے کی ساخت پہچانیں۔', 'گفتگو میں جملہ استعمال کریں۔'),
 'es':('Comprende el significado:', 'Reconoce la estructura de la oración.', 'Utiliza la expresión en una conversación.'),
}

def balanced_objectives(code,meaning):
    a,b,c=OBJECTIVE_COPY[code]
    return [f'{a} {meaning}',b,c]

# Original three-language tiered units: meaningful vocabulary rather than
# a whole grammar note placed in a vocabulary word field.
BASE_LEXEMES={
 'en':[('receipt','receipt'),('learning','learning'),('time','time'),('evidence','evidence'),('proposal','proposal')],
 'hi':[('रसीद','receipt'),('हिंदी','Hindi'),('समय','time'),('प्रमाण','evidence'),('सीमाएँ','limitations')],
 'mr':[('नाव','name'),('बहीण','sister'),('तीन','three'),('पाणी','water'),('स्थानक','station'),
       ('पावती','receipt'),('मराठी','Marathi'),('वेळ','time'),('पुरावे','evidence'),('मर्यादा','limitations')],
}
BASE_MEANINGS={
 'en':['Could I have a receipt, please?','I have been learning English for two years.',
       'If I had more time, I would read more.',
       'Although the evidence is limited, the hypothesis remains plausible.',
       'The proposal is compelling, albeit not without limitations.'],
 'hi':['Please give me a receipt.','I have been learning Hindi for two years.',
       'If I had time, I would read more.',
       'Although the evidence is limited, this idea deserves consideration.',
       'The proposal is compelling, but it has some limitations.'],
 'mr':['Hello, my name is Meera.','This is my sister.','It is three o’clock now.',
       'I want water.','Where is the railway station?','Please give me a receipt.',
       'I have been learning Marathi for two years.','If I had time, I would read more.',
       'Although the evidence is limited, this idea is important.',
       'The proposal is effective, but it has some limitations.'],
}

def repair_base_seed(db,curriculum):
    count=0
    for code,rows in curriculum.items():
        for index,(band,title,phrase,example,grammar,*_) in enumerate(rows):
            order=sum(1 for item in rows[:index] if item[0]==band)+1
            lid=f'les-{code}-{band.lower()}-{order}'
            phrase_v=db.get(m.Vocabulary,f'v-{lid}-0')
            grammar_v=db.get(m.Vocabulary,f'v-{lid}-1')
            meaning=BASE_MEANINGS[code][index]
            word,gloss=BASE_LEXEMES[code][index]
            if phrase_v:
                if phrase_v.word==phrase and phrase_v.translation==title:
                    phrase_v.translation=meaning;count+=1
                if phrase_v.example_sentence==example and phrase_v.example_translation==title:
                    phrase_v.example_translation=meaning;count+=1
            if grammar_v:
                if grammar_v.word==grammar and grammar_v.translation=='Grammar focus':
                    grammar_v.word=word;grammar_v.translation=gloss;count+=1
                if grammar_v.example_sentence==example and grammar_v.example_translation==title:
                    grammar_v.example_translation=meaning;count+=1
    return count

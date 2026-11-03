"""Balanced starter curricula for the seven additional LingoBridge languages.

Each CEFR band has three language-specific units. These are starter teaching
materials and should be reviewed by fluent educators before high-stakes use.
"""
LANGUAGES = {
    'gu': {'name':'Gujarati','native_name':'ગુજરાતી','flag':'🇮🇳','color':'#D97706','description':'Learn Gujarati script, everyday conversation, grammar and practical communication.'},
    'bn': {'name':'Bengali','native_name':'বাংলা','flag':'🇧🇩','color':'#059669','description':'Learn Bengali reading, pronunciation, grammar and everyday communication.'},
    'ta': {'name':'Tamil','native_name':'தமிழ்','flag':'🇮🇳','color':'#7C3AED','description':'Learn Tamil script, spoken expressions, grammar and practical communication.'},
    'te': {'name':'Telugu','native_name':'తెలుగు','flag':'🇮🇳','color':'#0D9488','description':'Learn Telugu script, vocabulary, grammar and everyday conversation.'},
    'kn': {'name':'Kannada','native_name':'ಕನ್ನಡ','flag':'🇮🇳','color':'#2563EB','description':'Learn Kannada script, useful expressions, grammar and conversation.'},
    'ur': {'name':'Urdu','native_name':'اردو','flag':'🇵🇰','color':'#0F766E','description':'Learn Urdu script, vocabulary, grammar and everyday communication.'},
    'es': {'name':'Spanish','native_name':'Español','flag':'🇪🇸','color':'#DC2626','description':'Learn Spanish vocabulary, grammar and communication for everyday and professional settings.'},
}

# Each item: (lesson title, target-language example, English meaning, grammar/usage note, target vocabulary, English gloss)
CURRICULA = {
'gu': {
'A1': [
('Greetings and introductions','નમસ્તે, મારું નામ આશા છે.','Hello, my name is Asha.','Use મારું નામ ... છે to introduce yourself.','નમસ્તે','hello'),
('Family','આ મારી બહેન છે.','This is my sister.','આ means this; મારી agrees with the feminine noun બહેન.','બહેન','sister'),
('Food and requests','મને પાણી જોઈએ છે.','I would like water.','મને ... જોઈએ છે expresses a need or request.','પાણી','water')],
'A2': [
('Daily routine','હું દરરોજ સવારે ચાલવા જાઉં છું.','I go for a walk every morning.','દરરોજ marks a repeated habit; જાઉં છું expresses present habitual action.','દરરોજ','every day'),
('Yesterday','ગઈકાલે અમે બજારમાં ગયા હતા.','Yesterday we went to the market.','ગઈકાલે sets a past-time reference; ગયા હતા describes a completed past action.','બજાર','market'),
('Making plans','અમે આવતી કાલે મુસાફરી કરીશું.','We will travel tomorrow.','કરીશું is a future form used with અમે.','મુસાફરી','journey')],
'B1': [
('Giving advice','તમારે દરરોજ થોડો અભ્યાસ કરવો જોઈએ.','You should study a little every day.','જોઈએ expresses advice or obligation.','અભ્યાસ','study'),
('Explaining a reason','વરસાદ પડતો હતો, તેથી અમે ઘરે રહ્યા.','It was raining, so we stayed home.','તેથી links a reason to its result.','તેથી','therefore'),
('Describing experience','હું ગયા વર્ષથી ગુજરાતી શીખી રહ્યો છું.','I have been learning Gujarati since last year.','થી marks the starting point of an ongoing period.','અનુભવ','experience')],
'B2': [
('Polite disagreement','તમારો મુદ્દો યોગ્ય છે, પરંતુ હું થોડું અલગ વિચારું છું.','Your point is valid, but I think a little differently.','પરંતુ introduces a contrast while keeping a respectful tone.','પરંતુ','however'),
('Hypothetical situations','જો મારી પાસે સમય હોત, તો હું વધુ વાંચત.','If I had time, I would read more.','જો ... તો introduces a hypothetical condition and result.','શક્યતા','possibility'),
('Reporting information','અહેવાલ સૂચવે છે કે પરિસ્થિતિમાં સુધારો થયો છે.','The report suggests that the situation has improved.','સૂચવે છે presents information cautiously rather than as absolute certainty.','અહેવાલ','report')],
'C1': [
('Evaluating evidence','પુરાવા મર્યાદિત હોવા છતાં, આ દલીલ વિચારવા યોગ્ય છે.','Although the evidence is limited, this argument deserves consideration.','હોવા છતાં concedes a limitation before presenting a position.','પુરાવા','evidence'),
('Formal recommendation','આ પ્રસ્તાવનો અમલ કરતાં પહેલાં તેની અસરનું મૂલ્યાંકન કરવું આવશ્યક છે.','It is essential to assess the impact before implementing this proposal.','તાં પહેલાં marks an action that should precede another action.','મૂલ્યાંકન','assessment'),
('Synthesizing ideas','સમગ્ર રીતે જોતા, બંને અભિગમો એકબીજાને પૂરક બને છે.','Taken as a whole, both approaches complement each other.','સમગ્ર રીતે signals a synthesis of multiple points.','અભિગમ','approach')],
'C2': [
('Nuanced qualification','નિષ્કર્ષ તર્કસંગત છે, તેમ છતાં તેના વ્યાપ અંગે ચર્ચા શક્ય છે.','The conclusion is reasonable, although its scope remains open to debate.','તેમ છતાં qualifies a statement without fully rejecting it.','વ્યાપ','scope'),
('Diplomatic response','સમિતિએ વ્યક્ત કરેલી ચિંતાઓને અવગણવી યોગ્ય ગણાશે નહીં.','It would not be appropriate to disregard the concerns raised by the committee.','યોગ્ય ગણાશે નહીં is a measured formal evaluation.','અવગણના','disregard'),
('Refined argument','આ દૃષ્ટિકોણ સ્વીકાર્ય છે, શરતે કે તેની મર્યાદાઓ સ્પષ્ટ કરવામાં આવે.','This perspective is acceptable, provided its limitations are made clear.','શરતે કે introduces a precise condition.','મર્યાદા','limitation')]
},
'bn': {
'A1': [
('Greetings and introductions','নমস্কার, আমার নাম আশা।','Hello, my name is Asha.','আমার নাম ... introduces a speaker by name.','নমস্কার','hello'),
('Family','ইনি আমার বোন।','This is my sister.','ইনি is a respectful demonstrative for a person.','বোন','sister'),
('Food and requests','আমার জল চাই।','I want water.','চাই expresses wanting or needing something.','জল','water')],
'A2': [
('Daily routine','আমি প্রতিদিন সকালে হাঁটতে যাই।','I go for a walk every morning.','প্রতিদিন marks a repeated daily action.','প্রতিদিন','every day'),
('Yesterday','গতকাল আমরা বাজারে গিয়েছিলাম।','Yesterday we went to the market.','গতকাল sets past time; গিয়েছিলাম is a past form.','বাজার','market'),
('Making plans','আমরা আগামীকাল ভ্রমণ করব।','We will travel tomorrow.','করব expresses a future action with আমরা.','ভ্রমণ','travel')],
'B1': [
('Giving advice','তোমার প্রতিদিন একটু অনুশীলন করা উচিত।','You should practise a little every day.','উচিত expresses advice or recommendation.','অনুশীলন','practice'),
('Explaining a reason','বৃষ্টি হচ্ছিল, তাই আমরা বাড়িতে ছিলাম।','It was raining, so we stayed at home.','তাই connects a cause with its result.','তাই','therefore'),
('Describing experience','আমি গত বছর থেকে বাংলা শিখছি।','I have been learning Bengali since last year.','থেকে marks the starting point of an ongoing action.','অভিজ্ঞতা','experience')],
'B2': [
('Polite disagreement','আপনার বক্তব্য ঠিক, তবে আমি একটু ভিন্নভাবে ভাবি।','Your point is valid, but I think a little differently.','তবে introduces a respectful contrast.','তবে','however'),
('Hypothetical situations','আমার সময় থাকলে আমি আরও পড়তাম।','If I had time, I would read more.','থাকলে introduces a condition; পড়তাম expresses a hypothetical result.','সম্ভাবনা','possibility'),
('Reporting information','প্রতিবেদনটি ইঙ্গিত দেয় যে পরিস্থিতির উন্নতি হয়েছে।','The report suggests that the situation has improved.','ইঙ্গিত দেয় reports information cautiously.','প্রতিবেদন','report')],
'C1': [
('Evaluating evidence','প্রমাণ সীমিত হলেও, এই যুক্তিটি বিবেচনার যোগ্য।','Although the evidence is limited, this argument deserves consideration.','হলেও acknowledges a limitation before a contrasting point.','প্রমাণ','evidence'),
('Formal recommendation','এই প্রস্তাব বাস্তবায়নের আগে এর প্রভাব মূল্যায়ন করা জরুরি।','It is essential to assess its impact before implementing this proposal.','আগে marks an action that should happen earlier.','মূল্যায়ন','assessment'),
('Synthesizing ideas','সামগ্রিকভাবে, দুটি পদ্ধতি একে অপরের পরিপূরক।','Overall, the two approaches complement each other.','সামগ্রিকভাবে signals a synthesis or overall assessment.','পদ্ধতি','approach')],
'C2': [
('Nuanced qualification','সিদ্ধান্তটি যুক্তিসঙ্গত, যদিও এর পরিধি নিয়ে বিতর্ক হতে পারে।','The conclusion is reasonable, although its scope may be debated.','যদিও introduces a nuanced qualification.','পরিধি','scope'),
('Diplomatic response','কমিটির উত্থাপিত উদ্বেগ উপেক্ষা করা সমীচীন হবে না।','It would not be appropriate to disregard the concerns raised by the committee.','সমীচীন হবে না expresses a measured formal judgment.','উদ্বেগ','concern'),
('Refined argument','এই দৃষ্টিভঙ্গি গ্রহণযোগ্য, যদি এর সীমাবদ্ধতাগুলি স্পষ্ট করা হয়।','This perspective is acceptable, provided its limitations are made clear.','যদি introduces a precise condition.','সীমাবদ্ধতা','limitation')]
},
'ta': {
'A1': [
('Greetings and introductions','வணக்கம், என் பெயர் ஆஷா.','Hello, my name is Asha.','என் பெயர் ... introduces your name.','வணக்கம்','hello'),
('Family','இவர் என் சகோதரி.','This is my sister.','இவர் is a respectful demonstrative for a person.','சகோதரி','sister'),
('Food and requests','எனக்குத் தண்ணீர் வேண்டும்.','I want water.','வேண்டும் expresses a need or want.','தண்ணீர்','water')],
'A2': [
('Daily routine','நான் தினமும் காலையில் நடக்கச் செல்கிறேன்.','I go for a walk every morning.','தினமும் marks a repeated daily action.','தினமும்','every day'),
('Yesterday','நேற்று நாங்கள் சந்தைக்குச் சென்றோம்.','Yesterday we went to the market.','நேற்று establishes past time; சென்றோம் is a past-tense form.','சந்தை','market'),
('Making plans','நாங்கள் நாளை பயணம் செய்வோம்.','We will travel tomorrow.','செய்வோம் expresses a future action with நாங்கள்.','பயணம்','travel')],
'B1': [
('Giving advice','நீங்கள் தினமும் சிறிது பயிற்சி செய்ய வேண்டும்.','You should practise a little every day.','வேண்டும் expresses advice or obligation.','பயிற்சி','practice'),
('Explaining a reason','மழை பெய்ததால் நாங்கள் வீட்டில் இருந்தோம்.','Because it rained, we stayed at home.','தால் introduces a reason or cause.','காரணம்','reason'),
('Describing experience','நான் கடந்த ஆண்டிலிருந்து தமிழ் கற்று வருகிறேன்.','I have been learning Tamil since last year.','இலிருந்து marks the starting point of a continuing period.','அனுபவம்','experience')],
'B2': [
('Polite disagreement','உங்கள் கருத்து சரிதான், ஆனால் நான் சற்று வேறுபடுகிறேன்.','Your point is valid, but I differ slightly.','ஆனால் introduces a contrast politely.','கருத்து','opinion'),
('Hypothetical situations','எனக்கு நேரம் இருந்தால், நான் இன்னும் படிப்பேன்.','If I had time, I would read more.','இருந்தால் introduces a condition.','சாத்தியம்','possibility'),
('Reporting information','அறிக்கை நிலைமை மேம்பட்டுள்ளதாகக் குறிப்பிடுகிறது.','The report indicates that the situation has improved.','குறிப்பிடுகிறது reports a finding without overstatement.','அறிக்கை','report')],
'C1': [
('Evaluating evidence','ஆதாரம் குறைவாக இருந்தாலும், இந்த வாதம் பரிசீலிக்கத் தகுந்தது.','Although evidence is limited, this argument deserves consideration.','இருந்தாலும் concedes a limitation before a contrasting claim.','ஆதாரம்','evidence'),
('Formal recommendation','இந்தத் திட்டத்தைச் செயல்படுத்தும் முன் அதன் தாக்கத்தை மதிப்பிடுவது அவசியம்.','It is essential to assess the impact before implementing this plan.','முன் marks an action that should precede another.','மதிப்பீடு','assessment'),
('Synthesizing ideas','ஒட்டுமொத்தமாக, இரு அணுகுமுறைகளும் ஒன்றுக்கொன்று துணையாக உள்ளன.','Overall, both approaches complement each other.','ஒட்டுமொத்தமாக signals an overall synthesis.','அணுகுமுறை','approach')],
'C2': [
('Nuanced qualification','இந்த முடிவு நியாயமானது; இருப்பினும் அதன் வரம்பு விவாதத்திற்குரியது.','The conclusion is reasonable; nevertheless, its scope is debatable.','இருப்பினும் introduces a refined qualification.','வரம்பு','scope'),
('Diplomatic response','குழு முன்வைத்த கவலைகளைப் புறக்கணிப்பது பொருத்தமாக இருக்காது.','It would not be appropriate to disregard the concerns raised by the committee.','பொருத்தமாக இருக்காது expresses a measured formal judgment.','கவலை','concern'),
('Refined argument','அதன் வரம்புகள் தெளிவுபடுத்தப்பட்டால் இந்தக் கண்ணோட்டம் ஏற்றுக்கொள்ளத்தக்கது.','This perspective is acceptable provided its limitations are clarified.','ஆல் introduces a condition in this formal construction.','கண்ணோட்டம்','perspective')]
},
'te': {
'A1': [
('Greetings and introductions','నమస్కారం, నా పేరు ఆశ.','Hello, my name is Asha.','నా పేరు ... introduces your name.','నమస్కారం','hello'),
('Family','ఈమె నా సోదరి.','This is my sister.','ఈమె is a feminine demonstrative for a person.','సోదరి','sister'),
('Food and requests','నాకు నీళ్లు కావాలి.','I want water.','కావాలి expresses a want or need.','నీళ్లు','water')],
'A2': [
('Daily routine','నేను ప్రతిరోజూ ఉదయం నడవడానికి వెళ్తాను.','I go for a walk every morning.','ప్రతిరోజూ marks a repeated daily action.','ప్రతిరోజూ','every day'),
('Yesterday','నిన్న మేము మార్కెట్‌కు వెళ్లాము.','Yesterday we went to the market.','నిన్న establishes past time; వెళ్లాము is a past form.','మార్కెట్','market'),
('Making plans','మేము రేపు ప్రయాణం చేస్తాము.','We will travel tomorrow.','చేస్తాము expresses a future action with మేము.','ప్రయాణం','travel')],
'B1': [
('Giving advice','మీరు ప్రతిరోజూ కొద్దిగా సాధన చేయాలి.','You should practise a little every day.','చేయాలి expresses advice or obligation.','సాధన','practice'),
('Explaining a reason','వర్షం పడుతోంది, కాబట్టి మేము ఇంట్లో ఉన్నాము.','It is raining, so we are at home.','కాబట్టి links a cause and its result.','కాబట్టి','therefore'),
('Describing experience','నేను గత సంవత్సరం నుంచి తెలుగు నేర్చుకుంటున్నాను.','I have been learning Telugu since last year.','నుంచి marks the starting point of an ongoing action.','అనుభవం','experience')],
'B2': [
('Polite disagreement','మీ అభిప్రాయం సరైనదే, కానీ నేను కొంచెం భిన్నంగా ఆలోచిస్తున్నాను.','Your point is valid, but I think a little differently.','కానీ introduces a polite contrast.','అభిప్రాయం','opinion'),
('Hypothetical situations','నాకు సమయం ఉంటే, నేను ఇంకా ఎక్కువ చదివేవాడిని.','If I had time, I would read more.','ఉంటే introduces a condition; చదివేవాడిని gives a hypothetical result.','సంభావ్యత','possibility'),
('Reporting information','నివేదిక పరిస్థితి మెరుగుపడిందని సూచిస్తోంది.','The report suggests that the situation has improved.','సూచిస్తోంది presents a reported finding cautiously.','నివేదిక','report')],
'C1': [
('Evaluating evidence','ఆధారాలు పరిమితంగా ఉన్నప్పటికీ, ఈ వాదన పరిశీలనకు అర్హమైనది.','Although evidence is limited, this argument deserves consideration.','ఉన్నప్పటికీ concedes a limitation before the main claim.','ఆధారం','evidence'),
('Formal recommendation','ఈ ప్రతిపాదనను అమలు చేసే ముందు దాని ప్రభావాన్ని అంచనా వేయడం అవసరం.','It is essential to assess the impact before implementing this proposal.','ముందు marks an action that should happen beforehand.','అంచనా','assessment'),
('Synthesizing ideas','మొత్తంగా చూస్తే, ఈ రెండు విధానాలు ఒకదానికొకటి తోడ్పడతాయి.','Overall, these two approaches complement each other.','మొత్తంగా చూస్తే signals a synthesis.','విధానం','approach')],
'C2': [
('Nuanced qualification','ఈ నిర్ణయం సమర్థనీయమే, అయినప్పటికీ దాని పరిధిపై చర్చకు అవకాశం ఉంది.','The conclusion is defensible, although its scope remains open to debate.','అయినప్పటికీ introduces a careful qualification.','పరిధి','scope'),
('Diplomatic response','కమిటీ వ్యక్తం చేసిన ఆందోళనలను విస్మరించడం సముచితం కాదు.','It would not be appropriate to disregard the concerns raised by the committee.','సముచితం కాదు expresses a measured formal judgment.','ఆందోళన','concern'),
('Refined argument','దాని పరిమితులను స్పష్టంగా పేర్కొంటే ఈ దృక్కోణం ఆమోదయోగ్యమే.','This perspective is acceptable if its limitations are stated clearly.','If-clause construction states a precise condition.','దృక్కోణం','perspective')]
},
'kn': {
'A1': [
('Greetings and introductions','ನಮಸ್ಕಾರ, ನನ್ನ ಹೆಸರು ಆಶಾ.','Hello, my name is Asha.','ನನ್ನ ಹೆಸರು ... introduces your name.','ನಮಸ್ಕಾರ','hello'),
('Family','ಇವರು ನನ್ನ ಅಕ್ಕ.','This is my elder sister.','ಇವರು is a respectful demonstrative for a person.','ಅಕ್ಕ','elder sister'),
('Food and requests','ನನಗೆ ನೀರು ಬೇಕು.','I want water.','ಬೇಕು expresses a need or want.','ನೀರು','water')],
'A2': [
('Daily routine','ನಾನು ಪ್ರತಿದಿನ ಬೆಳಿಗ್ಗೆ ನಡೆಯಲು ಹೋಗುತ್ತೇನೆ.','I go for a walk every morning.','ಪ್ರತಿದಿನ marks a repeated daily action.','ಪ್ರತಿದಿನ','every day'),
('Yesterday','ನಿನ್ನೆ ನಾವು ಮಾರುಕಟ್ಟೆಗೆ ಹೋದೆವು.','Yesterday we went to the market.','ನಿನ್ನೆ establishes past time; ಹೋದೆವು is a past form.','ಮಾರುಕಟ್ಟೆ','market'),
('Making plans','ನಾವು ನಾಳೆ ಪ್ರಯಾಣ ಮಾಡುತ್ತೇವೆ.','We will travel tomorrow.','ಮಾಡುತ್ತೇವೆ expresses a future or planned action.','ಪ್ರಯಾಣ','travel')],
'B1': [
('Giving advice','ನೀವು ಪ್ರತಿದಿನ ಸ್ವಲ್ಪ ಅಭ್ಯಾಸ ಮಾಡಬೇಕು.','You should practise a little every day.','ಮಾಡಬೇಕು expresses advice or obligation.','ಅಭ್ಯಾಸ','practice'),
('Explaining a reason','ಮಳೆ ಬರುತ್ತಿತ್ತು, ಆದ್ದರಿಂದ ನಾವು ಮನೆಯಲ್ಲೇ ಇದ್ದೆವು.','It was raining, so we stayed at home.','ಆದ್ದರಿಂದ links a reason to its result.','ಆದ್ದರಿಂದ','therefore'),
('Describing experience','ನಾನು ಕಳೆದ ವರ್ಷದಿಂದ ಕನ್ನಡ ಕಲಿಯುತ್ತಿದ್ದೇನೆ.','I have been learning Kannada since last year.','ದಿಂದ marks the starting point of an ongoing period.','ಅನುಭವ','experience')],
'B2': [
('Polite disagreement','ನಿಮ್ಮ ಅಭಿಪ್ರಾಯ ಸರಿಯಾಗಿದೆ, ಆದರೆ ನಾನು ಸ್ವಲ್ಪ ವಿಭಿನ್ನವಾಗಿ ಯೋಚಿಸುತ್ತೇನೆ.','Your point is valid, but I think a little differently.','ಆದರೆ introduces a respectful contrast.','ಅಭಿಪ್ರಾಯ','opinion'),
('Hypothetical situations','ನನಗೆ ಸಮಯವಿದ್ದರೆ, ನಾನು ಇನ್ನಷ್ಟು ಓದುತ್ತಿದ್ದೆ.','If I had time, I would read more.','ವಿದ್ದರೆ introduces a hypothetical condition.','ಸಾಧ್ಯತೆ','possibility'),
('Reporting information','ವರದಿಯು ಪರಿಸ್ಥಿತಿ ಸುಧಾರಿಸಿದೆ ಎಂದು ಸೂಚಿಸುತ್ತದೆ.','The report suggests that the situation has improved.','ಸೂಚಿಸುತ್ತದೆ reports information cautiously.','ವರದಿ','report')],
'C1': [
('Evaluating evidence','ಪುರಾವೆಗಳು ಸೀಮಿತವಾಗಿದ್ದರೂ, ಈ ವಾದವು ಪರಿಶೀಲನೆಗೆ ಅರ್ಹವಾಗಿದೆ.','Although evidence is limited, this argument deserves consideration.','ಆಗಿದ್ದರೂ acknowledges a limitation before the main claim.','ಪುರಾವೆ','evidence'),
('Formal recommendation','ಈ ಪ್ರಸ್ತಾವನೆಯನ್ನು ಜಾರಿಗೆ ತರುವ ಮೊದಲು ಅದರ ಪರಿಣಾಮವನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಬೇಕು.','The impact should be assessed before implementing this proposal.','ಮೊದಲು marks an action that should precede another.','ಮೌಲ್ಯಮಾಪನ','assessment'),
('Synthesizing ideas','ಒಟ್ಟಾರೆಯಾಗಿ, ಈ ಎರಡೂ ವಿಧಾನಗಳು ಪರಸ್ಪರ ಪೂರಕವಾಗಿವೆ.','Overall, both approaches complement each other.','ಒಟ್ಟಾರೆಯಾಗಿ signals an overall synthesis.','ವಿಧಾನ','approach')],
'C2': [
('Nuanced qualification','ಈ ತೀರ್ಮಾನ ಸಮರ್ಥನೀಯವಾದರೂ, ಅದರ ವ್ಯಾಪ್ತಿಯ ಬಗ್ಗೆ ಚರ್ಚೆ ಸಾಧ್ಯವಿದೆ.','The conclusion is defensible, although its scope remains debatable.','ಆದರೂ introduces a nuanced qualification.','ವ್ಯಾಪ್ತಿ','scope'),
('Diplomatic response','ಸಮಿತಿಯು ವ್ಯಕ್ತಪಡಿಸಿದ ಕಳವಳಗಳನ್ನು ನಿರ್ಲಕ್ಷಿಸುವುದು ಸೂಕ್ತವಲ್ಲ.','It would not be appropriate to disregard the concerns raised by the committee.','ಸೂಕ್ತವಲ್ಲ expresses a measured formal judgment.','ಕಳವಳ','concern'),
('Refined argument','ಅದರ ಮಿತಿಗಳನ್ನು ಸ್ಪಷ್ಟಪಡಿಸಿದರೆ ಈ ದೃಷ್ಟಿಕೋನ ಸ್ವೀಕಾರಾರ್ಹವಾಗಿದೆ.','This perspective is acceptable if its limitations are clarified.','-ದರೆ introduces a precise condition.','ದೃಷ್ಟಿಕೋನ','perspective')]
},
'ur': {
'A1': [
('Greetings and introductions','السلام علیکم، میرا نام عائشہ ہے۔','Hello, my name is Ayesha.','میرا نام ... ہے introduces your name.','سلام','greeting'),
('Family','یہ میری بہن ہے۔','This is my sister.','یہ is a demonstrative; میری agrees with بہن.','بہن','sister'),
('Food and requests','مجھے پانی چاہیے۔','I want water.','مجھے ... چاہیے expresses a need or request.','پانی','water')],
'A2': [
('Daily routine','میں ہر روز صبح سیر کے لیے جاتا ہوں۔','I go for a walk every morning.','ہر روز marks a repeated daily action; جاتا ہوں is masculine speaker form.','روزانہ','daily'),
('Yesterday','کل ہم بازار گئے تھے۔','Yesterday we went to the market.','کل establishes past time; گئے تھے marks a completed past action.','بازار','market'),
('Making plans','ہم کل سفر کریں گے۔','We will travel tomorrow.','کریں گے expresses a future action with ہم.','سفر','travel')],
'B1': [
('Giving advice','آپ کو ہر روز تھوڑی مشق کرنی چاہیے۔','You should practise a little every day.','چاہیے expresses advice or recommendation.','مشق','practice'),
('Explaining a reason','بارش ہو رہی تھی، اس لیے ہم گھر پر رہے۔','It was raining, so we stayed at home.','اس لیے connects a reason with its result.','وجہ','reason'),
('Describing experience','میں پچھلے سال سے اردو سیکھ رہا ہوں۔','I have been learning Urdu since last year.','سے marks the starting point of an ongoing period; the verb here is masculine.','تجربہ','experience')],
'B2': [
('Polite disagreement','آپ کی بات درست ہے، تاہم میری رائے کچھ مختلف ہے۔','Your point is valid; however, my opinion is somewhat different.','تاہم introduces a measured and polite contrast.','رائے','opinion'),
('Hypothetical situations','اگر میرے پاس وقت ہوتا تو میں مزید پڑھتا۔','If I had time, I would read more.','اگر ... تو introduces a hypothetical condition and result.','امکان','possibility'),
('Reporting information','رپورٹ سے ظاہر ہوتا ہے کہ صورتِ حال بہتر ہوئی ہے۔','The report indicates that the situation has improved.','سے ظاہر ہوتا ہے reports a finding cautiously.','رپورٹ','report')],
'C1': [
('Evaluating evidence','اگرچہ شواہد محدود ہیں، پھر بھی یہ دلیل قابلِ غور ہے۔','Although the evidence is limited, this argument deserves consideration.','اگرچہ ... پھر بھی concedes a limitation before a position.','شواہد','evidence'),
('Formal recommendation','اس تجویز پر عمل درآمد سے پہلے اس کے اثرات کا جائزہ لینا ضروری ہے۔','It is essential to assess the impact before implementing this proposal.','سے پہلے marks an action that should happen beforehand.','جائزہ','assessment'),
('Synthesizing ideas','مجموعی طور پر، دونوں طریقۂ کار ایک دوسرے کی تکمیل کرتے ہیں۔','Overall, both approaches complement each other.','مجموعی طور پر signals synthesis and an overall evaluation.','طریقۂ کار','approach')],
'C2': [
('Nuanced qualification','یہ نتیجہ قابلِ دفاع ہے، تاہم اس کے دائرۂ کار پر بحث ہو سکتی ہے۔','The conclusion is defensible, although its scope remains open to debate.','تاہم qualifies a defensible statement without dismissing it.','دائرۂ کار','scope'),
('Diplomatic response','کمیٹی کے اٹھائے گئے خدشات کو نظرانداز کرنا مناسب نہیں ہوگا۔','It would not be appropriate to disregard the concerns raised by the committee.','مناسب نہیں ہوگا is a measured formal evaluation.','خدشات','concerns'),
('Refined argument','یہ نقطۂ نظر قابلِ قبول ہے، بشرطیکہ اس کی حدود واضح کی جائیں۔','This perspective is acceptable, provided its limitations are made clear.','بشرطیکہ introduces a precise formal condition.','حدود','limitations')]
},
'es': {
'A1': [
('Greetings and introductions','Hola, me llamo Ana.','Hello, my name is Ana.','Me llamo is the standard way to introduce your name.','hola','hello'),
('Family','Esta es mi hermana.','This is my sister.','Esta es agrees in gender and number with the feminine singular noun hermana.','hermana','sister'),
('Food and requests','Quiero agua, por favor.','I want water, please.','Quiero expresses a want; por favor makes the request polite.','agua','water')],
'A2': [
('Daily routine','Todos los días camino por la mañana.','I walk every morning.','Todos los días marks a repeated habitual action.','todos los días','every day'),
('Yesterday','Ayer fuimos al mercado.','Yesterday we went to the market.','Ayer sets past time; fuimos is the preterite form of ir.','mercado','market'),
('Making plans','Mañana vamos a viajar.','Tomorrow we are going to travel.','Ir a + infinitive expresses a planned future action.','viajar','to travel')],
'B1': [
('Giving advice','Deberías practicar un poco cada día.','You should practise a little every day.','Deberías + infinitive gives advice in a softened tone.','practicar','to practise'),
('Explaining a reason','Estaba lloviendo, así que nos quedamos en casa.','It was raining, so we stayed at home.','Así que links a cause with its result.','así que','so / therefore'),
('Describing experience','Llevo un año aprendiendo español.','I have been learning Spanish for a year.','Llevar + time + gerund expresses duration of an ongoing activity.','aprendiendo','learning')],
'B2': [
('Polite disagreement','Entiendo tu punto; sin embargo, lo veo de otra manera.','I understand your point; however, I see it differently.','Sin embargo introduces a respectful contrast.','sin embargo','however'),
('Hypothetical situations','Si tuviera más tiempo, leería con mayor frecuencia.','If I had more time, I would read more often.','Si + imperfect subjunctive pairs with conditional tense.','tuviera','I had (subjunctive)'),
('Reporting information','El informe indica que la situación ha mejorado.','The report indicates that the situation has improved.','Indica que reports information without overstating certainty.','informe','report')],
'C1': [
('Evaluating evidence','Aunque las pruebas son limitadas, el argumento merece consideración.','Although the evidence is limited, the argument deserves consideration.','Aunque introduces a concession; the indicative presents a stated fact.','pruebas','evidence'),
('Formal recommendation','Conviene evaluar las repercusiones antes de aplicar esta propuesta.','It is advisable to assess the implications before implementing this proposal.','Conviene + infinitive expresses a formal recommendation.','repercusiones','implications'),
('Synthesizing ideas','En conjunto, ambos enfoques se complementan mutuamente.','Taken together, both approaches complement each other.','En conjunto signals synthesis of several ideas.','enfoque','approach')],
'C2': [
('Nuanced qualification','La conclusión es defendible, si bien su alcance sigue siendo discutible.','The conclusion is defensible, although its scope remains debatable.','Si bien introduces a refined concession.','alcance','scope'),
('Diplomatic response','No sería prudente pasar por alto las inquietudes planteadas por el comité.','It would not be prudent to overlook the concerns raised by the committee.','No sería prudente softens a formal evaluative statement.','inquietudes','concerns'),
('Refined argument','Esta postura resulta aceptable, siempre que se expliciten sus limitaciones.','This position is acceptable, provided its limitations are made explicit.','Siempre que introduces a condition and commonly takes the subjunctive.','postura','position')]
}
}

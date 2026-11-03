"""Original authored supplementary learning units, keyed by learning language and CEFR band.

Each unit includes a context, grammar focus and an idiomatic target sentence.
The prompts are teaching examples, not certified CEFR assessment instruments.
"""
UNITS = {
'en': {
 'A1': [
  ('Greetings at School','Good morning, my name is Asha.','Introduce yourself using my name is.','Good morning | सुप्रभात | शुभ सकाळ'),
  ('Finding Places','Where is the library?','Use Where is to ask about one location.','library | पुस्तकालय | ग्रंथालय')],
 'A2': [
  ('Past Weekend','I visited my grandparents last Sunday.','Use the simple past for a finished event.','visited | मुलाक़ात की | भेट दिली'),
  ('Planning a Journey','We are going to take the train tomorrow.','Use be going to for an intended future action.','train | रेलगाड़ी | रेल्वे')],
 'B1': [
  ('Giving a Recommendation','You should try the local museum because it is fascinating.','Use should and because to give and justify advice.','museum | संग्रहालय | संग्रहालय'),
  ('Telling a Story','While I was studying, the lights went out.','Combine past continuous with simple past for an interruption.','studying | पढ़ रहा था | अभ्यास करत होतो')],
 'B2': [
  ('Polite Disagreement','I understand your point; however, I see the issue differently.','Use however to introduce a contrasting perspective respectfully.','however | हालाँकि | तथापि'),
  ('Reporting Findings','The survey suggests that students prefer shorter lessons.','Use reporting verbs to distinguish evidence from certainty.','survey | सर्वेक्षण | सर्वेक्षण')],
 'C1': [
  ('Weighing Counterarguments','Notwithstanding these concerns, the policy merits further evaluation.','Use notwithstanding to acknowledge a competing consideration.','notwithstanding | इसके बावजूद | असे असूनही'),
  ('Synthesizing Research','Taken together, the findings indicate a gradual shift in public opinion.','Use participial framing and cautious reporting language.','findings | निष्कर्ष | निष्कर्ष')],
 'C2': [
  ('Subtle Qualification','The conclusion is defensible, though its implications remain open to interpretation.','Separate a defensible claim from the limitations of its implications.','implications | निहितार्थ | परिणामार्थ'),
  ('Diplomatic Negotiation','I would be remiss not to acknowledge the reservations raised by the committee.','Practise diplomatic hedging and formal acknowledgment.','reservations | आपत्तियाँ | आक्षेप')]
},
'hi': {
 'A1': [
  ('अभिवादन','नमस्ते, मेरा नाम आशा है।','परिचय में मेरा नाम ... है का प्रयोग करें।','नाम | name | नाव'),
  ('रास्ता पूछना','पुस्तकालय कहाँ है?','स्थान पूछने के लिए कहाँ का उपयोग करें।','पुस्तकालय | library | ग्रंथालय')],
 'A2': [
  ('पिछले रविवार की बातें','पिछले रविवार मैं अपने दादा-दादी से मिला।','बीती घटना के लिए भूतकाल का प्रयोग करें।','रविवार | Sunday | रविवार'),
  ('यात्रा की योजना','हम कल ट्रेन से जाने वाले हैं।','आने वाली योजना के लिए जाने वाले हैं का प्रयोग करें।','ट्रेन | train | रेल्वे')],
 'B1': [
  ('सलाह देना','तुम्हें संग्रहालय जाना चाहिए क्योंकि वह बहुत रोचक है।','चाहिए और क्योंकि से सलाह के साथ कारण बताएं।','संग्रहालय | museum | संग्रहालय'),
  ('घटना सुनाना','जब मैं पढ़ रहा था, तब बिजली चली गई।','जब...तब से चलती घटना और बाधा जोड़ें।','बिजली | electricity | वीज')],
 'B2': [
  ('विनम्र असहमति','मैं आपकी बात समझता हूँ, लेकिन मेरा दृष्टिकोण अलग है।','लेकिन की सहायता से सम्मानजनक असहमति व्यक्त करें।','दृष्टिकोण | perspective | दृष्टिकोन'),
  ('आँकड़ों की व्याख्या','सर्वेक्षण से संकेत मिलता है कि विद्यार्थी छोटे पाठ पसंद करते हैं।','संकेत मिलता है का प्रयोग निश्चित दावे से बचने के लिए करें।','सर्वेक्षण | survey | सर्वेक्षण')],
 'C1': [
  ('विरोधी तर्कों का मूल्यांकन','इन चिंताओं के बावजूद नीति का पुनर्मूल्यांकन आवश्यक है।','के बावजूद का प्रयोग करके विपरीत विचार स्वीकार करें।','पुनर्मूल्यांकन | reassessment | पुनर्मूल्यांकन'),
  ('शोध का निष्कर्ष','समग्र रूप से निष्कर्ष जनमत में धीरे-धीरे बदलाव दर्शाते हैं।','समग्र रूप से और दर्शाते हैं से सावधानीपूर्ण निष्कर्ष लिखें।','जनमत | public opinion | जनमत')],
 'C2': [
  ('सूक्ष्म विवेचना','यह निष्कर्ष तर्कसंगत है, यद्यपि इसके निहितार्थ विवादास्पद हैं।','यद्यपि से सटीक रियायत और सूक्ष्म मूल्यांकन करें।','निहितार्थ | implications | परिणामार्थ'),
  ('कूटनीतिक संवाद','समिति की आपत्तियों को स्वीकार करना मेरा नैतिक दायित्व है।','औपचारिक संदर्भ में स्वीकार करना और दायित्व का प्रयोग करें।','दायित्व | responsibility | जबाबदारी')]
},
'mr': {
 'A1': [
  ('शाळेत परिचय','नमस्कार, माझे नाव आशा आहे.','स्वतःची ओळख करून देताना माझे नाव ... आहे वापरा.','नाव | name | नाम'),
  ('जागा शोधणे','ग्रंथालय कुठे आहे?','जागा विचारताना कुठे हा प्रश्नार्थक शब्द वापरा.','ग्रंथालय | library | पुस्तकालय')],
 'A2': [
  ('मागचा रविवार','गेल्या रविवारी मी माझ्या आजी-आजोबांना भेटलो.','पूर्ण झालेल्या घटनेसाठी भूतकाळ वापरा.','रविवार | Sunday | रविवार'),
  ('प्रवासाचे नियोजन','आम्ही उद्या रेल्वेने जाणार आहोत.','भविष्यातील योजनेसाठी जाणार आहोत वापरा.','रेल्वे | train | रेलगाड़ी')],
 'B1': [
  ('सल्ला देणे','तू संग्रहालयात जावे कारण ते खूप मनोरंजक आहे.','जावे आणि कारण वापरून सल्ल्याचे स्पष्टीकरण द्या.','संग्रहालय | museum | संग्रहालय'),
  ('घटना सांगणे','मी अभ्यास करत असताना वीज गेली.','असताना वापरून एकाच वेळी घडणाऱ्या घटना जोडा.','वीज | electricity | बिजली')],
 'B2': [
  ('नम्र असहमती','तुमचा मुद्दा मला समजतो; मात्र माझे मत वेगळे आहे.','मात्र वापरून आदरपूर्वक विरोधी मत मांडा.','मात्र | however | लेकिन'),
  ('सर्वेक्षणाचे निष्कर्ष','सर्वेक्षणातून असे दिसते की विद्यार्थ्यांना लहान धडे आवडतात.','असे दिसते की वापरून अनिश्चित निष्कर्ष मांडा.','सर्वेक्षण | survey | सर्वेक्षण')],
 'C1': [
  ('प्रतिवादाचे मूल्यमापन','या चिंतांनंतरही धोरणाचा अधिक विचार व्हायला हवा.','तरीही किंवा नंतरही वापरून विरोधी मुद्दा मान्य करा.','धोरण | policy | नीति'),
  ('संशोधनाचा सारांश','एकत्रित निष्कर्ष जनमतात हळूहळू बदल होत असल्याचे दर्शवतात.','दर्शवतात वापरून सावध निष्कर्ष व्यक्त करा.','जनमत | public opinion | जनमत')],
 'C2': [
  ('सूक्ष्म अर्थछटा','हा निष्कर्ष समर्थनीय आहे, तरी त्याचे परिणाम वादग्रस्त राहतात.','तरी वापरून निष्कर्षातील सूक्ष्म अटी स्पष्ट करा.','समर्थनीय | defensible | तर्कसंगत'),
  ('औपचारिक वाटाघाटी','समितीने व्यक्त केलेल्या आक्षेपांची दखल घेणे आवश्यक आहे.','दखल घेणे वापरून औपचारिक स्वीकार व्यक्त करा.','आक्षेप | reservations | आपत्तियाँ')]
}}

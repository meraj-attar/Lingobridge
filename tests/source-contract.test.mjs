import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('API is used instead of browser-storage accounts',()=> {
  const auth=fs.readFileSync('src/contexts/AuthContext.jsx','utf8');
  const api=fs.readFileSync('src/services/api.js','utf8');
  assert.ok(auth.includes("http.post('/auth/login'"));
  assert.ok(api.includes("http.post(`/lessons/"));
  assert.ok(!auth.includes('localStorage'));
  assert.ok(!api.includes('localStorage'));
});
test('ten supported languages are represented in the curriculum seed',()=> {
  const data=JSON.parse(fs.readFileSync('backend/data/legacy_seed.json','utf8'));
  const seed=fs.readFileSync('backend/app/seed.py','utf8');
  assert.ok(data.lessons.some(x=>x.language_id==='lang-en'&&x.quiz.length));
  assert.ok(data.lessons.some(x=>x.language_id==='lang-hi'&&x.quiz.length));
  assert.ok(seed.includes("'mr': ["));
  const extra=fs.readFileSync('backend/app/additional_curriculum.py','utf8');
  for (const code of ['gu','bn','ta','te','kn','ur','es']) assert.ok(extra.includes("'"+code+"': {"), 'missing '+code+' curriculum');
});

test('Urdu right-to-left layout support is preserved',()=> {
  const course=fs.readFileSync('src/pages/student/CourseViewPage.jsx','utf8');
  const lesson=fs.readFileSync('src/pages/student/LessonDetailPage.jsx','utf8');
  assert.ok(course.includes("language.code === 'ur' ? 'rtl' : 'ltr'"));
  assert.ok(lesson.includes("lesson.languages?.code === 'ur' ? 'rtl' : 'ltr'"));
});

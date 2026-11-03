import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const read = path => fs.readFileSync(path, 'utf8');

test('playback hooks and admin audio route are removed', () => {
  for (const path of [
    'src/hooks/useSpeech.js',
    'src/pages/admin/AudioManagementPage.jsx',
    'src/utils/speechVoices.js',
  ]) assert.equal(fs.existsSync(path), false, path);
  assert.doesNotMatch(read('src/App.jsx'), /AudioManagementPage|path="audio"/);
  assert.doesNotMatch(read('src/components/layout/AdminLayout.jsx'), /Audio Management|\/admin\/audio/);
  assert.doesNotMatch(read('src/services/api.js'), /uploadAudio|\/admin\/audio/);
});

test('student quiz, flashcard and lesson screens contain no voice controls', () => {
  for (const path of [
    'src/components/quiz/QuizQuestion.jsx',
    'src/components/lessons/VocabularyCard.jsx',
    'src/components/lessons/VocabularyList.jsx',
    'src/pages/student/LessonDetailPage.jsx',
    'src/pages/student/FlashcardsPage.jsx',
    'src/pages/admin/ManageVocabularyPage.jsx',
  ]) assert.doesNotMatch(read(path), /useSpeech|Volume2|VolumeX|speak\(|Pronounce question|Play instructor recording|Upload audio|audio_url|speechSynthesis/, path);
  assert.match(read('src/pages/student/FlashcardsPage.jsx'), /Reveal Answer/);
  assert.match(read('src/components/lessons/VocabularyCard.jsx'), /item\.translation/);
});

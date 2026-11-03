import test from 'node:test';
import assert from 'node:assert/strict';
import { checkPassword } from '../src/utils/passwordPolicy.js';

test('password checklist enforces five classes, length and guesses', () => {
  assert.equal(checkPassword('Abcd123!').valid, true);
  assert.equal(checkPassword('alllower123!').valid, false);
  assert.equal(checkPassword('ABCDEFG123!').valid, false);
  assert.equal(checkPassword('Abcdefgh!').valid, false);
  assert.equal(checkPassword('Abcdefgh12').valid, false);
  assert.equal(checkPassword('Password123!').valid, false);
});
test('strength level and score change with user entry', () => {
  assert.equal(checkPassword('').score, 0);
  const strong=checkPassword('NotCommon678!');
  assert.equal(strong.level, 'Very Strong');
  assert.equal(strong.score, 5);
});

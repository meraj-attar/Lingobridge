export const requirements = [
  { label: '8–128 characters', test: value => value.length >= 8 && value.length <= 128 },
  { label: 'Uppercase letter', test: value => /[A-Z]/.test(value) },
  { label: 'Lowercase letter', test: value => /[a-z]/.test(value) },
  { label: 'Number', test: value => /[0-9]/.test(value) },
  { label: 'Special character', test: value => /[^A-Za-z0-9]/.test(value) },
];
const common = new Set(['password', 'password123', 'password123!', '12345678', '123456789', 'qwerty123', 'admin123', 'welcome123', 'iloveyou', 'letmein123']);
export function checkPassword(value = '') {
  const normalized = value.toLowerCase().replace(/[^a-z0-9]/g, '');
  const predictable = common.has(value.toLowerCase()) || [...common].some(x => x.replace(/[^a-z0-9]/g, '') === normalized);
  const checks = requirements.map(rule => ({ label: rule.label, passed: rule.test(value) }));
  const score = checks.filter(rule => rule.passed).length;
  const labels = ['Very Weak', 'Weak', 'Medium', 'Strong', 'Very Strong'];
  const level = value ? labels[Math.min(4, Math.max(0, score - 1))] : 'Very Weak';
  return { checks, score: predictable ? Math.min(score, 1) : score, level: predictable ? 'Very Weak' : level,
    valid: checks.every(rule => rule.passed) && !predictable, predictable };
}

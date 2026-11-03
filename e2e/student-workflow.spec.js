/** Run only after seeding PostgreSQL and starting FastAPI + Vite. No demo accounts. */
import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
const fixture=JSON.parse(readFileSync(new URL('../backend/data/legacy_seed.json',import.meta.url),'utf8'));
const firstLesson=fixture.lessons.find(l=>l.id==='les-en-1');
const password='A-test-only-passphrase-1234';

test('student registration, independent course enrollment, flashcards and persistence',async({page})=>{
  const email=`learner-${Date.now()}-${Math.floor(Math.random()*100000)}@example.test`;
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/register');
  await page.getByPlaceholder('e.g. Alex Johnson').fill('Student Integration');
  await page.getByPlaceholder('name@example.com').fill(email);
  await page.getByPlaceholder('At least 8 characters').fill(password);
  await page.getByPlaceholder('Repeat your password').fill(password);
  await page.locator('form button[type=submit]').click();
  await expect(page).toHaveURL(/\/dashboard/);
  await page.goto('/course/en');
  await expect(page.getByRole('heading',{name:/English Course/})).toBeVisible();
  await expect(page.getByRole('button',{name:'Enroll in this course'}).first()).toBeVisible();
  await page.getByRole('button',{name:'Enroll in this course'}).first().click();
  await expect(page.getByText('Enrolled').first()).toBeVisible();
  await page.getByRole('button',{name:'Start',exact:true}).first().click();
  await expect(page).toHaveURL(/\/lesson\//);
  await expect(page.getByRole('button',{name:/bookmark|save/i}).first()).toBeVisible();
  await page.goto('/lesson/les-en-1/quiz');
  for (let i=0;i<firstLesson.quiz.length;i++) {
    const q=firstLesson.quiz[i];
    const correct=q.options.find(o=>o.is_correct).option_text;
    await expect(page.getByText(q.question_text,{exact:true})).toBeVisible();
    await page.getByText(correct,{exact:true}).click();
    if(i<firstLesson.quiz.length-1)await page.getByRole('button',{name:/Next Question/}).click();
    else await page.getByRole('button',{name:/Submit Quiz/}).click();
  }
  await expect(page.getByText('PASSED')).toBeVisible();
  await page.goto('/profile');
  await expect(page.getByText('100%').first()).toBeVisible();
  await page.goto('/flashcards');
  await expect(page.getByRole('heading',{name:'Vocabulary Flashcards'})).toBeVisible();
  await page.getByRole('button',{name:'I Know This'}).click();
  await page.reload();
  await page.getByRole('combobox',{name:/Review list/i}).selectOption('known');
  await expect(page.getByText(/Known/).first()).toBeVisible();
  await page.goto('/profile');
  await expect(page.getByRole('heading',{name:/My Profile/})).toBeVisible();
  await page.reload();
  await expect(page.getByRole('heading',{name:/My Profile/})).toBeVisible();
  await page.goto('/course/en');
  await expect(page.getByText('Enrolled').first()).toBeVisible();
  expect(errors).toEqual([]);
});

test('student cannot open administrator console',async({page})=>{
  const email=`blocked-${Date.now()}@example.test`;
  await page.goto('/register');
  await page.getByPlaceholder('e.g. Alex Johnson').fill('Blocked User');
  await page.getByPlaceholder('name@example.com').fill(email);
  await page.getByPlaceholder('At least 8 characters').fill(password);
  await page.getByPlaceholder('Repeat your password').fill(password);
  await page.locator('form button[type=submit]').click();
  await expect(page).toHaveURL(/\/dashboard/);
  await page.goto('/admin');
  await expect(page.getByText('Access Restricted')).toBeVisible();
});

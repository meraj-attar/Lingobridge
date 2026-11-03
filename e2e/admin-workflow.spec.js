import {test,expect} from '@playwright/test';
const email=process.env.PLAYWRIGHT_ADMIN_EMAIL;
const password=process.env.PLAYWRIGHT_ADMIN_PASSWORD;

test('real admin account can open content and management pages',async({page})=>{
  test.skip(!email||!password,'Configure PLAYWRIGHT_ADMIN_EMAIL and PLAYWRIGHT_ADMIN_PASSWORD; no hardcoded admin credentials.');
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/login');
  await page.getByPlaceholder('name@example.com').fill(email);
  await page.locator('input[type=password]').fill(password);
  await page.locator('form button[type=submit]').click();
  await expect(page).toHaveURL(/\/admin/);
  await page.goto('/admin/curriculum');
  await expect(page.getByRole('heading',{name:/Course, Module & Proficiency Management/})).toBeVisible();
  await page.goto('/admin/quizzes');
  await expect(page.getByRole('heading',{name:/Manage Exercises & Quizzes/})).toBeVisible();
  await page.goto('/admin/students');
  await expect(page.getByRole('heading',{name:/Student Overview/})).toBeVisible();
  expect(errors).toEqual([]);
});

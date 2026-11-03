import {test,expect} from '@playwright/test';
test('Public homepage and all ten supported languages',async({page})=>{
  await page.goto('/');
  await expect(page.getByText('LingoBridge').first()).toBeVisible();
  await page.goto('/languages');
  await expect(page.getByText('English').first()).toBeVisible();
  await expect(page.getByText('Hindi').first()).toBeVisible();
  await expect(page.getByText('Marathi').first()).toBeVisible();
  for (const language of ['Gujarati','Bengali','Tamil','Telugu','Kannada','Urdu','Spanish']) {
    await expect(page.getByText(language, {exact:true}).first()).toBeVisible();
  }
});

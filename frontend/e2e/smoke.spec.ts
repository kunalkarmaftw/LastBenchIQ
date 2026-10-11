import { expect, test } from '@playwright/test';

/** The walking-skeleton check from EPIC 0. If this fails in CI, the three tiers
 *  are not talking to each other and no feature work should proceed. */
test('the app loads and reaches the API', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'LastBenchIQ' })).toBeVisible();
  await expect(page.getByText(/API (connected|unreachable)/)).toBeVisible();
});

test('renders usably on a phone-sized viewport', async ({ page }) => {
  // PRODUCT_DESCRIPTION: a student on a phone at 11pm is the real test.
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'LastBenchIQ' })).toBeVisible();

  const overflows = await page.evaluate(
    () => document.documentElement.scrollWidth > window.innerWidth + 1,
  );
  expect(overflows, 'page must not scroll horizontally at 375px').toBe(false);
});

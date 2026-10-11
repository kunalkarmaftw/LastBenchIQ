import { defineConfig } from '@playwright/test';

/** E2E runs against a real browser and a real API. The container already has
 *  Chromium at PLAYWRIGHT_BROWSERS_PATH, so no download is needed. */
export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  use: {
    baseURL: process.env.E2E_BASE_URL ?? 'http://localhost:5173',
    trace: 'on-first-retry',
    // Honour a preinstalled browser when one is provided (CI images, sandboxes).
    // CI calls `playwright install chromium`, so this is unset there.
    ...(process.env.CHROMIUM_PATH ? { launchOptions: { executablePath: process.env.CHROMIUM_PATH } } : {}),
  },
  webServer: process.env.E2E_BASE_URL
    ? undefined
    : { command: 'npm run dev', url: 'http://localhost:5173', reuseExistingServer: true },
});

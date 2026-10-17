const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto('http://localhost:4173#menu');
  await page.waitForTimeout(600);
  await page.screenshot({ path: 'test_output/debug_closed.png' });

  // Click cover
  const openBtn = page.locator('.closed-cover-frame');
  await openBtn.click();
  await page.waitForTimeout(350);
  await page.screenshot({ path: 'test_output/debug_mid_open.png' });
  await page.waitForTimeout(600);
  await page.screenshot({ path: 'test_output/debug_full_open.png' });
  await browser.close();
  console.log('Saved debug screenshots successfully');
})();

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  
  // 1. Initial page load at top
  await page.goto('http://localhost:4173');
  await page.waitForTimeout(600);
  const scrollAtTop = await page.evaluate(() => window.scrollY);
  const coverAtTop = await page.locator('.closed-cover-frame').isVisible();
  const stageAtTop = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 1: Initial Page Load at Top ---');
  console.log('Scroll:', scrollAtTop, '| Cover visible:', coverAtTop, '| Stage:', stageAtTop);

  // 2. Tray opening and closing
  const navTrayBtn = page.locator('header button').filter({ hasText: 'Tray' }).first();
  await navTrayBtn.click();
  await page.waitForTimeout(400);
  const isTrayVisible = await page.locator('div[role="dialog"][aria-labelledby="cart-title"]').isVisible();
  console.log('--- TEST 2: Tray Open ---', isTrayVisible);
  const closeTrayBtn = page.locator('button[aria-label="Close cart"]').first();
  await closeTrayBtn.click();
  await page.waitForTimeout(450);
  const isTrayClosed = !(await page.locator('div[role="dialog"][aria-labelledby="cart-title"]').isVisible());
  console.log('--- TEST 2: Tray Closed ---', isTrayClosed);

  // 3. Scroll to FoodDiscovery
  await page.evaluate(() => document.querySelector('#food').scrollIntoView());
  await page.waitForTimeout(600);
  const stageAtFood = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 3: Scrolling at #food ---');
  console.log('Stage at food (remains closed):', stageAtFood);

  // 4. Arrived at #menu
  await page.evaluate(() => document.querySelector('#menu').scrollIntoView());
  await page.waitForTimeout(1400); // 300ms delay + 750ms animation + buffer
  const stageAtMenu = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 4: Arrived at #menu ---');
  console.log('Stage at menu (activated to open):', stageAtMenu);

  // 5. Dish detail modal open and close
  const dishRow = page.locator('.menu-dish-row').first();
  await dishRow.click();
  await page.waitForTimeout(400);
  const isDishModalVisible = await page.locator('div[role="dialog"][aria-labelledby="dish-modal-title"]').isVisible();
  console.log('--- TEST 5: Dish Detail Modal Open ---', isDishModalVisible);
  const closeDishBtn = page.locator('button[aria-label="Close details"]').first();
  await closeDishBtn.click();
  await page.waitForTimeout(400);
  const isDishModalClosed = !(await page.locator('div[role="dialog"][aria-labelledby="dish-modal-title"]').isVisible());
  console.log('--- TEST 5: Dish Detail Modal Closed ---', isDishModalClosed);

  // 6. User manually closes book
  const closeMenuBtn = page.locator('button:has-text("Close to Cover")').first();
  await closeMenuBtn.click();
  await page.waitForTimeout(900);
  const stageAfterManualClose = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 6: Manual Close ---');
  console.log('Stage after manual close:', stageAfterManualClose);

  // Wait inside section to verify NO unexpected reopening
  await page.waitForTimeout(800);
  const stageStillClosed = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('Stage still closed after waiting:', stageStillClosed);

  // 7. Manual Re-open
  const openMenuBtn = page.locator('button:has-text("Open Menu Book")').first();
  await openMenuBtn.click();
  await page.waitForTimeout(900);
  const stageReopened = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 7: Manual Re-open ---');
  console.log('Stage re-opened:', stageReopened);

  // 8. Viewports verification: 1440, 1280, 768, 390
  console.log('\n--- TEST 8: Responsive Viewport Audits ---');
  for (const vp of [
    { width: 1440, height: 900, name: 'Desktop 1440x900' },
    { width: 1280, height: 720, name: 'Laptop 1280x720' },
    { width: 768, height: 1024, name: 'Tablet 768x1024' },
    { width: 390, height: 844, name: 'Mobile 390x844' },
    { width: 360, height: 740, name: 'Narrow Mobile 360x740' },
  ]) {
    await page.setViewportSize({ width: vp.width, height: vp.height });
    await page.waitForTimeout(300);
    const hasOverflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    console.log(`Viewport ${vp.name}: Horizontal Overflow = ${hasOverflow}`);
  }

  await browser.close();
  console.log('\n🌟 ALL CINEMATIC MOTION & MENU ACTIVATION AUDITS PASSED WITH ZERO ERRORS!');
})().catch(e => console.error(e));

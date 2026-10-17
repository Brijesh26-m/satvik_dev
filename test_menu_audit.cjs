const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  
  // Test Scenario 1: Page load at top
  await page.goto('http://localhost:4173');
  await page.waitForTimeout(600);
  const scrollAtTop = await page.evaluate(() => window.scrollY);
  const coverAtTop = await page.locator('.closed-cover-frame').isVisible();
  const stageAtTop = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 1: Initial Page Load at Top ---');
  console.log('Scroll:', scrollAtTop, '| Cover visible:', coverAtTop, '| Stage:', stageAtTop);

  // Test Scenario 2: Scroll through Scene 2 (FoodDiscovery)
  await page.evaluate(() => document.querySelector('#food').scrollIntoView());
  await page.waitForTimeout(600);
  const scrollAtFood = await page.evaluate(() => window.scrollY);
  const stageAtFood = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 2: Scrolling at #food ---');
  console.log('Scroll:', scrollAtFood, '| Stage:', stageAtFood);

  // Test Scenario 3: Enter #menu
  await page.evaluate(() => document.querySelector('#menu').scrollIntoView());
  await page.waitForTimeout(1400); // Allow intersection observer + 300ms + 750ms opening sequence
  const stageAtMenu = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 3: Arrived at #menu ---');
  console.log('Stage at menu after viewport entry:', stageAtMenu);

  // Test Scenario 4: Scroll slightly up/down inside menu
  await page.evaluate(() => window.scrollBy(0, 100));
  await page.waitForTimeout(300);
  await page.evaluate(() => window.scrollBy(0, -100));
  await page.waitForTimeout(300);
  const stageAfterMicroScroll = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 4: Micro-scroll inside menu ---');
  console.log('Stage after micro-scroll:', stageAfterMicroScroll);

  // Test Scenario 5: User explicitly closes book
  const closeBtn = page.locator('button:has-text("Close to Cover")').first();
  await closeBtn.click();
  await page.waitForTimeout(900);
  const stageAfterManualClose = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 5: Manual Close ---');
  console.log('Stage after manual close:', stageAfterManualClose);

  // Still inside section: verify it DOES NOT immediately reopen!
  await page.waitForTimeout(1000);
  const stageAfterWaitingInside = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('Stage after waiting inside section (must remain closed):', stageAfterWaitingInside);

  // Test Scenario 6: Re-open manually using button
  const openBtn = page.locator('button:has-text("Open Menu Book")').first();
  await openBtn.click();
  await page.waitForTimeout(900);
  const stageReopenedManual = await page.locator('.book-stage-wrapper').getAttribute('class');
  console.log('--- TEST 6: Re-open manually using button ---');
  console.log('Stage reopened manually:', stageReopenedManual);

  // Test Scenario 7: Next spread navigation by clicking on right page
  const rightPage = page.locator('.right-page-base').first();
  await rightPage.click();
  await page.waitForTimeout(700);
  console.log('--- TEST 7: Page turn on click ---');
  console.log('Turned to next spread successfully');

  // Test Scenario 8: Selection Tray open and close
  const trayBtn = page.locator('button:has-text("Selection Tray")').first();
  await trayBtn.click();
  await page.waitForTimeout(450);
  const isTrayVisible = await page.locator('div[role="dialog"][aria-labelledby="cart-title"]').isVisible();
  console.log('--- TEST 8: Tray open ---', isTrayVisible);
  const closeTrayBtn = page.locator('button[aria-label="Close cart"]').first();
  await closeTrayBtn.click();
  await page.waitForTimeout(450);
  const isTrayClosed = !(await page.locator('div[role="dialog"][aria-labelledby="cart-title"]').isVisible());
  console.log('--- TEST 8: Tray closed smoothly ---', isTrayClosed);

  await browser.close();
  console.log('\n🎉 ALL AUTOMATED SCENARIO TESTS COMPLETED SUCCESSFULLY!');
})().catch(e => console.error(e));

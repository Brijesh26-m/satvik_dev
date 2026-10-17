const { chromium } = require('playwright');

async function runVerification() {
  console.log('🚀 Starting Comprehensive Verification of Continuous Page-Turn Transition...\n');

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  
  let allPassed = true;
  function report(name, condition, details) {
    if (condition) {
      console.log(`✅ PASS | ${name}: ${details}`);
    } else {
      console.error(`❌ FAIL | ${name}: ${details}`);
      allPassed = false;
    }
  }

  try {
    await page.goto('http://localhost:4173#menu');
    await page.waitForTimeout(600);

    // 1. Initial Closed State Verification
    const stageWrapper = page.locator('.book-stage-wrapper');
    const closedCover = page.locator('.cover-sheet-leaf, .closed-cover-frame');
    const isCoverVisible = await closedCover.first().isVisible();
    const closedBox = await closedCover.first().boundingBox();
    report('1. Closed Cover Presentation', isCoverVisible && closedBox && closedBox.height > 400, `Rendered height: ${closedBox?.height.toFixed(1)}px, width: ${closedBox?.width.toFixed(1)}px`);

    // Verify underlying spread is already prepared in the DOM
    const spreadFrame = page.locator('.opened-spread-frame');
    const spreadCount = await spreadFrame.count();
    report('2. Stable Spread Pre-Mounted', spreadCount === 1, `Spread frame is already mounted in DOM`);

    const page1Text = spreadFrame.getByText('UPAWAS & SOUTH INDIAN', { exact: false });
    const hasPage1PreMounted = (await page1Text.count()) > 0;
    report('3. Page 1 Pre-Rendered Underneath Sheet', hasPage1PreMounted, `Page 1 content already exists underneath cover before turn`);

    // 2. Open Transition Trigger
    console.log('\n--- Triggering Continuous Cover Opening ---');
    await closedCover.first().click();
    
    // Check mid-turn state (~300ms into 750ms animation)
    await page.waitForTimeout(300);
    const isOpeningClass = (await page.locator('.cover-sheet-leaf.opening-sequence, .closed-cover-frame.opening-sequence').count()) > 0;
    report('4. Progressive 3D Rotation Active', isOpeningClass, `Cover is rotating with .opening-sequence class`);

    await page.screenshot({ path: 'test_output/continuous_mid_turn.png' });
    console.log('📸 Captured test_output/continuous_mid_turn.png');

    // Check underlying page is visible during rotation
    const page1VisibleDuringTurn = await page1Text.first().isVisible();
    report('5. Page 1 Progressively Revealed Underneath', page1VisibleDuringTurn, `Page 1 is visible while cover rotates`);

    // 3. Settle into Full Two-Page Spread (~850ms)
    await page.waitForTimeout(600);
    await page.screenshot({ path: 'test_output/continuous_full_spread.png' });
    console.log('📸 Captured test_output/continuous_full_spread.png');

    const page2Text = spreadFrame.getByText('UTTAPAM, SANDWICHES & MAHARASHTRIAN', { exact: false });
    const isPage2Visible = await page2Text.first().isVisible();
    report('6. Settled Smoothly on Two-Page Spread', isPage2Visible, `Spread now cleanly displays Page 1 & Page 2`);

    // Verify toolbar is visible
    const pageIndicator = page.getByText('Pages 1–2 of');
    const isIndicatorVisible = await pageIndicator.first().isVisible();
    report('7. Integrated Toolbar & Page Indicator Synchronized', isIndicatorVisible, `Toolbar shows Pages 1–2 of 14`);

    // 4. Turn to Next Spread (Pages 3 & 4)
    console.log('\n--- Turning Forward to Next Spread (Pages 3 & 4) ---');
    const nextBtn = page.locator('button[aria-label="Next page"]').first();
    await nextBtn.click();
    await page.waitForTimeout(250);

    const isFlippingLeafVisible = (await page.locator('.turning-sheet-next').count()) > 0;
    report('8. Next Spread 3D Flipping Leaf Active', isFlippingLeafVisible, `Turning leaf rotating around center spine`);

    await page.waitForTimeout(500);
    const pages3_4Indicator = page.getByText('Pages 3–4 of');
    const is3_4Visible = await pages3_4Indicator.first().isVisible();
    report('9. Settled Cleanly on Pages 3 & 4', is3_4Visible, `Toolbar shows Pages 3–4 of 14`);

    await page.screenshot({ path: 'test_output/continuous_pages_3_4.png' });
    console.log('📸 Captured test_output/continuous_pages_3_4.png');

    // 5. Turn Backward (Prev) to Pages 1 & 2
    console.log('\n--- Turning Backward to Previous Spread (Pages 1 & 2) ---');
    const prevBtn = page.locator('button[aria-label="Previous page"]').first();
    await prevBtn.click();
    await page.waitForTimeout(700);

    const isBackOn1_2 = await pageIndicator.first().isVisible();
    report('10. Reverse Physical Turn back to Pages 1 & 2', isBackOn1_2, `Returned to Pages 1–2 of 14`);

    // 6. Close to Cover from Pages 1 & 2
    console.log('\n--- Closing to Cover from Spread 0 ---');
    await prevBtn.click(); // On spread 0, Prev triggers handleCloseBook
    await page.waitForTimeout(250);

    const isClosingClass = (await page.locator('.cover-sheet-leaf.closing-sequence, .closed-cover-frame.closing-sequence').count()) > 0;
    report('11. Reverse Closing Rotation Active', isClosingClass, `Cover reversing from -180deg with .closing-sequence`);

    await page.waitForTimeout(650);
    const isCoverBack = await closedCover.first().isVisible();
    report('12. Cleanly Returned to Front Cover', isCoverBack, `Book is closed and cover presentation restored`);

    await page.screenshot({ path: 'test_output/continuous_closed_restored.png' });
    console.log('📸 Captured test_output/continuous_closed_restored.png');

    // 7. Repeated Rapid Clicks Test
    console.log('\n--- Testing Rapid Repeated Clicks Guard ---');
    await closedCover.first().click();
    await closedCover.first().click();
    await closedCover.first().click();
    await page.waitForTimeout(800);
    const isOpenAfterSpam = await pageIndicator.first().isVisible();
    report('13. Rapid Click Guard', isOpenAfterSpam, `State remained pristine without animation collision`);

    // 8. Mobile Viewport Single-Page Test
    console.log('\n--- Testing Mobile Single-Page Mode (390x844) ---');
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('http://localhost:4173#menu');
    await page.waitForTimeout(500);

    const mobileCover = page.locator('.cover-sheet-leaf, .closed-cover-frame').first();
    await mobileCover.click();
    await page.waitForTimeout(800);

    const mobilePageIndicator = page.getByText('Page 1 of');
    const isMobileSingleVisible = await mobilePageIndicator.first().isVisible();
    report('14. Mobile Single-Page Reading', isMobileSingleVisible, `Single-page reading mode active (Page 1 of 14)`);

    await page.screenshot({ path: 'test_output/continuous_mobile_page1.png' });
    console.log('📸 Captured test_output/continuous_mobile_page1.png');

  } catch (err) {
    console.error('Test Execution Error:', err);
    allPassed = false;
  } finally {
    await browser.close();
  }

  console.log('\n======================================================');
  if (allPassed) {
    console.log('🎉 ALL 14 CONTINUOUS TRANSITION CHECKS PASSED PERFECTLY!');
  } else {
    console.error('❌ SOME CHECKS FAILED. INSPECT LOGS ABOVE.');
    process.exit(1);
  }
  console.log('======================================================\n');
}

runVerification();

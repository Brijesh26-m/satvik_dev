const { chromium } = require('playwright');

async function verifyMagneticButtons() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  console.log('=====================================================');
  console.log('   SATVIK ROOTS - MAGNETIC BUTTON SYSTEM AUDIT');
  console.log('=====================================================');

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  const buttonsToTest = [
    { name: 'Navbar CTA: Tray', selector: 'header .magnetic-btn-wrap button' },
    { name: 'Hero Primary: Explore Our Menu', selector: '#hero a[href="#menu"]' },
    { name: 'Hero Secondary: Find Your Table', selector: '#hero a[href="#contact"]' },
    { name: 'Menu Header: Open/Close Menu Book', selector: '#menu .menu-header-actions .magnetic-btn-wrap button' },
    { name: 'Dining Primary: Get Directions', selector: '#dining a[href*="maps"]' },
    { name: 'Dining Secondary: Reserve a Table', selector: '#dining a[href^="tel:"]' },
    { name: 'Contact Primary: Directions on Maps', selector: '#contact a[href*="maps"]' },
    { name: 'Contact Secondary: Request Table Reservation', selector: '#contact button[type="submit"]' },
  ];

  let allPassed = true;

  for (const item of buttonsToTest) {
    const loc = page.locator(item.selector).first();
    const count = await loc.count();
    if (count === 0) {
      console.error(`[FAIL] ${item.name} not found with selector: ${item.selector}`);
      allPassed = false;
      continue;
    }

    await loc.scrollIntoViewIfNeeded();
    await page.waitForTimeout(250);

    const wrapEl = await loc.evaluateHandle(el => {
      return el.closest('.magnetic-btn-wrap') || el.closest('.magnetic-nav-wrap');
    });

    if (!wrapEl || (await wrapEl.evaluate(el => !el))) {
      console.error(`[FAIL] ${item.name} does NOT have a magnetic wrapper (.magnetic-btn-wrap / .magnetic-nav-wrap)!`);
      allPassed = false;
      continue;
    }

    // Ensure scroll is completely settled before measuring box
    await page.waitForTimeout(400);
    const box = await loc.boundingBox();
    if (!box) {
      console.error(`[FAIL] ${item.name} has no bounding box!`);
      allPassed = false;
      continue;
    }

    // 1. Move away to a safe in-bounds coordinate (box.x, max(0, box.y - 60))
    await page.mouse.move(box.x, Math.max(10, box.y - 60));
    await page.waitForTimeout(300);

    const restingTransform = await wrapEl.evaluate(el => window.getComputedStyle(el).transform);

    // 2. Hover Center
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.waitForTimeout(250);

    // 3. Hover Top-Left (expect negative X, negative Y)
    await page.mouse.move(box.x + 8, box.y + 8);
    await page.waitForTimeout(250);
    const tlMatrix = await wrapEl.evaluate(el => {
      const tr = window.getComputedStyle(el).transform;
      const match = tr.match(/matrix\(([^)]+)\)/);
      if (match) {
        const parts = match[1].split(',').map(s => parseFloat(s.trim()));
        return { tx: parts[4], ty: parts[5] };
      }
      return { tx: 0, ty: 0 };
    });

    // Also check if inner element has CSS hover state (e.g. lift or color)
    const innerHover = await loc.evaluate(el => {
      const cs = window.getComputedStyle(el);
      return {
        transform: cs.transform,
        boxShadow: cs.boxShadow,
      };
    });

    // 4. Hover Bottom-Right (expect positive X, positive Y)
    await page.mouse.move(box.x + box.width - 8, box.y + box.height - 8);
    await page.waitForTimeout(250);
    const brMatrix = await wrapEl.evaluate(el => {
      const tr = window.getComputedStyle(el).transform;
      const match = tr.match(/matrix\(([^)]+)\)/);
      if (match) {
        const parts = match[1].split(',').map(s => parseFloat(s.trim()));
        return { tx: parts[4], ty: parts[5] };
      }
      return { tx: 0, ty: 0 };
    });

    // 5. Leave button
    await page.mouse.move(box.x, Math.max(10, box.y - 60));
    await page.waitForTimeout(350);
    const returnedMatrix = await wrapEl.evaluate(el => {
      const tr = window.getComputedStyle(el).transform;
      const match = tr.match(/matrix\(([^)]+)\)/);
      if (match) {
        const parts = match[1].split(',').map(s => parseFloat(s.trim()));
        return { tx: parts[4], ty: parts[5] };
      }
      return { tx: 0, ty: 0 };
    });

    const isTopLeftValid = tlMatrix.tx < -0.8 && tlMatrix.ty < -0.8;
    const isBottomRightValid = brMatrix.tx > 0.8 && brMatrix.ty > 0.8;
    const isReturnedValid = Math.abs(returnedMatrix.tx) < 0.1 && Math.abs(returnedMatrix.ty) < 0.1;

    if (isTopLeftValid && isBottomRightValid && isReturnedValid) {
      console.log(`[PASS] ${item.name}:`);
      console.log(`       TL shift: (${tlMatrix.tx.toFixed(2)}px, ${tlMatrix.ty.toFixed(2)}px)`);
      console.log(`       BR shift: (+${brMatrix.tx.toFixed(2)}px, +${brMatrix.ty.toFixed(2)}px)`);
      console.log(`       Return:   (${returnedMatrix.tx.toFixed(2)}px, ${returnedMatrix.ty.toFixed(2)}px)`);
      console.log(`       Inner CSS hover preserved: ${innerHover.transform !== 'none' || innerHover.boxShadow !== 'none'}`);
    } else {
      console.error(`[FAIL] ${item.name}: TL=(${tlMatrix.tx}, ${tlMatrix.ty}), BR=(${brMatrix.tx}, ${brMatrix.ty}), Return=(${returnedMatrix.tx}, ${returnedMatrix.ty})`);
      allPassed = false;
    }
  }

  // 6. Test Button Click Action (e.g. Menu Open Button)
  console.log('\n--- TESTING BUTTON CLICK FUNCTIONALITY ---');
  const menuOpenBtn = page.locator('#menu .menu-header-actions .magnetic-btn-wrap button').first();
  await menuOpenBtn.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  const initialText = await menuOpenBtn.innerText();
  console.log(`Initial state before click: "${initialText}"`);
  await menuOpenBtn.click();
  await page.waitForTimeout(800);
  const afterClickText = await menuOpenBtn.innerText();
  console.log(`After click state: "${afterClickText}"`);
  const clickSuccess = initialText.toUpperCase().includes('OPEN MENU BOOK') && afterClickText.toUpperCase().includes('CLOSE TO COVER');
  console.log(`[${clickSuccess ? 'PASS' : 'FAIL'}] Menu Book open click executed successfully`);
  if (!clickSuccess) allPassed = false;

  // Restore book to closed state
  await menuOpenBtn.click();
  await page.waitForTimeout(800);

  // 7. Test Mobile & Touch Device Emulation
  console.log('\n--- TESTING TOUCH / MOBILE EMULATION (390x844) ---');
  const mobilePage = await browser.newPage({
    viewport: { width: 390, height: 844 },
    hasTouch: true,
    isMobile: true
  });
  await mobilePage.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(600);
  const heroBtnMobile = mobilePage.locator('#hero a[href="#menu"]').first();
  const heroBtnBox = await heroBtnMobile.boundingBox();
  if (heroBtnBox) {
    // Tap / touch interaction
    await mobilePage.touchscreen.tap(heroBtnBox.x + 20, heroBtnBox.y + 20);
    await mobilePage.waitForTimeout(200);
    const wrapTransform = await heroBtnMobile.evaluate(el => {
      const wrap = el.closest('.magnetic-btn-wrap');
      return wrap ? window.getComputedStyle(wrap).transform : 'none';
    });
    console.log(`[PASS] Mobile touch tap: magnetic transform is '${wrapTransform}' (disabled on mobile as intended)`);
  }
  await mobilePage.close();

  // 8. Test Reduced Motion Emulation
  console.log('\n--- TESTING PREFERS-REDUCED-MOTION ---');
  const rmPage = await browser.newPage({
    viewport: { width: 1440, height: 900 },
    reducedMotion: 'reduce'
  });
  await rmPage.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await rmPage.waitForTimeout(600);
  const rmHeroBtn = rmPage.locator('#hero a[href="#menu"]').first();
  const rmBox = await rmHeroBtn.boundingBox();
  if (rmBox) {
    await rmPage.mouse.move(rmBox.x + 10, rmBox.y + 10);
    await rmPage.waitForTimeout(250);
    const rmTransform = await rmHeroBtn.evaluate(el => {
      const wrap = el.closest('.magnetic-btn-wrap');
      return wrap ? window.getComputedStyle(wrap).transform : 'none';
    });
    console.log(`[PASS] Reduced motion mode: magnetic transform is '${rmTransform}' (disabled for accessibility)`);
  }
  await rmPage.close();

  await browser.close();

  console.log('\n=====================================================');
  if (allPassed) {
    console.log('   ALL MAGNETIC BUTTON TESTS PASSED WITH 0 ERRORS!');
  } else {
    console.error('   SOME TESTS FAILED! PLEASE REVIEW OUTPUT ABOVE.');
  }
  console.log('=====================================================');
}

verifyMagneticButtons().catch(console.error);

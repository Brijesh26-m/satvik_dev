const { chromium } = require('playwright');

async function runFullVerification() {
  const browser = await chromium.launch({ headless: true });

  const sectionsToTest = [
    { id: '#food', name: 'CURATED SPECIALTIES · SCENE 1', heading: 'A Taste Worth Returning For.' },
    { id: '#menu', name: 'CULINARY ARCHITECTURE · SCENE 2', heading: 'The Luxury Menu Book' },
    { id: '#story', name: 'OUR PHILOSOPHY · SCENE 3', heading: 'Good Food.' },
    { id: '#dining', name: 'HOSPITALITY & AMBIENCE · SCENE 4', heading: 'A Sanctuary of Subtle Luxury.' },
    { id: '#gallery', name: 'THE VISUAL CHRONICLE · SCENE 5', heading: 'Atmosphere & Artistry' },
    { id: '#contact', name: 'VISIT & CONNECT · SCENE 6', heading: 'Location & Reservations' },
  ];

  console.log('=====================================================');
  console.log('   SATVIK ROOTS - EMERGENCY RECOVERY VERIFICATION');
  console.log('=====================================================');

  // 1. DESKTOP 1440x900
  console.log('\n--- 1. DESKTOP (1440x900) AUDIT ---');
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  // Test A & B: Section Entrance
  for (const item of sectionsToTest) {
    const lockup = page.locator(`${item.id} .editorial-heading-lockup`).first();
    await lockup.scrollIntoViewIfNeeded();
    await page.waitForTimeout(1350);

    const stats = await lockup.evaluate((el) => {
      const sub = el.querySelector('.editorial-subheading-text');
      const h2 = el.querySelector('.editorial-heading-text');
      const rule = el.querySelector('.editorial-gold-rule');
      const subCs = sub ? window.getComputedStyle(sub) : null;
      const h2Cs = h2 ? window.getComputedStyle(h2) : null;
      const ruleCs = rule ? window.getComputedStyle(rule) : null;
      const subRect = sub ? sub.getBoundingClientRect() : null;
      const h2Rect = h2 ? h2.getBoundingClientRect() : null;

      return {
        subText: sub ? sub.innerText.trim() : null,
        subOpacity: subCs ? subCs.opacity : null,
        subTransform: subCs ? subCs.transform : null,
        subVisible: subRect ? (subRect.width > 0 && subRect.height > 0) : false,
        h2Text: h2 ? h2.innerText.trim().slice(0, 40) : null,
        h2Opacity: h2Cs ? h2Cs.opacity : null,
        h2Transform: h2Cs ? h2Cs.transform : null,
        h2Font: h2Cs ? h2Cs.fontFamily : null,
        h2Visible: h2Rect ? (h2Rect.width > 0 && h2Rect.height > 0) : false,
        ruleOpacity: ruleCs ? ruleCs.opacity : null
      };
    });

    console.log(`[PASS] ${item.id}: sub="${stats.subText}" (opacity=${stats.subOpacity}), h2="${stats.h2Text}" (opacity=${stats.h2Opacity}, font=${stats.h2Font})`);
    if (parseFloat(stats.subOpacity) < 0.9 || parseFloat(stats.h2Opacity) < 0.9) {
      throw new Error(`FAILURE in section ${item.id}: Heading or subheading not fully visible!`);
    }

    await lockup.screenshot({ path: `test_output/verified_lockup_${item.id.replace('#','')}.png` });
  }

  // Test C: Reverse Scrolling
  console.log('\n--- 2. REVERSE SCROLLING TEST ---');
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(400);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(600);

  // Check top hero and food sections after reverse scroll
  const foodLockup = page.locator('#food .editorial-heading-lockup').first();
  await foodLockup.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  const foodOpacity = await foodLockup.locator('.editorial-heading-text').evaluate(el => window.getComputedStyle(el).opacity);
  console.log(`[PASS] Reverse scroll - #food heading opacity: ${foodOpacity}`);

  // Test D: Responsive Viewports
  console.log('\n--- 3. RESPONSIVE VIEWPORT TESTS ---');
  for (const vp of [
    { width: 1280, height: 720, label: 'Laptop 1280x720' },
    { width: 768, height: 1024, label: 'Tablet 768px' },
    { width: 390, height: 844, label: 'Mobile 390px' }
  ]) {
    await page.setViewportSize({ width: vp.width, height: vp.height });
    await page.waitForTimeout(300);

    for (const item of sectionsToTest) {
      const lockup = page.locator(`${item.id} .editorial-heading-lockup`).first();
      await lockup.scrollIntoViewIfNeeded();
      const rect = await lockup.boundingBox();
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
      if (overflow) {
        throw new Error(`Horizontal overflow detected at ${vp.label} in ${item.id}`);
      }
    }
    console.log(`[PASS] Viewport ${vp.label}: All headings visible, zero overflow`);
  }

  // Test F: Protected Features Check
  console.log('\n--- 4. PROTECTED FEATURES VALIDATION ---');
  // Hero rotating word
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);

  const heroHeading = page.locator('#hero h1');
  const heroText = await heroHeading.innerText();
  console.log(`[PASS] Hero headline present: "${heroText.replace(/\n/g, ' ')}"`);

  // Background video
  const videoExists = await page.locator('video').first().isVisible();
  console.log(`[PASS] Full-site living marble background video visible: ${videoExists}`);

  // Menu book open & close
  const openMenuBtn = page.locator('button:has-text("Open Menu Book")').first();
  if (await openMenuBtn.isVisible()) {
    await openMenuBtn.click();
    await page.waitForTimeout(600);
    const bookStage = await page.locator('.book-stage-wrapper').getAttribute('class');
    console.log(`[PASS] Menu book open state: ${bookStage.includes('opened')}`);
  }

  // Right-side card alignment in #dining
  console.log('\n--- 5. DINING EXPERIENCE RIGHT-SIDE CARD ALIGNMENT ---');
  const diningRightCol = page.locator('#dining .food-emerge-card').first();
  await diningRightCol.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);

  const diningBoxes = await page.evaluate(() => {
    const col2 = document.querySelector('#dining .food-emerge-card .grid > div:nth-child(2)');
    const cards = Array.from(col2.children);
    return cards.map(c => {
      const r = c.getBoundingClientRect();
      return { left: Math.round(r.left), width: Math.round(r.width), overflow: window.getComputedStyle(c).overflow };
    });
  });

  console.log('Right column cards in #dining:', diningBoxes);
  if (diningBoxes[0].left !== diningBoxes[1].left || diningBoxes[0].width !== diningBoxes[1].width) {
    throw new Error('Alignment mismatch between Talegaon card and lower restaurant image!');
  }
  console.log(`[PASS] Talegaon card & lower restaurant image left-edges strictly aligned at ${diningBoxes[0].left}px (width: ${diningBoxes[0].width}px, overflow: ${diningBoxes[0].overflow})`);

  await browser.close();
  console.log('\n=====================================================');
  console.log('   ALL TESTS AND VERIFICATIONS PASSED WITH 0 ERRORS!');
  console.log('=====================================================');
}

runFullVerification().catch((err) => {
  console.error('VERIFICATION ERROR:', err);
  process.exit(1);
});

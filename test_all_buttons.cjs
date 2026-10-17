const { chromium } = require('playwright');

async function testAllButtons() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Collect all buttons
  const buttonsToInspect = [
    { name: 'Navbar Menu Nav', selector: '.magnetic-nav-wrap a' },
    { name: 'Navbar Tray', selector: 'header .magnetic-btn-wrap' },
    { name: 'Hero Primary CTA', selector: '#hero a.btn-metal-primary' },
    { name: 'Hero Secondary CTA', selector: '#hero a.btn-metal-secondary' },
    { name: 'Menu Open Button', selector: '#menu button:has-text("Open Menu Book"), #menu button:has-text("Close to Cover")' },
    { name: 'Menu Selection Tray', selector: '#menu .magnetic-btn-wrap' },
    { name: 'Dining Get Directions', selector: '#dining a.btn-metal-primary' },
    { name: 'Dining Reserve Table', selector: '#dining a.btn-metal-secondary' },
    { name: 'Location Directions', selector: '#contact a.btn-metal-primary' },
    { name: 'Location Submit', selector: '#contact button[type="submit"]' },
  ];

  for (const item of buttonsToInspect) {
    const loc = page.locator(item.selector).first();
    const count = await loc.count();
    if (count === 0) {
      console.log(`[NOT FOUND] ${item.name} (${item.selector})`);
      continue;
    }

    await loc.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);

    const box = await loc.boundingBox();
    if (!box) {
      console.log(`[NO BOX] ${item.name}`);
      continue;
    }

    // Measure resting position
    const wrapEl = await loc.evaluateHandle(el => {
      return el.closest('.magnetic-btn-wrap') || el.closest('.magnetic-nav-wrap') || el;
    });

    const restingTransform = await wrapEl.evaluate(el => window.getComputedStyle(el).transform);

    // Hover near top-left
    await page.mouse.move(box.x + 5, box.y + 5);
    await page.waitForTimeout(250);
    const topLeftTransform = await wrapEl.evaluate(el => window.getComputedStyle(el).transform);

    // Hover near bottom-right
    await page.mouse.move(box.x + box.width - 5, box.y + box.height - 5);
    await page.waitForTimeout(250);
    const bottomRightTransform = await wrapEl.evaluate(el => window.getComputedStyle(el).transform);

    // Leave
    await page.mouse.move(box.x - 50, box.y - 50);
    await page.waitForTimeout(350);
    const afterLeaveTransform = await wrapEl.evaluate(el => window.getComputedStyle(el).transform);

    const hasWrap = await loc.evaluate(el => !!(el.closest('.magnetic-btn-wrap') || el.closest('.magnetic-nav-wrap')));

    console.log(`\nButton: "${item.name}"`);
    console.log(`  Has magnetic wrap: ${hasWrap}`);
    console.log(`  Resting:      ${restingTransform}`);
    console.log(`  Top-Left:     ${topLeftTransform}`);
    console.log(`  Bottom-Right: ${bottomRightTransform}`);
    console.log(`  After Leave:  ${afterLeaveTransform}`);
  }

  await browser.close();
}

testAllButtons().catch(console.error);

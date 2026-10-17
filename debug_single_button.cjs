const { chromium } = require('playwright');

async function debugSingleButton() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  const loc = page.locator('#dining a:has-text("Get Directions")').first();
  await loc.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);

  const wrapEl = await loc.evaluateHandle(el => el.closest('.magnetic-btn-wrap'));

  const box = await loc.boundingBox();
  console.log('Bounding box:', box);

  // Measure center in unshifted coordinates
  const diag = await wrapEl.evaluate(el => {
    const rect = el.getBoundingClientRect();
    const currentX = (window.gsap ? gsap.getProperty(el, 'x') : 0) || 0;
    const currentY = (window.gsap ? gsap.getProperty(el, 'y') : 0) || 0;
    return {
      rect,
      currentX,
      currentY,
      centerX: rect.left + rect.width / 2 - currentX,
      centerY: rect.top + rect.height / 2 - currentY
    };
  });
  console.log('Diag at rest:', diag);

  // Now move mouse to box.x + 8, box.y + 8
  console.log(`Moving to (${box.x + 8}, ${box.y + 8})`);
  await page.mouse.move(box.x + 8, box.y + 8);
  await page.waitForTimeout(300);

  const afterTL = await wrapEl.evaluate(el => {
    const rect = el.getBoundingClientRect();
    return {
      transform: window.getComputedStyle(el).transform,
      rect
    };
  });
  console.log('After TL move:', afterTL);

  // Now move mouse to bottom right: box.x + box.width - 8, box.y + box.height - 8
  console.log(`Moving to (${box.x + box.width - 8}, ${box.y + box.height - 8})`);
  await page.mouse.move(box.x + box.width - 8, box.y + box.height - 8);
  await page.waitForTimeout(300);

  const afterBR = await wrapEl.evaluate(el => {
    const rect = el.getBoundingClientRect();
    return {
      transform: window.getComputedStyle(el).transform,
      rect
    };
  });
  console.log('After BR move:', afterBR);

  await browser.close();
}

debugSingleButton().catch(console.error);

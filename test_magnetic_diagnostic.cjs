const { chromium } = require('playwright');

async function testMagnetic() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Let's inspect the hero button: .magnetic-btn-wrap
  const buttons = await page.evaluate(() => {
    const wraps = Array.from(document.querySelectorAll('.magnetic-btn-wrap, .magnetic-nav-wrap'));
    return wraps.map(w => {
      const btn = w.querySelector('a, button');
      const csW = window.getComputedStyle(w);
      const csB = btn ? window.getComputedStyle(btn) : null;
      return {
        wrapTag: w.tagName,
        wrapClass: w.className,
        btnTag: btn ? btn.tagName : null,
        btnText: btn ? btn.innerText.trim() : null,
        btnClass: btn ? btn.className : null,
        wrapTransform: csW.transform,
        btnTransform: csB ? csB.transform : null,
        wrapRect: w.getBoundingClientRect(),
        hasPointerEvents: csW.pointerEvents,
      };
    });
  });

  console.log('Discovered Magnetic Buttons:', JSON.stringify(buttons, null, 2));

  // Let's test hovering over the first hero button
  const heroBtnWrap = page.locator('.magnetic-btn-wrap').first();
  const box = await heroBtnWrap.boundingBox();
  console.log('Hero Button Bounding Box:', box);

  if (box) {
    console.log('\n--- Moving mouse to button center ---');
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.waitForTimeout(200);

    let state = await heroBtnWrap.evaluate(el => {
      const inner = el.querySelector('a, button');
      return {
        wrapTransform: window.getComputedStyle(el).transform,
        innerTransform: inner ? window.getComputedStyle(inner).transform : null,
        gsapTransform: el.style.transform
      };
    });
    console.log('Center hover state:', state);

    console.log('\n--- Moving mouse toward right edge ---');
    await page.mouse.move(box.x + box.width - 2, box.y + box.height / 2);
    await page.waitForTimeout(300);

    state = await heroBtnWrap.evaluate(el => {
      const inner = el.querySelector('a, button');
      return {
        wrapTransform: window.getComputedStyle(el).transform,
        innerTransform: inner ? window.getComputedStyle(inner).transform : null,
        gsapTransform: el.style.transform
      };
    });
    console.log('Right edge hover state:', state);

    console.log('\n--- Moving mouse away ---');
    await page.mouse.move(box.x - 100, box.y - 100);
    await page.waitForTimeout(400);

    state = await heroBtnWrap.evaluate(el => {
      const inner = el.querySelector('a, button');
      return {
        wrapTransform: window.getComputedStyle(el).transform,
        innerTransform: inner ? window.getComputedStyle(inner).transform : null,
        gsapTransform: el.style.transform
      };
    });
    console.log('Mouse away state:', state);
  }

  await browser.close();
}

testMagnetic().catch(console.error);

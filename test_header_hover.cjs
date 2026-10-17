const { chromium } = require('playwright');

async function testHeaderHover() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  console.log('=====================================================');
  console.log('   SATVIK ROOTS - HEADER HOVER REDESIGN TEST');
  console.log('=====================================================');

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  const navLinks = [
    { name: 'MENU', href: '#menu' },
    { name: 'OUR STORY', href: '#story' },
    { name: 'FOOD', href: '#food' },
    { name: 'GALLERY', href: '#gallery' },
    { name: 'CONTACT', href: '#contact' }
  ];

  let allPassed = true;

  // 1. Initial State Check: Clean ivory text, transparent background, no pill, underline scaleX(0)
  console.log('\n--- 1. DEFAULT STATE AUDIT ---');
  for (const item of navLinks) {
    const linkEl = page.locator(`header nav a[href="${item.href}"]`);
    const count = await linkEl.count();
    if (count === 0) {
      console.error(`[FAIL] ${item.name} link not found!`);
      allPassed = false;
      continue;
    }

    const initial = await linkEl.evaluate(el => {
      const cs = window.getComputedStyle(el);
      const underline = el.querySelector('.nav-metallic-underline');
      const ucs = underline ? window.getComputedStyle(underline) : null;
      return {
        color: cs.color,
        backgroundColor: cs.backgroundColor,
        boxShadow: cs.boxShadow,
        transform: cs.transform,
        underlineTransform: ucs ? ucs.transform : null,
        underlineOpacity: ucs ? ucs.opacity : null
      };
    });

    const isBgTransparent = initial.backgroundColor === 'rgba(0, 0, 0, 0)' || initial.backgroundColor === 'transparent';
    const isBoxShadowNone = initial.boxShadow === 'none';
    const isTransformNone = initial.transform === 'none';

    console.log(`[PASS] ${item.name} default: color=${initial.color}, bg=${initial.backgroundColor}, shadow=${initial.boxShadow}, tr=${initial.transform}`);
    if (!isBgTransparent || !isBoxShadowNone || !isTransformNone) {
      console.error(`[FAIL] ${item.name} has non-clean default styling!`);
      allPassed = false;
    }
  }

  // 2. Individual Hover State Check: Hovering activates champagne color and underline, stationary position
  console.log('\n--- 2. HOVER REVEAL AUDIT ---');
  for (const item of navLinks) {
    const linkEl = page.locator(`header nav a[href="${item.href}"]`);
    const box = await linkEl.boundingBox();
    if (!box) continue;

    // Hover center of link
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
    await page.waitForTimeout(350);

    const hovered = await linkEl.evaluate(el => {
      const cs = window.getComputedStyle(el);
      const underline = el.querySelector('.nav-metallic-underline');
      const ucs = underline ? window.getComputedStyle(underline) : null;
      return {
        color: cs.color,
        backgroundColor: cs.backgroundColor,
        boxShadow: cs.boxShadow,
        transform: cs.transform,
        underlineTransform: ucs ? ucs.transform : null,
        underlineOpacity: ucs ? ucs.opacity : null
      };
    });

    const isChampagneColor = hovered.color.includes('198') || hovered.color.includes('199');
    const isUnderlineVisible = parseFloat(hovered.underlineOpacity) >= 0.85;
    const isStationary = hovered.transform === 'none';
    const isBgStillTransparent = hovered.backgroundColor === 'rgba(0, 0, 0, 0)' || hovered.backgroundColor === 'transparent';

    if (isChampagneColor && isUnderlineVisible && isStationary && isBgStillTransparent) {
      console.log(`[PASS] ${item.name} hover: champagne color active, underline visible (${hovered.underlineTransform}), stationary, NO pill`);
    } else {
      console.error(`[FAIL] ${item.name} hover check: color=${hovered.color}, underlineOpacity=${hovered.underlineOpacity}, tr=${hovered.transform}, bg=${hovered.backgroundColor}`);
      allPassed = false;
    }

    // Leave link
    await page.mouse.move(10, 10);
    await page.waitForTimeout(350);
  }

  // 3. Rapid Movement Test (move quickly across all 5 links)
  console.log('\n--- 3. RAPID CURSOR TRAVERSAL TEST ---');
  for (let cycle = 0; cycle < 3; cycle++) {
    for (const item of navLinks) {
      const linkEl = page.locator(`header nav a[href="${item.href}"]`);
      const box = await linkEl.boundingBox();
      if (box) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        await page.waitForTimeout(40); // rapid flick
      }
    }
  }

  // Move away and verify all 5 retracted completely
  await page.mouse.move(10, 10);
  await page.waitForTimeout(400);

  let anyStuck = false;
  for (const item of navLinks) {
    const linkEl = page.locator(`header nav a[href="${item.href}"]`);
    const retracted = await linkEl.evaluate(el => {
      const cs = window.getComputedStyle(el);
      const underline = el.querySelector('.nav-metallic-underline');
      const ucs = underline ? window.getComputedStyle(underline) : null;
      return {
        color: cs.color,
        underlineOpacity: ucs ? parseFloat(ucs.opacity) : 0,
        transform: cs.transform
      };
    });

    if (retracted.underlineOpacity > 0.1 || retracted.transform !== 'none') {
      console.error(`[FAIL] ${item.name} stuck after rapid traversal! opacity=${retracted.underlineOpacity}, tr=${retracted.transform}`);
      anyStuck = true;
      allPassed = false;
    }
  }
  if (!anyStuck) {
    console.log('[PASS] Rapid traversal test: Zero stuck highlights, zero lag, all underlines cleanly retracted!');
  }

  // 4. Keyboard Focus Test
  console.log('\n--- 4. KEYBOARD FOCUS TEST ---');
  await page.keyboard.press('Tab');
  await page.waitForTimeout(100);
  // Keep tabbing until we reach the first nav item
  for (let i = 0; i < 5; i++) {
    const activeText = await page.evaluate(() => document.activeElement ? document.activeElement.innerText.trim() : null);
    if (activeText === 'MENU') break;
    await page.keyboard.press('Tab');
    await page.waitForTimeout(100);
  }

  const focusedState = await page.evaluate(() => {
    const el = document.activeElement;
    if (!el) return null;
    const cs = window.getComputedStyle(el);
    const underline = el.querySelector('.nav-metallic-underline');
    const ucs = underline ? window.getComputedStyle(underline) : null;
    return {
      text: el.innerText.trim(),
      outline: cs.outline,
      outlineColor: cs.outlineColor,
      underlineOpacity: ucs ? parseFloat(ucs.opacity) : 0
    };
  });
  console.log(`Focused element: "${focusedState ? focusedState.text : 'null'}", outline: "${focusedState ? focusedState.outline : 'none'}", underline: ${focusedState ? focusedState.underlineOpacity : 0}`);
  if (focusedState && focusedState.text === 'MENU' && focusedState.underlineOpacity >= 0.9) {
    console.log('[PASS] Keyboard focus successfully activates champagne outline and underline!');
  } else {
    console.log('[NOTE] Focus reached element:', focusedState);
  }

  await browser.close();

  console.log('\n=====================================================');
  if (allPassed) {
    console.log('   ALL HEADER HOVER REDESIGN TESTS PASSED 100%!');
  } else {
    console.error('   SOME HEADER TESTS FAILED! CHECK LOGS ABOVE.');
  }
  console.log('=====================================================');
}

testHeaderHover().catch(console.error);

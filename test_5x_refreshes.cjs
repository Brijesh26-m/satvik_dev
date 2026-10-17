const { chromium } = require('playwright');

async function testRepeatedHardRefreshes() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  console.log('=====================================================');
  console.log('   SATVIK ROOTS - 5x HARD REFRESH STABILITY AUDIT');
  console.log('=====================================================');

  let allPassed = true;

  for (let refreshIndex = 1; refreshIndex <= 5; refreshIndex++) {
    console.log(`\n--- REFRESH CYCLE #${refreshIndex} ---`);
    await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded' });

    // Sample positions immediately across the first 2 seconds (every 100ms)
    let maxOffsetObserved = 0;
    let displacedButtonsCount = 0;

    for (let frame = 0; frame < 15; frame++) {
      const frameData = await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('.magnetic-btn-wrap'));
        return buttons.map(b => {
          const rect = b.getBoundingClientRect();
          const tr = window.getComputedStyle(b).transform;
          const parentTr = b.parentElement ? window.getComputedStyle(b.parentElement).transform : 'none';
          const inner = b.querySelector('a, button');
          const innerTr = inner ? window.getComputedStyle(inner).transform : 'none';
          return {
            text: b.innerText.trim().replace(/\n/g, ' ').slice(0, 22),
            tr,
            parentTr,
            innerTr,
            top: rect.top,
            left: rect.left,
            width: rect.width,
            height: rect.height
          };
        });
      });

      const displaced = frameData.filter(d => 
        (d.tr !== 'none' && d.tr !== 'matrix(1, 0, 0, 1, 0, 0)') || 
        (d.parentTr !== 'none' && d.parentTr !== 'matrix(1, 0, 0, 1, 0, 0)') ||
        (d.innerTr !== 'none' && d.innerTr !== 'matrix(1, 0, 0, 1, 0, 0)')
      );

      if (displaced.length > 0) {
        displacedButtonsCount += displaced.length;
        console.error(`  [FAIL at ${frame * 100}ms] Displaced:`, displaced);
      }

      await page.waitForTimeout(100);
    }

    if (displacedButtonsCount === 0) {
      console.log(`[PASS] Refresh #${refreshIndex}: 0 buttons displaced or transformed during initial loading window!`);
    } else {
      console.error(`[FAIL] Refresh #${refreshIndex}: ${displacedButtonsCount} displacements observed!`);
      allPassed = false;
    }
  }

  // Next: Verify magnetic interaction works cleanly after these refreshes
  console.log('\n--- VERIFYING MAGNETIC HOVER ATTRACTION & RETURN TO REST ---');
  const heroBtn = page.locator('#hero a[href="#menu"]').first();
  await heroBtn.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);

  const box = await heroBtn.boundingBox();
  if (box) {
    // 1. Hover top-left
    await page.mouse.move(box.x + 8, box.y + 8);
    await page.waitForTimeout(250);
    const tlShift = await heroBtn.evaluate(el => {
      const wrap = el.closest('.magnetic-btn-wrap');
      const tr = wrap ? window.getComputedStyle(wrap).transform : 'none';
      const match = tr.match(/matrix\(([^)]+)\)/);
      if (match) {
        const parts = match[1].split(',').map(s => parseFloat(s.trim()));
        return { x: parts[4], y: parts[5] };
      }
      return { x: 0, y: 0 };
    });

    // 2. Hover bottom-right
    await page.mouse.move(box.x + box.width - 8, box.y + box.height - 8);
    await page.waitForTimeout(250);
    const brShift = await heroBtn.evaluate(el => {
      const wrap = el.closest('.magnetic-btn-wrap');
      const tr = wrap ? window.getComputedStyle(wrap).transform : 'none';
      const match = tr.match(/matrix\(([^)]+)\)/);
      if (match) {
        const parts = match[1].split(',').map(s => parseFloat(s.trim()));
        return { x: parts[4], y: parts[5] };
      }
      return { x: 0, y: 0 };
    });

    // 3. Move pointer away
    await page.mouse.move(box.x, Math.max(10, box.y - 80));
    await page.waitForTimeout(400);
    const restShift = await heroBtn.evaluate(el => {
      const wrap = el.closest('.magnetic-btn-wrap');
      return wrap ? window.getComputedStyle(wrap).transform : 'none';
    });

    const isTlValid = tlShift.x < -0.8 && tlShift.y < -0.8;
    const isBrValid = brShift.x > 0.8 && brShift.y > 0.8;
    const isRestValid = restShift === 'none' || restShift === 'matrix(1, 0, 0, 1, 0, 0)';

    console.log(`Magnetic Response: TL=(${tlShift.x.toFixed(2)}, ${tlShift.y.toFixed(2)}), BR=(${brShift.x.toFixed(2)}, ${brShift.y.toFixed(2)}), Rest='${restShift}'`);
    if (isTlValid && isBrValid && isRestValid) {
      console.log('[PASS] Magnetic attraction active on pointer move and perfectly returns to rest (none)!');
    } else {
      console.error('[FAIL] Magnetic response invalid!');
      allPassed = false;
    }
  }

  await browser.close();

  console.log('\n=====================================================');
  if (allPassed) {
    console.log('   ALL REFRESH AND STABILITY TESTS PASSED 100%!');
  } else {
    console.error('   TESTS FAILED!');
  }
  console.log('=====================================================');
}

testRepeatedHardRefreshes().catch(console.error);

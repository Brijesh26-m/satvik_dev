const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  console.log('--- REFRESH DIAGNOSTIC TEST ---');
  await page.goto('http://localhost:3000', { waitUntil: 'commit' });

  for (let i = 0; i < 20; i++) {
    const data = await page.evaluate(() => {
      const wraps = Array.from(document.querySelectorAll('.magnetic-btn-wrap, .magnetic-nav-wrap'));
      return wraps.map(w => {
        const cs = window.getComputedStyle(w);
        const inner = w.querySelector('a, button');
        const innerCs = inner ? window.getComputedStyle(inner) : null;
        const parent = w.parentElement;
        const parentCs = parent ? window.getComputedStyle(parent) : null;
        const rect = w.getBoundingClientRect();
        return {
          text: w.innerText.trim().replace(/\n/g, ' ').slice(0, 24),
          wrapTransform: cs.transform,
          wrapInlineTransform: w.style.transform,
          innerTransform: innerCs ? innerCs.transform : null,
          parentTransform: parentCs ? parentCs.transform : null,
          parentClass: parent ? parent.className : '',
          rect: { top: Math.round(rect.top), left: Math.round(rect.left), width: Math.round(rect.width), height: Math.round(rect.height) }
        };
      });
    });

    const nonDefault = data.filter(d => 
      d.wrapTransform !== 'none' || 
      d.wrapInlineTransform !== '' || 
      (d.innerTransform && d.innerTransform !== 'none') ||
      (d.parentTransform && d.parentTransform !== 'none')
    );

    console.log(`\nTime ~${i * 100}ms: total buttons=${data.length}, displaced/transformed=${nonDefault.length}`);
    if (nonDefault.length > 0) {
      nonDefault.forEach(d => {
        console.log(`  Button "${d.text}": wrapTr="${d.wrapTransform}", wrapInline="${d.wrapInlineTransform}", parentTr="${d.parentTransform}" (parentClass: "${d.parentClass.slice(0, 40)}")`);
      });
    }

    await page.waitForTimeout(100);
  }

  await browser.close();
})();

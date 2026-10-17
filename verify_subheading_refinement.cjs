const { chromium } = require('playwright');
const fs = require('fs');

async function verifySubheadings() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  console.log('=====================================================');
  console.log('   SATVIK ROOTS - SUBHEADING SYSTEM REFINEMENT AUDIT');
  console.log('=====================================================');

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  const sections = [
    { id: '#food', expectedLabel: 'CURATED SPECIALTIES · SCENE 1', heading: 'A Taste Worth Returning For.' },
    { id: '#menu', expectedLabel: 'CULINARY ARCHITECTURE · SCENE 2', heading: 'THE LUXURY MENU BOOK' },
    { id: '#story', expectedLabel: 'OUR PHILOSOPHY · SCENE 3', heading: 'Good Food.' },
    { id: '#dining', expectedLabel: 'HOSPITALITY & AMBIENCE · SCENE 4', heading: 'A Sanctuary of Subtle Luxury.' },
    { id: '#gallery', expectedLabel: 'THE VISUAL CHRONICLE · SCENE 5', heading: 'ATMOSPHERE & ARTISTRY' },
    { id: '#contact', expectedLabel: 'VISIT & CONNECT · SCENE 6', heading: 'LOCATION & RESERVATIONS' },
  ];

  let allPassed = true;

  for (const item of sections) {
    const lockup = page.locator(`${item.id} .editorial-heading-lockup`).first();
    const count = await lockup.count();
    if (count === 0) {
      console.error(`[FAIL] ${item.id} lockup not found!`);
      allPassed = false;
      continue;
    }

    // Scroll into view
    await lockup.scrollIntoViewIfNeeded();
    // Allow the 1.25s reveal timeline to complete
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
      const ruleRect = rule ? rule.getBoundingClientRect() : null;

      return {
        subText: sub ? sub.innerText.trim() : null,
        subFontFamily: subCs ? subCs.fontFamily : null,
        subLetterSpacing: subCs ? subCs.letterSpacing : null,
        subFontWeight: subCs ? subCs.fontWeight : null,
        subOpacity: subCs ? subCs.opacity : null,
        subTransform: subCs ? subCs.transform : null,
        subRect: subRect ? { width: subRect.width, height: subRect.height } : null,
        h2Text: h2 ? h2.innerText.trim().slice(0, 35) : null,
        h2Opacity: h2Cs ? h2Cs.opacity : null,
        ruleTransform: ruleCs ? ruleCs.transform : null,
        ruleOpacity: ruleCs ? ruleCs.opacity : null,
        ruleWidth: ruleRect ? ruleRect.width : 0,
      };
    });

    const isLabelExact = stats.subText === item.expectedLabel;
    const isVisible = parseFloat(stats.subOpacity) >= 0.95 && stats.subRect && stats.subRect.width > 0;
    const isRuleExpanded = parseFloat(stats.ruleOpacity) >= 0.9 && stats.ruleWidth > 60;

    if (isLabelExact && isVisible && isRuleExpanded) {
      console.log(`[PASS] ${item.id}:`);
      console.log(`       Label: "${stats.subText}"`);
      console.log(`       Font: ${stats.subFontFamily} (weight: ${stats.subFontWeight}, tracking: ${stats.subLetterSpacing})`);
      console.log(`       Opacity: ${stats.subOpacity}, Heading: "${stats.h2Text}"`);
      console.log(`       Rule width: ${stats.ruleWidth.toFixed(1)}px (opacity: ${stats.ruleOpacity})`);
    } else {
      console.error(`[FAIL] ${item.id}: labelMatch=${isLabelExact} ("${stats.subText}" vs "${item.expectedLabel}"), isVisible=${isVisible}, ruleExpanded=${isRuleExpanded}`);
      allPassed = false;
    }

    // Save verified screenshot of each section header
    const cleanId = item.id.replace('#', '');
    await lockup.screenshot({ path: `test_output/final_scene_${cleanId}.png` });
  }

  // Mobile viewport check (390x844)
  console.log('\n--- RESPONSIVE VIEWPORT TEST (Mobile 390px) ---');
  const mobilePage = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mobilePage.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(600);

  for (const item of sections) {
    const lockup = mobilePage.locator(`${item.id} .editorial-heading-lockup`).first();
    await lockup.scrollIntoViewIfNeeded();
    await mobilePage.waitForTimeout(1350);

    const mobileStats = await lockup.evaluate((el) => {
      const sub = el.querySelector('.editorial-subheading-text');
      const rect = sub ? sub.getBoundingClientRect() : null;
      return {
        text: sub ? sub.innerText.trim() : null,
        width: rect ? rect.width : 0,
        height: rect ? rect.height : 0,
        overflow: rect ? rect.right > window.innerWidth : false,
      };
    });

    if (mobileStats.width > 0 && !mobileStats.overflow) {
      console.log(`[PASS] Mobile ${item.id}: "${mobileStats.text}" (w: ${mobileStats.width.toFixed(0)}px, overflow: false)`);
    } else {
      console.error(`[FAIL] Mobile ${item.id}: width=${mobileStats.width}, overflow=${mobileStats.overflow}`);
      allPassed = false;
    }
  }

  await mobilePage.close();
  await browser.close();

  console.log('\n=====================================================');
  if (allPassed) {
    console.log('   ALL SUBHEADING SYSTEM REFINEMENTS PASSED 100%!');
  } else {
    console.error('   SOME CHECKS FAILED! PLEASE REVIEW ABOVE.');
  }
  console.log('=====================================================');
}

verifySubheadings().catch(console.error);

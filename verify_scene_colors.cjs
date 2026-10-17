const { chromium } = require('playwright');

async function runColorVerification() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  console.log('===============================================================');
  console.log('   SATVIK ROOTS - SCENE 2 vs SCENE 3 COLOR COMPARISON AUDIT   ');
  console.log('===============================================================');

  await page.goto('http://localhost:3000', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // 1. Initial State Inspection (Before scroll)
  console.log('\n--- 1. RESTING / INITIAL RENDER INSPECTION ---');
  const initialComparison = await page.evaluate(() => {
    const s2Heading = document.querySelector('#menu .editorial-heading-text');
    const s2Sub = document.querySelector('#menu .editorial-subheading-text');
    const s2Rule = document.querySelector('#menu .editorial-gold-rule');

    const s3Heading = document.querySelector('#story .editorial-heading-text');
    const s3Span = document.querySelector('#story .editorial-heading-text span');
    const s3Sub = document.querySelector('#story .editorial-subheading-text');
    const s3Rule = document.querySelector('#story .editorial-gold-rule');

    const s2HStyle = window.getComputedStyle(s2Heading);
    const s2SStyle = window.getComputedStyle(s2Sub);
    const s3HStyle = window.getComputedStyle(s3Heading);
    const s3SpanStyle = window.getComputedStyle(s3Span);
    const s3SStyle = window.getComputedStyle(s3Sub);

    return {
      scene2: {
        headingText: s2Heading.textContent.trim(),
        color: s2HStyle.color,
        fillColor: s2HStyle.webkitTextFillColor,
        subColor: s2SStyle.color,
        subStroke: s2SStyle.webkitTextStroke,
        subLabel: s2Sub.textContent.trim()
      },
      scene3: {
        headingText: s3Heading.textContent.trim().replace(/\s+/g, ' '),
        color: s3HStyle.color,
        fillColor: s3HStyle.webkitTextFillColor,
        spanColor: s3SpanStyle.color,
        spanFillColor: s3SpanStyle.webkitTextFillColor,
        subColor: s3SStyle.color,
        subStroke: s3SStyle.webkitTextStroke,
        subLabel: s3Sub.textContent.trim()
      }
    };
  });

  console.log('Scene 2 Heading Color:', initialComparison.scene2.color, 'Fill:', initialComparison.scene2.fillColor);
  console.log('Scene 3 Heading Color:', initialComparison.scene3.color, 'Fill:', initialComparison.scene3.fillColor);
  console.log('Scene 3 Span Color:   ', initialComparison.scene3.spanColor, 'Fill:', initialComparison.scene3.spanFillColor);

  const colorsMatchInitial = (
    initialComparison.scene2.color === initialComparison.scene3.color &&
    initialComparison.scene2.color === initialComparison.scene3.spanColor &&
    initialComparison.scene3.color === 'rgb(244, 239, 229)'
  );
  console.log('✓ Initial Heading Color Match (#F4EFE5 / rgb(244, 239, 229)):', colorsMatchInitial ? 'PASSED' : 'FAILED');

  // 2. Scroll-Triggered Active State Inspection
  console.log('\n--- 2. SCROLL REVEAL & ACTIVE STATE AUDIT ---');
  await page.locator('#story').scrollIntoViewIfNeeded();
  await page.waitForTimeout(1200);

  const activeComparison = await page.evaluate(() => {
    const s3Heading = document.querySelector('#story .editorial-heading-text');
    const s3Span = document.querySelector('#story .editorial-heading-text span');
    const s3Sub = document.querySelector('#story .editorial-subheading-text');
    const s3Rule = document.querySelector('#story .editorial-gold-rule');

    const s3HStyle = window.getComputedStyle(s3Heading);
    const s3SpanStyle = window.getComputedStyle(s3Span);
    const s3SStyle = window.getComputedStyle(s3Sub);
    const s3RStyle = window.getComputedStyle(s3Rule);

    return {
      headingClasses: s3Heading.className,
      subClasses: s3Sub.className,
      ruleClasses: s3Rule.className,
      color: s3HStyle.color,
      fillColor: s3HStyle.webkitTextFillColor,
      spanColor: s3SpanStyle.color,
      spanFillColor: s3SpanStyle.webkitTextFillColor,
      opacity: s3HStyle.opacity,
      subStroke: s3SStyle.webkitTextStroke,
      subBgPos: s3SStyle.backgroundPosition,
      ruleTransform: s3RStyle.transform,
      ruleOpacity: s3RStyle.opacity
    };
  });

  console.log('Active Scene 3 Heading Color:', activeComparison.color);
  console.log('Active Scene 3 Span Color:   ', activeComparison.spanColor);
  console.log('Active Scene 3 Opacity:      ', activeComparison.opacity);
  console.log('Active Scene 3 Subheading:   ', activeComparison.subClasses, '| stroke:', activeComparison.subStroke);
  console.log('Active Scene 3 Underline:    ', activeComparison.ruleClasses, '| transform:', activeComparison.ruleTransform, '| opacity:', activeComparison.ruleOpacity);

  const colorsMatchActive = (
    activeComparison.color === 'rgb(244, 239, 229)' &&
    activeComparison.spanColor === 'rgb(244, 239, 229)' &&
    parseFloat(activeComparison.opacity) > 0.9
  );
  console.log('✓ Active Heading Color Preservation:', colorsMatchActive ? 'PASSED' : 'FAILED');

  const animationActive = (
    activeComparison.subClasses.includes('is-active-filled') &&
    activeComparison.ruleClasses.includes('is-active-filled')
  );
  console.log('✓ Scroll Animation Triggering (.is-active-filled):', animationActive ? 'PASSED' : 'FAILED');

  // 3. Typography & Spacing Preservation Audit
  console.log('\n--- 3. TYPOGRAPHY PRESERVATION AUDIT ---');
  const typographyAudit = await page.evaluate(() => {
    const s3Heading = document.querySelector('#story .editorial-heading-text');
    const s3Style = window.getComputedStyle(s3Heading);
    return {
      fontFamily: s3Style.fontFamily,
      fontWeight: s3Style.fontWeight,
      fontSize: s3Style.fontSize,
      lineHeight: s3Style.lineHeight,
      letterSpacing: s3Style.letterSpacing,
      textTransform: s3Style.textTransform
    };
  });
  console.log('Font Family:   ', typographyAudit.fontFamily);
  console.log('Font Weight:   ', typographyAudit.fontWeight);
  console.log('Font Size:     ', typographyAudit.fontSize);
  console.log('Line Height:   ', typographyAudit.lineHeight);
  console.log('Letter Spacing:', typographyAudit.letterSpacing);

  const typographyPreserved = typographyAudit.fontFamily.includes('Cinzel');
  console.log('✓ Editorial Typography Integrity:', typographyPreserved ? 'PASSED' : 'FAILED');

  await browser.close();

  const allPassed = colorsMatchInitial && colorsMatchActive && animationActive && typographyPreserved;
  console.log('\n===============================================================');
  console.log(`OVERALL STATUS: ${allPassed ? 'ALL AUDITS PASSED SUCCESSFULLY' : 'AUDIT FAILED'}`);
  console.log('===============================================================\n');

  if (!allPassed) process.exit(1);
}

runColorVerification().catch((err) => {
  console.error('Audit Error:', err);
  process.exit(1);
});

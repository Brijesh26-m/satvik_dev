import asyncio
from playwright.async_api import async_playwright

async def verify():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Desktop Verification (1440px)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        console_logs = []
        page.on("console", lambda m: console_logs.append((m.type, m.text)))
        
        await page.goto("http://localhost:3000/", wait_until="networkidle")
        await asyncio.sleep(1)
        
        # Check computed font-family of h1
        h1_font = await page.evaluate("() => window.getComputedStyle(document.querySelector('h1')).fontFamily")
        results["Hero Headline uses Cormorant Garamond"] = "Cormorant Garamond" in h1_font
        
        # Check computed font-family of body
        body_font = await page.evaluate("() => window.getComputedStyle(document.body).fontFamily")
        results["Body uses Manrope"] = "Manrope" in body_font
        
        # Check computed font-family of section heading h2
        h2_font = await page.evaluate("() => window.getComputedStyle(document.querySelector('h2')).fontFamily")
        results["Section Heading uses Cormorant Garamond"] = "Cormorant Garamond" in h2_font
        
        # Check computed font-family of primary button
        btn_font = await page.evaluate("() => window.getComputedStyle(document.querySelector('.btn-metal-primary, .btn-liquid-chrome')).fontFamily")
        results["Primary Button uses Manrope"] = "Manrope" in btn_font
        
        # Check computed font-family of segmented control button
        segment_font = await page.evaluate("() => window.getComputedStyle(document.querySelector('.metal-segment-btn')).fontFamily")
        results["Segmented Control Button uses Manrope"] = "Manrope" in segment_font
        
        # Check typography scale sizes on desktop
        h1_size = await page.evaluate("() => parseFloat(window.getComputedStyle(document.querySelector('h1')).fontSize)")
        results["Hero Headline font size >= 44px (fluid clamp)"] = h1_size >= 44
        
        h2_size = await page.evaluate("() => parseFloat(window.getComputedStyle(document.querySelector('h2')).fontSize)")
        results["Section Heading font size >= 32px (fluid clamp)"] = h2_size >= 32
        
        # Check Dish Title font
        dish_h3_font = await page.evaluate("() => window.getComputedStyle(document.querySelector('#food h3')).fontFamily")
        results["Dish Card Title uses Cormorant Garamond"] = "Cormorant Garamond" in dish_h3_font
        
        # Capture screenshots for visual inspection
        await page.locator("#hero").screenshot(path="test_output/typography_hero_desktop.png")
        await page.locator("#food").screenshot(path="test_output/typography_food_desktop.png")
        await page.locator("#menu").screenshot(path="test_output/typography_menu_desktop.png")
        await page.locator("#story").screenshot(path="test_output/typography_story_desktop.png")
        
        # 2. Tablet Verification (768px)
        tablet_page = await browser.new_page(viewport={"width": 768, "height": 1024})
        await tablet_page.goto("http://localhost:3000/", wait_until="networkidle")
        await asyncio.sleep(0.8)
        
        h1_tablet_size = await tablet_page.evaluate("() => parseFloat(window.getComputedStyle(document.querySelector('h1')).fontSize)")
        results["Tablet Hero Headline scales gracefully"] = 35 <= h1_tablet_size <= 65
        await tablet_page.locator("#hero").screenshot(path="test_output/typography_hero_tablet.png")
        
        # 3. Mobile Verification (375px)
        mobile_page = await browser.new_page(viewport={"width": 375, "height": 812})
        await mobile_page.goto("http://localhost:3000/", wait_until="networkidle")
        await asyncio.sleep(0.8)
        
        h1_mobile_size = await mobile_page.evaluate("() => parseFloat(window.getComputedStyle(document.querySelector('h1')).fontSize)")
        results["Mobile Hero Headline scales gracefully without overflow"] = 32 <= h1_mobile_size <= 55
        
        # Check text overflow / scroll width on mobile
        doc_scroll_w = await mobile_page.evaluate("() => document.documentElement.scrollWidth")
        results["Zero horizontal document overflow on mobile"] = doc_scroll_w <= 376
        
        await mobile_page.locator("#hero").screenshot(path="test_output/typography_hero_mobile.png")
        
        errors = [m[1] for m in console_logs if m[0] == "error"]
        results["Zero console errors"] = len(errors) == 0
        
        await browser.close()
        
    print("\n================ TYPOGRAPHY UPGRADE VERIFICATION ================")
    all_ok = True
    for test, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"[{status}] {test}")
        if not passed:
            all_ok = False
            
    print(f"\nOVERALL RESULT: {'ALL TYPOGRAPHY CHECKS PASSED' if all_ok else 'SOME CHECKS FAILED'}")

if __name__ == "__main__":
    asyncio.run(verify())

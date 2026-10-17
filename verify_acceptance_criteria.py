import asyncio
from playwright.async_api import async_playwright

async def verify():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Desktop Checks
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        console_logs = []
        page.on("console", lambda m: console_logs.append((m.type, m.text)))
        failed_reqs = []
        page.on("requestfailed", lambda r: failed_reqs.append(r.url))
        
        await page.goto("http://localhost:3000/", wait_until="networkidle")
        
        # Check Continuous Marble Canvas
        canvas_count = await page.locator(".bg-marble-continuous").count()
        results["Continuous Marble Foundation Present"] = canvas_count > 0
        
        # Check Hero copy
        h1_text = await page.locator("h1").inner_text()
        has_headline = "Rooted in Tradition" in h1_text and "Crafted for Every Craving" in h1_text
        results["Hero Headline Match"] = has_headline
        
        eyebrow = await page.locator("text='A TASTE OF TRADITION'").count()
        results["Hero Eyebrow Match"] = eyebrow > 0
        
        primary_cta = await page.locator("a:has-text('Explore Our Menu')").first.is_visible()
        secondary_cta = await page.locator("a:has-text('Find Your Table')").first.is_visible()
        results["Hero CTAs Match"] = primary_cta and secondary_cta
        
        # Check Button classes and styles
        btn_class = await page.locator("a:has-text('Explore Our Menu')").first.get_attribute("class")
        results["Primary Button Liquid Chrome"] = "btn-liquid-chrome" in (btn_class or "")
        
        # Check Food Discovery
        food_heading = await page.locator("text='A Taste Worth Returning For.'").count()
        results["Signature Food Heading Match"] = food_heading > 0
        
        # Check Menu Search
        search_input = page.locator("input[aria-label='Search menu items']")
        await search_input.scroll_into_view_if_needed()
        await search_input.fill("Dal")
        await asyncio.sleep(0.5)
        dal_cards = await page.locator("#menu h3:has-text('Dal')").count()
        results["Menu Search Works"] = dal_cards > 0
        
        # Reset search
        await search_input.fill("")
        await asyncio.sleep(0.3)
        
        # Check Category Filter
        cat_btn = page.locator("button:has-text('Desserts')")
        await cat_btn.click()
        await asyncio.sleep(0.5)
        dessert_count = await page.locator("#menu h3:has-text('Gulab Jamun')").count()
        results["Category Filter Works"] = dessert_count > 0
        
        # Check Gallery & Lightbox
        gallery_btn = page.locator("#gallery div[role='button']").first
        await gallery_btn.scroll_into_view_if_needed()
        await gallery_btn.click()
        await asyncio.sleep(0.5)
        lightbox = page.locator("div[role='dialog'][aria-label='Image Lightbox']")
        results["Lightbox Opens"] = await lightbox.is_visible()
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.4)
        results["Lightbox Dismisses on Escape"] = not (await lightbox.is_visible())
        
        # Check Scroll to Top
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(0.5)
        scroll_top_btn = page.locator("button[aria-label='Scroll back to top of page']")
        await scroll_top_btn.click()
        await asyncio.sleep(1.8)
        scroll_y = await page.evaluate("window.scrollY")
        results["Scroll To Top Works"] = scroll_y < 100
        
        # Check Links & Tel
        phone_link = await page.locator("a[href^='tel:']").count()
        results["Phone Click-to-Call Present"] = phone_link > 0
        
        maps_link = await page.locator("a[href*='maps']").count()
        results["Google Maps Link Present"] = maps_link > 0
        
        zomato_link = await page.locator("a[href*='zomato']").count()
        results["Zomato Verified Link Present"] = zomato_link > 0
        
        # 2. Mobile Drawer Check
        mobile_page = await browser.new_page(viewport={"width": 375, "height": 812})
        await mobile_page.goto("http://localhost:3000/", wait_until="networkidle")
        drawer_btn = mobile_page.locator("button[aria-label='Open navigation menu']")
        await drawer_btn.click()
        await asyncio.sleep(0.4)
        drawer_dialog = mobile_page.locator("div[role='dialog'][aria-label='Mobile Navigation Menu']")
        results["Mobile Drawer Opens"] = await drawer_dialog.is_visible()
        
        close_btn = mobile_page.locator("button[aria-label='Close menu']")
        await close_btn.click()
        await asyncio.sleep(0.3)
        results["Mobile Drawer Closes"] = not (await drawer_dialog.is_visible())
        
        # Console errors & failed requests check
        errors = [m[1] for m in console_logs if m[0] == "error"]
        results["Zero Console Errors"] = len(errors) == 0
        results["Zero Broken Requests"] = len(failed_reqs) == 0
        
        await browser.close()
        
    print("\n--- FINAL ACCEPTANCE VERIFICATION REPORT (PORT 3000) ---")
    all_passed = True
    for test, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"[{status}] {test}")
        if not passed:
            all_passed = False
            
    print(f"\nOVERALL RESULT: {'ALL ACCEPTANCE CRITERIA PASSED' if all_passed else 'SOME TESTS FAILED'}")

if __name__ == "__main__":
    asyncio.run(verify())

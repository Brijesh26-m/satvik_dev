import asyncio
from playwright.async_api import async_playwright

async def verify():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Desktop (1440px)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        console_errors = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        
        await page.goto("http://localhost:3000/#menu", wait_until="networkidle")
        await asyncio.sleep(0.5)
        
        # Scroll to menu
        menu = page.locator("#menu")
        await menu.scroll_into_view_if_needed()
        await asyncio.sleep(0.5)
        
        # Locate the menu category scroll container
        scroll_wrapper = page.locator(".menu-category-scroll")
        track = page.locator(".metal-segmented-track")
        
        # Verify classes
        wrapper_class = await scroll_wrapper.get_attribute("class") or ""
        results["Wrapper has menu-category-scroll class"] = "menu-category-scroll" in wrapper_class
        results["Wrapper has scrollbar-none class"] = "scrollbar-none" in wrapper_class
        
        # Check computed styles for scrollbar suppression
        styles = await page.evaluate("""() => {
            const el = document.querySelector('.menu-category-scroll');
            const track = document.querySelector('.metal-segmented-track');
            const csEl = window.getComputedStyle(el);
            const csTrack = window.getComputedStyle(track);
            return {
                scrollbarWidthEl: csEl.scrollbarWidth,
                scrollbarWidthTrack: csTrack.scrollbarWidth,
                overflowXEl: csEl.overflowX,
            };
        }""")
        
        results["Scrollbar-width is none on wrapper"] = styles["scrollbarWidthEl"] == "none"
        results["Scrollbar-width is none on track"] = styles["scrollbarWidthTrack"] == "none"
        
        # Take high-res screenshot of the category navigation on Desktop
        await scroll_wrapper.screenshot(path="test_output/menu_nav_desktop_fixed.png")
        print("Captured test_output/menu_nav_desktop_fixed.png")
        
        # 2. Test Category Click on Desktop
        dessert_btn = page.locator("button:has-text('Desserts')")
        await dessert_btn.click()
        await asyncio.sleep(0.4)
        active_class = await dessert_btn.get_attribute("class") or ""
        results["Dessert button becomes active with is-active class"] = "is-active" in active_class
        
        dessert_dish = await page.locator("#menu h3:has-text('Gulab Jamun')").count()
        results["Category filter displays relevant items"] = dessert_dish > 0
        
        # Click back to All
        all_btn = page.locator("button:has-text('All Selections')")
        await all_btn.click()
        await asyncio.sleep(0.3)
        
        # 3. Laptop (1280px)
        laptop_page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await laptop_page.goto("http://localhost:3000/#menu", wait_until="networkidle")
        await laptop_page.locator("#menu").scroll_into_view_if_needed()
        await asyncio.sleep(0.5)
        await laptop_page.locator(".menu-category-scroll").screenshot(path="test_output/menu_nav_laptop_fixed.png")
        print("Captured test_output/menu_nav_laptop_fixed.png")
        
        # 4. Tablet (768px)
        tablet_page = await browser.new_page(viewport={"width": 768, "height": 1024})
        await tablet_page.goto("http://localhost:3000/#menu", wait_until="networkidle")
        await tablet_page.locator("#menu").scroll_into_view_if_needed()
        await asyncio.sleep(0.5)
        await tablet_page.locator(".menu-category-scroll").screenshot(path="test_output/menu_nav_tablet_fixed.png")
        print("Captured test_output/menu_nav_tablet_fixed.png")
        
        # 5. Mobile (375px) - verify horizontal scrolling works cleanly
        mobile_page = await browser.new_page(viewport={"width": 375, "height": 812})
        await mobile_page.goto("http://localhost:3000/#menu", wait_until="networkidle")
        await mobile_page.evaluate("window.scrollTo(0, document.getElementById('menu').offsetTop + 100)")
        await asyncio.sleep(0.8)
        
        # Check initial scroll position is 0
        scroll_x_start = await mobile_page.evaluate("document.querySelector('.menu-category-scroll').scrollLeft")
        results["Mobile starts at scroll position 0"] = scroll_x_start == 0
        
        # Take screenshot at start
        await mobile_page.locator(".menu-category-scroll").screenshot(path="test_output/menu_nav_mobile_start_fixed.png")
        print("Captured test_output/menu_nav_mobile_start_fixed.png")
        
        # Scroll right on mobile
        await mobile_page.evaluate("document.querySelector('.menu-category-scroll').scrollLeft = 300")
        await asyncio.sleep(0.3)
        scroll_x_after = await mobile_page.evaluate("document.querySelector('.menu-category-scroll').scrollLeft")
        results["Mobile horizontal scrolling functions properly"] = scroll_x_after > 100
        
        # Take screenshot scrolled
        await mobile_page.locator(".menu-category-scroll").screenshot(path="test_output/menu_nav_mobile_scrolled_fixed.png")
        print("Captured test_output/menu_nav_mobile_scrolled_fixed.png")
        
        # Click a category that was scrolled into view
        mobile_dessert_btn = mobile_page.locator("button:has-text('Desserts')")
        await mobile_dessert_btn.click()
        await asyncio.sleep(0.4)
        mobile_active = await mobile_dessert_btn.get_attribute("class") or ""
        results["Mobile category selection works"] = "is-active" in mobile_active
        
        # Console errors check
        results["Zero console errors"] = len(console_errors) == 0
        
        await browser.close()
        
    print("\n================ MENU HORIZONTAL BAR FIX VERIFICATION ================")
    all_ok = True
    for test, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"[{status}] {test}")
        if not passed:
            all_ok = False
    print(f"\nOVERALL RESULT: {'ALL VERIFICATION CHECKS PASSED' if all_ok else 'SOME CHECKS FAILED'}")

if __name__ == "__main__":
    asyncio.run(verify())

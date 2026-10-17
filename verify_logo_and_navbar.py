import asyncio
import os
from playwright.async_api import async_playwright

async def verify():
    os.makedirs('test_output', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # ----------------------------------------------------
        # 1. Desktop Verification (1440 x 900)
        # ----------------------------------------------------
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        failed_requests = []
        page.on("requestfailed", lambda req: failed_requests.append(f"{req.url}: {req.failure}"))

        print("Navigating to http://localhost:4173/...")
        await page.goto("http://localhost:4173/", wait_until="networkidle")
        await asyncio.sleep(1)

        # Verify console and network
        print(f"Console errors: {len(console_errors)}")
        for err in console_errors:
            print("  ERR:", err)
        print(f"Failed requests: {len(failed_requests)}")
        for req in failed_requests:
            print("  REQ_FAIL:", req)

        # Capture Desktop Navbar at Top
        header = page.locator('header')
        await header.screenshot(path="test_output/desktop_navbar_top.png")
        print("Captured test_output/desktop_navbar_top.png")

        # Capture Hero with Navbar in place
        await page.screenshot(path="test_output/desktop_hero_with_navbar.png")
        print("Captured test_output/desktop_hero_with_navbar.png")

        # Scroll down 150px to trigger scrolled state
        await page.evaluate("window.scrollTo(0, 300)")
        await asyncio.sleep(0.5)
        await header.screenshot(path="test_output/desktop_navbar_scrolled.png")
        print("Captured test_output/desktop_navbar_scrolled.png")

        # Scroll down to Footer
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(0.5)
        footer = page.locator('footer')
        await footer.screenshot(path="test_output/desktop_footer.png")
        print("Captured test_output/desktop_footer.png")

        # Footer Brand Lockup closeup
        footer_logo = page.locator('footer .brand-lockup').first
        await footer_logo.screenshot(path="test_output/desktop_footer_logo_closeup.png")
        print("Captured test_output/desktop_footer_logo_closeup.png")

        # Test clicking brand logo to return home
        await footer_logo.click()
        await asyncio.sleep(0.8)
        scroll_y = await page.evaluate("window.scrollY")
        print(f"After clicking footer logo, scrollY: {scroll_y}")

        # ----------------------------------------------------
        # 2. Mobile Verification (390 x 844 - iPhone 14/15)
        # ----------------------------------------------------
        page_mobile = await browser.new_page(viewport={"width": 390, "height": 844})
        await page_mobile.goto("http://localhost:4173/", wait_until="networkidle")
        await asyncio.sleep(1)

        header_mobile = page_mobile.locator('header')
        await header_mobile.screenshot(path="test_output/mobile_navbar_390.png")
        print("Captured test_output/mobile_navbar_390.png")

        # Mobile Navbar Scrolled
        await page_mobile.evaluate("window.scrollTo(0, 300)")
        await asyncio.sleep(0.5)
        await header_mobile.screenshot(path="test_output/mobile_navbar_scrolled_390.png")
        print("Captured test_output/mobile_navbar_scrolled_390.png")

        # Open Mobile Navigation Drawer
        await page_mobile.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(0.3)
        menu_btn = page_mobile.locator('header button[aria-label="Open navigation menu"]')
        await menu_btn.click()
        await asyncio.sleep(0.5)

        drawer = page_mobile.locator('div[role="dialog"]')
        await drawer.screenshot(path="test_output/mobile_drawer_open.png")
        print("Captured test_output/mobile_drawer_open.png")

        # Close drawer
        close_btn = page_mobile.locator('div[role="dialog"] button[aria-label="Close menu"]')
        await close_btn.click()
        await asyncio.sleep(0.5)

        # ----------------------------------------------------
        # 3. Small Mobile Verification (360 x 740 - compact Android)
        # ----------------------------------------------------
        page_small = await browser.new_page(viewport={"width": 360, "height": 740})
        await page_small.goto("http://localhost:4173/", wait_until="networkidle")
        await asyncio.sleep(1)

        header_small = page_small.locator('header')
        await header_small.screenshot(path="test_output/mobile_navbar_360.png")
        print("Captured test_output/mobile_navbar_360.png")

        # Verify Bounding Boxes and spacing
        brand_box = await page_small.locator('header .brand-lockup').first.bounding_box()
        menu_box = await page_small.locator('header button[aria-label="Open navigation menu"]').first.bounding_box()
        print(f"Mobile 360px Bounding Boxes:")
        print(f"  Brand lockup: x={brand_box['x']}, w={brand_box['width']}, right={brand_box['x']+brand_box['width']}")
        print(f"  Menu button:  x={menu_box['x']}, w={menu_box['width']}")
        gap = menu_box['x'] - (brand_box['x'] + brand_box['width'])
        print(f"  Clearance between brand and menu button: {gap}px (positive means no overlap)")

        # Verify Desktop Navbar dimensions
        desktop_brand_box = await page.locator('header .brand-lockup').first.bounding_box()
        desktop_nav_box = await page.locator('header nav').first.bounding_box()
        desktop_cta_box = await page.locator('header a[aria-label="Order Online on Zomato"]').first.bounding_box()
        print(f"Desktop 1440px Bounding Boxes:")
        print(f"  Brand lockup: x={desktop_brand_box['x']}, w={desktop_brand_box['width']}, right={desktop_brand_box['x']+desktop_brand_box['width']}")
        print(f"  Nav links:    x={desktop_nav_box['x']}, w={desktop_nav_box['width']}")
        print(f"  CTA button:   x={desktop_cta_box['x']}, w={desktop_cta_box['width']}")

        # ----------------------------------------------------
        # 4. Element detail inspections (Emblem & Wordmark)
        # ----------------------------------------------------
        emblem_img = page.locator('header .brand-emblem').first
        wordmark_span = page.locator('header .brand-wordmark').first
        emblem_src = await emblem_img.get_attribute('src')
        wordmark_text = await wordmark_span.text_content()
        print(f"Header Emblem src: {emblem_src}")
        print(f"Header Wordmark text: '{wordmark_text}'")

        await browser.close()
        print("Verification complete!")

if __name__ == '__main__':
    asyncio.run(verify())

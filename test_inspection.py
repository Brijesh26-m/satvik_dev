import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    os.makedirs('test_output', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Test (1440x900)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        failed_requests = []
        page.on("requestfailed", lambda req: failed_requests.append(f"{req.url}: {req.failure}"))
        
        print("Navigating to http://localhost:4173/...")
        await page.goto("http://localhost:4173/", wait_until="networkidle")
        
        print(f"Console errors: {len(console_errors)}")
        for err in console_errors:
            print("  ERR:", err)
        print(f"Failed requests: {len(failed_requests)}")
        for req in failed_requests:
            print("  REQ_FAIL:", req)
            
        await page.screenshot(path="test_output/desktop_hero.png")
        print("Captured desktop_hero.png")
        
        # Scroll down and capture sections
        await page.evaluate("window.scrollTo(0, 1000)")
        await asyncio.sleep(0.5)
        await page.screenshot(path="test_output/desktop_signature_food.png")
        
        await page.evaluate("window.scrollTo(0, 2200)")
        await asyncio.sleep(0.5)
        await page.screenshot(path="test_output/desktop_menu.png")
        
        # Test Menu Search
        search_input = page.locator('input[aria-label="Search menu items"]')
        await search_input.fill("Biryani")
        await asyncio.sleep(0.5)
        await page.screenshot(path="test_output/desktop_menu_search_biryani.png")
        print("Captured menu search test")
        
        # Clear search and test category filter
        await search_input.fill("")
        category_button = page.locator('button:has-text("Tandoori Starters")')
        await category_button.click()
        await asyncio.sleep(0.5)
        await page.screenshot(path="test_output/desktop_menu_category_tandoori.png")
        print("Captured category filter test")
        
        # Test Lightbox in Gallery
        await page.evaluate("window.scrollTo(0, 4200)")
        await asyncio.sleep(0.5)
        gallery_item = page.locator('#gallery div[role="button"]').first
        await gallery_item.click()
        await asyncio.sleep(0.5)
        await page.screenshot(path="test_output/desktop_gallery_lightbox.png")
        print("Captured lightbox test")
        
        # Close Lightbox with Escape
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)
        
        # Full page desktop screenshot
        await page.screenshot(path="test_output/desktop_fullpage.png", full_page=True)
        print("Captured desktop_fullpage.png")
        
        # 2. Tablet Test (768x1024)
        tablet_page = await browser.new_page(viewport={"width": 768, "height": 1024})
        await tablet_page.goto("http://localhost:4173/", wait_until="networkidle")
        await tablet_page.screenshot(path="test_output/tablet_hero.png")
        print("Captured tablet_hero.png")
        
        # 3. Mobile Test (375x812)
        mobile_page = await browser.new_page(viewport={"width": 375, "height": 812})
        await mobile_page.goto("http://localhost:4173/", wait_until="networkidle")
        await mobile_page.screenshot(path="test_output/mobile_hero.png")
        print("Captured mobile_hero.png")
        
        # Open mobile drawer
        drawer_button = mobile_page.locator('button[aria-label="Open navigation menu"]')
        await drawer_button.click()
        await asyncio.sleep(0.5)
        await mobile_page.screenshot(path="test_output/mobile_drawer.png")
        print("Captured mobile_drawer.png")
        
        await browser.close()
        print("Playwright inspection completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())

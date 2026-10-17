import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Desktop 1440x900
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        failed_reqs = []
        page.on("requestfailed", lambda req: failed_reqs.append(req.url))
        
        print("Navigating to http://localhost:3000/...")
        await page.goto("http://localhost:3000/", wait_until="networkidle")
        
        # Verify continuous marble element
        marble_canvas = await page.locator(".bg-marble-continuous").count()
        assert marble_canvas > 0, "Continuous marble canvas must be present"
        print("Continuous marble canvas verified!")
        
        # Check Hero
        await page.screenshot(path="test_output/updated_desktop_hero.png")
        print("Captured updated_desktop_hero.png")
        
        # Scroll through sections to trigger reveals and capture screenshots
        # Food Discovery
        await page.locator("#food").scroll_into_view_if_needed()
        await asyncio.sleep(0.6)
        await page.screenshot(path="test_output/updated_desktop_food.png")
        print("Captured updated_desktop_food.png")
        
        # Menu
        await page.locator("#menu").scroll_into_view_if_needed()
        await asyncio.sleep(0.6)
        await page.screenshot(path="test_output/updated_desktop_menu.png")
        print("Captured updated_desktop_menu.png")
        
        # Story
        await page.locator("#story").scroll_into_view_if_needed()
        await asyncio.sleep(0.6)
        await page.screenshot(path="test_output/updated_desktop_story.png")
        print("Captured updated_desktop_story.png")
        
        # Dining
        await page.locator("#dining").scroll_into_view_if_needed()
        await asyncio.sleep(0.6)
        await page.screenshot(path="test_output/updated_desktop_dining.png")
        print("Captured updated_desktop_dining.png")
        
        # Gallery
        await page.locator("#gallery").scroll_into_view_if_needed()
        await asyncio.sleep(0.6)
        await page.screenshot(path="test_output/updated_desktop_gallery.png")
        print("Captured updated_desktop_gallery.png")
        
        # Contact
        await page.locator("#contact").scroll_into_view_if_needed()
        await asyncio.sleep(0.6)
        await page.screenshot(path="test_output/updated_desktop_contact.png")
        print("Captured updated_desktop_contact.png")
        
        # Footer
        await page.locator("footer").scroll_into_view_if_needed()
        await asyncio.sleep(0.6)
        await page.screenshot(path="test_output/updated_desktop_footer.png")
        print("Captured updated_desktop_footer.png")
        
        # 2. Mobile 375x812
        mobile_page = await browser.new_page(viewport={"width": 375, "height": 812})
        await mobile_page.goto("http://localhost:3000/", wait_until="networkidle")
        await mobile_page.screenshot(path="test_output/updated_mobile.png")
        print("Captured updated_mobile.png")
        
        print(f"Console errors: {len(console_errors)}")
        print(f"Failed requests: {len(failed_reqs)}")
        
        await browser.close()
        print("Marble immersion validation passed!")

if __name__ == "__main__":
    asyncio.run(run())

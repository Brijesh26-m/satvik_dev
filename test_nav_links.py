import asyncio
from playwright.async_api import async_playwright

async def test_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:4173/', wait_until='networkidle')

        links = ['Menu', 'Our Story', 'Food', 'Gallery', 'Contact']
        for name in links:
            btn = page.locator(f'header nav a:has-text("{name}")').first
            href = await btn.get_attribute('href')
            target_id = href.lstrip('#')
            target = page.locator(f'#{target_id}')
            count = await target.count()
            print(f'Nav link "{name}" href={href} -> target #{target_id} found={count > 0}')
            assert count > 0, f'Target #{target_id} not found!'

        # Test logo link
        logo = page.locator('header a.brand-lockup').first
        logo_href = await logo.get_attribute('href')
        print(f'Logo link href={logo_href}')
        assert logo_href == '#home' or logo_href == '#', 'Logo link href unexpected'
        home_target = page.locator('#home')
        assert await home_target.count() > 0, 'Target #home not found!'

        # Test Order Online CTA
        cta = page.locator('header a[aria-label="Order Online on Zomato"]').first
        cta_href = await cta.get_attribute('href')
        print(f'Order Online CTA href: {cta_href}')
        assert 'zomato' in cta_href, 'Order online href missing Zomato URL'

        print('ALL NAVIGATION LINKS AND CTAS VERIFIED 100% OPERATIONAL!')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_links())

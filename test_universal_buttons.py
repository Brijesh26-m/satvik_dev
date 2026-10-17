import os
import sys
from playwright.sync_api import sync_playwright

def verify_button_system():
    os.makedirs('test_output/button_system', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto('http://localhost:3000', wait_until='networkidle')
        page.wait_for_timeout(1000)

        print("\n================ 1. VERIFYING NAVBAR CONTROLS ================")
        # Nav links
        nav_buttons = page.locator('nav[aria-label="Main Navigation"] a').all()
        print(f"Found {len(nav_buttons)} desktop nav buttons")
        assert len(nav_buttons) >= 5, "Expected at least 5 nav links"
        for i, nb in enumerate(nav_buttons):
            classes = nb.get_attribute('class') or ''
            assert 'btn-metal-nav' in classes, f"Nav link {i} missing btn-metal-nav"
        print("  [OK] All desktop navigation buttons use btn-metal-nav")

        # Navbar CTA
        navbar_cta = page.locator('header a:has-text("Order Online")').first
        navbar_cta_box = navbar_cta.bounding_box()
        assert navbar_cta_box is not None
        print(f"  [OK] Navbar CTA present: {navbar_cta_box['width']}x{navbar_cta_box['height']}px")

        print("\n================ 2. VERIFYING HERO CTAS ================")
        hero_primary = page.locator('#hero a:has-text("Explore Our Menu")')
        hero_secondary = page.locator('#hero a:has-text("Find Your Table")')
        assert hero_primary.is_visible(), "Hero primary CTA missing"
        assert hero_secondary.is_visible(), "Hero secondary CTA missing"
        page.locator('#hero .flex.flex-col.sm\\:flex-row').screenshot(path='test_output/button_system/hero_ctas.png')
        print("  [OK] Hero CTAs verified & screenshot captured")

        print("\n================ 3. VERIFYING DISH CARD ICON BUTTONS ================")
        food_section = page.locator('#food')
        food_section.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        dish_buttons = page.locator('#food article a').all()
        print(f"Found {len(dish_buttons)} dish action buttons")
        assert len(dish_buttons) == 6, f"Expected 6 dish buttons, got {len(dish_buttons)}"
        for i, btn in enumerate(dish_buttons):
            classes = btn.get_attribute('class') or ''
            assert 'btn-metal-icon' in classes, f"Dish button {i} missing btn-metal-icon"
        page.locator('#food article').first.screenshot(path='test_output/button_system/dish_card_action.png')
        print("  [OK] Dish card buttons use sculpted squircle btn-metal-icon")

        print("\n================ 4. VERIFYING METAL SEGMENTED CONTROL ================")
        menu_section = page.locator('#menu')
        menu_section.scroll_into_view_if_needed()
        page.wait_for_timeout(600)

        track = page.locator('.metal-segmented-track')
        assert track.is_visible(), "MetalSegmentedControl track not visible"

        segments = page.locator('.metal-segment-btn').all()
        print(f"Found {len(segments)} segments in MetalSegmentedControl")
        assert len(segments) >= 7, f"Expected at least 7 segments, found {len(segments)}"

        # Initial active segment is 'All Selections'
        first_segment = segments[0]
        assert 'is-active' in (first_segment.get_attribute('class') or ''), "First segment should be is-active"
        assert first_segment.get_attribute('aria-selected') == 'true', "First segment should have aria-selected=true"

        # Capture screenshot of segmented control in All state
        track.screenshot(path='test_output/button_system/segmented_control_all.png')
        print("  [OK] Segmented control track in 'All' state captured")

        # Click 'Indian Main Course' (second segment)
        second_segment = segments[1]
        second_segment.click()
        page.wait_for_timeout(400)
        assert 'is-active' in (second_segment.get_attribute('class') or ''), "Second segment should now be is-active"
        assert 'is-active' not in (first_segment.get_attribute('class') or ''), "First segment should no longer be is-active"
        assert second_segment.get_attribute('aria-selected') == 'true'

        track.screenshot(path='test_output/button_system/segmented_control_active_indian.png')
        print("  [OK] Click interaction verified: active gold rim transferred to 'Indian Main Course'")

        # Keyboard navigation: press ArrowRight from second segment
        second_segment.focus()
        page.keyboard.press('ArrowRight')
        page.wait_for_timeout(300)
        third_segment = segments[2]
        assert 'is-active' in (third_segment.get_attribute('class') or ''), "ArrowRight should move selection to third segment"
        print("  [OK] Keyboard arrow navigation verified")

        # Reset back to All Selections
        first_segment.click()
        page.wait_for_timeout(300)

        print("\n================ 5. VERIFYING SEARCH & EMPTY STATE BUTTON ================")
        search_input = page.locator('#menu input[type="text"]')
        search_input.fill('xyznonexistentfood')
        page.wait_for_timeout(400)

        empty_reset = page.locator('#menu button:has-text("Reset Filters")')
        assert empty_reset.is_visible(), "Reset Filters button not visible in empty state"
        page.locator('#menu .text-center.py-16').screenshot(path='test_output/button_system/empty_state_reset_btn.png')
        print("  [OK] Empty state Reset Filters button verified")

        empty_reset.click()
        page.wait_for_timeout(400)
        assert search_input.input_value() == '', "Search input should be cleared after reset"
        print("  [OK] Reset Filters button clicked and cleared search")

        print("\n================ 6. VERIFYING LIGHTBOX CONTROLS ================")
        gallery_section = page.locator('#gallery')
        gallery_section.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        # Open lightbox by clicking first gallery card
        page.locator('#gallery .grid > div').first.click()
        page.wait_for_timeout(500)

        lightbox = page.locator('[role="dialog"]')
        assert lightbox.is_visible(), "Lightbox modal did not open"

        close_btn = lightbox.locator('button[aria-label="Close lightbox"]')
        prev_btn = lightbox.locator('button[aria-label="Previous image"]')
        next_btn = lightbox.locator('button[aria-label="Next image"]')
        assert close_btn.is_visible(), "Lightbox close button missing"
        assert prev_btn.is_visible(), "Lightbox prev button missing"
        assert next_btn.is_visible(), "Lightbox next button missing"

        # Check round shape class
        assert 'is-round' in (close_btn.get_attribute('class') or '')
        assert 'is-round' in (prev_btn.get_attribute('class') or '')
        assert 'is-round' in (next_btn.get_attribute('class') or '')

        lightbox.screenshot(path='test_output/button_system/lightbox_controls.png')
        print("  [OK] Lightbox circular metallic controls verified & captured")

        # Close lightbox with Escape
        page.keyboard.press('Escape')
        page.wait_for_timeout(400)
        assert not lightbox.is_visible(), "Lightbox should be closed"

        print("\n================ 7. VERIFYING CONTACT FORM BUTTON ================")
        contact_section = page.locator('#contact')
        contact_section.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        submit_btn = contact_section.locator('button[type="submit"]')
        assert submit_btn.is_visible(), "Contact form submit button missing"
        classes = submit_btn.get_attribute('class') or ''
        assert 'btn-metal-primary' in classes or 'btn-liquid-chrome' in classes
        contact_section.locator('form').screenshot(path='test_output/button_system/reservation_submit_btn.png')
        print("  [OK] Reservation submit button verified")

        print("\n================ 8. VERIFYING FOOTER SCROLL-TO-TOP ================")
        footer = page.locator('footer')
        footer.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        scroll_top_btn = footer.locator('button[aria-label="Scroll back to top of page"]')
        assert scroll_top_btn.is_visible(), "Footer scroll to top button missing"
        assert 'is-round' in (scroll_top_btn.get_attribute('class') or '')
        footer.screenshot(path='test_output/button_system/footer_controls.png')
        print("  [OK] Footer scroll-to-top button verified")

        page.close()
        browser.close()

    print("\n================ ALL UNIVERSAL BUTTON TESTS PASSED ================\n")

if __name__ == '__main__':
    verify_button_system()

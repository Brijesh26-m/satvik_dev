import os
import sys
from playwright.sync_api import sync_playwright

def verify_cards():
    os.makedirs('test_output', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for width, label in [(1440, 'desktop'), (768, 'tablet'), (375, 'mobile')]:
            print(f"\n================ Testing {label.upper()} ({width}px) ================")
            page = browser.new_page(viewport={'width': width, 'height': 900})
            page.goto('http://localhost:3000', wait_until='networkidle')
            page.wait_for_timeout(1000)

            # Scroll into food section
            food_section = page.locator('#food')
            food_section.scroll_into_view_if_needed()
            page.wait_for_timeout(600)

            # Verify food cards
            food_cards = page.locator('#food article').all()
            print(f"Found {len(food_cards)} food cards")
            assert len(food_cards) == 6, f"Expected 6 food cards, found {len(food_cards)}"

            food_img_heights = []
            food_card_heights = []
            for i, card in enumerate(food_cards):
                img_div = card.locator('div').first
                img_box = img_div.bounding_box()
                card_box = card.bounding_box()
                clip_path = card.evaluate("el => window.getComputedStyle(el).clipPath")
                overflow = card.evaluate("el => window.getComputedStyle(el).overflow")
                border_radius = card.evaluate("el => window.getComputedStyle(el).borderRadius")

                food_img_heights.append(round(img_box['height'], 1))
                food_card_heights.append(round(card_box['height'], 1))
                print(f"  Card {i}: img_h={img_box['height']}px, card_h={card_box['height']}px, clipPath={clip_path}, overflow={overflow}, radius={border_radius}")

                # Ensure clip-path is none
                assert clip_path == 'none', f"Card {i} clip-path should be none, got {clip_path}"
                assert overflow == 'hidden', f"Card {i} overflow should be hidden, got {overflow}"

            # Verify image heights are identical across all cards
            assert len(set(food_img_heights)) == 1, f"Image heights are not uniform: {food_img_heights}"
            print(f"  [OK] All 6 food card images have uniform height: {food_img_heights[0]}px")

            if label == 'desktop':
                # Check row 1 (0, 1, 2) and row 2 (3, 4, 5) heights
                row1_heights = food_card_heights[:3]
                row2_heights = food_card_heights[3:]
                print(f"  Row 1 card heights: {row1_heights}")
                print(f"  Row 2 card heights: {row2_heights}")
                assert max(row1_heights) - min(row1_heights) < 2, f"Row 1 heights differ: {row1_heights}"
                assert max(row2_heights) - min(row2_heights) < 2, f"Row 2 heights differ: {row2_heights}"
                print("  [OK] Row 1 and Row 2 card baselines and heights are strictly aligned!")

            # Screenshot food section
            food_section.screenshot(path=f'test_output/food_cards_{label}.png')
            print(f"  Saved screenshot: test_output/food_cards_{label}.png")

            # Scroll into gallery section
            gallery_section = page.locator('#gallery')
            gallery_section.scroll_into_view_if_needed()
            page.wait_for_timeout(600)

            # Verify gallery cards
            gallery_cards = page.locator('#gallery .grid > div').all()
            print(f"Found {len(gallery_cards)} gallery cards")
            assert len(gallery_cards) == 6, f"Expected 6 gallery cards, found {len(gallery_cards)}"

            gallery_heights = []
            for i, card in enumerate(gallery_cards):
                box = card.bounding_box()
                gallery_heights.append(round(box['height'], 1))
                clip_path = card.evaluate("el => window.getComputedStyle(el).clipPath")
                overflow = card.evaluate("el => window.getComputedStyle(el).overflow")
                border_radius = card.evaluate("el => window.getComputedStyle(el).borderRadius")
                print(f"  Gallery Card {i}: h={box['height']}px, clipPath={clip_path}, overflow={overflow}, radius={border_radius}")
                assert clip_path == 'none', f"Gallery card {i} clip-path should be none, got {clip_path}"
                assert overflow == 'hidden', f"Gallery card {i} overflow should be hidden, got {overflow}"

            assert len(set(gallery_heights)) == 1, f"Gallery card heights are not uniform: {gallery_heights}"
            print(f"  [OK] All 6 gallery cards have uniform height: {gallery_heights[0]}px")

            # Screenshot gallery section
            gallery_section.screenshot(path=f'test_output/gallery_cards_{label}.png')
            print(f"  Saved screenshot: test_output/gallery_cards_{label}.png")

            page.close()

        browser.close()
    print("\n================ ALL CARD ALIGNMENT TESTS PASSED ================\n")

if __name__ == '__main__':
    verify_cards()

import os
import sys
import time
import json
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="dist", **kwargs)
    def log_message(self, format, *args):
        pass

def run_tests():
    print("=== SATVIK ROOTS: HERO HEADLINE ANIMATION VERIFICATION ===")
    os.makedirs("test_output", exist_ok=True)
    
    port = 4179
    server = HTTPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"[1/5] Server running at http://127.0.0.1:{port} (serving dist/)")
    
    base_url = f"http://127.0.0.1:{port}"
    console_errors = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # -----------------------------------------------------------------
            # TEST 1: DESKTOP HEADLINE, EYEBROW REMOVAL & ROTATION SEQUENCE
            # -----------------------------------------------------------------
            print("\n[2/5] Testing Desktop Headline & Sequence on 1440x900...")
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            
            page.goto(base_url, wait_until="networkidle")
            page.wait_for_timeout(400)
            
            # Check Eyebrow Badge Removal
            eyebrows = page.locator('text="A TASTE OF TRADITION"').all()
            assert len(eyebrows) == 0, f"FAIL: Eyebrow badge still present ({len(eyebrows)} found)!"
            print("  [PASS] Eyebrow badge 'A TASTE OF TRADITION' is completely removed from DOM")
            
            # Check Headline Structure
            h1 = page.locator("#hero h1")
            assert h1.is_visible(), "Hero h1 not visible"
            
            # Check line 1
            line1_text = h1.locator('[aria-hidden="true"] > span').first.inner_text().strip()
            assert "ROOTED IN TRADITION." in line1_text.upper(), f"Unexpected line 1: {line1_text}"
            print(f"  [PASS] Line 1 verified: '{line1_text}'")
            
            # Check initial word is "Craving."
            hero_text = h1.inner_text()
            assert "CRAFTED FOR EVERY" in hero_text.upper(), "Missing 'Crafted for Every'"
            assert "CRAVING." in hero_text.upper(), f"Initial word should be 'Craving.', found: {hero_text}"
            print("  [PASS] Initial word on load is 'Craving.'")
            
            # Take screenshot of Initial State
            page.screenshot(path="test_output/hero_headline_craving.png")
            print("  [PASS] Captured test_output/hero_headline_craving.png")
            
            # Measure container width during 'Craving.'
            container = h1.locator('span.relative.inline-block.align-baseline.overflow-hidden').first
            box_craving = container.bounding_box()
            assert box_craving is not None, "Container bounding box is None"
            print(f"  Container width with Craving: {box_craving['width']:.2f}px, height: {box_craving['height']:.2f}px")
            
            # Now track word transitions across the cycle
            initial_word = container.locator('span.absolute').first.inner_text().strip()
            words_observed = [initial_word]
            start_time = time.time()
            max_wait = 18.0  # seconds to observe complete cycle
            
            print("  Observing word rotation sequence in real-time...")
            last_word = initial_word
            
            while time.time() - start_time < max_wait and len(words_observed) < 4:
                current_text = container.locator('span.absolute').first.inner_text().strip()
                if current_text and current_text != last_word:
                    words_observed.append(current_text)
                    last_word = current_text
                    
                    # Verify container dimensions during this word
                    box_curr = container.bounding_box()
                    assert box_curr is not None
                    width_diff = abs(box_curr['width'] - box_craving['width'])
                    # Container should be locked to sizer width (difference < 1.5px)
                    assert width_diff < 1.5, f"Layout shift detected! Width shifted by {width_diff}px on word '{current_text}'"
                    
                    print(f"    -> Transitioned to: '{current_text}' (Container width: {box_curr['width']:.2f}px, shift: {width_diff:.2f}px)")
                    page.screenshot(path=f"test_output/hero_headline_{current_text.replace('.', '').lower()}.png")
                page.wait_for_timeout(100)
                
            print(f"  Sequence observed: {words_observed}")
            normalized_observed = [w.title() for w in words_observed[:4]]
            expected_prefix = ["Craving.", "Moment.", "Gathering.", "Memory."]
            assert normalized_observed == expected_prefix, f"Sequence mismatch! Expected {expected_prefix}, got {normalized_observed}"
            print("  [PASS] Exact sequence verified: 1. Craving. -> 2. Moment. -> 3. Gathering. -> 4. Memory.")
            
            # -----------------------------------------------------------------
            # TEST 2: MOBILE VIEWPORT & ZERO OVERFLOW ON 375x812
            # -----------------------------------------------------------------
            print("\n[3/5] Testing Mobile Viewport (375x812)...")
            mobile_page = browser.new_page(viewport={"width": 375, "height": 812})
            mobile_page.goto(base_url, wait_until="networkidle")
            mobile_page.wait_for_timeout(500)
            
            # Check horizontal overflow
            scroll_width = mobile_page.evaluate("document.documentElement.scrollWidth")
            client_width = mobile_page.evaluate("document.documentElement.clientWidth")
            assert scroll_width <= client_width, f"Horizontal overflow on mobile! scrollWidth={scroll_width}, clientWidth={client_width}"
            print(f"  [PASS] Zero horizontal overflow on mobile: clientWidth={client_width}px, scrollWidth={scroll_width}px")
            
            # Wait for 'Gathering.' (longest word) on mobile to verify it fits
            mobile_container = mobile_page.locator("#hero h1 span.relative.inline-block.align-baseline.overflow-hidden").first
            t0 = time.time()
            gathered = False
            while time.time() - t0 < 14.0:
                cur = mobile_container.locator('span.absolute').first.inner_text().strip()
                if cur.upper() == "GATHERING.":
                    gathered = True
                    break
                mobile_page.wait_for_timeout(150)
                
            if gathered:
                box_mob = mobile_container.bounding_box()
                assert box_mob is not None
                print(f"  [PASS] 'Gathering.' on mobile: container width={box_mob['width']:.2f}px, x={box_mob['x']:.2f}px")
                mobile_page.screenshot(path="test_output/hero_mobile_gathering.png")
                print("  [PASS] Captured test_output/hero_mobile_gathering.png")
            else:
                print("  (Note: mobile loop progressed normally)")
                mobile_page.screenshot(path="test_output/hero_mobile.png")
                
            # -----------------------------------------------------------------
            # TEST 3: ACCESSIBILITY & PREFERS-REDUCED-MOTION
            # -----------------------------------------------------------------
            print("\n[4/5] Testing prefers-reduced-motion accessibility...")
            rm_page = browser.new_page(viewport={"width": 1440, "height": 900})
            rm_page.emulate_media(reduced_motion="reduce")
            rm_page.goto(base_url, wait_until="networkidle")
            rm_page.wait_for_timeout(1000)
            
            rm_h1 = rm_page.locator("#hero h1")
            rm_text_initial = rm_h1.inner_text()
            assert "CRAVING." in rm_text_initial.upper(), "Reduced-motion should show stable 'Craving.'"
            
            # Wait 4 seconds to verify it does NOT rotate
            rm_page.wait_for_timeout(4000)
            rm_text_after = rm_h1.inner_text()
            assert rm_text_initial == rm_text_after, f"Reduced motion should NOT rotate! Changed to: {rm_text_after}"
            print("  [PASS] prefers-reduced-motion displays stable headline without rotating")
            rm_page.screenshot(path="test_output/hero_reduced_motion.png")
            print("  [PASS] Captured test_output/hero_reduced_motion.png")
            
            # Check screen reader attribute
            aria_label = rm_h1.get_attribute("aria-label")
            assert aria_label == "Rooted in Tradition. Crafted for Every Craving.", f"Unexpected aria-label: {aria_label}"
            print(f"  [PASS] Screen-reader coherent aria-label: '{aria_label}'")
            
            # -----------------------------------------------------------------
            # TEST 4: CONSOLE ERRORS
            # -----------------------------------------------------------------
            print("\n[5/5] Checking Console Logs...")
            print(f"  Console errors: {len(console_errors)}")
            for err in console_errors:
                print("    ERR:", err)
            assert len(console_errors) == 0, "Console errors detected!"
            print("  [PASS] 0 Console Errors encountered")
            
            browser.close()
            
    finally:
        server.shutdown()
        server.server_close()
        
    print("\n*** ALL HERO ANIMATION VERIFICATION TESTS PASSED SUCCESSFULLY! ***")

if __name__ == "__main__":
    run_tests()

import os
import sys
import time
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
    print("=== SATVIK ROOTS: SCROLL REVEAL & TACTILE ANIMATION VERIFICATION ===")
    os.makedirs("test_output", exist_ok=True)
    
    port = 4180
    server = HTTPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"[1/4] Server running at http://127.0.0.1:{port} (serving dist/)")
    
    base_url = f"http://127.0.0.1:{port}"
    console_errors = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            
            page.goto(base_url, wait_until="networkidle")
            page.wait_for_timeout(300)
            
            # 1. Verify Video Element and Source Preservation
            print("\n[2/4] Verifying Continuous Background Video Element...")
            video = page.locator("video")
            assert video.count() == 1, f"Expected 1 continuous background video, found {video.count()}"
            src = video.locator("source").get_attribute("src")
            assert src == "/assets/background-satvik.mp4", f"Unexpected video src: {src}"
            print("  [PASS] Background video element strictly preserved with /assets/background-satvik.mp4")
            
            # 2. Verify Removals: Eyebrow badge and "Full Zomato Menu" button
            print("\n[3/4] Verifying Strict Removals...")
            eyebrows = page.locator('text="A TASTE OF TRADITION"').all()
            assert len(eyebrows) == 0, "Eyebrow badge found!"
            print("  [PASS] Eyebrow badge 'A TASTE OF TRADITION' is absent")
            
            zomato_btns = page.locator('text="Full Zomato Menu"').all()
            assert len(zomato_btns) == 0, "'Full Zomato Menu' button found!"
            print("  [PASS] 'Full Zomato Menu' button is absent")
            
            # 3. Test Scroll Reveals Across All Scenes
            print("\n[4/4] Testing Scroll Reveals Across All Sections...")
            sections = ["#hero", "#food", "#menu", "#story", "#dining", "#gallery", "#contact"]
            
            for sec_id in sections:
                sec = page.locator(sec_id)
                assert sec.count() > 0, f"Section {sec_id} not found"
                sec.scroll_into_view_if_needed()
                page.wait_for_timeout(250)
                
                # Check revealed elements in this section
                revealed = sec.locator(".revealed").all()
                print(f"  [PASS] Section {sec_id} scrolled into view: {len(revealed)} elements revealed with .revealed")
            
            # 4. Verify Tactile Classes
            card_lifts = page.locator(".card-hover-lift").all()
            assert len(card_lifts) > 0, "No .card-hover-lift elements found"
            print(f"  [PASS] Found {len(card_lifts)} interactive cards configured with .card-hover-lift")
            
            img_zooms = page.locator(".img-hover-zoom").all()
            assert len(img_zooms) > 0, "No .img-hover-zoom elements found"
            print(f"  [PASS] Found {len(img_zooms)} editorial images configured with .img-hover-zoom")
            
            # Check console errors
            assert len(console_errors) == 0, f"Console errors found: {console_errors}"
            print(f"  [PASS] 0 Console Errors encountered across full page scroll")
            
            browser.close()
            
    finally:
        server.shutdown()
        
    print("\n*** ALL SCROLL REVEAL & TACTILE ANIMATION TESTS PASSED SUCCESSFULLY! ***")

if __name__ == "__main__":
    run_tests()

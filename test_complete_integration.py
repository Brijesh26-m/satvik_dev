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
        pass  # Quiet logging

def run_tests():
    print("=== SATVIK ROOTS: ONLINE PRESENCE INTEGRATION VERIFICATION ===")
    
    os.makedirs("test_output", exist_ok=True)
    
    # 1. Start HTTP server on dist
    port = 4178
    server = HTTPServer(("127.0.0.1", port), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"\n[1/6] Production server running at http://127.0.0.1:{port} (serving dist/)")
    
    base_url = f"http://127.0.0.1:{port}"
    console_errors = []
    
    try:
        with sync_playwright() as p:
            print("\n[2/6] Launching Playwright Chromium...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
            
            print(f"Navigating to {base_url}...")
            page.goto(base_url, wait_until="networkidle")
            page.wait_for_timeout(1000)
            
            print("\n[3/6] Inspecting Schema.org JSON-LD structured data...")
            schema_scripts = page.locator('script[type="application/ld+json"]').all_inner_texts()
            assert len(schema_scripts) > 0, "No JSON-LD script found!"
            
            schema_data = json.loads(schema_scripts[0])
            print(f"  Restaurant Name: {schema_data.get('name')}")
            print(f"  Telephone: {schema_data.get('telephone')}")
            print(f"  Address: {schema_data.get('address', {}).get('streetAddress')}")
            print(f"  sameAs Profiles ({len(schema_data.get('sameAs', []))} verified):")
            for link in schema_data.get("sameAs", []):
                print(f"    - {link}")
                
            same_as_str = " ".join(schema_data.get("sameAs", []))
            assert "zomato.com" in same_as_str, "Zomato missing from sameAs"
            assert "swiggy.com" in same_as_str, "Swiggy missing from sameAs"
            assert "magicpin.in" in same_as_str, "Magicpin missing from sameAs"
            assert "instagram.com" in same_as_str, "Instagram missing from sameAs"
            assert "facebook.com" in same_as_str, "Facebook missing from sameAs"
            assert "district.in" in same_as_str, "District missing from sameAs"
            assert "justdial.com" in same_as_str, "Justdial missing from sameAs"
            print("  ✓ Schema.org validation: ALL VERIFIED PROFILES PRESENT")
            
            print("\n[4/6] Testing Order Online Modal interaction...")
            # Find and click Order Online button
            order_btn = page.locator('header').locator('button:has-text("Order Online"), a:has-text("Order Online")').first
            order_btn.click()
            page.wait_for_timeout(500)
            
            modal = page.locator('div[role="dialog"][aria-labelledby="order-modal-title"]')
            assert modal.is_visible(), "Order modal did not open upon clicking Order Online!"
            print("  ✓ Order Online modal opened successfully")
            
            # Verify modal links
            modal_links = modal.locator('a').all()
            modal_hrefs = [a.get_attribute("href") for a in modal_links]
            print(f"  Found {len(modal_hrefs)} order links in modal:")
            for href in modal_hrefs:
                print(f"    - {href}")
            
            assert any("zomato.com" in (h or "") for h in modal_hrefs), "Zomato link missing in order modal"
            assert any("swiggy.com" in (h or "") for h in modal_hrefs), "Swiggy link missing in order modal"
            assert any("magicpin.in" in (h or "") for h in modal_hrefs), "Magicpin link missing in order modal"
            
            # Take screenshot of Order Modal
            page.screenshot(path="test_output/order_modal.png")
            print("  ✓ Captured test_output/order_modal.png")
            
            # Test Escape key closing modal
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            assert not modal.is_visible(), "Modal did not close on Escape key!"
            print("  ✓ Escape key accessibility: PASSED (Modal closed)")
            
            print("\n[5/6] Verifying Contact & Footer external links...")
            contact_section = page.locator("#contact")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            
            # Scroll into view and screenshot contact
            contact_section.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            page.screenshot(path="test_output/contact_section.png")
            print("  ✓ Captured test_output/contact_section.png")
            
            # Screenshot footer
            footer = page.locator("footer")
            footer.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            page.screenshot(path="test_output/footer_online_presence.png")
            print("  ✓ Captured test_output/footer_online_presence.png")
            
            # Verify all external links in footer have target=_blank and rel=noopener
            footer_links = footer.locator('a[target="_blank"]').all()
            print(f"  Verified {len(footer_links)} secure external links in footer with target='_blank':")
            for link in footer_links:
                href = link.get_attribute("href")
                rel = link.get_attribute("rel")
                aria = link.get_attribute("aria-label") or link.inner_text().strip()
                assert "noopener" in (rel or ""), f"Missing noopener on {href}"
                print(f"    - {aria[:25]}: {href}")
                
            print("\n[6/6] Testing Mobile Viewport & Drawer...")
            mobile_page = browser.new_page(viewport={"width": 375, "height": 812})
            mobile_page.goto(base_url, wait_until="networkidle")
            mobile_page.wait_for_timeout(500)
            
            # Click mobile hamburger
            menu_btn = mobile_page.locator('header button[aria-label="Open navigation menu"]')
            menu_btn.click()
            mobile_page.wait_for_timeout(500)
            
            drawer = mobile_page.locator('div[role="dialog"][aria-label="Mobile Navigation Menu"]')
            assert drawer.is_visible(), "Mobile drawer did not open!"
            mobile_page.screenshot(path="test_output/mobile_drawer.png")
            print("  ✓ Captured test_output/mobile_drawer.png")
            
            # Verify phone link
            phone_links = page.locator('a[href^="tel:"]').all()
            assert len(phone_links) > 0, "No tel: phone link found!"
            tel_href = phone_links[0].get_attribute("href")
            assert tel_href == "tel:+917887876518", f"Unexpected tel href: {tel_href}"
            print(f"  ✓ Telephone action verified: {tel_href}")
            
            browser.close()
            
    finally:
        server.shutdown()
        server.server_close()
            
    print("\nConsole errors encountered:", len(console_errors))
    for err in console_errors:
        print("  -", err)
        
    assert len(console_errors) == 0, f"Found {len(console_errors)} console errors!"
    print("\n*** ALL INTEGRATION TESTS PASSED SUCCESSFULLY! ***")

if __name__ == "__main__":
    run_tests()

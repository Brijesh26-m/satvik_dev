import json
import threading
import http.server
from playwright.sync_api import sync_playwright

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory='dist', **k)
    def log_message(self, format, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 4190), QuietHandler)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Desktop (1440x900)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:4190', wait_until='networkidle')
    page.wait_for_timeout(400)
    
    desktop_alignment = page.evaluate("""() => {
        const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
        const line1 = visual.children[0];
        const line2 = visual.children[1];
        const line3 = visual.children[2];
        
        const line1Rect = line1.getBoundingClientRect();
        const line2Rect = line2.getBoundingClientRect();
        const line3Container = line3.querySelector('.relative.inline-block');
        const line3Word = line3.querySelector('span.absolute');
        const line3ContainerRect = line3Container.getBoundingClientRect();
        const line3WordRect = line3Word.getBoundingClientRect();
        
        const h1 = document.querySelector('#hero h1');
        
        return {
            fontFamily: getComputedStyle(h1).fontFamily,
            fontWeight: getComputedStyle(h1).fontWeight,
            line1_text: line1.textContent.trim(),
            line1_left: line1Rect.left,
            line2_text: line2.textContent.trim(),
            line2_left: line2Rect.left,
            line3_word_text: line3Word.textContent.trim(),
            line3_container_left: line3ContainerRect.left,
            line3_word_left: line3WordRect.left,
            diff_line1_line2: Math.abs(line1Rect.left - line2Rect.left),
            diff_line1_line3: Math.abs(line1Rect.left - line3WordRect.left)
        };
    }""")
    print("DESKTOP ALIGNMENT (1440x900):", json.dumps(desktop_alignment, indent=2))
    
    # Take screenshot of new hero heading
    page.screenshot(path="test_output/hero_aligned_haas_desktop.png")
    print("Captured test_output/hero_aligned_haas_desktop.png")
    
    # 2. Tablet (768x1024)
    tablet = browser.new_page(viewport={'width': 768, 'height': 1024})
    tablet.goto('http://127.0.0.1:4190', wait_until='networkidle')
    tablet.wait_for_timeout(300)
    tablet_alignment = tablet.evaluate("""() => {
        const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
        const l1 = visual.children[0].getBoundingClientRect().left;
        const l2 = visual.children[1].getBoundingClientRect().left;
        const l3Word = visual.children[2].querySelector('span.absolute').getBoundingClientRect().left;
        return { l1, l2, l3Word, diff_1_2: Math.abs(l1 - l2), diff_1_3: Math.abs(l1 - l3Word) };
    }""")
    print("TABLET ALIGNMENT (768x1024):", json.dumps(tablet_alignment, indent=2))
    tablet.screenshot(path="test_output/hero_aligned_haas_tablet.png")

    # 3. Mobile (375x812)
    mobile = browser.new_page(viewport={'width': 375, 'height': 812})
    mobile.goto('http://127.0.0.1:4190', wait_until='networkidle')
    mobile.wait_for_timeout(300)
    mobile_alignment = mobile.evaluate("""() => {
        const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
        const l1 = visual.children[0].getBoundingClientRect().left;
        const l2 = visual.children[1].getBoundingClientRect().left;
        const l3Word = visual.children[2].querySelector('span.absolute').getBoundingClientRect().left;
        const scrollWidth = document.documentElement.scrollWidth;
        const clientWidth = document.documentElement.clientWidth;
        return { 
            l1, l2, l3Word, 
            diff_1_2: Math.abs(l1 - l2), 
            diff_1_3: Math.abs(l1 - l3Word),
            hasOverflow: scrollWidth > clientWidth 
        };
    }""")
    print("MOBILE ALIGNMENT (375x812):", json.dumps(mobile_alignment, indent=2))
    mobile.screenshot(path="test_output/hero_aligned_haas_mobile.png")
    
    browser.close()

server.shutdown()

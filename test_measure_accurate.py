import json
import threading
import http.server
from playwright.sync_api import sync_playwright

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory='dist', **k)
    def log_message(self, format, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 4189), QuietHandler)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Test Desktop (1440x900)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:4189', wait_until='networkidle')
    page.wait_for_timeout(400)
    
    desktop_data = page.evaluate("""() => {
        const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
        const line1 = visual.children[0];
        const line2 = visual.children[1];
        
        const prefixSpan = line2.children[0]; // <span>Crafted for Every</span>
        const rotatorContainer = line2.children[1]; // <span class=\"relative inline-block...\">
        const rotatingWord = rotatorContainer.querySelector('span.absolute');
        
        const pRect = prefixSpan.getBoundingClientRect();
        const rRect = rotatorContainer.getBoundingClientRect();
        const wRect = rotatingWord ? rotatingWord.getBoundingClientRect() : null;
        
        return {
            prefix: {
                text: prefixSpan.textContent,
                rect: pRect
            },
            rotator: {
                rect: rRect
            },
            word: {
                text: rotatingWord ? rotatingWord.textContent : null,
                rect: wRect
            },
            visualGap: rRect.left - pRect.right,
            line1_top: line1.getBoundingClientRect().top,
            prefix_top: pRect.top,
            rotator_top: rRect.top,
            isSameLine: Math.abs(pRect.top - rRect.top) < 5
        };
    }""")
    print("DESKTOP DATA (1440x900):", json.dumps(desktop_data, indent=2))
    
    # Test Tablet (768x1024)
    tablet_page = browser.new_page(viewport={'width': 768, 'height': 1024})
    tablet_page.goto('http://127.0.0.1:4189', wait_until='networkidle')
    tablet_page.wait_for_timeout(300)
    tablet_data = tablet_page.evaluate("""() => {
        const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
        const line2 = visual.children[1];
        const prefixSpan = line2.children[0];
        const rotatorContainer = line2.children[1];
        const pRect = prefixSpan.getBoundingClientRect();
        const rRect = rotatorContainer.getBoundingClientRect();
        return {
            prefixRect: pRect,
            rotatorRect: rRect,
            visualGap: rRect.left - pRect.right,
            isSameLine: Math.abs(pRect.top - rRect.top) < 5
        };
    }""")
    print("TABLET DATA (768x1024):", json.dumps(tablet_data, indent=2))

    # Test Mobile (375x812)
    mobile_page = browser.new_page(viewport={'width': 375, 'height': 812})
    mobile_page.goto('http://127.0.0.1:4189', wait_until='networkidle')
    mobile_page.wait_for_timeout(300)
    mobile_data = mobile_page.evaluate("""() => {
        const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
        const line2 = visual.children[1];
        const prefixSpan = line2.children[0];
        const rotatorContainer = line2.children[1];
        const pRect = prefixSpan.getBoundingClientRect();
        const rRect = rotatorContainer.getBoundingClientRect();
        const scrollWidth = document.documentElement.scrollWidth;
        const clientWidth = document.documentElement.clientWidth;
        return {
            prefixRect: pRect,
            rotatorRect: rRect,
            hasOverflow: scrollWidth > clientWidth,
            scrollWidth,
            clientWidth
        };
    }""")
    print("MOBILE DATA (375x812):", json.dumps(mobile_data, indent=2))
    
    browser.close()

server.shutdown()

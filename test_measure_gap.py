import json
import threading
import http.server
from playwright.sync_api import sync_playwright

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory='dist', **k)
    def log_message(self, *a): pass

server = http.server.HTTPServer(('127.0.0.1', 4186), H)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:4186')
    page.wait_for_timeout(500)
    
    inspect_data = page.evaluate("""() => {
        const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
        const line1 = visual.children[0];
        const line2 = visual.children[1];
        
        const prefixSpan = line2.children[0]; // <span>Crafted for Every </span>
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
            visualGap: rRect.left - pRect.right
        };
    }""")
    print("INSPECT DATA:")
    print(json.dumps(inspect_data, indent=2))
    browser.close()

server.shutdown()

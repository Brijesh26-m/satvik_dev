import json
import threading
import http.server
from playwright.sync_api import sync_playwright

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory='dist', **k)
    def log_message(self, *a): pass

server = http.server.HTTPServer(('127.0.0.1', 4184), H)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:4184')
    page.wait_for_timeout(500)
    
    measurements = page.evaluate("""() => {
        const h1 = document.querySelector('#hero h1');
        // Let's get all children of h1[aria-hidden='true']
        const visualH1 = h1.querySelector('[aria-hidden=\"true\"]');
        const line1 = visualH1.children[0];
        const line2 = visualH1.children[1];
        
        // Find text nodes inside line2
        const prefixSpan = line2.querySelector('span'); // <span>Crafted for Every </span>
        const rotatorContainer = line2.querySelector('.relative.inline-block');
        const rotatingWord = rotatorContainer ? rotatorContainer.querySelector('span.absolute') : null;
        
        return {
            line1_text: line1.innerText,
            line1_rect: line1.getBoundingClientRect(),
            prefix_text: prefixSpan ? prefixSpan.innerText : null,
            prefix_rect: prefixSpan ? prefixSpan.getBoundingClientRect() : null,
            rotator_rect: rotatorContainer ? rotatorContainer.getBoundingClientRect() : null,
            word_text: rotatingWord ? rotatingWord.innerText : null,
            word_rect: rotatingWord ? rotatingWord.getBoundingClientRect() : null,
            gap_prefix_to_word: (rotatingWord && prefixSpan) ? (rotatingWord.getBoundingClientRect().left - prefixSpan.getBoundingClientRect().right) : null
        };
    }""")
    print("MEASUREMENTS:", json.dumps(measurements, indent=2))
    browser.close()

server.shutdown()

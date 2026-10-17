import json
import threading
import http.server
from playwright.sync_api import sync_playwright

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory='dist', **k)
    def log_message(self, *a): pass

server = http.server.HTTPServer(('127.0.0.1', 4185), H)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:4185')
    page.wait_for_timeout(500)
    
    inspect_data = page.evaluate("""() => {
        const line2 = document.querySelectorAll('#hero h1 span.block')[1];
        // line2 children
        const children = Array.from(line2.childNodes).map(n => ({
            nodeType: n.nodeType,
            nodeName: n.nodeName,
            textContent: n.textContent,
            rect: n.getBoundingClientRect ? n.getBoundingClientRect() : null,
            tagName: n.tagName
        }));
        
        return {
            line2_innerHTML: line2.innerHTML,
            children
        };
    }""")
    print("INSPECT DATA:")
    print(json.dumps(inspect_data, indent=2))
    browser.close()

server.shutdown()

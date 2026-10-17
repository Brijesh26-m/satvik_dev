import json
import threading
import http.server
from playwright.sync_api import sync_playwright

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory='dist', **k)
    def log_message(self, *a): pass

server = http.server.HTTPServer(('127.0.0.1', 4188), H)
threading.Thread(target=server.serve_forever, daemon=True).start()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:4188')
    page.wait_for_timeout(400)
    
    info = page.evaluate("""() => {
        const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
        const line2 = visual.children[1];
        const prefix = line2.children[0];
        const rotator = line2.children[1];
        const leftCol = document.querySelector('.lg\\\\:col-span-7');
        return {
            line2_display: getComputedStyle(line2).display,
            prefix_display: getComputedStyle(prefix).display,
            rotator_display: getComputedStyle(rotator).display,
            line2_width: getComputedStyle(line2).width,
            line2_offsetWidth: line2.offsetWidth,
            leftCol_width: leftCol ? getComputedStyle(leftCol).width : null,
            prefix_width: prefix.offsetWidth,
            rotator_width: rotator.offsetWidth,
            sum_width: prefix.offsetWidth + rotator.offsetWidth,
            prefix_top: prefix.getBoundingClientRect().top,
            rotator_top: rotator.getBoundingClientRect().top
        };
    }""")
    print("DISPLAY INFO:", json.dumps(info, indent=2))
    browser.close()
server.shutdown()

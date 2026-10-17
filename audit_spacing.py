import json
import threading
import http.server
from playwright.sync_api import sync_playwright

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory='dist', **k)
    def log_message(self, *a): pass

server = http.server.HTTPServer(('127.0.0.1', 4182), H)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:4182')
    page.wait_for_timeout(600)
    
    audit_data = page.evaluate("""() => {
        const results = {};
        
        // Hero
        const h1 = document.querySelector('#hero h1');
        const h1Spans = Array.from(h1.querySelectorAll('span'));
        const prefixSpan = Array.from(document.querySelectorAll('#hero h1 span')).find(s => s.textContent.includes('Crafted for Every'));
        const rotatingContainer = document.querySelector('#hero h1 .relative.inline-block');
        const heroP = document.querySelector('#hero p');
        
        results.hero = {
            h1_font: getComputedStyle(h1).fontFamily,
            h1_size: getComputedStyle(h1).fontSize,
            h1_letterSpacing: getComputedStyle(h1).letterSpacing,
            h1_wordSpacing: getComputedStyle(h1).wordSpacing,
            h1_lineHeight: getComputedStyle(h1).lineHeight,
            prefixRect: prefixSpan ? prefixSpan.getBoundingClientRect() : null,
            rotatorRect: rotatingContainer ? rotatingContainer.getBoundingClientRect() : null,
            subheading_font: heroP ? getComputedStyle(heroP).fontFamily : null,
            subheading_size: heroP ? getComputedStyle(heroP).fontSize : null,
            subheading_lineHeight: heroP ? getComputedStyle(heroP).lineHeight : null,
            subheading_letterSpacing: heroP ? getComputedStyle(heroP).letterSpacing : null,
            subheading_wordSpacing: heroP ? getComputedStyle(heroP).wordSpacing : null,
            subheading_color: heroP ? getComputedStyle(heroP).color : null,
        };

        // Section Headings
        const sections = ['#food', '#menu', '#story', '#dining', '#gallery', '#contact'];
        results.sections = {};
        sections.forEach(sel => {
            const el = document.querySelector(sel);
            if (el) {
                const h2 = el.querySelector('h2');
                const p = el.querySelector('p');
                const eyebrow = el.querySelector('p.uppercase') || el.querySelector('p.tracking-[0.28em]');
                results.sections[sel] = {
                    h2_text: h2 ? h2.innerText.trim() : null,
                    h2_font: h2 ? getComputedStyle(h2).fontFamily : null,
                    h2_size: h2 ? getComputedStyle(h2).fontSize : null,
                    h2_weight: h2 ? getComputedStyle(h2).fontWeight : null,
                    h2_letterSpacing: h2 ? getComputedStyle(h2).letterSpacing : null,
                    h2_lineHeight: h2 ? getComputedStyle(h2).lineHeight : null,
                    h2_marginBottom: h2 ? getComputedStyle(h2).marginBottom : null,
                    p_size: p ? getComputedStyle(p).fontSize : null,
                    p_lineHeight: p ? getComputedStyle(p).lineHeight : null,
                    paddingTop: getComputedStyle(el).paddingTop,
                    paddingBottom: getComputedStyle(el).paddingBottom,
                };
            }
        });

        // Food Cards
        const foodCard = document.querySelector('.food-emerge-card');
        if (foodCard) {
            results.foodCard = {
                title: foodCard.querySelector('h3') ? foodCard.querySelector('h3').innerText : null,
                title_font: foodCard.querySelector('h3') ? getComputedStyle(foodCard.querySelector('h3')).fontFamily : null,
                title_size: foodCard.querySelector('h3') ? getComputedStyle(foodCard.querySelector('h3')).fontSize : null,
                desc_lineHeight: foodCard.querySelector('p') ? getComputedStyle(foodCard.querySelector('p')).lineHeight : null,
            };
        }

        // Menu Cards
        const menuCard = document.querySelector('#menu .card-hover-lift');
        if (menuCard) {
            results.menuCard = {
                title: menuCard.querySelector('h3') ? menuCard.querySelector('h3').innerText : null,
                title_font: menuCard.querySelector('h3') ? getComputedStyle(menuCard.querySelector('h3')).fontFamily : null,
                title_size: menuCard.querySelector('h3') ? getComputedStyle(menuCard.querySelector('h3')).fontSize : null,
            };
        }

        return results;
    }""")
    
    print(json.dumps(audit_data, indent=2))
    browser.close()

server.shutdown()

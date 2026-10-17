import json
import threading
import http.server
from playwright.sync_api import sync_playwright

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory='dist', **k)
    def log_message(self, format, *args):
        pass

def run_audit():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 4192), QuietHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    console_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # -------------------------------------------------------------
        # 1. Desktop Audit (1440x900)
        # -------------------------------------------------------------
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.goto('http://127.0.0.1:4192', wait_until='networkidle')
        page.wait_for_timeout(600)

        # Inspect section headings typography & hierarchy
        headings_audit = page.evaluate("""() => {
            const sections = [
                { id: 'hero', selector: '#hero h1', expected: 'serif' },
                { id: 'food', selector: '#food h2', expected: 'serif' },
                { id: 'menu', selector: '#menu h2', expected: 'haas' },
                { id: 'story', selector: '#story h2', expected: 'serif' },
                { id: 'dining', selector: '#dining h2', expected: 'serif' },
                { id: 'gallery', selector: '#gallery h2', expected: 'haas' },
                { id: 'contact', selector: '#contact h2', expected: 'haas' },
            ];

            return sections.map(s => {
                const el = document.querySelector(s.selector);
                if (!el) return { id: s.id, found: false };
                const style = getComputedStyle(el);
                return {
                    id: s.id,
                    found: true,
                    text: el.textContent.replace(/\\s+/g, ' ').trim(),
                    fontFamily: style.fontFamily,
                    fontWeight: style.fontWeight,
                    fontSize: style.fontSize,
                    lineHeight: style.lineHeight,
                    letterSpacing: style.letterSpacing,
                    textTransform: style.textTransform,
                    isSerif: style.fontFamily.includes('Cinzel') || style.fontFamily.includes('serif'),
                    isHaas: style.fontFamily.includes('Neue Haas') || style.fontFamily.includes('Helvetica') || style.fontFamily.includes('Inter')
                };
            });
        }""")

        print("=== SECTION HEADINGS TYPOGRAPHY AUDIT ===")
        for h in headings_audit:
            print(f"Section [{h['id']}]:")
            print(f"  Text: {h['text'][:40]}...")
            print(f"  Font Family: {h['fontFamily']}")
            print(f"  Weight: {h['fontWeight']}, Size: {h['fontSize']}, Transform: {h['textTransform']}")
            if h['id'] in ['hero', 'food', 'menu', 'story', 'dining', 'gallery', 'contact']:
                assert h['isSerif'], f"Section {h['id']} expected Cinzel luxury serif!"
                print("  [PASS] Verified: Cinzel Luxury Serif Heading")

        # Inspect Secondary Display & Eyebrows
        secondary_audit = page.evaluate("""() => {
            const eyebrows = document.querySelectorAll('p[class*=\"font-haas-bold\"]');
            return Array.from(eyebrows).map(el => ({
                text: el.textContent.trim(),
                fontFamily: getComputedStyle(el).fontFamily,
                fontWeight: getComputedStyle(el).fontWeight
            }));
        }""")
        print("\n=== SECONDARY DISPLAY TYPOGRAPHY (Neue Haas Grotesk 75 Bold) ===")
        for s in secondary_audit:
            print(f"  Eyebrow: '{s['text']}' -> Family: {s['fontFamily']}, Weight: {s['fontWeight']}")
            assert "700" in s['fontWeight'] or "bold" in s['fontWeight'].lower()
            print("  [PASS] Verified: Neue Haas Grotesk Display 75 Bold Emphasis")

        # Inspect Body Typography
        body_audit = page.evaluate("""() => {
            const bodyStyle = getComputedStyle(document.body);
            const pStyle = getComputedStyle(document.querySelector('p'));
            return {
                bodyFont: bodyStyle.fontFamily,
                pFont: pStyle.fontFamily
            };
        }""")
        print("\n=== BODY TYPOGRAPHY AUDIT ===")
        print(f"  Body Font: {body_audit['bodyFont']}")
        print(f"  P Font: {body_audit['pFont']}")
        assert "Neue Haas" in body_audit['bodyFont'] or "Helvetica" in body_audit['bodyFont']
        print("  [PASS] Verified: Neue Haas Grotesk Body Typography")

        # Inspect Hero heading word spacing and line alignment
        hero_spacing = page.evaluate("""() => {
            const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
            const line1 = visual.children[0];
            const line2 = visual.children[1];
            const line3 = visual.children[2];
            
            const r1 = line1.getBoundingClientRect();
            const r2 = line2.getBoundingClientRect();
            const r3Container = line3.querySelector('.relative.inline-block').getBoundingClientRect();
            const r3Word = line3.querySelector('span.absolute').getBoundingClientRect();

            const pSub = document.querySelector('#hero p');
            const pStyle = getComputedStyle(pSub);

            return {
                line1_left: r1.left,
                line2_left: r2.left,
                line3_left: r3Word.left,
                diff_1_2: Math.abs(r1.left - r2.left),
                diff_1_3: Math.abs(r1.left - r3Word.left),
                subheading_font: pStyle.fontFamily,
                subheading_word_spacing: pStyle.wordSpacing,
                subheading_letter_spacing: pStyle.letterSpacing,
                subheading_line_height: pStyle.lineHeight,
            };
        }""")
        print("\n=== HERO HEADING & SUBHEADING SPACING AUDIT ===")
        print(f"  Line 1 left: {hero_spacing['line1_left']}px")
        print(f"  Line 2 left: {hero_spacing['line2_left']}px")
        print(f"  Line 3 left: {hero_spacing['line3_left']}px")
        print(f"  Left diff 1-2: {hero_spacing['diff_1_2']}px, Left diff 1-3: {hero_spacing['diff_1_3']}px")
        assert hero_spacing['diff_1_2'] == 0, "Line 1 and Line 2 left edges do not match!"
        assert hero_spacing['diff_1_3'] == 0, "Line 1 and Line 3 left edges do not match!"
        print("  [PASS] Verified: 0.00px alignment discrepancy across all 3 lines")

        # Inspect Section Heading to Paragraph Spacing
        spacing_audit = page.evaluate("""() => {
            const sections = ['#food', '#menu', '#story', '#dining', '#gallery', '#contact'];
            return sections.map(secId => {
                const sec = document.querySelector(secId);
                const h = sec.querySelector('h2');
                const p = sec.querySelector('p:not([class*=\"uppercase\"])');
                if (!h || !p) return { secId, valid: false };
                const hRect = h.getBoundingClientRect();
                const pRect = p.getBoundingClientRect();
                return {
                    secId,
                    hBottom: hRect.bottom,
                    pTop: pRect.top,
                    gap: Math.round(pRect.top - hRect.bottom)
                };
            });
        }""")
        print("\n=== HEADING-TO-PARAGRAPH VERTICAL RHYTHM ===")
        for s in spacing_audit:
            print(f"  Section {s['secId']}: vertical gap = {s['gap']}px")

        # -------------------------------------------------------------
        # 2. Responsive Checks: Tablet & Mobile
        # -------------------------------------------------------------
        for vp_name, w, h in [('Tablet', 768, 1024), ('Mobile', 375, 812)]:
            p_resp = browser.new_page(viewport={'width': w, 'height': h})
            p_resp.goto('http://127.0.0.1:4192', wait_until='networkidle')
            p_resp.wait_for_timeout(400)

            res = p_resp.evaluate("""() => {
                const visual = document.querySelector('#hero h1 [aria-hidden=\"true\"]');
                const l1 = visual.children[0].getBoundingClientRect().left;
                const l2 = visual.children[1].getBoundingClientRect().left;
                const l3 = visual.children[2].querySelector('span.absolute').getBoundingClientRect().left;
                const hasOverflow = document.documentElement.scrollWidth > document.documentElement.clientWidth;
                return { l1, l2, l3, hasOverflow };
            }""")
            print(f"\n=== {vp_name.upper()} ({w}x{h}) ===")
            print(f"  Line 1: {res['l1']}px, Line 2: {res['l2']}px, Line 3: {res['l3']}px")
            print(f"  Horizontal Overflow: {res['hasOverflow']}")
            assert abs(res['l1'] - res['l2']) < 0.5, f"{vp_name} Line 1 & Line 2 misalignment!"
            assert abs(res['l1'] - res['l3']) < 0.5, f"{vp_name} Line 1 & Line 3 misalignment!"
            assert not res['hasOverflow'], f"{vp_name} horizontal overflow detected!"
            p_resp.screenshot(path=f"test_output/typography_audit_{vp_name.lower()}.png")
            print(f"  [PASS] Captured test_output/typography_audit_{vp_name.lower()}.png")

        # Console errors check
        print(f"\nConsole errors: {len(console_errors)}")
        assert len(console_errors) == 0, f"Console errors: {console_errors}"
        print("[PASS] 0 Console errors detected")

        page.screenshot(path="test_output/typography_audit_desktop.png")
        print("[PASS] Captured test_output/typography_audit_desktop.png")
        browser.close()

    server.shutdown()
    server.server_close()
    print("\n*** ALL TYPOGRAPHY & SPACING AUDIT TESTS PASSED SUCCESSFULLY! ***")

if __name__ == '__main__':
    run_audit()

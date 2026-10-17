# SATVIK ROOTS — OPENCODE MASTER PROMPT
## Black Marble × Liquid Black Chrome × Molten Champagne Gold

You are OpenCode acting as an autonomous senior creative director, brand designer, UX architect, frontend engineer, animation specialist, accessibility engineer, and QA lead.

Build a complete, production-quality, responsive restaurant website for **Satvik Roots, Talegaon, Pune**. This must be a working website—not just a landing-page mockup or generic restaurant template.

## FIRST: READ THE PDF AND USE ITS IMAGES
The source brief is in the project root: `Satvik Roots breif and prompts.pdf` (21 pages). Read the whole PDF before coding, including embedded visual references. If necessary, use available PDF tools to render/extract the page images and inspect them.

Reference guide:
- **Pages 1–2:** black marble texture, sculpted black-metal/gold button reference, authentic Indian food photography.
- **Page 3:** website concept and 70% dark surfaces / 20% food photography / 10% gold balance.
- **Pages 4–7:** section concepts for hero, signature dishes, menu, and dining experience.
- **Pages 8–21:** visual references and full technical/creative prompt.

Treat this PDF as the primary design specification. Preserve its terminology, visual direction, colours, component behaviour, structure, and non-negotiable rules. Do not skip the reference images. Inspect the existing repository and assets before editing; preserve useful work and never blindly overwrite project configuration.

Before coding, create `/docs/satvik-roots-implementation-plan.md` with the design tokens, section architecture, reusable components, asset inventory/provenance, fact-verification status, motion/accessibility plan, implementation steps, and QA checklist. Then implement the site; do not stop at planning.

## 1. CREATIVE NORTH STAR
**Black marble × liquid black chrome × molten champagne gold × authentic Indian food photography.**

The result should feel like a custom luxury hospitality brand: refined and cinematic like high-end automotive materials, yet warm, authentic, appetising, rooted in Indian dining, and trustworthy. Avoid generic restaurant themes, a plain black background with gold text, repeated identical food cards, excessive ornament, or a template-like look.

Composition guideline: approximately **70% dark surfaces, 20% food photography, 10% gold accents**. The food is the emotional hero; marble must not overpower it.

## 2. DESIGN TOKENS
Use reusable CSS variables:
- Obsidian black `#080808`
- Deep black `#0C0C0C`
- Charcoal `#151515`
- Graphite `#242424`
- Metallic grey `#3B3B3B`
- Champagne gold `#C6A15B`
- Molten-gold highlight `#E9D39A`
- Dark antique gold `#806234`
- Warm ivory `#F4EFE5`
- Muted text `#AAA49A`

Gold is a material accent, not a flat colour used everywhere. Avoid neon gold, glitter, excessive gold outlines, and large gold-filled blocks.

Typography: elegant editorial serif for major headlines; clean modern sans-serif for navigation, body copy, menu, and controls. Use large editorial headlines with intentional line breaks, small uppercase labels with tracking, readable body text, generous negative space, warm ivory primary text, and selective gold typography. Avoid decorative scripts and excessive italics.

## 3. MATERIALS AND IMAGERY

### Black marble
Use a real photographic texture wherever possible, matching the PDF: deep obsidian stone, smoky charcoal formations, subtle graphite veins, fine irregular champagne-gold mineral fractures, natural lighting variation, and believable depth. Extract/use the supplied reference if practical. CSS gradients may enhance real texture, not replace it. Use marble mainly in the hero, selected story transitions, and footer; use solid charcoal for content-heavy sections. Prevent obvious repeating patterns and maintain readable contrast. Keep parallax subtle and optional.

### Food photography
Prefer genuine Satvik Roots assets if present. Food imagery should have warm natural light, authentic Indian serving details, realistic colour, rich appetising textures, and thoughtful close-up compositions. If genuine venue/dish images are unavailable, use suitable food imagery only as illustrative material and do not claim it depicts Satvik Roots. Never label unrelated restaurant/hotel images as this venue.

### Signature liquid-metal controls
This is the defining design feature. Buttons must look like polished sculpted black chrome with flowing champagne-gold reflections—not ordinary black buttons with gold borders.

Material cues: obsidian base, curved graphite reflections, soft silver-grey specular highlights, organic gold reflections, selective molten highlights under a polished surface, and contrast between reflective edges and near-black areas. Avoid plastic gloss, rainbow chrome, glitter, cartoon effects, excessive glow, or heavy WebGL/video just for buttons.

Build reusable components:
- `LiquidMetalButton`
- `LiquidMetalIconButton`
- `LiquidMetalSecondaryButton`

Prefer layered CSS gradients, pseudo-elements, radial highlights, masks, and animated background positions. Use SVG filters/WebGL only if genuinely necessary and performant. Use CSS custom properties for colours/timing.

States:
- Default: reflective black chrome, subtle curved highlights, restrained gold reflection.
- Hover: organic gold reflection travels smoothly; graphite reflections shift; label stays readable.
- Pressed: slight physical compression and brief subtle light ripple.
- Focus: clear accessible gold-accented focus indicator; do not rely on colour alone.
- Touch: retain material feel without hover and use lightweight feedback.
- Reduced motion: preserve appearance but disable unnecessary movement.
Do not make every button circular; reserve circular metallic controls for arrows, gallery navigation, menu toggle, and scroll-to-top.

## 4. COMPLETE WEBSITE STRUCTURE

### Navigation
Desktop: SATVIK ROOTS wordmark; Menu, Our Story, Food, Gallery, Contact; `Order Online` CTA. Start transparent/dark marble if appropriate and transition to deep charcoal on scroll for legibility.
Mobile: wordmark, refined circular menu control, accessible navigation drawer, and visible ordering/contact actions. Test keyboard, touch, close/escape behaviour, and focus. Avoid a generic oversized hamburger in a bright gold circle.

### Hero
Cinematic full-width opening, preferably asymmetric split-screen: editorial copy/actions on one side and a substantial beautifully lit Indian vegetarian food image on the other. Use black marble, charcoal shadows, restrained gold veins, and controlled cinematic lighting.

Required copy from the PDF:
- Eyebrow: `A TASTE OF TRADITION`
- Headline: `Rooted in Tradition. Crafted for Every Craving.`
- Supporting text: `Discover comforting Indian favourites, vibrant flavours and a dining experience made to bring people together.`
- Primary CTA: `Explore Our Menu`
- Secondary CTA: `Find Your Table`

Immediately communicate food, warmth, quality, and hospitality. Avoid excessive text over the photo. Use restrained entrance motion; never delay access to content. Stack naturally on mobile and keep CTAs easy to tap.

### Signature food discovery
Heading: `A Taste Worth Returning For.`
Use premium image-led cards with image, dish name, short description, verified price where available, vegetarian indicator where appropriate, category label, and a small circular liquid-metal arrow. Suggested categories: Indian Main Course, Tandoori Starters, Oriental Favourites, Continental Selection, Breads and Rice, Desserts. Use actual published menu items where verifiable. Do not invent dishes, ingredients, popularity claims, or prices; use clearly marked editable placeholders if verification is not possible. Vary image ratios and card composition.

### Functional menu
Must be real and usable, not a static mockup:
- Search field
- Working category filters
- Responsive dish cards or clear list view
- Dish names/descriptions
- Verified prices
- Vegetarian indicators where appropriate
- Loading, empty, and error states as needed
- Prominent `Order Online` CTA

Reference: `https://www.zomato.com/pune/satvik-roots-talegaon/menu`
Use charcoal surfaces and subtle champagne-gold active states. Connect to the actual ordering destination only after verification. Do not build a fake checkout, simulate successful orders, or claim an integration works when it does not. Make unverified destinations explicitly configurable and document them.

### Brand story
Heading: `Good Food. Good Company. Memorable Moments.`
Use dark marble/charcoal, warm food/dining photography, editorial serif type, fine gold details, and negative space. Copy should be welcoming, authentic, and food-focused. Do not invent founding year, founder biography, family history, sourcing practices, awards, health claims, or claim every dish is traditionally sattvik unless confirmed. Use verified information or clearly labelled editable placeholders.

### Gallery and dining atmosphere
Build an editorial gallery with varied proportions—not a monotonous grid. Include suitable food, presentation, interior, ambience, hospitality, and detail imagery where authentic assets exist. Add subtle hover zoom, refined transitions, accessible controls, optional lightbox, and liquid-metal circular previous/next controls. Never present unrelated restaurant/hotel images as actual Satvik Roots photos. Optimise and lazy-load below-the-fold images.

### Location and contact
The PDF gives these as **starting references to verify before launch**:
- Name: Satvik Roots
- Address: `Plot 289/290, Manohar Nagar, Talegaon, Pune`
- Phone: `+91 78878 76518`

Include address, click-to-call link, Google Maps directions, Zomato menu/ordering link, opening hours only after verification, optional map embed, and a clear contact CTA. Keep these actions easy to find and fast to use. Track unverified information in the implementation plan.

### Footer
Black marble with restrained gold veins. Include wordmark, short brand statement, navigation, menu, contact details, directions, Zomato link, social links only if verified, thin separators, refined type, and a circular liquid-metal scroll-to-top control. Keep it uncluttered and readable.

## 5. MOTION
Use a coherent restrained system: subtle section entrances, gentle image zoom, organic button reflections, soft gold highlights, optional restrained marble parallax, and smooth mobile navigation. Smooth scrolling is optional and must not hijack normal browsing. Avoid constant moving backgrounds, excessive particles, heavy 3D transitions, unnecessary animation libraries, scroll hijacking, and animations that delay content. Preserve existing project stack where sensible. Use GSAP/ScrollTrigger only if useful and available; do not add unnecessary dependencies. Respect `prefers-reduced-motion`.

## 6. ENGINEERING REQUIREMENTS
- Inspect current repository, package manager, routes, assets, and existing implementation first.
- Preserve useful existing work; do not overwrite project configuration blindly.
- Use the current stack if sound; if React, create reusable components.
- Semantic HTML, accessible labels, keyboard navigation, visible focus, sufficient contrast, meaningful alt text.
- Responsive desktop/tablet/mobile layouts.
- Optimised/responsive images and lazy loading.
- SEO title, description, and relevant local restaurant SEO without spam.
- Functional navigation, search, filters, gallery controls, phone/map links, and CTAs.
- Appropriate loading/empty/error states.
- Reduced-motion support and good Core Web Vitals.
- No unnecessary dependencies or heavy 3D engine just to signal luxury.
- No invented business facts, reviews, awards, hours, prices, or integrations.
- Distinguish authentic assets from illustrative placeholders.
- Use current documentation tools when necessary.
- If Playwright/browser automation is available, use it to test the running site.
- Do not stop when the code compiles: run, inspect visually, identify shortcomings, and iterate.

## 7. AUTONOMOUS WORKFLOW
1. Read all 21 PDF pages and inspect embedded reference images.
2. Inspect repository and assets.
3. Create `/docs/satvik-roots-implementation-plan.md`.
4. Inventory assets and note provenance; identify which facts, menu items, prices, hours, and links need verification.
5. Establish design tokens, marble treatment, and reusable liquid-metal buttons.
6. Build navigation, hero, signature dishes, functional menu, story, gallery, location/contact, and footer.
7. Run the development server using the repository's actual scripts.
8. Test desktop and mobile; test navigation, search/filtering, gallery, CTA destinations, phone/directions links, keyboard focus, and reduced motion.
9. Fix console errors, overflow, broken images, inaccessible controls, and inconsistencies.
10. Do a creative-director polish pass based on the actual rendered site: ensure the hero is cinematic and appetising, the site feels custom rather than templated, the 70/20/10 balance holds, buttons truly resemble liquid black chrome, gold is restrained, typography/spacing/crops are coherent, mobile is excellent, key actions are easy, and imagery/facts are honest.
11. Continue making fixes without asking for approval after every small decision.

## 8. REQUIRED DELIVERABLES
- Complete working responsive website.
- `/docs/satvik-roots-implementation-plan.md`
- Reusable liquid-metal button components.
- Functional navigation, menu search/filters, gallery, contact/directions/ordering links where verified.
- Editable menu/business-data structure.
- Final concise report: what was built, files/components changed, tests performed, details needing restaurant confirmation, and how to run the project.

## NON-NEGOTIABLE RULES
1. Black marble, liquid black chrome, molten champagne gold, and authentic Indian food photography define the identity.
2. Buttons must look reflective and tactile, not like ordinary buttons with gold outlines.
3. Gold reflections move organically but with restraint.
4. Food photography creates warmth against dark surfaces.
5. Premium aesthetics must not harm legibility or usability.
6. Avoid generic templates, excessive gold, neon, plastic gloss, and unnecessary glassmorphism.
7. Never invent restaurant facts, reviews, awards, opening hours, or prices.
8. Preserve negative space, editorial typography, and strong composition.
9. Prioritise menu, ordering, contact, and directions.
10. Make this feel custom-designed for Satvik Roots.

## FINAL CREATIVE TARGET
Create a memorable cinematic restaurant website where **black marble provides the foundation, Indian food photography creates warmth, and interactive controls feel like sculpted black liquid chrome infused with flowing molten gold**. Every section must belong to the same visual world. Build the complete website, test it, inspect it visually, and iterate until it is cohesive, functional, responsive, and production-minded.

---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: Asif2902/achswapv3
# corpus-url: https://github.com/Asif2902/achswapv3/blob/d5872d3d00a429fdb0f34f77acd966535e291c4a/AI_Frontend_Design_Skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# AI Frontend Design Rules — No More Slop

> A strict, opinionated ruleset for AI systems generating frontend interfaces.  
> These rules exist to prevent cookie-cutter, thoughtless, and visually dead output.

---

## PART 1 — MANDATORY PRE-FLIGHT THINKING

Before writing a single line of code, the AI **must** answer all of the following internally:

1. **Who is this for?** Define the user: age, technical literacy, emotional state when using this interface.
2. **What is the one emotion this UI should trigger?** Pick exactly one: awe, calm, urgency, delight, trust, curiosity, power, nostalgia, focus, etc.
3. **What is the aesthetic direction?** Commit to a named, specific direction (see Part 2). Not "modern" or "clean" — those are non-answers.
4. **What will make this UNFORGETTABLE?** Identify one signature element before building anything.
5. **What would a mediocre AI do here?** Name it. Then do the opposite.

**If any of these are left unanswered, the AI may not proceed.**

---

## PART 2 — AESTHETIC DIRECTION (PICK ONE, COMMIT FULLY)

The AI must select a clear, named aesthetic and execute it with conviction. Mixing is permitted only if there is an intentional conceptual reason. Vagueness is not permitted.

### Approved Aesthetic Directions (non-exhaustive)

| Direction | Characteristics |
|---|---|
| **Brutalist/Raw** | Exposed structure, stark typography, intentional ugliness as a statement, no decorative softening |
| **Luxury/Refined** | Tight kerning, serif fonts, muted palettes, whisper-quiet animations, precision spacing |
| **Retro-Futuristic** | CRT effects, scan lines, terminal aesthetics, neon on dark, 80s sci-fi energy |
| **Organic/Natural** | Irregular shapes, earthy palettes, hand-drawn textures, fluid layouts, imperfection as beauty |
| **Editorial/Magazine** | Grid-breaking type, large pull quotes, dramatic contrast ratios, photo-centric |
| **Maximalist/Dense** | Everything has a place, rich patterns, layered depth, controlled chaos |
| **Brutally Minimal** | One typeface, two colors max, negative space as a primary element, zero decoration |
| **Toy-like/Playful** | Bold colors, rounded everything, tactile shadows, springy motion, childlike delight |
| **Industrial/Utilitarian** | Monospace fonts, data-dense layouts, no-nonsense hierarchy, dark UI, tool-first |
| **Art Deco/Geometric** | Symmetry, gold accents, repeating motifs, angular forms, 1920s visual language |
| **Soft/Dreamy** | Pastel gradients, blur effects, soft shadows, light frosted glass, gentle motion |
| **Cyberpunk/Neon** | High contrast, glitch effects, gradient type, dark backgrounds, electric accents |

**Restriction**: The AI may NOT describe its design as "modern," "clean," "minimal," or "professional" without also specifying which named aesthetic it falls under.

---

## PART 3 — TYPOGRAPHY RULES

Typography is the single most powerful tool in UI design. These rules are non-negotiable.

### BANNED Fonts (Absolute Prohibition)
The following fonts are overused to the point of invisibility and are **completely banned**:

- Inter
- Roboto
- Open Sans
- Lato
- Poppins
- Nunito
- Montserrat
- Source Sans Pro
- Arial
- Helvetica (unless used in a deliberate Helvetica-worship brutalist context)
- System UI defaults as a creative choice (acceptable only as a fallback)
- Space Grotesk (overused in AI outputs)
- DM Sans
- Plus Jakarta Sans

### Required Typography Behavior

- **Always pair** a display/heading font with a distinct body font. One font for everything is lazy.
- **Use Google Fonts or similar** for distinctive typefaces. Import them, don't assume availability.
- **Font size scales must have contrast.** Headings should feel dramatically different from body text — not just 4px larger.
- **Line-height matters.** Body text: 1.5–1.75. Display text: 0.9–1.1. Never default to browser defaults without intention.
- **Letter-spacing is a design tool.** All-caps labels should have `letter-spacing: 0.1em` minimum. Display fonts often benefit from tighter tracking.
- **Hierarchy must be immediately obvious** to a user with no context. If you have to explain the hierarchy, it failed.

### Typography Pairing Examples (for inspiration, not prescription)
- Playfair Display + Crimson Text (editorial luxury)
- Bebas Neue + IBM Plex Mono (industrial brutalist)
- Fraunces + Work Sans (organic modern)
- Syne + DM Mono (tech editorial)
- Abril Fatface + Libre Baskerville (maximalist editorial)
- Righteous + Courier Prime (retro-futuristic)

---

## PART 4 — COLOR RULES

### Banned Color Patterns

- **Purple/violet gradient on white** — the single most overused AI UI pattern. Completely banned.
- **Gradient backgrounds as a default** — gradients must serve a purpose, not fill space
- **Flat blue (`#3B82F6`, `#2563EB`, etc.) as the only accent** — overused beyond recognition
- **Gray text on white background without sufficient contrast** — accessibility failure AND visually dead
- **Rainbow/multi-gradient text on every heading** — use this once, as a signature element, or not at all
- **"Safe" palettes** — beige/white/navy, white/black/green, white/black/orange — only acceptable if executed with extraordinary intentionality

### Required Color Behavior

- **Commit to a palette before coding.** Define 2–4 colors maximum for a focused palette. Use CSS custom properties: `--color-bg`, `--color-fg`, `--color-accent`, `--color-surface`, etc.
- **Use a dominant tone.** The background should have a clear chromatic identity — not just white or near-black.
- **Accents should be used sparingly.** An accent color loses power when used everywhere. Use it for the one thing that matters most.
- **Dark themes need depth.** A dark theme is not `#000000` background + white text. Use layered dark tones: background, surface, elevated surface.
- **Light themes need warmth or edge.** Pure white (`#FFFFFF`) feels clinical unless intentional. Consider `#FAFAF7`, `#F5F0E8`, `#FFFBF2`, or cooler `#F0F4F8`.
- **Color must carry meaning.** Every color decision should be justifiable in terms of the emotional or functional role it plays.

---

## PART 5 — LAYOUT & SPATIAL COMPOSITION RULES

### Banned Layout Patterns

- **Centered card on gray background** — the default fallback of every lazy AI-generated UI
- **Symmetrical 3-column feature grids with icons** — used in 90% of landing pages, avoided unless subverted
- **Full-width hero → features → CTA** — allowed only if dramatically executed
- **Equal spacing everywhere** — visual rhythm requires variation. Not everything should be `gap: 1rem`
- **Responsive grids that just stack on mobile** — mobile layout must be designed, not collapsed

### Required Layout Behavior

- **Use unexpected spatial decisions.** Overlap elements. Break the grid deliberately. Use negative space as a compositional element, not just padding.
- **Asymmetry is a tool.** A layout that is slightly off-balance creates visual tension and interest. Perfect symmetry is often boring.
- **Establish a clear visual flow.** The eye must be guided — F-pattern, Z-pattern, or a deliberate subversion of both.
- **Size contrast matters.** Not all elements should feel the same weight. Something should be dramatically large or dramatically small.
- **Whitespace is not emptiness.** Generous whitespace around a key element elevates it. Whitespace is a design choice, not a lack of design.

---

## PART 6 — ANIMATION & MOTION RULES

### Banned Motion Patterns

- **Fade-in everything on load** — the default animation of every template. Use sparingly or not at all.
- **Spin animations on icons** — looks like 2012
- **Bounce animations without purpose** — toyish when not intentional
- **Hover: `transform: scale(1.05)` on every interactive element** — overused beyond all meaning
- **CSS transitions with no easing consideration** — `transition: all 0.3s ease` copy-pasted everywhere is not design

### Required Motion Behavior

- **Motion must serve a purpose:** feedback, orientation, delight, or emphasis. Justify every animation.
- **Stagger reveals for lists/grids.** Items appearing one by one feels crafted. All at once feels broken.
- **Easing is personality.** `cubic-bezier(0.34, 1.56, 0.64, 1)` feels bouncy and playful. `cubic-bezier(0.87, 0, 0.13, 1)` feels powerful and decisive. Choose accordingly.
- **One showstopper animation per page.** Identify the single most important moment and make that motion exceptional. Everything else should be subtle.
- **Respect `prefers-reduced-motion`.** Always include this media query for accessibility.
- **Duration guidelines:** Micro-interactions: 100–200ms. Transitions: 200–400ms. Entrances: 400–700ms. Anything longer needs a very strong reason.

---

## PART 7 — COMPONENT DESIGN RULES

### Banned Component Patterns

- **Default browser form styling** — all form elements must be custom styled
- **Blue underlined links as the only interactive affordance** — use context-appropriate interaction design
- **Generic card with image + title + description + button** — acceptable only if the card itself is remarkable
- **Hamburger menus on desktop** — navigation must be appropriate for the viewport
- **Tooltips as the only labeling strategy** — don't hide critical information in hover states
- **Modals for every confirmation** — use contextual inline actions when possible

### Buttons

- Buttons must have a clear hierarchy: primary, secondary, ghost/tertiary. Each must look distinct.
- Padding must be generous. Minimum `12px 24px`. Touch targets minimum `44px` tall.
- Hover and active states are mandatory. Not optional.
- Border-radius must match the overall aesthetic: `0` for brutalist, `4px` for refined, `999px` for playful, etc.

### Forms

- Labels must always be visible (not just placeholders)
- Focus states must be visually prominent and aesthetically consistent
- Error states must be obvious without relying on color alone
- Input fields must have sufficient padding: minimum `12px 16px`

### Icons

- Use a consistent icon library. Don't mix Heroicons with Material Icons with Font Awesome.
- Icons alone without labels fail accessibility — always include `aria-label` or accompanying text
- Icon size must match the typographic scale. Don't use 24px icons next to 12px text.

---

## PART 8 — BACKGROUND & TEXTURE RULES

### Banned Backgrounds

- **Plain `#FFFFFF` or `#000000` with no treatment** — acceptable only in deliberate brutalist/minimal contexts
- **Low-resolution stock gradient from CSS generators** — use custom-crafted gradients
- **Tiled patterns that don't align with the aesthetic** — every visual element must be intentional

### Encouraged Background Treatments (pick what fits)

- SVG noise textures for organic warmth (`feTurbulence` filter)
- Radial gradient "glow" spots for depth and atmosphere
- CSS mesh gradients for richness
- Geometric SVG patterns (dots, lines, grids) at low opacity
- Grain overlay using CSS `backdrop-filter` or a semi-transparent noise SVG
- Layered shapes with `mix-blend-mode` for complexity
- Dark backgrounds with subtle chromatic shifts (not flat black)

---

## PART 9 — ACCESSIBILITY RULES (NON-NEGOTIABLE)

These rules are not optional. Beautiful design that excludes people is failed design.

- **Color contrast minimum:** 4.5:1 for normal text, 3:1 for large text (WCAG AA)
- **All interactive elements must be keyboard accessible**
- **Focus indicators must be visible** — never `outline: none` without a custom replacement
- **Images must have `alt` text**
- **Form inputs must have associated `<label>` elements**
- **ARIA roles must be used correctly** — don't add ARIA to native semantic elements unnecessarily
- **`prefers-reduced-motion` media query must be respected**
- **`prefers-color-scheme` should be considered** for dark/light mode support
- **Touch targets minimum 44×44px** for mobile interfaces

---

## PART 10 — CODE QUALITY RULES

### Structure

- CSS custom properties (`--var`) must be used for all repeating values: colors, spacing scale, font families, radii, transitions
- Styles must be organized: reset/base → tokens → layout → components → utilities → animations
- No inline styles except for dynamic values that cannot be pre-defined
- No `!important` except as a last resort with a comment explaining why

### Performance

- No unnecessary external dependencies. Don't import a 50KB library to do something CSS can do natively.
- Images must have explicit `width` and `height` to prevent layout shift
- Fonts must use `font-display: swap`
- Animations must use `transform` and `opacity` — never animate `width`, `height`, `top`, `left` (causes reflow)

### Responsiveness

- Mobile-first CSS by default. Use `min-width` media queries.
- Test breakpoints: 375px (small phone), 768px (tablet), 1280px (desktop), 1920px (large desktop)
- No fixed pixel widths on containers — use `max-width` with percentage or `clamp()`
- Typography must be fluid: use `clamp()` for responsive type scaling

---

## PART 11 — THE SLOP CHECKLIST

Before delivering any frontend output, the AI must verify it does NOT contain any of the following:

- [ ] Inter, Roboto, Poppins, or any other banned font
- [ ] Purple gradient on white as the primary visual treatment
- [ ] A centered card on a gray background as the main layout pattern
- [ ] `transition: all 0.3s ease` copy-pasted on every element
- [ ] `transform: scale(1.05)` as the only hover effect
- [ ] A 3-column icon grid with title + description as the only feature section
- [ ] Default browser form or button styling
- [ ] Blue `#3B82F6` as the sole accent color
- [ ] Every heading having a rainbow gradient
- [ ] Fade-in animations on every single element
- [ ] `box-shadow: 0 4px 6px rgba(0,0,0,0.1)` on every card
- [ ] No defined aesthetic direction (just "modern" or "clean")
- [ ] The word "Revolutionize" or "Empower" in placeholder copy
- [ ] Generic placeholder text ("Lorem ipsum" or "Welcome to our platform")
- [ ] Missing focus styles on interactive elements
- [ ] No use of CSS custom properties for repeated values

**If any box is checked, the output must be revised before delivery.**

---

## PART 12 — SELF-EVALUATION BEFORE OUTPUT

The AI must ask itself these questions and answer honestly:

1. **Would a human designer be proud to put their name on this?** If not, rebuild.
2. **Is this visually different from the last 10 UIs the AI generated?** If not, make a different aesthetic choice.
3. **Does every design decision have a reason?** If a color, font, or spacing choice can't be justified, change it or own it.
4. **Is the typography doing heavy lifting?** If the layout were removed and only the type remained, would it still feel intentional?
5. **Is there one element in this UI that is genuinely surprising?** If not, add one.
6. **Could this design exist in a specific cultural context, era, or industry?** Rootless design is forgettable design.
7. **Has the AI defaulted to its own training distribution?** The most dangerous bias is the average of all training data — actively resist it.

---

## APPENDIX — USEFUL CSS PATTERNS (REFERENCE)

```css
/* Fluid typography */
font-size: clamp(1rem, 2.5vw + 0.5rem, 1.5rem);

/* CSS noise texture overlay */
.noise::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* SVG noise */
  opacity: 0.04;
  pointer-events: none;
}

/* Staggered list animation */
li { opacity: 0; animation: fadeUp 0.4s ease forwards; }
li:nth-child(1) { animation-delay: 0.1s; }
li:nth-child(2) { animation-delay: 0.2s; }

/* Accessible focus ring */
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 3px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Responsive container */
.container {
  width: min(100% - 2rem, 1200px);
  margin-inline: auto;
}

/* Mesh gradient background */
background: 
  radial-gradient(at 40% 20%, hsl(220, 80%, 60%) 0px, transparent 50%),
  radial-gradient(at 80% 0%, hsl(189, 100%, 56%) 0px, transparent 50%),
  radial-gradient(at 0% 50%, hsl(355, 85%, 60%) 0px, transparent 50%);
```

---

*These rules are living guidelines. They exist to raise the floor of AI-generated frontend design — not to constrain creativity, but to force it.*
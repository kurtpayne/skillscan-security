---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: nielskaspers/bold-designs
# corpus-url: https://github.com/nielskaspers/bold-designs/blob/725ea413770e30e446a203a46ad7093f538208a5/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Bold Designs Skill

Create **bold, distinctive, production-grade** frontend interfaces. This skill produces expressive, modern designs that look nothing like generic AI output.

---

## When to Apply This Skill

Use this when:
- Building landing pages, marketing sites, or product interfaces
- Creating UI components (buttons, cards, heroes, navigation)
- Writing frontend code in React, Next.js, Vue, Svelte, or plain HTML/CSS
- Generating Tailwind CSS or vanilla CSS

---

## ⚠️ Project Styling Respect Rule

**This skill provides PRINCIPLES and TACTICS, not specific styling.**

When working in an existing project:
1. **ALWAYS** use the project's existing design system, colors, and tokens
2. **ALWAYS** match the project's existing spacing scale and typography
3. **ALWAYS** follow the project's component patterns and naming conventions
4. **NEVER** override existing Tailwind config, CSS variables, or theme settings
5. **NEVER** introduce new colors/fonts that conflict with the established palette

**What this skill DOES provide:**
- Anti-generic aesthetic principles (what to avoid, what makes designs feel templated)
- Accessibility requirements (APCA contrast, keyboard nav, ARIA)
- Animation performance rules (compositor properties, timing)
- Typography best practices (`text-balance`, `text-pretty`, hierarchy)
- Layout discipline (z-index scale, safe areas, optical alignment)
- Interaction patterns (focus-visible, touch targets, states)

**What this skill does NOT impose:**
- Specific color palettes (use the project's palette)
- Specific fonts (use the project's typography)
- Specific component library (adapt to project's stack)
- Specific spacing values (use the project's scale)

The color palettes and component examples below are **reference examples only** — use them for new/greenfield projects, or when no existing design system exists.

---

## Design Philosophy

### Core Principles

1. **Bold over safe** — Make visual choices that have a point of view. Boring is worse than slightly wrong.
2. **Intentional over uniform** — Every spacing, color, and size decision should serve a purpose.
3. **Expressive over minimal** — Users want personality, not sterile tech aesthetics.
4. **Readable over clever** — Visual interest must never sacrifice readability.
5. **Native over custom** — Use semantic HTML and CSS before JavaScript solutions.

### Anti-Generic Rules

**NEVER do these (they scream "AI generated"):**
- Uniform padding/margins everywhere (8px everywhere = AI)
- Default blue buttons without context
- Overly rounded corners on everything (rounded-2xl on everything = AI)
- Generic gradients (blue-to-purple is the new clipart)
- Centered everything with identical spacing
- Stock "hero + 3 features + testimonials + CTA" layout
- Sans-serif body text with no typographic personality
- Identical card components repeated without variation

**ALWAYS do these:**
- Mix spacing intentionally (tight headlines, generous section breaks)
- Use asymmetry where it serves hierarchy
- Add one unexpected visual element per section
- Vary component sizes based on importance
- Use color strategically, not decoratively
- Create visual rhythm through contrast, not repetition

---

## Visual Design System

### Typography

**Hierarchy (most important → least):**
| Level | Use | Size | Weight | Line Height |
|-------|-----|------|--------|-------------|
| Display | Hero headlines | 4xl-7xl | 700-900 | 1.0-1.1 |
| H1 | Page titles | 3xl-5xl | 700-800 | 1.1-1.2 |
| H2 | Section heads | 2xl-3xl | 600-700 | 1.2 |
| H3 | Card titles | xl-2xl | 600 | 1.3 |
| Body Large | Intro paragraphs | lg-xl | 400 | 1.6-1.7 |
| Body | Default text | base | 400 | 1.6 |
| Small | Captions, labels | sm | 500 | 1.4 |

**Typography Rules:**
- Apply `text-balance` to all headings
- Apply `text-pretty` to body paragraphs
- Use `tabular-nums` for any numerical data
- Use `truncate` or `line-clamp` for dense UI
- Never modify letter-spacing unless explicitly requested
- Font size ≥16px on mobile to prevent iOS auto-zoom
- Curly quotes (" ") not straight quotes (" ")
- Ellipsis character (…) not three periods (...)

**Font Pairing Strategy:**
- Headlines: Bold geometric sans (Inter, Satoshi, Plus Jakarta) or expressive display (Clash Display, Cabinet Grotesk)
- Body: Readable neutral sans (Inter, System UI) or humanist (Source Sans, Open Sans)
- Accent: Monospace for technical content, serif for editorial

### Color Strategy

**Palette Approach:**
- Bold primaries as accents, not backgrounds
- High contrast text (APCA preferred over WCAG 2)
- One accent color per view maximum
- Neon/vibrant colors for CTAs and highlights
- Dark mode should feel native, not inverted

**Contrast Requirements:**
- Text on backgrounds: APCA Lc 75+ for body, Lc 60+ for large text
- Interactive states (hover/active/focus) must have HIGHER contrast than rest state
- Never rely on color alone — always include text labels or icons

**Color Palette Examples:**

```css
/* Electric & Bold */
--primary: #7C3AED;      /* Vibrant purple */
--accent: #06B6D4;       /* Cyan pop */
--surface: #0F172A;      /* Deep slate */
--text: #F8FAFC;         /* Bright white */

/* Warm Energy */
--primary: #F97316;      /* Orange energy */
--accent: #FBBF24;       /* Golden highlight */
--surface: #1C1917;      /* Warm black */
--text: #FAFAF9;         /* Warm white */

/* Neo Brutalist */
--primary: #000000;      /* Pure black */
--accent: #CCFF00;       /* Acid green */
--surface: #FFFFFF;      /* Pure white */
--border: #000000;       /* Hard edges */
```

### Spacing System

**Use intentional, varied spacing:**

| Token | Value | Use Case |
|-------|-------|----------|
| xs | 4px | Icon gaps, tight inline |
| sm | 8px | Button padding, compact lists |
| md | 16px | Default element spacing |
| lg | 24px | Card padding, comfortable spacing |
| xl | 32px | Section element gaps |
| 2xl | 48px | Section padding |
| 3xl | 64px | Major section breaks |
| 4xl | 96px | Hero/footer margins |

**Spacing Rules:**
- Headlines: Tight line-height (1.0-1.2), generous margin-bottom
- Cards: Asymmetric padding (more bottom, less top creates visual lift)
- Sections: Large gaps between (3xl-4xl), tight within (md-lg)
- Never use identical spacing for everything

### Layout Discipline

**Grid & Alignment:**
- Every element aligns intentionally to grid, baseline, edge, or center
- Use optical alignment (±1px adjustment) when perception beats geometry
- Implement fixed z-index scale (never arbitrary values like z-[9999])
- Use `h-dvh` instead of `h-screen` for full viewport
- Respect `safe-area-inset` for fixed positioning

**Z-Index Scale:**
```css
--z-base: 0;
--z-dropdown: 100;
--z-sticky: 200;
--z-modal: 300;
--z-popover: 400;
--z-toast: 500;
```

**Responsive Approach:**
- Mobile-first breakpoints
- Touch targets: 44px minimum on mobile, 24px minimum on desktop
- Use `size-*` utilities for square elements (icons, avatars)
- Scrollbars: Only render necessary ones, fix overflow issues

---

## Interaction Design

### Animation Standards

**Performance Rules:**
- ONLY animate compositor properties: `transform`, `opacity`
- NEVER animate: `width`, `height`, `top`, `left`, `margin`, `padding`
- NEVER use `transition: all` — explicitly list properties
- Max `200ms` for interaction feedback
- Use `ease-out` for entrances, `ease-in` for exits

**Timing Functions:**
```css
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

**Motion Preferences:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Animation Use Cases:**
- Hover states: subtle scale (1.02-1.05) or translateY (-2px)
- Page transitions: fade + slight translate
- Loading: skeleton shimmer, not spinners
- Micro-interactions: button press feedback, toggle switches

### Interactive States

**Every interactive element needs:**
1. **Rest** — Default appearance
2. **Hover** — Visual change on mouse over
3. **Focus** — Keyboard navigation (use `:focus-visible`)
4. **Active** — During click/tap
5. **Disabled** — Reduced opacity + cursor-not-allowed

**Focus Visibility:**
```css
/* Only show focus ring for keyboard users */
:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;
}
```

### Button Patterns

**Primary CTA:**
```jsx
<button className="
  relative px-6 py-3
  bg-violet-600 text-white font-semibold
  rounded-lg
  transition-all duration-200
  hover:bg-violet-500 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-violet-500/25
  active:translate-y-0 active:shadow-none
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-500
">
  Get Started
</button>
```

**Secondary/Ghost:**
```jsx
<button className="
  px-6 py-3
  border-2 border-slate-200 text-slate-900 font-medium
  rounded-lg
  transition-all duration-200
  hover:border-slate-900 hover:bg-slate-50
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-900
">
  Learn More
</button>
```

---

## Accessibility Requirements

### Non-Negotiable Checklist

**Every component MUST:**
- [ ] Have proper heading hierarchy (h1 → h2 → h3, no skips)
- [ ] Include alt text for all images
- [ ] Support full keyboard navigation
- [ ] Have sufficient color contrast (APCA Lc 75+ for body text)
- [ ] Use ARIA labels for icon-only buttons
- [ ] Have visible focus indicators
- [ ] Work without JavaScript where possible

### HTML Semantics

```html
<!-- CORRECT -->
<nav aria-label="Main navigation">
  <a href="/features">Features</a>
</nav>

<main>
  <article>
    <h1>Page Title</h1>
    <section aria-labelledby="features-heading">
      <h2 id="features-heading">Features</h2>
    </section>
  </article>
</main>

<!-- WRONG -->
<div class="nav">
  <div onclick="navigate()">Features</div>
</div>
```

### Form Accessibility

```jsx
// Every input needs a label
<label htmlFor="email" className="block text-sm font-medium text-slate-700">
  Email address
</label>
<input
  type="email"
  id="email"
  name="email"
  autoComplete="email"
  inputMode="email"
  placeholder="you@example.com"
  aria-describedby="email-error"
  className="mt-1 block w-full rounded-lg border-slate-300 shadow-sm focus:border-violet-500 focus:ring-violet-500"
/>
<p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
  {error}
</p>
```

### Icon Buttons

```jsx
// Always include aria-label for icon-only buttons
<button
  aria-label="Close modal"
  className="p-2 rounded-lg hover:bg-slate-100"
>
  <XIcon className="h-5 w-5" aria-hidden="true" />
</button>
```

---

## Component Patterns

### Hero Sections (Bold, Not Generic)

**Pattern 1: Asymmetric Split**
```jsx
<section className="relative min-h-[90vh] overflow-hidden bg-slate-950">
  {/* Dramatic gradient blob */}
  <div className="absolute -right-1/4 top-1/4 h-[600px] w-[600px] rounded-full bg-violet-500/30 blur-[128px]" />

  <div className="relative mx-auto max-w-7xl px-6 py-24 lg:flex lg:items-center lg:gap-x-16 lg:py-40">
    {/* Content - takes 60% */}
    <div className="max-w-2xl lg:flex-auto">
      <p className="text-sm font-semibold uppercase tracking-widest text-violet-400">
        New Feature
      </p>

      <h1 className="mt-4 text-5xl font-bold tracking-tight text-white sm:text-7xl" style={{ textWrap: 'balance' }}>
        Design that actually
        <span className="block text-violet-400">stands out</span>
      </h1>

      <p className="mt-6 max-w-xl text-lg leading-relaxed text-slate-400" style={{ textWrap: 'pretty' }}>
        Stop shipping interfaces that look like every other AI-generated page.
        Create something memorable.
      </p>

      <div className="mt-10 flex flex-wrap gap-4">
        <a href="#" className="inline-flex items-center gap-2 rounded-full bg-violet-500 px-6 py-3 font-semibold text-white transition hover:bg-violet-400">
          Start building
          <ArrowRightIcon className="h-4 w-4" />
        </a>
        <a href="#" className="inline-flex items-center gap-2 rounded-full border-2 border-slate-700 px-6 py-3 font-semibold text-white transition hover:border-slate-500">
          View examples
        </a>
      </div>
    </div>

    {/* Visual - asymmetric, not centered */}
    <div className="mt-16 hidden lg:mt-0 lg:block lg:flex-shrink-0">
      <div className="relative">
        {/* Main visual with offset shadow/accent */}
        <div className="absolute -inset-4 rounded-2xl bg-gradient-to-r from-violet-500 to-cyan-500 opacity-20 blur-xl" />
        <img
          src="/hero-visual.png"
          alt="Product screenshot showing the dashboard interface"
          className="relative rounded-2xl shadow-2xl"
          width={600}
          height={400}
        />
      </div>
    </div>
  </div>
</section>
```

**Pattern 2: Full-Bleed Statement**
```jsx
<section className="relative flex min-h-screen items-center justify-center overflow-hidden bg-black px-6">
  {/* Animated gradient background */}
  <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-violet-900/40 via-black to-black" />

  <div className="relative max-w-4xl text-center">
    <h1 className="text-6xl font-black tracking-tight text-white sm:text-8xl lg:text-9xl">
      <span className="bg-gradient-to-r from-violet-400 via-pink-400 to-orange-400 bg-clip-text text-transparent">
        Create.
      </span>
    </h1>

    <p className="mx-auto mt-8 max-w-2xl text-xl text-slate-400">
      The only design tool that doesn't make everything look the same.
    </p>

    <div className="mt-12">
      <a href="#" className="group inline-flex items-center gap-3 text-lg font-semibold text-white">
        Start free
        <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/10 transition group-hover:bg-white/20">
          <ArrowRightIcon className="h-5 w-5" />
        </span>
      </a>
    </div>
  </div>
</section>
```

### Feature Sections

**Pattern: Bento Grid (varied sizes)**
```jsx
<section className="bg-slate-50 py-24">
  <div className="mx-auto max-w-7xl px-6">
    <h2 className="text-3xl font-bold text-slate-900">Everything you need</h2>

    <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {/* Large featured card - spans 2 cols */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-violet-500 to-purple-600 p-8 text-white sm:col-span-2 lg:row-span-2">
        <div className="relative z-10">
          <span className="inline-block rounded-full bg-white/20 px-3 py-1 text-sm font-medium">
            Featured
          </span>
          <h3 className="mt-4 text-2xl font-bold">AI-Powered Design</h3>
          <p className="mt-2 max-w-md text-violet-100">
            Generate layouts, color schemes, and components with natural language.
          </p>
        </div>
        <div className="absolute -bottom-8 -right-8 h-64 w-64 rounded-full bg-white/10" />
      </div>

      {/* Regular cards */}
      <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-orange-100 text-orange-600">
          <ZapIcon className="h-6 w-6" />
        </div>
        <h3 className="mt-4 text-lg font-semibold text-slate-900">Lightning Fast</h3>
        <p className="mt-2 text-sm text-slate-600">
          Build in minutes, not hours. Our components are optimized for speed.
        </p>
      </div>

      <div className="rounded-3xl bg-slate-900 p-6 text-white">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-500/20 text-cyan-400">
          <CodeIcon className="h-6 w-6" />
        </div>
        <h3 className="mt-4 text-lg font-semibold">Developer First</h3>
        <p className="mt-2 text-sm text-slate-400">
          Clean, semantic code that your team will actually want to maintain.
        </p>
      </div>

      {/* Horizontal card */}
      <div className="flex items-center gap-6 rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200 sm:col-span-2 lg:col-span-1">
        <div className="flex h-16 w-16 flex-shrink-0 items-center justify-center rounded-2xl bg-emerald-100 text-emerald-600">
          <ShieldCheckIcon className="h-8 w-8" />
        </div>
        <div>
          <h3 className="font-semibold text-slate-900">Accessible by Default</h3>
          <p className="mt-1 text-sm text-slate-600">
            WCAG AA compliant out of the box.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>
```

### Cards (Varied, Not Identical)

```jsx
{/* Mix card styles for visual interest */}
<div className="grid gap-6 md:grid-cols-3">
  {/* Style 1: Clean with accent border */}
  <article className="rounded-2xl border-l-4 border-violet-500 bg-white p-6 shadow-sm">
    <time className="text-sm text-slate-500">Mar 15, 2024</time>
    <h3 className="mt-2 text-lg font-semibold text-slate-900">
      Design Systems at Scale
    </h3>
    <p className="mt-2 text-slate-600">
      How we maintain consistency across 50+ products.
    </p>
  </article>

  {/* Style 2: Dark with gradient */}
  <article className="rounded-2xl bg-gradient-to-br from-slate-800 to-slate-900 p-6 text-white">
    <span className="text-xs font-semibold uppercase tracking-wider text-violet-400">
      Case Study
    </span>
    <h3 className="mt-2 text-lg font-semibold">
      Redesigning for Gen Z
    </h3>
    <p className="mt-2 text-slate-400">
      Bold colors, authentic voice, instant engagement.
    </p>
  </article>

  {/* Style 3: Image-forward */}
  <article className="group overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-slate-200">
    <div className="aspect-video overflow-hidden bg-slate-100">
      <img
        src="/thumbnail.jpg"
        alt=""
        className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
      />
    </div>
    <div className="p-6">
      <h3 className="font-semibold text-slate-900 group-hover:text-violet-600 transition">
        Motion Design Principles
      </h3>
    </div>
  </article>
</div>
```

### Navigation

```jsx
<header className="fixed inset-x-0 top-0 z-50 backdrop-blur-md">
  <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4" aria-label="Main navigation">
    {/* Logo */}
    <a href="/" className="flex items-center gap-2">
      <span className="text-xl font-bold text-slate-900">Brand</span>
    </a>

    {/* Desktop nav */}
    <div className="hidden items-center gap-8 md:flex">
      <a href="/features" className="text-sm font-medium text-slate-600 transition hover:text-slate-900">
        Features
      </a>
      <a href="/pricing" className="text-sm font-medium text-slate-600 transition hover:text-slate-900">
        Pricing
      </a>
      <a href="/docs" className="text-sm font-medium text-slate-600 transition hover:text-slate-900">
        Docs
      </a>
    </div>

    {/* CTA */}
    <div className="flex items-center gap-4">
      <a href="/login" className="hidden text-sm font-medium text-slate-600 transition hover:text-slate-900 sm:block">
        Sign in
      </a>
      <a
        href="/signup"
        className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-700"
      >
        Get Started
      </a>
    </div>

    {/* Mobile menu button */}
    <button
      type="button"
      aria-label="Open menu"
      aria-expanded="false"
      className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 md:hidden"
    >
      <MenuIcon className="h-6 w-6" aria-hidden="true" />
    </button>
  </nav>
</header>
```

---

## Loading States

**Use skeletons, not spinners:**
```jsx
{/* Skeleton for card */}
<div className="animate-pulse rounded-2xl bg-white p-6 shadow-sm">
  <div className="h-12 w-12 rounded-xl bg-slate-200" />
  <div className="mt-4 h-5 w-3/4 rounded bg-slate-200" />
  <div className="mt-3 space-y-2">
    <div className="h-3 w-full rounded bg-slate-100" />
    <div className="h-3 w-5/6 rounded bg-slate-100" />
  </div>
</div>

{/* Shimmer effect */}
<style>
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton-shimmer {
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
</style>
```

---

## Empty States

**Design all states:**
```jsx
<div className="flex flex-col items-center justify-center py-16 text-center">
  <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-100">
    <InboxIcon className="h-8 w-8 text-slate-400" />
  </div>
  <h3 className="mt-4 text-lg font-semibold text-slate-900">No projects yet</h3>
  <p className="mt-2 max-w-sm text-slate-600">
    Get started by creating your first project. It only takes a minute.
  </p>
  <button className="mt-6 rounded-lg bg-violet-600 px-4 py-2 text-sm font-semibold text-white hover:bg-violet-500">
    Create project
  </button>
</div>
```

---

## Performance Requirements

**Image Optimization:**
- Always set explicit `width` and `height` to prevent layout shift
- Use `loading="lazy"` for below-fold images
- Use `priority` prop (Next.js) for LCP images
- Prefer WebP/AVIF formats

**Font Loading:**
```jsx
// Next.js font optimization
import { Inter, Plus_Jakarta_Sans } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  variable: '--font-jakarta',
  weight: ['500', '600', '700', '800']
})
```

**Large Lists:**
- Virtualize lists >50 items
- Or use `content-visibility: auto` for simpler cases

---

## Output Format

When generating components, provide:

```markdown
## [Component Name]

**What it does:** [One-line description]

**Design decisions:**
- [Why specific color/spacing/layout choices were made]
- [How it avoids generic AI aesthetics]

### Code

[Full implementation]

### Customization

| Prop/Variable | Default | Options |
|---------------|---------|---------|
| variant | "default" | "default", "dark", "accent" |

### Accessibility Notes

- [Specific a11y considerations for this component]
```

---

## Framework-Specific Notes

### React/Next.js
- Use functional components with hooks
- TypeScript when requested
- Use Next.js `<Link>` and `<Image>` components
- Server components by default, client only when needed

### Tailwind CSS
- Use design tokens via theme extension
- Extract repeated patterns to components, not utility classes
- Use `@apply` sparingly (only in base layer)

### Vue/Svelte
- Adapt patterns to framework idioms
- Use framework-specific transition components
- Maintain same accessibility standards

### Plain HTML/CSS
- These patterns work without any framework
- Use CSS custom properties for theming
- Modern CSS features (`text-wrap`, `container queries`) have good browser support

---

## Integration Notes

**With Figma:** If design specs are provided, match them exactly while applying the accessibility and performance rules from this skill.

**With Design Systems:** Ask what system is in use, then adapt patterns to match existing tokens.

**With Existing Codebases:** Match the project's existing conventions for naming, file structure, and styling approach.

---

## First-Time Project Checklist

Before writing any frontend code in a project, check for:

1. **Tailwind config** — `tailwind.config.js/ts` for custom colors, spacing, fonts
2. **CSS variables** — `:root` or theme files for design tokens
3. **Component library** — Existing UI components to extend, not replace
4. **Typography setup** — Font imports, base styles, heading scales
5. **Spacing conventions** — Padding/margin patterns already in use

**If these exist:** Use them. Apply the principles from this skill (accessibility, animation, anti-generic patterns) while respecting the established visual language.

**If these don't exist (greenfield):** Use the example palettes and patterns in this skill as a starting point.

---

## Quick Reference Checklist

Before shipping any frontend code:

- [ ] No uniform spacing everywhere (varied, intentional)
- [ ] At least one unexpected visual element per section
- [ ] Cards/components vary in style, not copy-pasted
- [ ] All interactive elements have hover, focus, active states
- [ ] Animations only use `transform` and `opacity`
- [ ] `prefers-reduced-motion` respected
- [ ] APCA Lc 75+ for body text contrast
- [ ] Proper heading hierarchy (no skips)
- [ ] All images have alt text
- [ ] Icon buttons have aria-labels
- [ ] Mobile touch targets are 44px+
- [ ] No `transition: all`
- [ ] No arbitrary z-index values
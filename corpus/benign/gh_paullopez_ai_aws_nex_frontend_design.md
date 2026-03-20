---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: paullopez-ai/aws-nextjs-host
# corpus-url: https://github.com/paullopez-ai/aws-nextjs-host/blob/67f75a8771da7e0821f44ecf9d04a75ed25e0408/Front-end-design-skill.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Project Technical Context

This project uses a modern, distinctive tech stack that enables creative expression:

**Core Stack**
**Use the following core stack in all next.js applications:**
- **Next.js 16.1.1** with React 19.2.3 and App Router
- **Tailwind CSS v4** - CSS-first configuration (no `tailwind.config.js`)
- **ShadCN base-vega** style with sky theme
- **@base-ui/react** - Headless accessible primitives
- **OKLCH color space** - Perceptually accurate colors
- **Raleway font** - Primary typeface (avoid defaulting to this for every design)
- **Hugeicons** - Icon library
- **tw-animate-css** - Animation utilities built-in

**Styling Configuration:**
- Theme tokens defined in `app/globals.css` using `@theme inline`
- CSS variables for all colors (easily customizable)
- Dark mode via `.dark` class with `@custom-variant dark (&:is(.dark *))`
- Sharp corners by default (`--radius: 0`) - can be overridden
- `cn()` utility for intelligent class merging (clsx + tailwind-merge)

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, glass morphism luxury, kinetic/motion-driven, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial, Inter, and Roboto; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font. Use Google Fonts or custom fonts. Consider display fonts like: Fraunces, Playfair Display, DM Serif Display, Bebas Neue, Oswald, Archivo Black, Righteous, or explore unique options beyond these.

- **Icons:** Use Hugeicons exclusively in all designs

- **Color & Theme**: Commit to a cohesive aesthetic. Use OKLCH color space for perceptually uniform colors. Leverage CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Go beyond the default sky blue theme - choose colors that match your aesthetic direction.

- **Motion & Animation**: Use animations for effects and micro-interactions. Multiple approaches available:
  - **CSS-only**: Use `tw-animate-css` utilities for simple animations
  - **Motion Primitives** (available at motion-primitives.com): Spring-based physics animations, text effects (scramble, shimmer, loop, fade-in-blur), morphing dialogs, cursor tracking, InView-triggered animations, background effects (BorderTrail), natural motion curves
  - **Framer Motion**: For complex orchestrated animations
  - Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.

- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density. Break free from standard two-column grids.

- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like:
  - Gradient meshes and mesh gradients
  - Noise textures and grain overlays
  - Geometric patterns
  - Layered transparencies
  - Dramatic shadows and glows
  - Decorative borders
  - Custom cursors
  - Glass morphism effects (translucency, backdrop-filter blur)

**NEVER** use generic AI-generated aesthetics like:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character
- Standard ShadCN component styling without customization
- Generic card-grid layouts with uniform spacing
- Boring hero sections with centered text and a button

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, Raleway, Inter, for example) across generations.

## Innovative Design Patterns & Registries

Beyond standard ShadCN components, explore these specialized registries for distinctive designs:

### Kokonut UI Patterns (kokonutui.com)

**Design Philosophy**: Motion-first, contemporary luxury with glass morphism

**When to Use**: Use always for the primary home page screen for apps as well as any Premium landing pages, portfolio sites, SaaS products, creative showcases

**Key Techniques:**
- **Glass Morphism**: `backdrop-filter: blur()` with semi-transparent backgrounds
- **Motion Integration**: Heavy use of Framer Motion for entrance/exit animations
- **Gradient Overlays**: Layer gradients over images for color harmony
- **Visual-Heavy Components**: Emphasize eye-catching, portfolio-worthy elements
- **Translucency & Depth**: Multiple layered elements with varying opacity

**Example Patterns:**
```tsx
// Glass effect card
<div className="bg-white/10 backdrop-blur-xl border border-white/20
                rounded-2xl shadow-2xl p-8">
  {/* Content with subtle animations */}
</div>

// Gradient overlay on image
<div className="relative">
  <img src="..." className="brightness-75" />
  <div className="absolute inset-0 bg-gradient-to-br
                  from-purple-500/60 to-pink-500/60 mix-blend-multiply" />
</div>
```

### Motion Primitives Patterns (motion-primitives.com)

**Design Philosophy**: Spring-based physics for natural, performant motion

**When to Use**: Interactive interfaces, engaging content sections, micro-interactions

**Key Components:**
- **Text Effects**: Scramble text reveals, shimmer effects, looping animations, fade-in-blur
- **Dialog Morphing**: Smooth transitions with image/content orchestration
- **Cursor Tracking**: Custom cursor implementations with hover interactions
- **InView Animations**: Trigger animations as elements enter viewport
- **Background Effects**: BorderTrail, animated backgrounds
- **Spring Physics**: Natural motion curves instead of linear transitions

**Example Patterns:**
```tsx
// Text scramble effect on hover
<motion.h1
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  whileHover={{ scale: 1.05 }}
  transition={{ type: "spring", stiffness: 300, damping: 20 }}
>
  Scrambled Text Effect
</motion.h1>

// InView triggered animation
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
  transition={{ type: "spring", duration: 0.8 }}
>
  Content revealed on scroll
</motion.div>
```

## Integration Strategies

**Approach 1: Extend Base Components**
Use accessible base components (Button, Card, Input) and layer distinctive styling:

```tsx
import { Button } from "@/components/ui/button"

// Transform generic button into distinctive design
<Button className="relative overflow-hidden bg-gradient-to-r from-emerald-500 to-teal-600
                   hover:from-emerald-600 hover:to-teal-700
                   shadow-lg hover:shadow-2xl
                   transform hover:scale-105 transition-all duration-300
                   font-display text-lg tracking-tight
                   before:absolute before:inset-0 before:bg-white/20
                   before:translate-x-full hover:before:translate-x-0
                   before:transition-transform before:duration-500">
  <span className="relative z-10">Get Started</span>
</Button>
```

**Approach 2: Build Custom Components**
Create entirely new components for unique aesthetic directions:

```tsx
export function GlassHeroSection() {
  return (
    <section className="relative min-h-screen overflow-hidden bg-slate-950">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-transparent to-pink-900/20" />

      {/* Glass morphism content card */}
      <div className="relative z-10 backdrop-blur-2xl bg-white/5 border border-white/10
                      rounded-3xl shadow-2xl p-12 max-w-4xl mx-auto mt-32">
        {/* Distinctive content */}
      </div>
    </section>
  )
}
```

**Approach 3: Combine Registry Patterns**
Mix Kokonut UI's glass effects with Motion Primitives' animations:

```tsx
import { motion } from "framer-motion"

<motion.div
  initial={{ opacity: 0, scale: 0.9 }}
  animate={{ opacity: 1, scale: 1 }}
  transition={{ type: "spring", stiffness: 200, damping: 20 }}
  className="bg-white/10 backdrop-blur-xl border border-white/20
             rounded-2xl shadow-2xl p-8"
>
  <motion.h2
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: 0.2, type: "spring" }}
  >
    Glass Effect with Spring Physics
  </motion.h2>
</motion.div>
```

## Project Structure & Setup

**Avoiding Workspace Root Issues:**

When creating Next.js projects, ensure clean project structure to avoid workspace root inference warnings:

1. **Single Lockfile Per Project**: Each Next.js project should have its own isolated `package-lock.json` in the project root, not in parent directories
2. **Explicit Root Configuration**: If you have a monorepo or multiple projects, explicitly set the root in `next.config.ts`:
   ```typescript
   import type { NextConfig } from 'next'

   const config: NextConfig = {
     turbopack: {
       root: process.cwd(), // Explicitly set workspace root
     },
   }

   export default config
   ```
3. **Clean Directory Structure**: When creating a new Next.js app, ensure it's in its own dedicated directory with no parent lockfiles interfering
4. **Remove Stray Lockfiles**: If you see warnings about multiple lockfiles, remove unnecessary ones from parent or sibling directories

**Common Warning:**
```
⚠ Warning: Next.js inferred your workspace root, but it may not be correct.
We detected multiple lockfiles and selected the directory of /path/to/package-lock.json
```

**Fix**: Either add `turbopack.root` to your config or clean up unnecessary lockfiles to have a single source of truth per project.

## Technical Implementation Tips

**Working with Tailwind v4:**
- Define custom colors in `app/globals.css` using OKLCH:
  ```css
  @theme inline {
    --color-accent: oklch(0.75 0.20 150);  /* Custom accent color */
  }
  ```
- Use CSS variables for dynamic theming
- Leverage arbitrary values: `bg-[oklch(0.5_0.2_200)]`

**Using @base-ui Primitives:**
- Start with accessible primitives (Button, Dialog, Input)
- Layer custom styling without losing accessibility
- Maintain ARIA attributes and keyboard navigation

**Animation Performance:**
- Use `transform` and `opacity` for GPU-accelerated animations
- Prefer CSS animations for simple effects
- Use Framer Motion or Motion Primitives for complex orchestrations
- Add `will-change` sparingly for performance-critical animations

**Color System:**
- Use OKLCH for perceptually uniform color scales
- Maintain WCAG contrast ratios (4.5:1 for text)
- Test dark mode thoroughly
- Create color schemes beyond blue/purple defaults

## Design Execution Checklist

Before delivering, ensure:
- [ ] **Distinctive aesthetic** - Not a generic ShadCN template
- [ ] **Typography** - Custom fonts that match the tone
- [ ] **Color harmony** - Cohesive palette using OKLCH
- [ ] **Strategic motion** - Animations enhance, not distract
- [ ] **Unexpected layout** - Not standard grid patterns
- [ ] **Atmospheric details** - Backgrounds, textures, effects
- [ ] **Accessibility** - Focus states, ARIA labels, keyboard nav
- [ ] **Responsiveness** - Works on all breakpoints
- [ ] **Performance** - Optimized animations and assets
- [ ] **Production-ready** - Clean, maintainable code

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision. Every design should make someone stop scrolling and say "wow, this is different."
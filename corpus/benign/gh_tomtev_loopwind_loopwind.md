---
name: loopwind
description: Use when working with .loopwind/ templates, loopwind CLI, OG images, social cards, or animated videos. Helps create, edit, and render image/video templates using Tailwind CSS + Satori.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata:
  version: "0.25.11"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: tomtev/loopwind
# corpus-url: https://github.com/tomtev/loopwind/blob/78b1a7dbc1ce4034f101cdb04e0cbdfeda9d7432/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# loopwind - Template-based image & video generation

Generate images (PNG, WebP, JPEG, SVG) and videos (MP4, GIF) from JSX templates using Tailwind CSS + Satori.

## Installed templates

!`npx loopwind list 2>/dev/null || echo "No templates found. Run: loopwind init && loopwind add <template>"`

## Commands

```bash
loopwind init                                    # Create loopwind.json config
loopwind add <template>                          # Install template from registry
loopwind list                                    # List installed templates
loopwind render <name> '{"prop":"value"}'        # Render image
loopwind render <name> '{"prop":"value"}' --format gif  # Render as GIF
loopwind validate [template]                     # Validate template metadata
```

## Project structure

```
.loopwind/
├── loopwind.json          # Config (colors, fonts, tokens)
├── my-template/
│   └── template.tsx       # Image template
└── my-video/
    └── template.tsx       # Video template
```

## Image template

```tsx
export const meta = {
  name: "my-template",
  type: "image",
  size: { width: 1200, height: 630, scale: 2 },
  props: { title: "string", subtitle: "string?" }
};

export default function Template({ title, subtitle, tw }) {
  return (
    <div style={tw('flex flex-col items-center justify-center w-full h-full bg-primary')}>
      <h1 style={tw('text-6xl font-bold text-white')}>{title}</h1>
      {subtitle && <p style={tw('text-2xl text-white/80 mt-4')}>{subtitle}</p>}
    </div>
  );
}
```

## Video template

```tsx
export const meta = {
  name: "my-video",
  type: "video",
  size: { width: 1920, height: 1080 },
  video: { fps: 30, duration: 3 },
  props: { title: "string", subtitle: "string?" }
};

export default function Template({ title, subtitle, tw }) {
  return (
    <div style={tw('flex flex-col items-center justify-center w-full h-full bg-black')}>
      <h1 style={tw('text-8xl font-bold text-white ease-out enter-bounce-in-up/0/600')}>
        {title}
      </h1>
      {subtitle && (
        <p style={tw('text-2xl text-white/80 mt-4 ease-out enter-fade-in-up/400/600')}>
          {subtitle}
        </p>
      )}
    </div>
  );
}
```

## Template helpers

All templates receive these props:

| Helper | Description |
|--------|-------------|
| `tw(classes)` | Convert Tailwind classes to inline styles |
| `qr(text)` | Generate QR code as data URI |
| `image(propKey)` | Load image prop as data URI |
| `video(propKey)` | Load video frame synced to animation (video only) |
| `template(name, props)` | Embed another template |
| `config` | Access loopwind.json config |
| `frame` | Current frame number (video only) |
| `progress` | Animation progress 0-1 (video only) |

### Helper examples

```tsx
// tw() - Tailwind to inline styles
<div style={tw('flex items-center justify-center bg-primary text-white p-8')}>

// qr() - Generate QR codes
<img src={qr('https://example.com')} width={200} height={200} />

// image() - Embed images (prop value: "./bg.jpg")
<img src={image('background')} style={tw('w-full h-full')} />

// video() - Embed video frames (prop value: "./video.mp4")
<img src={video('background')} style={tw('absolute inset-0')} />

// template() - Compose templates
{template('banner-hero', { title: 'Nested', subtitle: 'Template' })}
```

## Animation classes (video only)

Format: `enter-{anim}/{startMs}/{durationMs}`, `exit-{anim}/{startMs}/{durationMs}`, `loop-{anim}/{durationMs}`

### Enter animations

```tsx
<h1 style={tw('enter-fade-in/0/500')}>Fade in</h1>
<h1 style={tw('ease-out enter-bounce-in-up/0/600')}>Bounce in</h1>
<h1 style={tw('ease-out enter-fade-in-up/0/400')}>First</h1>
<p style={tw('ease-out enter-fade-in-up/200/400')}>Second (staggered)</p>
```

Available: `fade-in`, `fade-in-up`, `fade-in-down`, `fade-in-left`, `fade-in-right`, `slide-up`, `slide-down`, `slide-left`, `slide-right`, `bounce-in`, `bounce-in-up`, `bounce-in-down`, `bounce-in-left`, `bounce-in-right`, `scale-in`, `zoom-in`, `rotate-in`, `flip-in-x`, `flip-in-y`

### Exit animations

```tsx
<h1 style={tw('exit-fade-out/2500/500')}>Fade out at 2.5s</h1>
<h1 style={tw('enter-fade-in/0/500 exit-fade-out/2500/500')}>Enter and exit</h1>
```

Same names as enter but with "out" suffix (`fade-out`, `bounce-out-up`, etc.)

### Loop animations

```tsx
<div style={tw('loop-fade/500')}>Pulsing</div>
<div style={tw('loop-spin/2000')}>Spinning</div>
```

Available: `loop-fade`, `loop-bounce`, `loop-spin`, `loop-ping`, `loop-wiggle`, `loop-float`, `loop-pulse`, `loop-shake`

### Utility-based animations

Animate any property directly:

```tsx
<div style={tw('enter-translate-x-5/0/500')}>Slide 20px</div>
<div style={tw('enter-translate-y-full/0/800')}>Slide full height</div>
<div style={tw('enter-translate-y-[20px]/0/500')}>Exact 20px</div>
<div style={tw('enter-opacity-100/0/500')}>Fade in</div>
<div style={tw('enter-scale-150/0/800')}>Scale to 1.5x</div>
<div style={tw('enter-rotate-90/0/500')}>Rotate 90deg</div>
<div style={tw('enter--translate-x-5/0/500')}>Negative (slide left)</div>
```

Utilities: `translate-x-{n}`, `translate-y-{n}`, `opacity-{n}`, `scale-{n}`, `rotate-{n}`, `skew-x-{n}`, `skew-y-{n}`

### Easing

```tsx
<h1 style={tw('ease-out-cubic enter-bounce-in/0/500')}>With easing</h1>
<h1 style={tw('ease-spring enter-bounce-in/0/500')}>Spring physics</h1>
<h1 style={tw('ease-spring/1/170/8 enter-scale-in/0/800')}>Custom spring</h1>
```

Global: `linear`, `ease-in`, `ease-out`, `ease-in-out`, `ease-in-cubic`, `ease-out-cubic`, `ease-in-out-cubic`, `ease-in-quart`, `ease-out-quart`, `ease-in-out-quart`

Per-type: `enter-ease-*`, `exit-ease-*`, `loop-ease-*`

Spring: `ease-spring` (default), `ease-spring/mass/stiffness/damping`

## Satori limitations

**Not supported:** backdrop filters, 3D transforms, `calc()`, `z-index`

**Workarounds:** pre-calculate values instead of `calc()`, use DOM order instead of `z-index`

**Supported:** flexbox, colors, gradients, typography, spacing, borders, opacity, shadows, text-shadow, filters (blur, brightness, contrast, etc.)

## Key rules

1. Run `loopwind init` first in new projects
2. Every `<div>` with 2+ children MUST have `display: flex` (use `tw('flex ...')`)
3. Use `tw()` for all styling - it uses the project's Tailwind config
4. Image props auto-detected by file extension (.jpg, .png, etc.)
5. Default output: current directory (`my-template.png` or `my-video.mp4`)
6. Templates use React/JSX but render to static images/videos via Satori
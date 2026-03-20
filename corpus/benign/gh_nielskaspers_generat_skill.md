---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: nielskaspers/generate-visuals
# corpus-url: https://github.com/nielskaspers/generate-visuals/blob/c0eef407069cbcda45c41d390461844a1e63a95b/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# /generate-visuals — AI Image & Video Generation

Generate production-quality images and videos using AI. Works with any model — Gemini, Midjourney, DALL-E, Flux, Stable Diffusion, VEO, Runway, Kling, Sora, and others. All outputs should look authentic and human-made — never generic, never plastic, never stock.

## Trigger

`/generate-visuals` — or auto-suggest when user says: "generate image", "create image", "visual", "image gen", "generate video", "create video", "video gen", "text to video"

---

## Quick Start

**Fastest path to a good result:**

1. Tell me what you need: "I need a hero image for my SaaS landing page"
2. I'll ask 2-4 clarifying questions (or skip if you give enough detail)
3. I'll enhance your prompt using the pipeline below
4. You paste the enhanced prompt into your tool of choice

**Example — from vague to production-ready in one step:**

| You say | I generate |
|---------|-----------|
| "A person working on a laptop" | "A product designer in her early 30s sitting at a standing desk, reviewing a design system on a 27-inch monitor, one hand on a ceramic coffee mug. Late afternoon light through bamboo blinds casting striped shadows across the desk. Shot on Canon 5D Mark IV with an 85mm f/1.8 lens. Kodak Portra 400 warmth, slight film grain. Natural desk clutter: cable, notebook, pens. Slightly off-center handheld framing." |

---

## Decision Tree

```
User wants a visual?
├─ IMAGE
│  ├─ NEW image from text → generate prompt
│  ├─ EDIT existing image → generate edit instructions
│  └─ Multiple images (batch) → generate prompt variations
├─ VIDEO
│  ├─ NEW video from text → generate video prompt
│  ├─ Video from IMAGE + text → generate image-to-video prompt
│  └─ Multiple videos (batch) → generate prompt variations
└─ Unclear
   └─ Ask: "Do you want an image or a video?"
```

---

## Workflow Phases

### Phase 1: Interview (MANDATORY)

**Always ask before generating.** Batch these questions in a single message:

#### Common Questions (always ask)

1. **Image or video?** (if not clear from context)
2. **Aspect ratio**: `16:9` (hero/banner), `1:1` (social square), `4:5` (portrait), `9:16` (story/reel)
3. **Where will this live?**: Website hero, blog header, social post, ad creative, thumbnail, reel, internal doc?
4. **Vibe direction**: Bold & energetic? Clean & minimal? Warm & editorial? Dark & dramatic? Playful & colorful? Cinematic?

#### Image-Specific Questions

5. **Text on image?**: Any text to render? (headlines, CTAs, product names) — if yes, get exact wording
6. **Negative space**: Need space for text overlay? Which side?

#### Video-Specific Questions

5. **Duration**: `4s` (quick cut), `6s` (standard), `8s` (full scene)
6. **Audio/dialogue**: Dialogue, sound effects, ambient sound, music? If dialogue, exact words?
7. **Resolution**: `720p` (standard), `1080p`, `4k`?
8. **Starting image?**: Do you have a first frame to use?

#### Conditional Questions (ask when relevant)

- **Brand context**: Do you have brand guidelines (colors, archetype, visual style) to follow?
- **Reference**: Any visual reference or existing page/footage to match?

**Smart defaults — skip questions when context is obvious:**
- "Website hero" → `16:9`, need negative space for headline
- "Social post" → `1:1` or `4:5`, bold/eye-catching
- "Blog header" → `16:9`, editorial feel
- "Social reel" → `9:16`, 6-8s, bold/eye-catching, 720p
- "Hero background video" → `16:9`, 8s, ambient/cinematic loop, 720p

**Skip the interview ONLY when:** user provides a fully detailed prompt with ratio, style, and context already specified.

### Phase 2: Enhance Prompt

This is the critical step. Transform the user's raw description into a production-grade prompt that produces bold, authentic-looking assets.

**Enhancement Pipeline:**

```
Raw user input
  ↓
Step 1: SCENE EXPANSION — Turn vague descriptions into specific, tangible scenes
  ↓
Step 2: ANTI-AI INJECTION — Add imperfection cues that break the AI-generated look
  ↓
Step 3: PHOTOGRAPHY/CINEMATOGRAPHY GROUNDING — Anchor in real camera/lens/film language
  ↓
Step 4: BRAND DNA (if applicable) — Layer on the user's brand visual identity
  ↓
Step 5: COMPOSITION & MOTION — Optimize layout for context; add motion direction for video
  ↓
Step 6: TECHNICAL SPEC — Aspect ratio, quality, duration (video), hard constraints
  ↓
Enhanced prompt
```

**CRITICAL PRINCIPLE — Write like a creative director, not a tag list:**
AI models respond dramatically better to narrative scene descriptions than keyword lists. `"Cinematic wide shot of a futuristic sports car speeding through rainy Tokyo at night, neon reflections on wet asphalt"` destroys `"Cool car, neon, city, night, 8k"` every time. Always transform user input into a vivid narrative paragraph.

**The factors every enhanced prompt must include:**

| Factor | Image | Video |
|--------|-------|-------|
| **Subject** | who/what is in the scene | who/what is in the scene |
| **Composition** | camera angle, framing, depth | camera angle, framing, depth |
| **Action** | what's happening (even if static) | what's happening + how things move |
| **Environment** | specific setting with tangible details | specific setting with tangible details |
| **Lighting** | direction, quality, color temperature | direction, quality, color temp + how it changes |
| **Style/Mood** | emotional tone and visual treatment | emotional tone and visual treatment |
| **Camera movement** | — | dolly, pan, track, static, crane, handheld, drone |
| **Audio direction** | — | dialogue, ambient, music, sound effects |
| **Pacing** | — | slow/contemplative, medium/natural, fast/energetic |

**Step 1 — Scene Expansion:**
Never pass a vague prompt through. Transform every vague input into a specific, tangible scene.

| Vague | Expanded |
|-------|----------|
| "A person editing photos" | "A young creative professional sitting cross-legged on a mustard-yellow velvet couch, laptop balanced on their knees, colorful mood board pinned to the exposed-brick wall behind them, afternoon sunlight cutting diagonal shadows across the floor" |
| "A nice restaurant" | "A dimly lit corner table at a Mediterranean restaurant — a single candle in a glass holder, olive oil in a ceramic dish, fresh rosemary sprig on a terracotta plate, exposed stone wall with warm sconce lighting" |
| "Someone running" | "A trail runner mid-stride on a single-track mountain path at dawn, breath visible in the cold air, mud-splattered compression tights, distant peaks catching the first pink light of sunrise" |
| "Office workspace" | "A standing desk setup with a 27-inch monitor showing code, a half-drunk pour-over coffee in a double-walled glass, a well-loved mechanical keyboard with visible key wear, afternoon light through bamboo blinds casting striped shadows" |
| "A car" | "A dusty 1974 Porsche 911 Carrera parked on a gravel shoulder overlooking the Pacific coast, late afternoon fog rolling in, paint faded to a warm patina of Tangerine Orange" |

**Step 2 — Anti-AI Injection (CRITICAL):**
The number one goal is visuals that DON'T look AI-generated. Always include 2-3 of these cues:

| Technique | Prompt Fragment |
|-----------|----------------|
| Film stock reference | "Shot on Kodak Portra 400" or "Kodak Vision3 500T film grain" |
| Lens imperfection | "Slight chromatic aberration at edges" or "natural lens vignette" |
| Handheld micro-motion (video) | "Subtle handheld camera movement" or "organic steadicam drift" |
| Light physics | "Subtle lens flare from backlight" or "light spill from off-frame window" |
| Material texture | "Visible weave in the fabric" or "fingerprints on the glass surface" |
| Environmental detail | "Dust particles caught in the light beam" or "leaves gently rustling in background" |
| Analog process | "Slightly lifted blacks like faded print" or "gentle halation around highlights" |
| Human touch | "Slightly asymmetric framing" or "not perfectly centered, as if shot handheld" |
| Depth cues | "Foreground element slightly soft" or "rack focus between subjects" |
| Audio realism (video) | "Ambient room tone with distant city sounds" or "footsteps echoing on concrete" |

**Step 3 — Photography/Cinematography Grounding:**
Anchor every visual in real camera language:

For images:
```
Camera: "Shot on [Canon 5D Mark IV / Sony A7III / Hasselblad 500C]"
Lens: "[35mm f/1.4 / 85mm f/1.8 / 24-70mm f/2.8]"
Film: "[Kodak Portra 400 / Fuji Pro 400H / cross-processed Ektachrome]"
```

For video:
```
Camera: "Shot on Arri Alexa Mini / RED V-Raptor / Canon C300"
Lens: "Anamorphic 40mm / Cooke S4 50mm / vintage Helios 44-2 swirl bokeh"
Movement: "Slow dolly push-in / smooth Steadicam follow / locked-off tripod"
Grade: "Teal and orange grade / lifted shadows / high contrast with milky blacks"
```

For illustration/graphic styles, skip camera grounding and instead specify:
```
Medium: "[Gouache on textured paper / screen print / risograph in 3 colors]"
Style: "[2D cel animation / stop-motion with visible texture / kinetic typography]"
```

**Step 4 — Brand DNA (if applicable):**

If the user has a defined brand, layer it here. If not, skip this step.

Use the **Brand DNA Template** to capture the user's visual identity:

```
Brand Archetype: [Your brand's personality — e.g., "The Explorer", "The Sage", "The Creator"]

Visual Language:
- [Trait 1]: [How it manifests in images — e.g., "Bold, not safe: High contrast, saturated accents"]
- [Trait 2]: [e.g., "Warm and human: Real emotions, candid energy"]
- [Trait 3]: [e.g., "Premium but approachable: Sophisticated yet welcoming"]

Signature Colors (use as accents, not floods):
- Primary accent: [color name + hex code]
- Secondary accent: [color name + hex code]
- Background: [color name + hex code]
- Text: [color name + hex code]

Color Palettes (rotate between assets — never use just one):
- Palette A: [3-4 colors]
- Palette B: [3-4 colors]
- Palette C: [3-4 colors]

Photography Direction:
- Subjects: [Who appears in brand imagery]
- Environments: [Where scenes take place]
- Energy: [Calm/energetic/contemplative/bold]

What We Are NOT:
- [Anti-pattern 1 — e.g., "Corporate stock photography"]
- [Anti-pattern 2 — e.g., "Sterile tech minimalism"]
- [Anti-pattern 3 — e.g., "Static, lifeless compositions"]
```

**First time using this skill?** I'll ask if you have brand guidelines. If yes, we fill this in once and reference it for all future generations. If no, I'll generate with universal aesthetic principles.

**Step 5 — Composition & Motion:**

**Image composition by context:**

| Where It Lives | Composition Rules |
|----------------|-------------------|
| **Website hero** | Leave 40% negative space on left OR right for headline. Subject anchored to opposite side. |
| **Section image** | Centered or slightly off-center. Self-contained. |
| **Blog header** | Wider, more atmospheric. Subject can be smaller. Mood > detail. |
| **Social post** | Fill the frame. Bold, immediate impact. Works at thumbnail size. |
| **Thumbnail** | Extreme contrast. Face or key object fills 60%+. Space for 2-3 word overlay. |
| **Ad creative** | Product/result front and center. Clear visual hierarchy. CTA-ready zone. |

**Video motion direction:**

| Element | Direction Options |
|---------|-------------------|
| **Camera** | Static/locked, slow dolly, tracking follow, crane up/down, handheld, drone aerial, whip pan, push-in, pull-out |
| **Subject motion** | Walking, creating, gesturing, turning, revealing, reacting, interacting |
| **Background motion** | Clouds moving, traffic flowing, particles drifting, light shifting, leaves rustling |
| **Pacing** | Slow-motion (dreamy), real-time (natural), time-lapse (dynamic), quick cuts (energetic) |
| **Audio** | Dialogue in quotes, ambient (city, nature, room), music style, sound effects, silence |

**Step 6 — Technical Spec:**

For images, always append:
```
Aspect ratio: {ratio}
Output: Single high-fidelity image, production-ready
No watermarks, no "AI-generated" artifacts, no placeholder text
No generic stock-photo compositions
```

For videos, always append:
```
Aspect ratio: {ratio}
Duration: {seconds} seconds
Resolution: {resolution}
Output: Single high-fidelity video, production-ready
No watermarks, no "AI-generated" artifacts, no placeholder text overlays
Smooth, natural motion — no jittering or morphing artifacts
```

### Phase 3: Use Your Tool

Take the enhanced prompt and paste it into your AI generation tool of choice.

**Recommended free tool to get started:** [Picsart Aura](https://picsart.com/aura/) — free to try, supports the narrative prompting style this skill teaches.

**Other popular tools:**

| Tool | Best For | Notes |
|------|----------|-------|
| **Gemini** | Text rendering, complex constraints, editing | Best prompt adherence |
| **Midjourney** | Artistic interpretation, style mixing | May over-stylize; add specificity |
| **DALL-E** | Prompt following, safety compliance | Can feel polished; add imperfection cues |
| **Flux** | Photorealism, faces | Can default to "AI pretty"; push for imperfection |
| **Stable Diffusion** | Full control (LoRAs, ControlNet) | Needs more technical prompts |
| **VEO 3** | Natural video motion, audio generation | 8s max clips; push for imperfection |
| **Runway** | Video generation, motion control | Good for stylized content |
| **Sora** | Physics, long coherent video shots | Push hard for imperfection |
| **Kling** | Character consistency in video | Good for narrative clips |

**Model-agnostic tips:**
- If a model ignores imperfection cues, double them — add both a film stock AND a lens artifact AND environmental detail
- If output looks too "clean", add: "Shot on expired Kodak Gold 200, slight color shift, visible grain structure"
- If faces look uncanny, add: "Natural skin texture with visible pores, asymmetric features, genuine expression — not retouched"
- For video: if motion feels robotic, add: "Organic handheld micro-movement, not robotically smooth, subtle breathing rhythm"

### Phase 4: Review & Iterate

After generating:
1. Show the user the output
2. Ask: "How does this look? Any adjustments?"
3. If iterating:
   - **Round 1**: Fix composition, scene, subjects (major changes OK)
   - **Round 2**: Fix lighting, colors, textures (targeted refinements)
   - **Round 3**: Polish artifacts, text, final details (minimal changes)
4. If 80% correct, use conversational editing: "Keep everything, but change the lighting to golden hour"
5. For video: extend duration if the tool supports it

---

## Use-Case Taxonomy

### Image Use Cases (16 categories)

| Slug | Description | Default Style |
|------|-------------|---------------|
| `photorealistic-natural` | Real-world scenes, landscapes, people | Sharp detail, natural light, film-grounded |
| `photorealistic-studio` | Product shots, controlled lighting | Studio setup, clean background, tactile materials |
| `product-mockup` | Device/packaging mockups | Clean floating product, environmental context |
| `ui-mockup` | App/web interface screenshots | Flat design, crisp edges, realistic device |
| `editorial-illustration` | Blog/article illustrations | Artistic, conceptual, textured medium |
| `icon-set` | Icons, badges, small graphics | Consistent style, simple, graphic |
| `infographic` | Data viz, process diagrams | Clean layout, bold colors, clear hierarchy |
| `social-media` | Posts, stories, covers | Bold, high-contrast, scroll-stopping |
| `banner-ad` | Display ads, promotional | CTA-focused, vibrant, high-contrast |
| `hero-image` | Website hero sections | Cinematic, high-impact, negative space for text |
| `thumbnail` | Video/article thumbnails | Bold text, faces, extreme contrast |
| `logo-concept` | Logo explorations | Minimal, scalable, memorable |
| `pattern-texture` | Repeating patterns, backgrounds | Tileable, subtle, organic feel |
| `character-design` | Characters, mascots, avatars | Expressive, consistent style sheet |
| `3d-render` | 3D product/scene renders | Realistic materials, dramatic lighting |
| `abstract-art` | Abstract, generative art | Bold, experimental, tactile |

### Video Use Cases (12 categories)

| Slug | Description | Default Style |
|------|-------------|---------------|
| `cinematic-narrative` | Story-driven scenes, short films, hero videos | Arri Alexa look, anamorphic, dramatic lighting |
| `product-demo` | Product in use, feature showcase | Clean studio/environment, focused tracking shots |
| `social-reel` | Instagram/TikTok reels, YouTube Shorts | Bold, fast-paced, scroll-stopping, 9:16 |
| `hero-background` | Website hero section ambient video | Slow, atmospheric, seamless loop potential |
| `ad-creative` | Display/social ads, promotional clips | CTA-focused, high-energy, product-centric |
| `explainer` | How-to, tutorial, process visualization | Clean, step-by-step, clear visual hierarchy |
| `ambient-mood` | Background loops, atmosphere, texture | Slow-motion, abstract, meditative |
| `testimonial-style` | Talking head, interview format | Natural lighting, shallow DOF, conversational |
| `event-hype` | Launch announcements, event promos | Energetic, quick cuts, building momentum |
| `aerial-landscape` | Drone shots, establishing shots, environments | Wide, sweeping, golden hour, epic scale |
| `motion-graphics` | Kinetic typography, animated infographics | Clean, bold, geometric |
| `behind-the-scenes` | Process, making-of, authentic moments | Handheld, candid, documentary feel |

---

## Prompt Scaling

When you need to generate multiple related assets (e.g., a set of blog headers, a social media campaign, product shots from different angles), use systematic prompt variations:

### Variation Strategies

| What to Vary | Keep Constant | Use Case |
|--------------|---------------|----------|
| **Subject/person** | Lighting, composition, style | Diverse representation across assets |
| **Color palette** | Subject, composition, mood | A/B testing, seasonal variants |
| **Angle/composition** | Subject, lighting, style | Product shots, architectural series |
| **Time of day** | Subject, location, composition | Mood variations for the same scene |
| **Style treatment** | Subject, composition | Photo vs. illustration vs. 3D comparison |
| **Environment** | Subject, action, style | Same person in different settings |

### Batch Prompt Template

```
BASE PROMPT: [Your core scene description — subject, action, composition]

VARIATION 1: [Base] + "Morning golden hour, warm tones, Kodak Portra 400"
VARIATION 2: [Base] + "Overcast afternoon, muted tones, Fuji Pro 400H"
VARIATION 3: [Base] + "Blue hour twilight, cool tones, Kodak Ektachrome"
VARIATION 4: [Base] + "Harsh midday sun, high contrast, Ilford HP5 black and white"
```

### Campaign Consistency

For a cohesive series of images:
1. Lock these elements: camera body, lens, film stock, color grade
2. Vary these elements: subject, location, time of day
3. Define your "visual thread" — the one element that ties them all together (e.g., always shot on 35mm, always includes a warm accent color, always slightly off-center framing)

---

## Anti-AI Visual Checklist

Before finalizing any prompt, verify it includes:

- [ ] **Film/camera anchor** — Real camera, lens, or film stock reference (OR analog medium/animation style)
- [ ] **At least 2 imperfection cues** — Grain, lens artifacts, texture, asymmetry, environmental detail
- [ ] **Specific material descriptions** — "Worn leather" not "leather", "brushed aluminum" not "metal"
- [ ] **Real-world lighting** — Named light source, direction, color temperature
- [ ] **NO banned phrases**: "stunning", "sleek", "futuristic", "cutting-edge", "vibrant" (these produce generic AI output)
- [ ] **Human energy** — Candid poses, real emotions, environmental context (not floating in void)

**Video-specific additions:**
- [ ] **Specific motion description** — Camera movement + subject movement + environmental movement
- [ ] **Audio direction** — Ambient sound, dialogue, music mood, or intentional silence
- [ ] **Temporal arc** — The scene should evolve over its duration (light shifts, subject moves, something changes)

---

## Prompting Best Practices (Quick Reference)

1. **Ground in reality** — Reference specific cameras, film stocks, lenses, or analog mediums
2. **Describe materials, not just objects** — "Cracked leather-bound journal" beats "a book"
3. **Name the light** — "Late afternoon sun through venetian blinds" beats "warm lighting"
4. **Add imperfection** — Film grain, bokeh, lens vignette, dust, asymmetry
5. **Be compositionally specific** — "Subject in right third, looking left, negative space on left"
6. **Set mood through environment** — Show context, not just subject
7. **For text rendering (images)** — Specify exact text, font style, size, position, color
8. **For website heroes** — Always specify where negative space should be for headline overlay
9. **For video: describe motion, not stills** — "Camera slowly tracks left as..." not "a scene of..."
10. **For video: direct audio explicitly** — Dialogue in quotes, describe ambient sounds, suggest music mood
11. **Vary your palette** — Never default to blue/purple gradients. Surprise yourself.
12. **Iterate** — First pass for composition, second for details, third for polish

---

## Auto-Load

This skill is self-contained. No external writing guides or references needed.

**Dependencies loaded by this skill:**
- `references/image-prompting.md` — comprehensive image prompt engineering guide
- `references/video-prompting.md` — video prompt engineering guide
- `references/image-sample-prompts.md` — copy-paste image prompt templates
- `references/video-sample-prompts.md` — copy-paste video prompt templates
- `references/advanced-prompting-research.md` — advanced prompting techniques and research

---

## Quality Checklist

Before delivering the final output:

**Common:**
- [ ] Correct aspect ratio for the use case
- [ ] No unwanted text, watermarks, or labels
- [ ] Composition matches the requested style
- [ ] Production-ready (no artifacts, proper resolution)
- [ ] Anti-AI checklist passed (imperfections, grounding, materials)

**Image-specific:**
- [ ] Text overlays (if any) are legible and correctly spelled

**Video-specific:**
- [ ] Duration matches the requested length
- [ ] Motion is smooth and natural (no jittering/morphing)
- [ ] Audio (if included) matches the scene
- [ ] Temporal arc present (something changes over the duration)
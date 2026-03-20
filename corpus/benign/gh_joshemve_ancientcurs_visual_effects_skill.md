---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: joshemve/ancientcurse
# corpus-url: https://github.com/joshemve/ancientcurse/blob/7539d0aad792e97b938d2fbca0d24f7b789e8aef/VISUAL_EFFECTS_SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Visual Effects Skill Guide for Minecraft 1.20.1 Fabric

This document provides comprehensive guidance for creating high-quality visual effects in Minecraft 1.20.1 Fabric mods. Use this as a reference when implementing shaders, particle effects, glow effects, and anime-style visuals.

## Table of Contents
1. [Core Shader Architecture](#1-core-shader-architecture)
2. [RenderLayer System](#2-renderlayer-system)
3. [GLSL Shader Programming](#3-glsl-shader-programming)
4. [Procedural Noise Functions](#4-procedural-noise-functions)
5. [Glow and Bloom Techniques](#5-glow-and-bloom-techniques)
6. [Anime-Style Effects](#6-anime-style-effects)
7. [Particle Systems](#7-particle-systems)
8. [Performance Optimization](#8-performance-optimization)
9. [Common Patterns and Examples](#9-common-patterns-and-examples)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Core Shader Architecture

### Overview

Minecraft 1.20.1 uses **core shaders** for rendering game elements. These are separate from post-processing shaders (Iris/OptiFine).

**Key Limitation:** Core shaders cannot do screen-space post-processing (true bloom, motion blur, depth of field). All effects must be achieved through geometry, multi-pass rendering, and clever shader tricks.

### File Structure

```
assets/<namespace>/shaders/
├── core/
│   ├── <shader_name>.json     # Configuration
│   ├── <shader_name>.vsh      # Vertex shader (GLSL 150)
│   └── <shader_name>.fsh      # Fragment shader (GLSL 150)
└── include/
    └── <helper>.glsl          # Shared functions
```

### Shader JSON Configuration

```json
{
    "blend": {
        "func": "add",
        "srcrgb": "srcalpha",
        "dstrgb": "one"
    },
    "vertex": "ancientcurse:rendertype_sun_beam",
    "fragment": "ancientcurse:rendertype_sun_beam",
    "attributes": ["Position", "Color", "UV0"],
    "samplers": [
        { "name": "Sampler0" }
    ],
    "uniforms": [
        { "name": "ModelViewMat", "type": "matrix4x4", "count": 16, "values": [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] },
        { "name": "ProjMat", "type": "matrix4x4", "count": 16, "values": [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1] },
        { "name": "ColorModulator", "type": "float", "count": 4, "values": [1.0, 1.0, 1.0, 1.0] },
        { "name": "GameTime", "type": "float", "count": 1, "values": [0.0] },
        { "name": "FogStart", "type": "float", "count": 1, "values": [0.0] },
        { "name": "FogEnd", "type": "float", "count": 1, "values": [1.0] },
        { "name": "FogColor", "type": "float", "count": 4, "values": [0.0, 0.0, 0.0, 0.0] }
    ]
}
```

### Available Uniforms

| Uniform | Type | Description |
|---------|------|-------------|
| `ModelViewMat` | mat4 | Model-view transformation matrix |
| `ProjMat` | mat4 | Projection matrix |
| `GameTime` | float | Cycles 0→1 over ~20 minutes (1200 seconds) |
| `ColorModulator` | vec4 | Global RGBA color multiplier |
| `FogStart` | float | Distance where fog begins |
| `FogEnd` | float | Distance where fog is complete |
| `FogColor` | vec4 | Fog RGBA color |

### Blend Modes Reference

| Effect | func | srcrgb | dstrgb | Formula |
|--------|------|--------|--------|---------|
| **Additive (Glow)** | add | srcalpha | one | `Src × α + Dst × 1` |
| **Alpha Blend** | add | srcalpha | one_minus_srcalpha | `Src × α + Dst × (1-α)` |
| **Multiply** | add | dstcolor | zero | `Src × Dst` |
| **Screen** | add | one | one_minus_srccolor | `1 - (1-Src)(1-Dst)` |

**For glow effects, always use additive blending:**
```json
"blend": { "func": "add", "srcrgb": "srcalpha", "dstrgb": "one" }
```

---

## 2. RenderLayer System

### Built-in RenderLayers for Effects

```java
// Additive glow (best for divine/energy effects)
RenderLayer.getBeaconBeam(texture, true);  // true = additive

// Transparent with depth
RenderLayer.getEntityTranslucent(texture);

// Alpha cutout (no blending)
RenderLayer.getEntityCutoutNoCull(texture);

// Solid opaque
RenderLayer.getEntitySolid(texture);
```

### Creating Custom RenderLayers

```java
import net.minecraft.client.render.RenderLayer;
import net.minecraft.client.render.RenderPhase;
import net.minecraft.client.render.VertexFormat;
import net.minecraft.client.render.VertexFormats;

public class ModRenderLayers extends RenderLayer {

    public static RenderLayer getCustomGlow(Identifier texture) {
        return RenderLayer.of(
            "custom_glow",
            VertexFormats.POSITION_COLOR_TEXTURE_OVERLAY_LIGHT_NORMAL,
            VertexFormat.DrawMode.QUADS,
            256,
            false,  // no affect crumbling
            true,   // translucent sorting
            RenderLayer.MultiPhaseParameters.builder()
                .program(BEACON_BEAM_PROGRAM)
                .texture(new RenderPhase.Texture(texture, false, false))
                .transparency(ADDITIVE_TRANSPARENCY)
                .writeMaskState(COLOR_MASK)
                .build(false)
        );
    }
}
```

---

## 3. GLSL Shader Programming

### GLSL 150 Syntax (Minecraft 1.20.1)

```glsl
#version 150

// Vertex shader inputs
in vec3 Position;
in vec4 Color;
in vec2 UV0;

// Vertex → Fragment communication
out vec4 vertexColor;
out vec2 texCoord0;
out float vertexDistance;

// Fragment shader output
out vec4 fragColor;
```

### Basic Vertex Shader Template

```glsl
#version 150

in vec3 Position;
in vec4 Color;
in vec2 UV0;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform float GameTime;

out vec4 vertexColor;
out vec2 texCoord0;
out float vertexDistance;

void main() {
    vec4 viewPos = ModelViewMat * vec4(Position, 1.0);
    gl_Position = ProjMat * viewPos;

    vertexDistance = length(viewPos.xyz);
    vertexColor = Color;

    // Animated UV scrolling
    texCoord0 = UV0 + vec2(0.0, GameTime * 20.0);
}
```

### Basic Fragment Shader Template

```glsl
#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;
uniform vec4 ColorModulator;
uniform float GameTime;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in vec4 vertexColor;
in vec2 texCoord0;
in float vertexDistance;

out vec4 fragColor;

void main() {
    vec4 texColor = texture(Sampler0, texCoord0);
    vec4 color = texColor * vertexColor * ColorModulator;

    // Apply fog
    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
```

---

## 4. Procedural Noise Functions

### Hash-Based Random

```glsl
float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

float random(float x) {
    return fract(sin(x) * 43758.5453123);
}
```

### Value Noise

```glsl
float valueNoise(vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    // Four corners
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    // Smooth interpolation
    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}
```

### Fractal Brownian Motion (FBM)

**Essential for organic effects like fire, plasma, clouds:**

```glsl
float fbm(vec2 st) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;

    // 5 octaves
    for (int i = 0; i < 5; i++) {
        value += amplitude * valueNoise(st * frequency);
        frequency *= 2.0;      // Lacunarity
        amplitude *= 0.5;      // Gain/Persistence
    }

    return value;
}

// Turbulence variation (sharper, more chaotic)
float turbulence(vec2 st) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;

    for (int i = 0; i < 5; i++) {
        value += amplitude * abs(valueNoise(st * frequency) * 2.0 - 1.0);
        frequency *= 2.0;
        amplitude *= 0.5;
    }

    return value;
}
```

### Simplex Noise (Higher Quality)

```glsl
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x * 34.0) + 1.0) * x); }

float snoise(vec2 v) {
    const vec4 C = vec4(0.211324865405187, 0.366025403784439,
                       -0.577350269189626, 0.024390243902439);

    vec2 i  = floor(v + dot(v, C.yy));
    vec2 x0 = v - i + dot(i, C.xx);

    vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;

    i = mod289(i);
    vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));

    vec3 m = max(0.5 - vec3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0);
    m = m * m;
    m = m * m;

    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;

    m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);

    vec3 g;
    g.x = a0.x * x0.x + h.x * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;

    return 130.0 * dot(m, g);
}
```

---

## 5. Glow and Bloom Techniques

### Multi-Layer Glow (No Post-Processing)

The key technique for creating convincing glow without true bloom:

```glsl
// Fragment shader glow simulation
vec3 simulateBloom(vec3 baseColor, vec2 uv, float intensity) {
    vec3 result = baseColor;

    // Layer 1: Core brightness
    float coreFalloff = 1.0 - length(uv - 0.5) * 2.0;
    coreFalloff = max(0.0, coreFalloff);
    result += baseColor * pow(coreFalloff, 2.0) * 0.5;

    // Layer 2: Warm corona
    vec3 warmTint = vec3(1.0, 0.9, 0.7);
    float coronaFalloff = 1.0 - length(uv - 0.5) * 1.5;
    coronaFalloff = max(0.0, coronaFalloff);
    result += warmTint * pow(coronaFalloff, 1.5) * 0.3;

    // Layer 3: Outer bloom
    vec3 bloomTint = vec3(1.0, 0.7, 0.3);
    float bloomFalloff = 1.0 - length(uv - 0.5);
    bloomFalloff = max(0.0, bloomFalloff);
    result += bloomTint * pow(bloomFalloff, 1.0) * 0.15;

    return result * intensity;
}
```

### Java-Side Multi-Layer Rendering

```java
private void renderBeamLayers(MatrixStack poseStack, VertexConsumerProvider bufferSource,
        float beamLength, float intensity, float time) {

    // Layer 1: Outer bloom (largest, faintest)
    renderBeamLayer(poseStack, bufferSource, TEXTURE,
            beamLength, BEAM_WIDTH * 1.5f,
            1.0f, 0.7f, 0.2f,  // Golden orange
            0.15f * intensity, time, 0);

    // Layer 2: Outer halo
    renderBeamLayer(poseStack, bufferSource, TEXTURE,
            beamLength, BEAM_WIDTH * 0.8f,
            1.0f, 0.85f, 0.4f,  // Light gold
            0.3f * intensity, time, 1);

    // Layer 3: Inner corona (with pulse)
    float pulse = 1.0f + MathHelper.sin(time * 0.5f) * 0.2f;
    renderBeamLayer(poseStack, bufferSource, TEXTURE,
            beamLength, BEAM_WIDTH * 0.4f * pulse,
            1.0f, 0.95f, 0.7f,  // Pale yellow
            0.6f * intensity, time, 2);

    // Layer 4: Core beam (brightest)
    renderBeamLayer(poseStack, bufferSource, TEXTURE,
            beamLength, BEAM_WIDTH * 0.15f,
            1.0f, 1.0f, 0.95f,  // Near white
            0.95f * intensity, time, 3);

    // Layer 5: Super-bright center
    renderBeamLayer(poseStack, bufferSource, TEXTURE,
            beamLength, BEAM_WIDTH * 0.05f,
            1.0f, 1.0f, 1.0f,  // Pure white
            1.0f * intensity, time, 4);
}
```

### Radial Glow Function

```glsl
float radialGlow(vec2 uv, float intensity) {
    float dist = length(uv - 0.5) * 2.0;
    float glow = 1.0 - smoothstep(0.0, 1.0, dist);
    return pow(glow, intensity);
}

// Usage in fragment shader
float glow = radialGlow(texCoord0, 2.0);
vec3 glowColor = baseColor.rgb * (1.0 + glow * 0.5);
```

---

## 6. Anime-Style Effects

### Energy Beam / Slash Effect

Key characteristics of anime energy effects:
1. **Hard edges with soft glow** - Sharp core, diffuse bloom
2. **Speed lines** - Radial or directional streaks
3. **Color gradients** - White core → saturated color → transparent
4. **Motion blur** - Stretched in direction of travel
5. **Sparkles/particles** - Small bright points

```glsl
// Anime-style energy slash
vec4 animeSlash(vec2 uv, float time) {
    // Core slash (sharp edge)
    float slashCore = 1.0 - abs(uv.y - 0.5) * 4.0;
    slashCore = max(0.0, slashCore);
    slashCore = pow(slashCore, 3.0);  // Sharpen

    // Soft glow around slash
    float slashGlow = 1.0 - abs(uv.y - 0.5) * 2.0;
    slashGlow = max(0.0, slashGlow);
    slashGlow = pow(slashGlow, 1.5);

    // Speed lines (horizontal streaks)
    float speedLines = 0.0;
    for (int i = 0; i < 8; i++) {
        float offset = random(float(i)) * 0.8 - 0.4;
        float lineY = uv.y + offset;
        float line = 1.0 - abs(lineY - 0.5) * 20.0;
        line = max(0.0, line);
        line *= random(vec2(float(i), time * 10.0));
        speedLines += line * 0.3;
    }

    // Sparkles
    float sparkle = random(uv * 50.0 + time * 5.0);
    sparkle = pow(sparkle, 20.0) * 3.0;

    // Combine
    vec3 coreColor = vec3(1.0, 1.0, 1.0);  // White core
    vec3 glowColor = vec3(1.0, 0.8, 0.3);  // Golden glow
    vec3 edgeColor = vec3(1.0, 0.4, 0.1);  // Orange edge

    vec3 color = coreColor * slashCore;
    color += glowColor * slashGlow * 0.5;
    color += edgeColor * speedLines;
    color += vec3(1.0) * sparkle;

    float alpha = slashCore + slashGlow * 0.3 + speedLines * 0.2 + sparkle;

    return vec4(color, alpha);
}
```

### Heat Distortion Effect

```glsl
// Heat shimmer/distortion
vec2 heatDistortion(vec2 uv, float time, float intensity) {
    float distortX = sin(uv.y * 30.0 + time * 3.0) * 0.01;
    float distortY = cos(uv.x * 20.0 + time * 2.5) * 0.005;

    // Stronger near center
    float centerDist = length(uv - 0.5);
    float falloff = 1.0 - smoothstep(0.0, 0.5, centerDist);

    return uv + vec2(distortX, distortY) * intensity * falloff;
}

// Usage
vec2 distortedUV = heatDistortion(texCoord0, GameTime * 1200.0, 1.0);
vec4 texColor = texture(Sampler0, distortedUV);
```

### Chromatic Aberration

```glsl
// Color fringing at edges
vec4 chromaticAberration(sampler2D tex, vec2 uv, float intensity) {
    float edgeFactor = length(uv - 0.5) * 2.0;
    float aberration = edgeFactor * intensity * 0.02;

    float r = texture(tex, uv + vec2(aberration, 0.0)).r;
    float g = texture(tex, uv).g;
    float b = texture(tex, uv - vec2(aberration, 0.0)).b;
    float a = texture(tex, uv).a;

    return vec4(r, g, b, a);
}
```

### Pulsing/Breathing Effect

```glsl
// Organic pulsing
float pulse(float time, float speed, float min, float max) {
    float t = sin(time * speed) * 0.5 + 0.5;
    return mix(min, max, t);
}

// Multiple layered pulses for organic feel
float organicPulse(float time) {
    float p1 = sin(time * 2.0) * 0.5 + 0.5;
    float p2 = sin(time * 3.7 + 1.2) * 0.3 + 0.5;
    float p3 = sin(time * 5.3 + 2.8) * 0.2 + 0.5;
    return (p1 + p2 + p3) / 3.0;
}
```

---

## 7. Particle Systems

### Spawning Particles from Java

```java
// Dust particles (custom color and size)
DustParticleEffect dust = new DustParticleEffect(
    new Vector3f(1.0f, 0.8f, 0.3f),  // RGB color
    1.2f  // Size
);
world.addParticle(dust, x, y, z, velocityX, velocityY, velocityZ);

// Built-in particle types
world.addParticle(ParticleTypes.FLAME, x, y, z, vx, vy, vz);
world.addParticle(ParticleTypes.END_ROD, x, y, z, vx, vy, vz);
world.addParticle(ParticleTypes.ELECTRIC_SPARK, x, y, z, vx, vy, vz);
world.addParticle(ParticleTypes.ENCHANT, x, y, z, vx, vy, vz);
world.addParticle(ParticleTypes.LAVA, x, y, z, 0, 0, 0);
```

### Circular Burst Pattern

```java
void spawnCircularBurst(World world, Vec3d center, int count, float speed) {
    for (int i = 0; i < count; i++) {
        double angle = (i / (double) count) * Math.PI * 2;
        double vx = Math.cos(angle) * speed;
        double vz = Math.sin(angle) * speed;

        world.addParticle(ParticleTypes.FLAME,
            center.x, center.y, center.z,
            vx, 0.02, vz);
    }
}
```

### Spherical Burst Pattern

```java
void spawnSphericalBurst(World world, Vec3d center, int count, float speed) {
    Random random = new Random();
    for (int i = 0; i < count; i++) {
        // Random point on sphere
        double theta = random.nextDouble() * Math.PI * 2;
        double phi = Math.acos(2 * random.nextDouble() - 1);

        double vx = Math.sin(phi) * Math.cos(theta) * speed;
        double vy = Math.sin(phi) * Math.sin(theta) * speed;
        double vz = Math.cos(phi) * speed;

        world.addParticle(ParticleTypes.END_ROD,
            center.x, center.y, center.z,
            vx, vy, vz);
    }
}
```

### Spiral Pattern

```java
void spawnSpiralParticles(World world, Vec3d center, float time, int count) {
    for (int i = 0; i < count; i++) {
        float progress = i / (float) count;
        float angle = time * 2.0f + progress * (float) Math.PI * 4;
        float radius = 0.3f + progress * 0.5f;
        float height = progress * 2.0f;

        double x = center.x + Math.cos(angle) * radius;
        double y = center.y + height;
        double z = center.z + Math.sin(angle) * radius;

        world.addParticle(ParticleTypes.ENCHANT,
            x, y, z,
            -Math.cos(angle) * 0.02,
            0.05,
            -Math.sin(angle) * 0.02);
    }
}
```

### Useful Particle Types for Effects

| Particle | Visual | Best For |
|----------|--------|----------|
| `FLAME` | Orange fire | Fire, heat |
| `SOUL_FIRE_FLAME` | Blue fire | Cold fire, magic |
| `END_ROD` | White sparkle, rises | Divine light, sparkles |
| `ELECTRIC_SPARK` | Blue spark | Energy, electricity |
| `ENCHANT` | Purple rising | Magic, enchantment |
| `TOTEM_OF_UNDYING` | Colorful burst | Celebration, power |
| `LAVA` | Orange drip | Intense heat |
| `DUST` | Custom color | Any colored effect |
| `CAMPFIRE_COSY_SMOKE` | Soft smoke | Atmosphere |
| `CLOUD` | White puff | Impact, explosion |

---

## 8. Performance Optimization

### Shader Optimization Rules

1. **Minimize texture samples** - Each sample is expensive
2. **Pre-compute in vertex shader** - Runs per-vertex, not per-pixel
3. **Avoid branches** - Use `mix()` instead of `if`
4. **Use `smoothstep`** - Hardware optimized
5. **Limit loop iterations** - Max 5-10 in fragment shader

```glsl
// BAD: Branch in fragment shader
if (intensity > 0.5) {
    color = brightColor;
} else {
    color = darkColor;
}

// GOOD: Branchless with mix
float t = smoothstep(0.4, 0.6, intensity);
color = mix(darkColor, brightColor, t);
```

### Vertex vs Fragment Distribution

```glsl
// Vertex shader - compute expensive things once per vertex
uniform float GameTime;
out float timeFactor;
out float pulseAmount;

void main() {
    // Compute once per vertex
    timeFactor = sin(GameTime * 2400.0);
    pulseAmount = 1.0 + timeFactor * 0.2;
    // ... rest of vertex shader
}

// Fragment shader - uses pre-computed values
in float timeFactor;
in float pulseAmount;

void main() {
    // Simple operations only
    vec4 color = texture(Sampler0, texCoord0) * pulseAmount;
    // ...
}
```

### Java-Side Optimization

```java
// Limit particle spawn rate
private int particleTick = 0;

void spawnParticles(Entity entity) {
    particleTick++;

    // Only spawn every 4 ticks
    if (particleTick % 4 != 0) return;

    // Random chance for expensive particles
    if (entity.getRandom().nextFloat() < 0.3f) {
        // Spawn particle
    }
}
```

### Layer Count Guidelines

| Effect Type | Recommended Layers |
|-------------|-------------------|
| Simple glow | 2-3 layers |
| Divine beam | 4-5 layers |
| Complex aura | 5-7 layers |
| Boss effect | 7-9 layers max |

---

## 9. Common Patterns and Examples

### Complete Glow Beam Fragment Shader

```glsl
#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;
uniform vec4 ColorModulator;
uniform float GameTime;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in vec4 vertexColor;
in vec2 texCoord0;
in float vertexDistance;

out vec4 fragColor;

// Noise function
float noise(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

// FBM for organic movement
float fbm(vec2 st, float time) {
    float value = 0.0;
    float amplitude = 0.5;
    vec2 shift = vec2(100.0);

    for (int i = 0; i < 4; i++) {
        value += amplitude * noise(st);
        st = st * 2.0 + shift + time * 0.1;
        amplitude *= 0.5;
    }
    return value;
}

// Radial glow
float radialGlow(vec2 uv, float power) {
    float dist = abs(uv.x - 0.5) * 2.0;
    return pow(1.0 - smoothstep(0.0, 1.0, dist), power);
}

// Energy flow animation
float energyFlow(vec2 uv, float time) {
    float flow1 = sin(uv.y * 10.0 + time * 3.0) * 0.5 + 0.5;
    float flow2 = sin(uv.y * 7.0 - time * 2.0 + 1.5) * 0.5 + 0.5;
    return (flow1 + flow2) * 0.5;
}

// Sparkle effect
float sparkle(vec2 uv, float time) {
    float spark = sin(uv.x * 50.0 + time * 10.0) * sin(uv.y * 50.0 - time * 8.0);
    return pow(max(0.0, spark), 8.0) * 2.0;
}

void main() {
    float time = GameTime * 1200.0;

    // Sample texture
    vec4 texColor = texture(Sampler0, texCoord0);
    vec4 baseColor = texColor * vertexColor * ColorModulator;

    // Calculate effects
    float glow = radialGlow(texCoord0, 2.0);
    float energy = energyFlow(texCoord0, time);
    float spark = sparkle(texCoord0, time);
    float organic = fbm(texCoord0 * 5.0, time);

    // Build bloom layers
    vec3 bloomColor = baseColor.rgb;

    // Core brightness
    bloomColor += baseColor.rgb * glow * 0.5;

    // Warm corona with energy flow
    vec3 warmTint = vec3(1.0, 0.9, 0.7);
    bloomColor += warmTint * glow * energy * 0.3;

    // Organic variation
    bloomColor += baseColor.rgb * organic * 0.1;

    // Divine sparkles
    bloomColor += vec3(1.0, 1.0, 0.95) * spark;

    // Edge glow
    float edge = 1.0 - glow;
    bloomColor += vec3(1.0, 0.6, 0.2) * edge * energy * 0.15;

    // Final alpha
    float alpha = baseColor.a * (glow * 0.8 + 0.2);
    alpha = min(1.0, alpha + spark * 0.3);

    // Distance fade (closer = brighter)
    float distFade = 1.0 - smoothstep(0.0, 32.0, vertexDistance);
    bloomColor *= 0.7 + 0.3 * distFade;

    // Apply fog (reduced for divine light)
    vec4 color = vec4(bloomColor, alpha);
    vec4 fogged = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
    fragColor = mix(fogged, color, 0.6);
}
```

### Billboard Quad Rendering

```java
private void drawBillboardQuad(Matrix4f posMatrix, Matrix3f normMatrix,
        VertexConsumer vertices, float width, float height,
        float r, float g, float b, float a) {

    // Front face
    addVertex(posMatrix, normMatrix, vertices, -width, -height, 0, r, g, b, a, 0, 1);
    addVertex(posMatrix, normMatrix, vertices,  width, -height, 0, r, g, b, a, 1, 1);
    addVertex(posMatrix, normMatrix, vertices,  width,  height, 0, r, g, b, a, 1, 0);
    addVertex(posMatrix, normMatrix, vertices, -width,  height, 0, r, g, b, a, 0, 0);

    // Back face (for double-sided)
    addVertex(posMatrix, normMatrix, vertices,  width, -height, 0, r, g, b, a, 1, 1);
    addVertex(posMatrix, normMatrix, vertices, -width, -height, 0, r, g, b, a, 0, 1);
    addVertex(posMatrix, normMatrix, vertices, -width,  height, 0, r, g, b, a, 0, 0);
    addVertex(posMatrix, normMatrix, vertices,  width,  height, 0, r, g, b, a, 1, 0);
}

private void addVertex(Matrix4f pos, Matrix3f norm, VertexConsumer vc,
        float x, float y, float z, float r, float g, float b, float a, float u, float v) {
    vc.vertex(pos, x, y, z)
        .color(r, g, b, a)
        .texture(u, v)
        .overlay(OverlayTexture.DEFAULT_UV)
        .light(15728880)  // Full brightness
        .normal(norm, 0, 1, 0)
        .next();
}
```

### Bone Position Tracking (GeckoLib)

```java
public Vec3d getBoneWorldPos(Entity entity, String boneName, BakedGeoModel model,
        double entityX, double entityY, double entityZ, float bodyYaw) {

    return model.getBone(boneName).map(bone -> {
        Matrix4f matrix = new Matrix4f();
        matrix.translation((float) entityX, (float) entityY, (float) entityZ);
        matrix.rotateY((float) Math.toRadians(-bodyYaw));

        Matrix4f boneMatrix = transformBoneRecursively(bone);
        matrix.mul(boneMatrix);

        Vector4f worldPos = new Vector4f(0, 0, 0, 1).mul(matrix);
        return new Vec3d(worldPos.x(), worldPos.y(), worldPos.z());
    }).orElse(new Vec3d(entityX, entityY, entityZ));
}

private Matrix4f transformBoneRecursively(GeoBone bone) {
    Matrix4f matrix = new Matrix4f();

    if (bone.getParent() != null) {
        matrix.mul(transformBoneRecursively(bone.getParent()));
    }

    // Apply bone transforms
    matrix.translate(bone.getPivotX() / 16f, bone.getPivotY() / 16f, bone.getPivotZ() / 16f);
    matrix.rotateZ(bone.getRotZ());
    matrix.rotateY(bone.getRotY());
    matrix.rotateX(bone.getRotX());
    matrix.scale(bone.getScaleX(), bone.getScaleY(), bone.getScaleZ());
    matrix.translate(-bone.getPivotX() / 16f, -bone.getPivotY() / 16f, -bone.getPivotZ() / 16f);
    matrix.translate(bone.getPosX() / 16f, bone.getPosY() / 16f, bone.getPosZ() / 16f);

    return matrix;
}
```

---

## 10. Troubleshooting

### Common Issues and Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| Effect not visible | Wrong RenderLayer | Use `getBeaconBeam(tex, true)` for glow |
| Black borders around texture | Alpha blend instead of additive | Set `"dstrgb": "one"` in shader JSON |
| Effect too dim | Low alpha values | Increase alpha and/or add more layers |
| Flickering | Z-fighting | Offset layers slightly in depth |
| Shader not loading | JSON syntax error | Validate JSON, check console for errors |
| Wrong colors | Color multiplication | Check ColorModulator and vertex colors |
| No animation | GameTime not used | Multiply GameTime by large number (1200+) |
| Performance issues | Too many layers/particles | Reduce layer count, limit particle rate |

### Debugging Shaders

```glsl
// Output UV coordinates as color to debug
fragColor = vec4(texCoord0.x, texCoord0.y, 0.0, 1.0);

// Output distance as grayscale
fragColor = vec4(vec3(vertexDistance / 32.0), 1.0);

// Output noise to see pattern
float n = noise(texCoord0 * 10.0);
fragColor = vec4(vec3(n), 1.0);

// Check if uniform is receiving data
fragColor = vec4(GameTime, 0.0, 0.0, 1.0);  // Should animate red
```

### Console Error Patterns

```
// Shader compilation failed
[Render thread/ERROR]: Shader <name> could not be loaded

// Missing texture
[Render thread/WARN]: Unable to load texture: ancientcurse:textures/...

// Invalid uniform
[Render thread/ERROR]: Shader uniform '<name>' not found
```

---

## References

- [Minecraft Wiki - Shaders](https://minecraft.wiki/w/Shader)
- [McTsts Minecraft Shaders Wiki](https://github.com/McTsts/Minecraft-Shaders-Wiki)
- [The Book of Shaders](https://thebookofshaders.com/)
- [Fabric Rendering Documentation](https://docs.fabricmc.net/develop/rendering/)
- [GLSL Noise Algorithms](https://gist.github.com/patriciogonzalezvivo/670c22f3966e662d2f83)
- [LearnOpenGL - Blending](https://learnopengl.com/Advanced-OpenGL/Blending)

---

## Version History

- **v1.0** (2026-01-24): Initial comprehensive guide for Ancient Curse mod
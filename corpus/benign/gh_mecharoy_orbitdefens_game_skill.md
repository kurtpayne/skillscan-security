---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: mecharoy/OrbitDefense
# corpus-url: https://github.com/mecharoy/OrbitDefense/blob/9dbe75f439476fdf2b3490881673e59d82f1baf0/GAME.skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
Development & Deployment Best Practices1. Code Quality & StructureECS Pattern (Entity-Component-System)Instead of deep OOP inheritance (e.g., class Guard extends Enemy extends Actor), use composition.Entities: Just IDs (e.g., Entity_1).Components: Data containers (e.g., Position, Velocity, Sprite, InputRecorder).Systems: Logic processors (e.g., MovementSystem updates all entities with Position and Velocity).Why? This makes managing the "Ghosts" significantly easier. The Ghost is just an entity with a InputReplay component instead of a InputListener component.Deterministic StateFor the time-loop replay to work, your game logic must be deterministic.Fixed Time Step: Do not rely on variable deltaTime for physics simulation. Use a fixed time step accumulator (e.g., 1/60th of a second) to ensure the ghost moves exactly the same distance as the player did, regardless of frame rate fluctuations.Avoid Randomness: Do not use Math.random() for anything affecting gameplay during the level. If you must, use a seeded random number generator so the "random" guard patrol is identical across loops.Object PoolingBrowser games suffer from Garbage Collection (GC) pauses.Never create new objects inside the game loop (e.g., new Bullet()).Pre-allocate: Create a pool of 50 bullets at start. When one is fired, activate an existing one. When it hits, deactivate it.2. Git & Version Control StrategyBranching Modelmain: Production-ready code. Vercel automatically deploys this to the live URL.dev: Staging branch. Vercel creates a "Preview Deployment" for this.feat/mechanic-name: Feature branches (e.g., feat/time-rewind, feat/guard-ai).Commit Standards (Conventional Commits)Use strict naming for clarity in history:feat: add rewinding logicfix: resolve collision bug with wallsstyle: update canvas background colorrefactor: optimize collision detection algorithm3. Vercel Deployment Configurationvercel.jsonAdd a configuration file to the root to handle routing, especially if you implement a Single Page Application (SPA) router later.{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
Environment VariablesNever hardcode API keys or debug flags. Use Vercel's Environment Variables UI.NEXT_PUBLIC_DEBUG_MODE=falseGAME_VERSION=1.0.24. Performance OptimizationCanvas Layers: Use multiple <canvas> elements layered on top of each other.Layer 1 (Background): Static floor tiles (drawn once).Layer 2 (Main): Dynamic entities (player, guards) cleared and redrawn every frame.Layer 3 (UI): HUD elements (timer, loop count).Off-screen Canvas: Pre-render complex sprites or procedural geometry to an off-screen canvas and draw that as an image to the main canvas.


# Browser Game Development Best Practices

## Performance Optimization

Frame rate consistency takes priority over visual complexity. Target 60 FPS on mid-range devices, scaling down effects automatically when performance drops. Implement frame skipping gracefully to maintain game logic timing even when rendering slows. Monitor performance metrics continuously during development, not just at the end.

Object pooling dramatically reduces garbage collection pauses. Pre-allocate arrays of commonly spawned objects like projectiles and enemies. Reset and reuse objects instead of destroying and creating new ones. Track pool usage to identify optimal pool sizes for different object types.

Rendering optimization focuses on minimizing draw calls. Batch similar sprites together when possible. Use sprite sheets to reduce texture switching. Implement viewport culling to skip rendering off-screen objects. Consider using WebGL for complex scenes with many moving parts.

## Code Architecture

Separation of concerns keeps code maintainable as complexity grows. Game logic should never directly manipulate DOM or Canvas. Rendering code shouldn't contain game rules. Input handling remains isolated from both. This separation enables easier testing and modification.

State management needs careful consideration from the start. Use a single source of truth for game state. Make state updates predictable and traceable. Implement save/load functionality early to ensure state structure supports persistence. Consider using immutable updates for easier debugging.

Event-driven architecture scales better than polling for game events. Use custom events for game milestones and state changes. Implement an event bus for loose coupling between systems. Throttle high-frequency events to prevent performance issues.

## Asset Management

Lazy loading improves initial load times significantly. Load only menu assets initially, game assets when starting play. Stream level-specific assets as needed. Provide loading progress feedback to maintain engagement.

Image optimization reduces bandwidth and memory usage. Use appropriate formats: PNG for sprites with transparency, JPEG for backgrounds. Compress images without visible quality loss. Generate multiple resolutions for different screen densities. Consider using WebP with fallbacks for older browsers.

Audio requires special attention in browsers. Use Web Audio API for precise timing and effects. Provide format fallbacks (WebM, MP3, OGG). Implement audio sprites for multiple short sounds. Handle browser autoplay policies gracefully with user interaction requirements.

## Cross-Browser Compatibility

Feature detection beats browser detection. Check for API availability before using. Provide fallbacks for missing features. Test on multiple browsers throughout development, not just at the end.

Mobile considerations affect design decisions. Touch controls need larger hit areas than mouse clicks. Prevent default touch behaviors that interfere with gameplay. Handle orientation changes gracefully. Account for variable screen sizes and aspect ratios.

## Security Considerations

Never trust client-side validation for critical game logic. If implementing multiplayer or leaderboards, validate all scores server-side. Obfuscate but don't rely on client-side anti-cheat measures. Rate limit API calls to prevent abuse.

Protect against XSS when displaying user-generated content. Sanitize any text input from users. Use Content Security Policy headers. Avoid eval() and inline scripts.

## Testing Strategy

Automated testing saves debugging time. Unit test game logic separately from rendering. Integration test major game systems. Use visual regression testing for rendering consistency. Implement performance benchmarks as tests.

Playtesting reveals issues automated tests miss. Test with real users early and often. Gather metrics on player behavior and difficulty. A/B test significant changes. Monitor error logs from production deployments.

## Deployment and Monitoring

Progressive Web App features enhance user experience. Implement service workers for offline play. Add web app manifest for installability. Cache assets intelligently for returning players.

Error tracking identifies issues in production. Implement error boundary handling. Send anonymous error reports. Track performance metrics from real devices. Monitor load times and interaction delays.

Version control strategy affects deployment ease. Use semantic versioning for releases. Tag stable versions for easy rollback. Implement feature flags for gradual rollouts. Maintain separate branches for development and production.

## Accessibility

Inclusive design expands your audience. Provide keyboard alternatives for all controls. Implement proper focus management. Add configurable difficulty settings. Include colorblind-friendly palettes.

Screen reader compatibility where applicable. Provide text alternatives for important visual information. Use ARIA labels for interactive elements. Announce important game events programmatically.
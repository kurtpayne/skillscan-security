---
name: kuenta-design
description: >
  Design system y guía visual completa para el proyecto KUENTA (PWA de pagos P2P Chile).
  Usar SIEMPRE que se cree o modifique cualquier componente visual, pantalla, estilo,
  layout o elemento de interfaz en el proyecto KUENTA. Incluye tipografía (Syne + DM Sans),
  paleta de colores con tokens CSS, glassmorphism, wordmark, modos claro/oscuro,
  iconografía SVG, animaciones, componentes y checklist de implementación.
  También usar cuando se mencione: wordmark, splash screen, login, header, tab bar,
  cards, botones, inputs, avatares, colores, fuentes o cualquier elemento visual de KUENTA.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: JROSES23/KUENTA
# corpus-url: https://github.com/JROSES23/KUENTA/blob/fa214b47f6bb0e9bf22558e47bde5646fe49b916/KUENTA_DESIGN_SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# KUENTA Design System Skill

## Instrucción de uso

Cuando trabajas en el proyecto KUENTA, **lee el archivo `DESIGN_SYSTEM.md`** antes de
escribir cualquier código de componente o pantalla:

```bash
# El archivo está en la raíz del proyecto KUENTA
cat DESIGN_SYSTEM.md
```

Si estás en un contexto donde el archivo no está disponible localmente,
está disponible en: `/mnt/user-data/outputs/DESIGN_SYSTEM.md`

## Resumen rápido (leer DESIGN_SYSTEM.md para detalles completos)

### Tipografía
- **Wordmark únicamente:** `Syne` 800, letter-spacing 8-12px, gradient morado
- **Todo lo demás:** `DM Sans` 300-700
- Importar ambas desde Google Fonts en `index.html`

### Componente Wordmark obligatorio
```tsx
// SIEMPRE usar este componente, nunca escribir "KUENTA" como texto plano
import { Wordmark } from '@/components/ui/Wordmark'
// <Wordmark size="lg" />  → splash (42px)
// <Wordmark size="md" />  → login header (28px)
// <Wordmark size="sm" />  → inline (22px)
```

### Reglas absolutas
1. **Cero emojis** — solo íconos SVG o Lucide React
2. **Cero hardcoded hex** — usar CSS vars (`var(--text)`, `var(--surface)`, etc.)
3. **Cero ShadCN** — design system propio
4. **Wordmark siempre** con `<Wordmark />`, nunca texto plano
5. **Dos temas** — `[data-theme="dark"]` y `[data-theme="light"]` en `<html>`
6. **Touch targets** ≥ 44×44px siempre

### Paleta core (ambos modos)
```
Morado primario:  #4C44AA / #6860C8 / #8880DE
Verde success:    var(--green)   → #0A5C45 light / #3DC99A dark
Rojo error:       var(--red)     → #8B2020 light / #F07070 dark
Header gradient:  siempre morado (no cambia con el tema)
```

### Pantallas de auth — estructura
```
/splash  → SplashPage    : blobs + Wordmark lg + tagline + dots → 2.5s → /login
/login   → LoginPage     : header gradient + Wordmark md + phone input + social btns
/otp     → OTPPage       : 6 dígitos + resend
/setup   → ProfileSetup  : nombre + foto
```

### Importar Google Fonts (index.html)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
```

### tailwind.config.ts — extensiones requeridas
```ts
fontFamily: {
  brand: ['Syne', 'sans-serif'],
  ui: ['DM Sans', 'system-ui', '-apple-system', 'sans-serif'],
},
borderRadius: {
  card: '20px', modal: '28px', input: '14px',
  btn: '16px', tab: '28px', pill: '100px', icon: '14px',
},
```

## Lee DESIGN_SYSTEM.md para:
- Tokens CSS completos de color (claro y oscuro)
- Código completo de `SplashPage.tsx` y `LoginPage.tsx`
- Componente `Wordmark.tsx` completo
- Componente `ThemeToggle.tsx` con Zustand persist
- `AmbientBlobs.tsx`
- Escala tipográfica completa (9 niveles)
- Todos los keyframes de animación
- Checklist de implementación
- Reglas de iconografía y tamaños

---

*Skill generado para el proyecto KUENTA — actualizar este archivo si cambia el design system.*
---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: sirenkovladd/transactify
# corpus-url: https://github.com/sirenkovladd/transactify/blob/ea027bebcae965950c3b7e12e8bb252cb433132a/vanjs_skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# VanJS Development Skill

This document outlines the best practices and patterns for developing web applications using [VanJS](https://vanjs.org/).

## Core Concepts

### 1. State & Reactivity
VanJS uses `van.state` to create reactive primitives.
-   **State**: `const count = van.state(0)`
-   **Access**: `count.val` (get/set)
-   **Binding**: Pass the state object *directly* to DOM properties or children to bind it.
    ```js
    div(count) // Updates text content when count changes
    input({value: count}) // Two-way binding (requires oninput handler to update state)
    ```

### 2. Derived State
Use `van.derive` for values that depend on other states.
```js
const double = van.derive(() => count.val * 2)
```
-   **Efficiency**: Derived states only re-compute when dependencies change.
-   **Side Effects**: You can use `van.derive` for side effects (like logging) if it returns nothing, but prefer explicit effect handling if possible.

### 3. DOM Construction
Use `van.tags` to create DOM elements.
```js
const { div, button, span } = van.tags
const App = () => div(
  button({onclick: () => alert('Hi')}, "Click Me")
)
```

## Component Patterns

### Functional Components
Components are just functions that return DOM nodes.
```js
const Button = ({ text, onClick }) => button({ onclick: onClick }, text)
```

### Async Components
Handle async data using a reactive pattern or the `Await` utility pattern.
```js
const AsyncData = () => {
  const data = van.state(null)
  fetch('/api/data').then(r => r.json()).then(d => data.val = d)

  return div(() => data.val ? JSON.stringify(data.val) : "Loading...")
}
```

## Best Practices

### Do's
-   **Bind directly**: Pass state objects to DOM attributes/children instead of manually subscribing.
    -   *Good*: `div({class: myState}, ...)`
    -   *Bad*: `van.derive(() => div({class: myState.val}, ...))` (unless complex logic is needed)
-   **Use `van.derive` for complex bindings**: If a property depends on multiple states or logic.
    ```js
    div({ class: () => active.val ? 'active' : 'inactive' })
    ```
-   **Cleanup**: VanJS handles cleanup for DOM nodes. For global listeners, ensure you clean them up if the component unmounts (though VanJS doesn't have a built-in "unmount" hook for simple functions, you can use `van.derive` with a cleanup return if attached to a state).

### Don'ts
-   **Avoid Direct DOM Manipulation**: Do not use `document.getElementById` or `querySelector` inside components to modify elements. Use `ref` or state binding.
    -   *Exception*: initializing 3rd party libraries (charts, maps) that require a DOM element. In that case, use a setup function or `queueMicrotask` after mounting.
-   **Don't over-derive**: If a value is simple, just use the state directly.

## Common Patterns

### List Rendering
VanJS handles arrays in children efficiently.
```js
const list = van.state(['A', 'B'])
const ListComponent = () => div(
  () => div(list.val.map(item => span(item)))
)
```
*Note: wrapping in `() => ...` ensures the list re-renders when `list.val` changes.*

### Modal/Popup
Control visibility with a boolean state.
```js
const isOpen = van.state(false)
const Modal = () => div(
  { style: () => `display: ${isOpen.val ? 'block' : 'none'}` },
  "Content"
)
```

### Conditional Rendering
When conditionally rendering components based on state, always return an empty string `""` instead of `null` if the component should be hidden.
-   **Why**: Returning `null` from a reactive callback can cause the element to be permanently removed from the DOM in a way that VanJS cannot easily restore when the state changes back. Returning `""` keeps a placeholder (text node) that VanJS can update.
-   **Pattern**:
    ```js
    const Component = () => {
      if (!isVisible.val) return "" // Good
      // if (!isVisible.val) return null // Bad - might not reappear
      return div("Visible Content")
    }
    ```

## Project Specifics
-   **Entry Point**: `client/main.ts`
-   **Styling**: Use CSS classes (defined in `index.css` or similar) and toggle them via state, rather than heavy inline styles.
-   **Addons**: Only use `vanjs-core` unless `vanjs-ui` or others are explicitly added to `package.json`.
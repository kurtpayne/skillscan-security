---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: kadikraman/do-you-remember
# corpus-url: https://github.com/kadikraman/do-you-remember/blob/5c7f68f693057e13f5a4b59854f993327e6245b5/expo-ui-skill.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# Expo UI Skill

## Overview

`@expo/ui` brings native SwiftUI (iOS/tvOS/macOS) and Jetpack Compose (Android) components to React Native via Expo. It is NOT a JS UI library — it exposes real native platform primitives directly to JavaScript.

- **Package:** `@expo/ui`
- **Install:** `npx expo install @expo/ui`
- **Requires:** Development build (not Expo Go)
- **Available since:** SDK 54 (SwiftUI focus), SDK 55 (expanded Jetpack Compose)

Two separate import paths:
- `@expo/ui/swift-ui` — iOS/tvOS/macOS components
- `@expo/ui/swift-ui/modifiers` — SwiftUI modifiers
- `@expo/ui/jetpack-compose` — Android components
- `@expo/ui/jetpack-compose/modifiers` — Jetpack Compose modifiers

## Critical Concept: The Host Component

`Host` is **required** as the root container to bridge from React Native (UIKit/Android Views) into SwiftUI/Jetpack Compose. Think of it like `<svg>` in HTML or `<Canvas>` in react-native-skia.

```tsx
import { Host, Text } from '@expo/ui/swift-ui';

// Host wraps SwiftUI content — style it with RN styles
<Host style={{ flex: 1 }}>
  <Text>Hello SwiftUI</Text>
</Host>

// matchContents makes Host shrink to fit its SwiftUI content
<Host matchContents>
  <Text>Sized to content</Text>
</Host>
```

**Key Host props:**
- `matchContents?: boolean | { vertical?: boolean, horizontal?: boolean }` — Shrink to fit content
- `style?: StyleProp<ViewStyle>` — Standard RN styles (flexbox works here)
- `colorScheme?: 'light' | 'dark'`
- `layoutDirection?: 'leftToRight' | 'rightToLeft'`
- `ignoreSafeArea?: 'all' | 'keyboard'` (SwiftUI) / `ignoreSafeAreaKeyboardInsets?: boolean` (Compose)

**Important:** Inside Host, Yoga/flexbox is NOT available. Use `HStack`, `VStack`, `Row`, `Column` etc. for layout. RN styles only work on the Host itself.

---

## SwiftUI Components (iOS)

Import from `@expo/ui/swift-ui`.

### Layout

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Host` | `matchContents`, `style`, `colorScheme` | Root bridge container |
| `HStack` | `spacing?: number`, `alignment?: 'top'\|'center'\|'bottom'\|'firstTextBaseline'\|'lastTextBaseline'` | Horizontal stack |
| `VStack` | `spacing?: number`, `alignment?: 'leading'\|'center'\|'trailing'` | Vertical stack |
| `ZStack` | `alignment?: 16 options` | Z-axis layering |
| `Group` | — | Grouping container |
| `Spacer` | — | Flexible space |
| `ScrollView` | `axes?: 'vertical'\|'horizontal'\|'both'`, `showsIndicators?: boolean` | Scrollable container |
| `Grid` | `verticalSpacing`, `horizontalSpacing`, `alignment` | Grid layout. Use `Grid.Row` for rows |
| `List` | `selection`, `onSelectionChange` | Native list with selection. Use `List.ForEach` for items |
| `Section` | `title`, `header`, `footer`, `isExpanded`, `onIsExpandedChange` | Section within List/Form |
| `Form` | — | Form container (iOS Settings style) |
| `Namespace` | `id: string` (use `React.useId()`) | For matched geometry animations |

### Text & Labels

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Text` | `children`, `markdownEnabled?: boolean` | Text with markdown support |
| `Label` | `title`, `systemImage?: SFSymbol`, `icon?: ReactNode` | Label with optional SF Symbol |
| `LabeledContent` | `label?: string\|ReactNode`, `children` | Content with label (key-value display) |

### Buttons & Controls

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Button` | `onPress`, `label`, `systemImage?: SFSymbol`, `role?: 'default'\|'cancel'\|'destructive'`, `target?: string`, `children` | Native button |
| `Toggle` | `isOn`, `label`, `systemImage`, `onIsOnChange` | Switch/toggle |
| `Slider` | `value`, `step`, `min`, `max`, `onValueChange`, `label`, `minimumValueLabel`, `maximumValueLabel` | Value slider |
| `Stepper` | `label`, `defaultValue`, `step`, `min`, `max`, `onValueChanged` | Increment/decrement |
| `TextField` | `defaultValue`, `placeholder`, `onChangeText`, `onSubmit`, `multiline`, `numberOfLines`, `keyboardType`, `autoFocus` | Text input |
| `SecureField` | `defaultValue`, `placeholder`, `onChangeText`, `onSubmit`, `autoFocus` | Password input |
| `Picker` | `selection`, `onSelectionChange`, `label`, `systemImage`, `children` | Selection picker (use `tag` modifier on options) |
| `DatePicker` | `title`, `selection?: Date`, `range?: {start, end}`, `displayedComponents?: ('date'\|'hourAndMinute')[]`, `onDateChange` | Date/time picker |
| `ColorPicker` | `selection`, `label`, `onSelectionChange`, `supportsOpacity` | Color picker |

### Display

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Image` | `systemName: SFSymbol`, `size`, `color`, `variableValue?: 0.0-1.0`, `onPress` | SF Symbol image |
| `ProgressView` | `value?: number\|null`, `timerInterval?: {lower, upper}`, `countsDown` | Progress indicator (null = indeterminate) |
| `Gauge` | `value`, `min`, `max`, `currentValueLabel`, `minimumValueLabel`, `maximumValueLabel` | Gauge display |
| `Chart` | `data: ChartDataPoint[]`, `type?: 'line'\|'point'\|'bar'\|'area'\|'pie'\|'rectangle'`, `showGrid`, `animate`, `showLegend` | Data visualization |
| `Divider` | — | Visual separator |
| `ContentUnavailableView` | `title`, `systemImage`, `description` | Empty state view |

### Dialogs & Sheets

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `BottomSheet` | `isPresented`, `onIsPresentedChange`, `fitToContents` | Bottom sheet modal |
| `Popover` | `isPresented`, `onIsPresentedChange`, `attachmentAnchor`, `arrowEdge` | Popover with `Popover.Trigger` and `Popover.Content` |
| `ConfirmationDialog` | `title`, `isPresented`, `onIsPresentedChange`, `titleVisibility` | With `.Trigger`, `.Actions`, `.Message` |

### Menus & Context

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Menu` | `label`, `systemImage`, `onPrimaryAction`, `children` | Dropdown menu |
| `ContextMenu` | `children` | With `.Trigger`, `.Preview`, `.Items` |
| `ControlGroup` | `label`, `systemImage`, `children` | Group controls in menus |

### Other

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `ShareLink` | `item`, `getItemAsync`, `subject`, `message`, `preview?: {title, image}` | Native share sheet |
| `DisclosureGroup` | `label`, `isExpanded`, `onIsExpandedChange` | Expandable/collapsible |
| `GlassEffectContainer` | `spacing` | Container for glass effects (iOS 26+) |

### Shapes

`Rectangle`, `RoundedRectangle` (`cornerRadius`), `Circle`, `Ellipse`, `Capsule` (`cornerStyle`), `UnevenRoundedRectangle` (individual corner radii), `ConcentricRectangle`

---

## Jetpack Compose Components (Android)

Import from `@expo/ui/jetpack-compose`.

### Layout

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Host` | `matchContents`, `style`, `colorScheme`, `layoutDirection` | Root bridge container |
| `Row` | `horizontalArrangement`, `verticalAlignment` | Horizontal layout |
| `Column` | `verticalArrangement`, `horizontalAlignment` | Vertical layout |
| `Box` | `contentAlignment` | Generic container |
| `FlowRow` | `horizontalArrangement`, `verticalArrangement` | Wrapping horizontal layout |
| `LazyColumn` | `verticalArrangement`, `horizontalAlignment`, `contentPadding` | Virtualized vertical list |
| `Spacer` | — | Flexible space |
| `AnimatedVisibility` | `visible: boolean` | Animated show/hide |
| `RNHostView` | `matchContents`, `verticalScrollEnabled` | Host RN views inside Compose |

**Arrangement values:** `'start'|'end'|'center'|'spaceBetween'|'spaceAround'|'spaceEvenly'|{spacedBy: number}`

### Text

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Text` | `color`, `overflow`, `softWrap`, `maxLines`, `minLines`, `style: TextStyle` | Text display |

**TextStyle:** `{ typography?, fontSize?, fontWeight?, fontStyle?, textAlign?, textDecoration?, letterSpacing?, lineHeight? }`

**Typography values:** `'displayLarge'|'displayMedium'|'displaySmall'|'headlineLarge'|'headlineMedium'|'headlineSmall'|'titleLarge'|'titleMedium'|'titleSmall'|'bodyLarge'|'bodyMedium'|'bodySmall'|'labelLarge'|'labelMedium'|'labelSmall'`

### Buttons

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Button` | `onPress`, `variant?: 'default'\|'bordered'\|'borderless'\|'outlined'\|'elevated'`, `leadingIcon`, `trailingIcon`, `color`, `shape`, `disabled` | Material button |
| `IconButton` | `onPress`, `variant?: 'default'\|'bordered'\|'outlined'`, `color`, `shape`, `disabled` | Icon-only button |
| `TextButton` | `onPress`, `color`, `disabled`, `children` | Text-only button |
| `ToggleButton` | `checked`, `onCheckedChange`, `text`, `variant?: 'default'\|'icon'\|'filledIcon'\|'outlinedIcon'`, `color` | Toggle button |
| `RadioButton` | `selected`, `onClick` | Radio button |

### Inputs

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Switch` | `value`, `label`, `variant?: 'checkbox'\|'switch'\|'button'`, `onValueChange`, `color`, `elementColors` | Switch/checkbox |
| `TextInput` | `defaultValue`, `onChangeText`, `multiline`, `numberOfLines`, `keyboardType`, `autocorrection`, `autoCapitalize` | Text input |
| `Slider` | `value`, `steps`, `min`, `max`, `color`, `elementColors`, `onValueChange` | Value slider |
| `DateTimePicker` | `initialDate`, `onDateSelected`, `variant?: 'picker'\|'input'`, `displayedComponents?: 'date'\|'hourAndMinute'\|'dateAndTime'`, `is24Hour` | Date/time picker |
| `Picker` | `options: string[]`, `selectedIndex`, `onOptionSelected`, `variant?: 'segmented'\|'radio'`, `color` | Selection picker |

### Display

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Icon` | `source`, `tintColor`, `size`, `contentDescription` | Icon display |
| `Card` | `variant?: 'default'\|'elevated'\|'outlined'`, `color`, `elementColors` | Material card |
| `Surface` | `color`, `contentColor`, `tonalElevation`, `shadowElevation` | Material surface |
| `Divider` | — | Visual separator |
| `CircularProgress` | `progress?: number\|null`, `color` | Circular indicator |
| `LinearProgress` | `progress?: number\|null`, `color` | Linear indicator |
| `CircularWavyProgress` | `progress?: number\|null`, `color` | Wavy circular |
| `LinearWavyProgress` | `progress?: number\|null`, `color` | Wavy linear |

### Chips

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `Chip` | `variant?: 'assist'\|'filter'\|'input'\|'suggestion'`, `label`, `leadingIcon`, `trailingIcon`, `selected`, `enabled`, `onPress`, `onDismiss` | Material chip |
| `FilterChip` | `selected`, `label`, `enabled`, `onPress`. Sub: `.LeadingIcon`, `.TrailingIcon` | Filter chip |

### Dialogs & Sheets

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `AlertDialog` | `title`, `text`, `visible`, `confirmButtonText`, `dismissButtonText`, `onConfirmPressed`, `onDismissPressed` | Alert dialog |
| `BasicAlertDialog` | `onDismissRequest`, `children` | Custom alert dialog |
| `ModalBottomSheet` | `onDismissRequest`, `skipPartiallyExpanded`, `children` | Bottom sheet |

### Other

| Component | Key Props | Description |
|-----------|-----------|-------------|
| `ContextMenu` | `color`, `style`. Sub: `.Trigger`, `.Preview`, `.Items` | Context menu |
| `SearchBar` | `onSearch`. Sub: `.Placeholder`, `.ExpandedFullScreenSearchBar` | Search bar |
| `DockedSearchBar` | `onQueryChange`. Sub: `.Placeholder`, `.LeadingIcon` | Docked search |
| `Carousel` | `variant?: 'multiBrowse'\|'unconstrained'`, `itemSpacing`, `contentPadding`, `flingBehavior` | Carousel |
| `PullToRefreshBox` | `isRefreshing`, `onRefresh` | Pull-to-refresh wrapper |
| `HorizontalFloatingToolbar` | `variant?: 'standard'\|'vibrant'`. Sub: `.FloatingActionButton` | Floating toolbar |
| `ListItem` | `headline`, `supportingText`, `overlineText`, `onPress`. Sub: `.Leading`, `.Trailing`, `.SupportingContent` | List item |
| `Shape` | Static methods: `.Star()`, `.PillStar()`, `.Pill()`, `.Circle()`, `.Rectangle()`, `.Polygon()`, `.RoundedCorner()` | Custom shapes |

---

## Modifiers System

Every component accepts a `modifiers` prop — an array of modifier configs. Modifiers are the primary way to style and configure views.

```tsx
import { padding, background, buttonStyle } from '@expo/ui/swift-ui/modifiers';

<Button
  label="Click me"
  modifiers={[
    padding({ all: 16 }),
    background('#f0f0f0'),
    buttonStyle('bordered'),
  ]}
/>
```

### SwiftUI Modifiers

Import from `@expo/ui/swift-ui/modifiers`.

#### Layout & Sizing
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `frame` | `({ width?, height?, minWidth?, maxWidth?, minHeight?, maxHeight?, idealWidth?, idealHeight?, alignment? })` | Set dimensions |
| `padding` | `({ top?, bottom?, leading?, trailing?, horizontal?, vertical?, all? })` | Padding (no args = default) |
| `fixedSize` | `({ horizontal?, vertical? })` | Prevent view from shrinking |
| `offset` | `({ x?, y? })` | Translate position |
| `aspectRatio` | `({ ratio, contentMode?: 'fit'\|'fill' })` | Aspect ratio constraint |
| `containerRelativeFrame` | `({ axes, count?, span?, spacing?, alignment? })` | Size relative to container (iOS 17+) |
| `ignoreSafeArea` | `({ regions?, edges? })` | Ignore safe area |
| `zIndex` | `(index: number)` | Z-ordering |
| `layoutPriority` | `(priority: number)` | Layout priority |

#### Visual Effects
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `background` | `(color, shape?)` | Background color with optional shape |
| `foregroundStyle` | `(style)` | Color, gradient, or hierarchical style |
| `foregroundColor` | `(color)` | Foreground color (deprecated, use foregroundStyle) |
| `tint` | `(color)` | Tint color |
| `opacity` | `(value: 0-1)` | Opacity |
| `cornerRadius` | `(radius: number)` | Corner radius |
| `clipShape` | `(shape, cornerRadius?)` | Clip to shape |
| `clipped` | `(boolean)` | Clip to bounds |
| `border` | `({ color, width? })` | Border |
| `shadow` | `({ radius, x?, y?, color? })` | Shadow |
| `blur` | `(radius)` | Blur |
| `brightness` | `(amount)` | Brightness |
| `contrast` | `(amount)` | Contrast |
| `saturation` | `(amount)` | Saturation |
| `hueRotation` | `(angle)` | Hue rotation (degrees) |
| `grayscale` | `(amount: 0-1)` | Grayscale |
| `colorInvert` | `(boolean)` | Invert colors |
| `luminanceToAlpha` | `()` | Luminance to alpha |
| `overlay` | `({ color?, alignment? })` | Overlay |
| `backgroundOverlay` | `({ color?, alignment? })` | Background overlay |
| `mask` | `(shape, cornerRadius?)` | Mask shape |
| `glassEffect` | `({ glass?: { variant, interactive?, tint? }, shape?, cornerRadius? })` | Glass effect (iOS 26+) |
| `glassEffectId` | `(id, namespaceId)` | Glass effect identity |

#### Transforms
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `scaleEffect` | `(scale \| { x, y })` | Scale |
| `rotationEffect` | `(angle)` | Rotation (degrees) |
| `rotation3DEffect` | `({ angle, axis?, perspective? })` | 3D rotation |
| `matchedGeometryEffect` | `(id, namespaceId)` | Matched geometry animation |

#### Text & Font
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `font` | `({ family?, size?, weight?, design?: 'default'\|'rounded'\|'serif'\|'monospaced' })` | Font |
| `bold` | `()` | Bold text |
| `italic` | `()` | Italic text |
| `monospacedDigit` | `()` | Fixed-width digits |
| `underline` | `({ isActive, pattern, color? })` | Underline |
| `strikethrough` | `({ isActive, pattern, color? })` | Strikethrough |
| `kerning` | `(value)` | Character spacing |
| `lineSpacing` | `(value)` | Line spacing |
| `lineLimit` | `(limit)` | Max lines |
| `truncationMode` | `('head'\|'middle'\|'tail')` | Truncation |
| `textCase` | `('lowercase'\|'uppercase')` | Text case |
| `textSelection` | `(boolean)` | Selectable text |
| `multilineTextAlignment` | `('center'\|'leading'\|'trailing')` | Text alignment |
| `allowsTightening` | `(boolean)` | Allow character compression |

#### Control Styles
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `buttonStyle` | `('automatic'\|'bordered'\|'borderedProminent'\|'borderless'\|'glass'\|'glassProminent'\|'plain')` | Button style |
| `toggleStyle` | `('automatic'\|'switch'\|'button')` | Toggle style |
| `controlSize` | `('mini'\|'small'\|'regular'\|'large'\|'extraLarge')` | Control size |
| `labelStyle` | `('automatic'\|'iconOnly'\|'titleAndIcon'\|'titleOnly')` | Label display style |
| `labelsHidden` | `()` | Hide labels |
| `textFieldStyle` | `('automatic'\|'plain'\|'roundedBorder')` | TextField style |
| `pickerStyle` | `('automatic'\|'inline'\|'menu'\|'navigationLink'\|'palette'\|'segmented'\|'wheel')` | Picker style |
| `datePickerStyle` | `('automatic'\|'compact'\|'graphical'\|'wheel')` | DatePicker style |
| `progressViewStyle` | `('automatic'\|'linear'\|'circular')` | ProgressView style |
| `gaugeStyle` | `('automatic'\|'circular'\|'circularCapacity'\|'linear'\|'linearCapacity')` | Gauge style |
| `submitLabel` | `('continue'\|'done'\|'go'\|'join'\|'next'\|'return'\|'route'\|'search'\|'send')` | Keyboard return key |

#### List & Collection
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `listStyle` | `('automatic'\|'plain'\|'inset'\|'insetGrouped'\|'grouped'\|'sidebar')` | List style |
| `listRowBackground` | `(color)` | Row background |
| `listRowSeparator` | `(visibility, edges?)` | Row separator visibility |
| `listRowInsets` | `({ top?, leading?, bottom?, trailing? })` | Row insets |
| `listSectionSpacing` | `('default'\|'compact'\|number)` | Section spacing |
| `listSectionMargins` | `({ length?, edges? })` | Section margins (iOS 26+) |
| `scrollContentBackground` | `('automatic'\|'visible'\|'hidden')` | Scroll background |
| `scrollDisabled` | `(boolean)` | Disable scrolling |
| `scrollDismissesKeyboard` | `('automatic'\|'never'\|'interactively'\|'immediately')` | Keyboard dismiss on scroll |
| `moveDisabled` | `(boolean)` | Disable reorder |
| `deleteDisabled` | `(boolean)` | Disable delete |
| `headerProminence` | `('standard'\|'increased')` | Header prominence |

#### Grid
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `gridCellColumns` | `(count)` | Column span |
| `gridCellUnsizedAxes` | `(axes)` | Unsized axes |
| `gridColumnAlignment` | `(alignment)` | Column alignment |
| `gridCellAnchor` | `(anchor)` | Cell anchor |

#### Gestures & Events
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `onTapGesture` | `(handler)` | Tap handler |
| `onLongPressGesture` | `(handler, minimumDuration?)` | Long press |
| `onAppear` | `(handler)` | View appeared |
| `onDisappear` | `(handler)` | View disappeared |
| `refreshable` | `(handler: () => Promise<void>)` | Pull to refresh |

#### State & Presentation
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `disabled` | `(boolean)` | Disable view |
| `hidden` | `(boolean)` | Hide view |
| `tag` | `(string \| number)` | Set tag (for Picker options) |
| `badge` | `(value?)` | Badge text |
| `badgeProminence` | `('standard'\|'increased'\|'decreased')` | Badge prominence |
| `environment` | `(key, value)` | Set environment (editMode, colorScheme) |
| `animation` | `(animationType, animatedValue)` | Animation (see [deep dive](#animation-modifier-deep-dive-ios)) |
| `contentTransition` | `(type, params?)` | Content transition animation |
| `presentationDetents` | `(detents, options?)` | Sheet heights |
| `presentationDragIndicator` | `(visibility)` | Sheet drag indicator |
| `presentationBackgroundInteraction` | `(interaction)` | Sheet background interaction |
| `interactiveDismissDisabled` | `(boolean)` | Prevent sheet dismissal |
| `menuActionDismissBehavior` | `('automatic'\|'disabled'\|'enabled')` | Menu dismiss behavior |

#### Accessibility
| Modifier | Signature | Description |
|----------|-----------|-------------|
| `accessibilityLabel` | `(label)` | Accessibility label |
| `accessibilityHint` | `(hint)` | Accessibility hint |
| `accessibilityValue` | `(value)` | Accessibility value |

#### Shape Builders (via `shapes` export)
```tsx
import { shapes } from '@expo/ui/swift-ui/modifiers';
shapes.roundedRectangle({ cornerRadius: 12 })
shapes.capsule()
shapes.rectangle()
shapes.ellipse()
shapes.circle()
```

### Jetpack Compose Modifiers

Import from `@expo/ui/jetpack-compose/modifiers`.

| Modifier | Signature | Description |
|----------|-----------|-------------|
| `paddingAll` | `(all: number)` | Equal padding all sides |
| `padding` | `(start, top, end, bottom)` | Individual padding (RTL-aware) |
| `size` | `(width, height)` | Exact size |
| `width` | `(value)` | Exact width |
| `height` | `(value)` | Exact height |
| `fillMaxSize` | `(fraction?)` | Fill available space |
| `fillMaxWidth` | `(fraction?)` | Fill available width |
| `fillMaxHeight` | `(fraction?)` | Fill available height |
| `wrapContentWidth` | `(alignment?)` | Wrap width to content |
| `wrapContentHeight` | `(alignment?)` | Wrap height to content |
| `offset` | `(x, y)` | Position offset |
| `background` | `(color)` | Background color |
| `border` | `(borderWidth, borderColor)` | Border |
| `shadow` | `(elevation)` | Shadow/elevation |
| `alpha` | `(value: 0-1)` | Opacity |
| `blur` | `(radius)` | Blur effect |
| `rotate` | `(degrees)` | Rotation |
| `zIndex` | `(index)` | Z-ordering |
| `weight` | `(weight)` | Flex weight (in Row/Column) |
| `align` | `(alignment)` | Alignment in container |
| `matchParentSize` | `()` | Match Box parent size |
| `animateContentSize` | `(dampingRatio?, stiffness?)` | Animate size changes |
| `clickable` | `(handler)` | Click handler |
| `selectable` | `(selected, handler)` | Selectable item |
| `clip` | `(shape)` | Clip to shape |
| `testID` | `(tag)` | Test identifier |

#### Compose Shape Builders (via `Shapes` export)
```tsx
import { Shapes } from '@expo/ui/jetpack-compose/modifiers';
Shapes.Rectangle
Shapes.Circle
Shapes.RoundedCorner(12) // or { topStart: 12, topEnd: 12, bottomStart: 0, bottomEnd: 0 }
Shapes.CutCorner(8)
Shapes.Material.Heart
Shapes.Material.Pill
Shapes.Material.Diamond
// Many more Material shapes available
```

---

## foregroundStyle Deep Dive

The `foregroundStyle` modifier is versatile and supports multiple style types:

```tsx
import { foregroundStyle } from '@expo/ui/swift-ui/modifiers';

// Simple color
foregroundStyle('red')
foregroundStyle('#FF6B35')

// Color object
foregroundStyle({ type: 'color', color: '#FF6B35' })

// Hierarchical (semantic, respects system theme)
foregroundStyle({ type: 'hierarchical', style: 'primary' })
foregroundStyle({ type: 'hierarchical', style: 'secondary' })  // lighter/subtle
foregroundStyle({ type: 'hierarchical', style: 'tertiary' })
foregroundStyle({ type: 'hierarchical', style: 'quaternary' })

// Linear gradient
foregroundStyle({
  type: 'linearGradient',
  colors: ['#FF0000', '#0000FF'],
  startPoint: { x: 0, y: 0 },
  endPoint: { x: 1, y: 1 },
})

// Radial gradient
foregroundStyle({
  type: 'radialGradient',
  colors: ['#FF0000', '#0000FF'],
  center: { x: 0.5, y: 0.5 },
  startRadius: 0,
  endRadius: 100,
})
```

---

## Common Patterns

### iOS Settings-Style Form
```tsx
import { Button, Form, Host, HStack, Image, Section, Spacer, Text, Toggle } from '@expo/ui/swift-ui';
import { background, buttonStyle, clipShape, foregroundStyle, frame } from '@expo/ui/swift-ui/modifiers';

<Host style={{ flex: 1 }}>
  <Form>
    <Section>
      <HStack spacing={8}>
        <Image systemName="airplane" color="white" size={18}
          modifiers={[frame({ width: 28, height: 28 }), background('#ffa500'), clipShape('roundedRectangle')]} />
        <Text>Airplane Mode</Text>
        <Spacer />
        <Toggle isOn={isAirplaneMode} onIsOnChange={setIsAirplaneMode} />
      </HStack>
    </Section>
  </Form>
</Host>
```

### Picker with tag Modifier
```tsx
import { Picker, Text } from '@expo/ui/swift-ui';
import { pickerStyle, tag } from '@expo/ui/swift-ui/modifiers';

<Picker label="Size" modifiers={[pickerStyle('menu')]}
  selection={selectedIndex} onSelectionChange={setSelectedIndex}>
  {options.map((option, index) => (
    <Text key={index} modifiers={[tag(index)]}>{option}</Text>
  ))}
</Picker>
```

### Button Variants (SwiftUI)
```tsx
<Button label="Default" />
<Button label="Glass" modifiers={[buttonStyle('glass')]} />
<Button label="Bordered" modifiers={[buttonStyle('bordered')]} />
<Button label="Destructive" role="destructive" />
<Button label="Small" modifiers={[controlSize('small'), buttonStyle('bordered')]} />
<Button label="Icon Only" systemImage="gear" modifiers={[buttonStyle('glass'), labelStyle('iconOnly')]} />
```

### Custom Button Content
```tsx
<Button>
  <VStack spacing={4}>
    <Image systemName="folder" />
    <Text>Folder</Text>
  </VStack>
</Button>
```

### Bottom Sheet (SwiftUI)
```tsx
import { BottomSheet, Text, Button } from '@expo/ui/swift-ui';
import { presentationDetents, presentationDragIndicator } from '@expo/ui/swift-ui/modifiers';

<BottomSheet isPresented={isOpen} onIsPresentedChange={setIsOpen}>
  <Text modifiers={[presentationDetents([{ type: 'medium' }, { type: 'large' }]),
    presentationDragIndicator('visible')]}>
    Sheet content
  </Text>
</BottomSheet>
```

### Glass Effect (iOS 26+)
```tsx
import { glassEffect, padding } from '@expo/ui/swift-ui/modifiers';

<Text modifiers={[
  padding({ all: 16 }),
  glassEffect({ glass: { variant: 'clear' } }),
]}>
  Glass effect text
</Text>
```

### Android Material Button
```tsx
import { Button, Host } from '@expo/ui/jetpack-compose';

<Host matchContents>
  <Button variant="outlined" onPress={() => {}} leadingIcon="add">
    Add Item
  </Button>
</Host>
```

### Android Progress Indicators
```tsx
import { CircularProgress, LinearProgress } from '@expo/ui/jetpack-compose';

<CircularProgress progress={0.7} color="#6200EE" />
<LinearProgress progress={null} />  {/* indeterminate */}
```

---

## Animation Modifier Deep Dive (iOS)

The `animation` modifier applies SwiftUI animations to any animatable modifier (e.g. `scaleEffect`, `rotationEffect`, `opacity`, `offset`). When the tracked value changes, SwiftUI interpolates the animatable properties using the specified curve.

```tsx
import { animation, Animation, scaleEffect, rotationEffect, opacity, offset } from '@expo/ui/swift-ui/modifiers';
```

### The `animation()` modifier

```tsx
animation(animationObject, animatedValue)
```

- **animationObject** — created via `Animation.*` factory methods (see below)
- **animatedValue** — a `boolean` or `number` that triggers the animation when it changes

**Important:** The animation only plays when `animatedValue` changes between renders. Toggling a boolean or incrementing a number both work.

### Animation Factory Methods

| Method | Params | Description |
|--------|--------|-------------|
| `Animation.easeInOut` | `{ duration?: number }` | Ease in and out curve |
| `Animation.easeIn` | `{ duration?: number }` | Ease in curve |
| `Animation.easeOut` | `{ duration?: number }` | Ease out curve |
| `Animation.linear` | `{ duration?: number }` | Linear curve |
| `Animation.spring` | `{ response?, dampingFraction?, blendDuration?, duration?, bounce? }` | Spring physics (most common) |
| `Animation.interpolatingSpring` | `{ mass?, stiffness?, damping?, initialVelocity?, duration?, bounce? }` | Low-level spring with mass/stiffness/damping |
| `Animation.default` | — | System default animation |

**Spring parameters explained:**
- `response` — How fast the spring settles (seconds). Lower = snappier. Typical: 0.3–0.6
- `dampingFraction` — How much bounce. 0 = infinite bounce, 1 = no bounce. Typical: 0.3–0.7
- `bounce` — Alternative to dampingFraction. Positive = more bouncy, negative = overdamped

**Interpolating spring parameters:**
- `mass` — Weight on the spring. Lower mass = faster. Typical: 0.5–1.0
- `stiffness` — Spring tension. Higher = faster snap. Typical: 100–300
- `damping` — Friction. Lower = more oscillation. Typical: 5–20

### Chainable Methods

Both `.delay()` and `.repeat()` can be chained on any animation:

```tsx
// Delay start by 1 second
Animation.easeInOut({ duration: 0.8 }).delay(1.0)

// Repeat 3 times with autoreversal
Animation.easeInOut({ duration: 0.6 }).repeat({ repeatCount: 3, autoreverses: true })

// Chain both
Animation.spring({ response: 0.4, dampingFraction: 0.5 }).delay(0.2).repeat({ repeatCount: 2, autoreverses: true })
```

### Animatable Modifiers

These modifiers can be animated:
- `scaleEffect(value)` — uniform scale, or `{ x, y }` for non-uniform
- `rotationEffect(degrees)` — rotation in degrees
- `opacity(value)` — 0.0 to 1.0
- `offset({ x, y })` — position offset

### Patterns

**Bounce on tap (scale out and back in one press):**
```tsx
const [pressed, setPressed] = useState(false);

<Button
  label="Go!"
  modifiers={[
    scaleEffect(pressed ? 1.1 : 1.0),
    animation(Animation.spring({ response: 0.4, dampingFraction: 0.4 }), pressed),
  ]}
  onPress={() => {
    setPressed(true);
    setTimeout(() => setPressed(false), 250);  // snap back
    setTimeout(() => doAction(), 500);          // delayed action so user sees bounce
  }}
/>
```

**Toggle rotation:**
```tsx
const [toggled, setToggled] = useState(false);

<VStack modifiers={[
  rotationEffect(toggled ? 180 : 0),
  animation(Animation.spring(), toggled),
  onTapGesture(() => setToggled(v => !v)),
]}>
  <Text>Flip me</Text>
</VStack>
```

**Incremental multi-effect (each tap adds more):**
```tsx
const [taps, setTaps] = useState(0);

<VStack modifiers={[
  scaleEffect(taps % 2 === 0 ? 1.0 : 1.2),
  rotationEffect(taps * 45),
  opacity(taps % 4 === 0 ? 1.0 : 0.7),
  animation(Animation.spring({ response: 0.7, dampingFraction: 0.8 }), taps),
  onTapGesture(() => setTaps(t => t + 1)),
]} />
```

**Delayed + repeated:**
```tsx
<HStack modifiers={[
  rotationEffect(active ? 180 : 0),
  animation(
    Animation.easeInOut({ duration: 0.6 }).repeat({ repeatCount: 3, autoreverses: true }),
    active,
  ),
]} />
```

### Gotchas

- **Animation is iOS-only.** Use platform-specific files (`.ios.tsx` / `.tsx` fallback) when using the animation modifier.
- **The animation doesn't play if the value doesn't change.** Toggling the same boolean `true → true` does nothing — the value must actually differ between renders.
- **Immediate actions hide the animation.** If tapping a button opens a sheet or navigates, the animation won't be visible. Use `setTimeout` to delay the action (300–500ms) so the user sees the bounce first.
- **Prefer `VStack`/`HStack` as animation targets over `Text`.** Applying animatable modifiers directly to `Text` may not produce visible results. Wrap the text in a layout container and animate that instead.

---

## Extending Expo UI (Custom Components)

You can create custom SwiftUI components that work with the modifier system:

1. Create a local Expo module: `npx create-expo-module@latest --local my-ui`
2. Add `ExpoUI` pod dependency
3. Extend `UIBaseViewProps` for automatic modifier support
4. Conform to `ExpoSwiftUI.View` protocol
5. Register with `ExpoUIView(MyView.self)`
6. Use `createViewModifierEventListener` in JS wrapper

### Custom Modifiers

1. Create Swift struct conforming to `ViewModifier` and `Record`
2. Register with `ViewModifierRegistry.register("name")` in `OnCreate`
3. Create JS helper with `createModifier('name', params)`

```tsx
// JS side
import { createModifier } from '@expo/ui/swift-ui/modifiers';
export const customBorder = (params) => createModifier('customBorder', params);
```

---

## Gotchas & Practical Lessons

### Platform file strategy for expo-router

Use Metro's platform extensions to keep web unchanged while adding native UI:
- `app/index.tsx` — web (original, fallback)
- `app/index.ios.tsx` — iOS (SwiftUI)
- `app/index.android.tsx` — Android (Jetpack Compose)

Metro resolves `.ios.tsx` > `.android.tsx` > `.tsx` automatically. No renaming of existing files needed.

### SwiftUI: Section header text is always grey

`Section` headers apply a secondary/grey `foregroundStyle` to ALL content inside the `header` prop — overriding any `foregroundStyle` you set on individual `Text` elements. To get primary-colored text in a section header, add `headerProminence('increased')` to the Section's modifiers:
```tsx
<Section
  header={<Text modifiers={[font({ size: 32, weight: 'bold' })]}>Title</Text>}
  modifiers={[headerProminence('increased')]}
>
```

### SwiftUI: foregroundStyle with system label colors

You can pass SwiftUI system color names as strings directly:
- `foregroundStyle('label')` — primary text (black/white)
- `foregroundStyle('secondaryLabel')` — ~60% gray
- `foregroundStyle('tertiaryLabel')` — ~30% gray
- `foregroundStyle('quaternaryLabel')` — ~18% gray

These are different from the hierarchical form (`{ type: 'hierarchical', style: 'secondary' }`) which derives from the parent's foreground color.

### SwiftUI: multiline text centering in Buttons

Text inside SwiftUI `Button` with `HStack` will center-align when wrapping to multiple lines. Add `multilineTextAlignment('leading')` to keep it left-aligned:
```tsx
<Button modifiers={[buttonStyle('bordered'), controlSize('large')]}>
  <HStack>
    <Text modifiers={[multilineTextAlignment('leading')]}>Long option text here</Text>
    <Spacer />
  </HStack>
</Button>
```

### SwiftUI: BottomSheet pattern

BottomSheet is a sibling to other content inside the same `Host`. Wrap content in `Group` and apply presentation modifiers to the Group:
```tsx
<Host style={{ flex: 1 }}>
  <ScrollView>{/* main content */}</ScrollView>
  <BottomSheet isPresented={show} onIsPresentedChange={setShow}>
    <Group modifiers={[presentationDetents(['large']), presentationDragIndicator('visible')]}>
      <ScrollView>{/* sheet content */}</ScrollView>
    </Group>
  </BottomSheet>
</Host>
```

### Android: Host matchContents + fillMaxWidth() conflicts

**Do NOT** combine `<Host matchContents>` with `fillMaxWidth()` on the root Compose child. `matchContents` measures intrinsic size while `fillMaxWidth()` wants to fill the parent — this conflict causes content to clip or overflow. Instead, either:
- Use `<Host style={{ flex: 1 }}>` (no matchContents) for full-screen layouts
- Use `matchContents` only for inline/wrapped content without fill modifiers

### Android: Prefer LazyColumn for full-page layouts

Instead of mixing RN ScrollView + multiple Host wrappers, use a single `Host` with `LazyColumn` and `contentPadding`:
```tsx
<Host style={{ flex: 1 }}>
  <LazyColumn
    verticalArrangement={{ spacedBy: 12 }}
    contentPadding={{ start: 20, end: 20, top: 48, bottom: 40 }}
  >
    <Text style={{ typography: 'headlineLarge' }}>Title</Text>
    <Card variant="outlined" modifiers={[fillMaxWidth()]}>{/* ... */}</Card>
  </LazyColumn>
</Host>
```
This avoids layout measurement issues and eliminates all RN imports.

### Android: BottomSheet pattern

Android BottomSheet must be conditionally rendered and wrapped in its own `Host matchContents`. Its children are RN views by default; nest another `Host` inside for Compose content:
```tsx
{visible && (
  <Host matchContents>
    <BottomSheet onDismissRequest={() => setVisible(false)} skipPartiallyExpanded>
      <Host style={{ flex: 1 }}>
        <LazyColumn>{/* Compose quiz content */}</LazyColumn>
      </Host>
    </BottomSheet>
  </Host>
)}
```

### Shared logic across platforms

Extract stateful logic (e.g., quiz state machine) into a shared hook so platform-specific screens only differ in rendering:
```tsx
// hooks/use-quiz.ts — shared by iOS, Android, web
export function useQuiz(categoryId: CategoryId, visible: boolean) {
  // state, handlers, helpers
  return { question, handleSelect, handleNext, getOptionState, ... };
}
```

---

## Key Differences: SwiftUI vs Jetpack Compose

| Aspect | SwiftUI | Jetpack Compose |
|--------|---------|-----------------|
| Import | `@expo/ui/swift-ui` | `@expo/ui/jetpack-compose` |
| Horizontal layout | `HStack` | `Row` |
| Vertical layout | `VStack` | `Column` |
| Toggle/Switch | `Toggle` | `Switch` |
| Text input | `TextField` / `SecureField` | `TextInput` |
| Icons | `Image` (SF Symbols via `systemName`) | `Icon` (XML vectors, URIs) |
| Progress | `ProgressView` | `CircularProgress` / `LinearProgress` |
| Form container | `Form` + `Section` | No direct equivalent |
| Button styling | Via `buttonStyle` modifier | Via `variant` prop |
| Modifiers | ~100 modifiers, rich styling | ~25 modifiers, layout-focused |
| Platform | iOS, tvOS, macOS | Android |
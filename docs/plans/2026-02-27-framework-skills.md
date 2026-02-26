# 8 Framework Deep Skills — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use sp-executing-plans to implement this plan task-by-task.

**Goal:** Tạo 8 standalone skill files chuyên sâu cho React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind — biến CSV stack guidelines (~50 entries) thành SKILL.md (~250-300 lines) theo format chuẩn.

**Architecture:** Mỗi skill = `SKILL.md` (YAML frontmatter + 5-7 framework sections + tables + scoring rubric + common mistakes + quick diagnostic). Dữ liệu gốc từ `data/stacks/*.csv` được tổ chức lại thành knowledge framework chuyên sâu.

**Tech Stack:** Markdown, YAML frontmatter, cross-skill references

---

## Current State

Hiện tại mỗi framework chỉ có **1 file CSV** (~50 entries) trong `data/stacks/`:

| Framework | CSV File | Entries | Lines |
|-----------|----------|---------|-------|
| React | `data/stacks/react.csv` | 53 | State, Effects, Rendering, Components, Props, Hooks, Context, Performance, Testing, A11y, TypeScript, Patterns |
| Next.js | `data/stacks/nextjs.csv` | 52 | Routing, Rendering, DataFetching, Images, Fonts, Metadata, API, Middleware, Environment, Performance, Link, Config, Deployment, Security |
| Vue | `data/stacks/vue.csv` | 49 | Composition, Reactivity, Watchers, Props, Emits, Lifecycle, Components, Composables, Templates, State (Pinia), Routing, Performance, TypeScript, Testing, Forms, A11y, SSR |
| Svelte | `data/stacks/svelte.csv` | 53 | Reactivity (Svelte 4&5 Runes), Props, Bindings, Events, Lifecycle, Stores, Slots, Styling, Transitions, Actions, Logic, SvelteKit, Performance, TypeScript, A11y |
| SwiftUI | `data/stacks/swiftui.csv` | 50 | Views, State, Observable, Layout, Modifiers, Navigation, Lists, Forms, Async, Animation, Preview, Performance, A11y, Testing, Architecture |
| React Native | `data/stacks/react-native.csv` | 51 | Components, Styling, Navigation, State, Lists, Performance, Images, Forms, Touch, Animation, Async, A11y, Testing, Native |
| Flutter | `data/stacks/flutter.csv` | 52 | Widgets, State, Layout, Lists, Navigation, Async, Theming, Animation, Forms, Performance, A11y, Testing, Platform, Packages |
| Tailwind | `data/stacks/html-tailwind.csv` | 55 | Animation, Z-Index, Layout, Images, Typography, Colors, Spacing, Forms, Responsive, Buttons, Cards, A11y, Performance, Plugins, Customization |

## Proposed Changes

### Target Structure

Mỗi skill mới sẽ có cấu trúc:

```
skills/
├── react-mastery/
│   └── SKILL.md          (~280 lines)
├── nextjs-mastery/
│   └── SKILL.md          (~280 lines)
├── vue-mastery/
│   └── SKILL.md          (~280 lines)
├── svelte-mastery/
│   └── SKILL.md          (~280 lines)
├── swiftui-mastery/
│   └── SKILL.md          (~280 lines)
├── react-native-mastery/
│   └── SKILL.md          (~280 lines)
├── flutter-mastery/
│   └── SKILL.md          (~280 lines)
└── tailwind-mastery/
     └── SKILL.md          (~280 lines)
```

### SKILL.md Template Format

Mỗi file theo format chuẩn đã có (xem `clean-code/SKILL.md` hoặc `system-design/SKILL.md`):

```yaml
---
name: [skill-name]
description: '[trigger keywords and description]'
license: MIT
metadata:
  author: todyle
  version: "1.0.0"
---
```

Followed by:
1. **Title & Core Principle** — 1 paragraph philosophy
2. **Scoring Rubric** — 0-10 scale with criteria
3. **5-7 Framework Sections** — Each with:
   - Core concept
   - Why it works
   - Key insights (6-8 bullets)
   - Code applications table (4-6 rows)
4. **Common Mistakes** — Table with 8-10 entries
5. **Quick Diagnostic** — Table with 8-10 questions
6. **Further Reading** — Official docs + books
7. **Cross-references** — Links to 2-3 related skills

---

### Skill 1: `react-mastery`

#### [NEW] `skills/react-mastery/SKILL.md`

**Sections:**
1. State Management — useState, useReducer, derived state, lazy init
2. Effects & Lifecycle — useEffect cleanup, dependency arrays, when NOT to useEffect
3. Component Patterns — Composition, compound components, render props, forwardRef
4. Performance — React.memo, useMemo, useCallback, lazy loading, virtualization
5. Hooks — Custom hooks, rules of hooks, Context API patterns
6. TypeScript — Props typing, event handlers, generics, discriminated unions
7. Testing — RTL queries, user events, async testing

**Cross-refs:** `nextjs-mastery`, `react-native-mastery`, `clean-code`

---

### Skill 2: `nextjs-mastery`

#### [NEW] `skills/nextjs-mastery/SKILL.md`

**Sections:**
1. App Router & Routing — File-based routing, route groups, layouts, parallel routes
2. Server vs Client Components — 'use client' boundary, RSC patterns, streaming
3. Data Fetching — Server Components fetch, Server Actions, caching, revalidation
4. Performance — Images, fonts, bundle analysis, Partial Prerendering
5. API & Middleware — Route handlers, middleware auth, edge runtime
6. Security & Config — CSP, env vars, Server Action validation

**Cross-refs:** `react-mastery`, `tailwind-mastery`, `system-design`

---

### Skill 3: `vue-mastery`

#### [NEW] `skills/vue-mastery/SKILL.md`

**Sections:**
1. Composition API — `<script setup>`, defineProps, defineEmits, withDefaults
2. Reactivity System — ref vs reactive, computed, watchEffect vs watch, shallowRef
3. Component Architecture — SFC, composables, provide/inject, async components
4. State Management (Pinia) — defineStore, storeToRefs, setup stores, plugins
5. Vue Router — useRouter, lazy loading, guards, programmatic navigation
6. Performance — v-once, v-memo, defineAsyncComponent, shallowReactive

**Cross-refs:** `svelte-mastery`, `react-mastery`, `clean-code`

---

### Skill 4: `svelte-mastery`

#### [NEW] `skills/svelte-mastery/SKILL.md`

**Sections:**
1. Reactivity — Svelte 4 ($:) vs Svelte 5 Runes ($state, $derived, $effect)
2. Component API — Props ($props), events, bindings, slots, actions
3. Stores — writable, readable, derived, $prefix auto-subscription
4. SvelteKit — File routing, load functions, form actions, $app/stores
5. Transitions & Actions — Built-in transitions, custom actions, use:directive
6. Styling — Scoped styles, :global(), CSS variables, animation

**Cross-refs:** `vue-mastery`, `react-mastery`, `tailwind-mastery`

---

### Skill 5: `swiftui-mastery`

#### [NEW] `skills/swiftui-mastery/SKILL.md`

**Sections:**
1. Views & Modifiers — Struct views, body, modifier order, ViewModifier protocol
2. State Management — @State, @Binding, @StateObject, @ObservedObject, @Observable
3. Navigation — NavigationStack, navigationDestination, programmatic navigation
4. Layout — VStack/HStack/ZStack, LazyStacks, GeometryReader, frame modifiers
5. Lists & Data — List, ForEach, Identifiable, .task, FocusState
6. Architecture — MVVM, @MainActor, dependency injection, previews

**Cross-refs:** `ios-hig-design`, `react-native-mastery`, `clean-architecture`

---

### Skill 6: `react-native-mastery`

#### [NEW] `skills/react-native-mastery/SKILL.md`

**Sections:**
1. Components & Styling — Functional components, StyleSheet.create, Platform-specific
2. Navigation — React Navigation, typed params, deep linking, back handling
3. Lists & Performance — FlatList, keyExtractor, getItemLayout, windowSize, React.memo
4. Animation — Reanimated, Gesture Handler, UI thread worklets
5. Native Integration — Expo, permissions, native modules, Hermes
6. Testing — RNTL, Detox E2E, real device testing

**Cross-refs:** `react-mastery`, `swiftui-mastery`, `flutter-mastery`

---

### Skill 7: `flutter-mastery`

#### [NEW] `skills/flutter-mastery/SKILL.md`

**Sections:**
1. Widgets — Stateless vs Stateful, const constructors, composition, key
2. State Management — setState, Provider/Riverpod, dispose, InheritedWidget
3. Layout & Lists — Column/Row, Expanded, ListView.builder, Slivers, LayoutBuilder
4. Navigation — GoRouter, PopScope, typed arguments, deep linking
5. Theming — ThemeData, ColorScheme, Material 3, dark mode
6. Performance — const widgets, RepaintBoundary, DevTools, build optimization

**Cross-refs:** `react-native-mastery`, `swiftui-mastery`, `clean-code`

---

### Skill 8: `tailwind-mastery`

#### [NEW] `skills/tailwind-mastery/SKILL.md`

**Sections:**
1. Utility Patterns — Spacing scale, typography, color opacity, arbitrary values
2. Layout — Container, grid, flexbox, responsive padding, container queries
3. Responsive Design — Mobile-first, breakpoints, hidden/shown, responsive images
4. Components — Buttons (touch targets/loading), cards (hover/spacing), forms (focus/disabled)
5. Accessibility — sr-only, focus-visible, motion-reduce, semantic colors
6. Performance — Content paths, JIT, @apply discipline, dark mode

**Cross-refs:** `react-mastery`, `nextjs-mastery`, `top-design`

---

## Verification Plan

### Automated Tests

Since this is creating new skill files (not modifying code), verification focuses on structural correctness:

**1. Verify YAML frontmatter is valid:**
```bash
cd /Users/todyle/Library/Mobile\ Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master
for skill in react-mastery nextjs-mastery vue-mastery svelte-mastery swiftui-mastery react-native-mastery flutter-mastery tailwind-mastery; do
  python3 -c "
import yaml
with open('../../.gemini/antigravity/skills/$skill/SKILL.md') as f:
    content = f.read()
    parts = content.split('---')
    meta = yaml.safe_load(parts[1])
    assert 'name' in meta, f'Missing name in $skill'
    assert 'description' in meta, f'Missing description in $skill'
    print(f'✅ $skill: YAML valid — name={meta[\"name\"]}')"
done
```

**2. Verify file structure:**
```bash
for skill in react-mastery nextjs-mastery vue-mastery svelte-mastery swiftui-mastery react-native-mastery flutter-mastery tailwind-mastery; do
  if [ -f "/Users/todyle/.gemini/antigravity/skills/$skill/SKILL.md" ]; then
    lines=$(wc -l < "/Users/todyle/.gemini/antigravity/skills/$skill/SKILL.md")
    echo "✅ $skill: $lines lines"
  else
    echo "❌ $skill: MISSING"
  fi
done
```

**3. Verify cross-references point to existing skills:**
```bash
cd /Users/todyle/.gemini/antigravity/skills
for skill in react-mastery nextjs-mastery vue-mastery svelte-mastery swiftui-mastery react-native-mastery flutter-mastery tailwind-mastery; do
  refs=$(grep -oP 'see \K[a-z-]+' "$skill/SKILL.md" 2>/dev/null | sort -u)
  for ref in $refs; do
    if [ -d "$ref" ]; then
      echo "  ✅ $skill → $ref exists"
    else
      echo "  ❌ $skill → $ref MISSING"
    fi
  done
done
```

**4. Verify minimum structural elements exist in each file:**
```bash
for skill in react-mastery nextjs-mastery vue-mastery svelte-mastery swiftui-mastery react-native-mastery flutter-mastery tailwind-mastery; do
  file="/Users/todyle/.gemini/antigravity/skills/$skill/SKILL.md"
  echo "=== $skill ==="
  grep -c "^### " "$file" | xargs -I{} echo "  Sections: {}"
  grep -c "^| " "$file" | xargs -I{} echo "  Table rows: {}"
  grep -c "Core concept" "$file" | xargs -I{} echo "  Core concepts: {}"
  grep -c "Common Mistakes" "$file" | xargs -I{} echo "  Common Mistakes: {}"
  grep -c "Quick Diagnostic" "$file" | xargs -I{} echo "  Quick Diagnostic: {}"
done
```

### Manual Verification

1. Open each SKILL.md in VS Code and verify:
   - Readable hierarchy (H1/H2/H3 make sense)
   - Tables render correctly
   - Code examples are syntactically valid
   - Cross-references use correct skill names
2. Verify Antigravity can discover skills by running a prompt mentioning each framework

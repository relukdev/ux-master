# Master Plan — Design System Generator

## Phase Overview

| Phase | Name | Status | Effort | Priority |
|-------|------|--------|--------|----------|
| 1 | Fix Core Quality | 🔴 Not Started | 1-2 weeks | P0 |
| 2 | Expand Component Library | 🔴 Not Started | 2-3 weeks | P0 |
| 3 | Source Code Extraction | 🔴 Not Started | 2-3 weeks | P1 |
| 4 | Semi Design Doc Site | 🔴 Not Started | 3-4 weeks | P1 |
| 5 | Theme Package + Ecosystem | 🔴 Not Started | 2-3 weeks | P2 |

---

## Phase 1: Fix Core Quality

**Goal**: All output files are valid, compile, and tokens are accurate.

### Task 1.1: Fix Component Generator (P0)

**File**: `scripts/component_generator.py`
**Spec**: `.claude/specs/01-fix-component-generator.md`

Current generated code has critical syntax errors:
- Wrong HTML tag casing (`<BUTTON>` → `<button>`)
- Missing destructuring braces in forwardRef
- Unclosed template strings
- Invalid className conditionals

**Acceptance Criteria**:
- [ ] `npx tsc --noEmit` passes on all generated `.tsx` files
- [ ] Generated components render without runtime errors
- [ ] Button, Card, Input, Badge all work with story-style demo

### Task 1.2: Fix Token Accuracy (P0)

**File**: `scripts/token_mapper.py`, `scripts/harvester_v4.js`
**Spec**: `.claude/specs/02-fix-token-accuracy.md`

Issues:
- Neutral scale produces near-identical shades (50-800 all ~ same color)
- Semantic colors map to background instead of base color
- Color histogram sampling misses important colors

**Acceptance Criteria**:
- [ ] Neutral scale shows visually distinct 10-step gradient
- [ ] Primary, success, warning, danger colors match visual inspection
- [ ] Run on 5 different admin templates, verify color accuracy > 90%

### Task 1.3: Fix Doc Generator Display (P0)

**File**: `scripts/design_doc_generator.py`
**Spec**: `.claude/specs/03-fix-doc-generator.md`

Issues:
- Color Palette section shows border radius instead of actual colors
- Missing actual color swatch rendering
- No component preview section

**Acceptance Criteria**:
- [ ] Color swatches show correct hex colors with labels
- [ ] Typography section shows rendered text specimens
- [ ] At least basic component previews (button, card, input)

### Task 1.4: Add Test Suite (P0)

**Files**: `tests/`
**Spec**: `.claude/specs/04-add-test-suite.md`

**Acceptance Criteria**:
- [ ] Unit tests for `token_mapper.py` color utilities
- [ ] Unit tests for `component_generator.py` template rendering
- [ ] Integration test: URL → harvest → tokens → components → verify
- [ ] CI-ready test runner

---

## Phase 2: Expand Component Library

**Goal**: 20+ production-ready component templates.

### Task 2.1: Create Component Template System

**Spec**: `.claude/specs/05-component-templates.md`

Replace current "generate from scratch" approach with tested templates:
1. Write 20+ React component templates (hand-crafted, tested)
2. Each template has token injection points (`{{primary}}`, `{{borderRadius}}`)
3. Generator fills templates with harvested tokens

### Task 2.2: Component List (Priority Order)

| # | Component | Semi Design Equivalent | Complexity |
|---|-----------|----------------------|------------|
| 1 | Button | `@douyinfe/semi-ui/button` | Low |
| 2 | Input | `@douyinfe/semi-ui/input` | Low |
| 3 | Card | Custom | Low |
| 4 | Badge/Tag | `@douyinfe/semi-ui/tag` | Low |
| 5 | Avatar | `@douyinfe/semi-ui/avatar` | Low |
| 6 | Alert | `@douyinfe/semi-ui/banner` | Low |
| 7 | Typography | `@douyinfe/semi-ui/typography` | Low |
| 8 | Divider | `@douyinfe/semi-ui/divider` | Low |
| 9 | Tooltip | `@douyinfe/semi-ui/tooltip` | Medium |
| 10 | Dropdown | `@douyinfe/semi-ui/dropdown` | Medium |
| 11 | Select | `@douyinfe/semi-ui/select` | Medium |
| 12 | Checkbox | `@douyinfe/semi-ui/checkbox` | Low |
| 13 | Radio | `@douyinfe/semi-ui/radio` | Low |
| 14 | Switch | `@douyinfe/semi-ui/switch` | Low |
| 15 | Table | `@douyinfe/semi-ui/table` | High |
| 16 | Modal | `@douyinfe/semi-ui/modal` | Medium |
| 17 | Tabs | `@douyinfe/semi-ui/tabs` | Medium |
| 18 | Breadcrumb | `@douyinfe/semi-ui/breadcrumb` | Low |
| 19 | Pagination | `@douyinfe/semi-ui/pagination` | Medium |
| 20 | Progress | `@douyinfe/semi-ui/progress` | Low |
| 21 | Skeleton | `@douyinfe/semi-ui/skeleton` | Low |
| 22 | Empty | `@douyinfe/semi-ui/empty` | Low |

---

## Phase 3: Source Code Extraction

**Goal**: Extract design system from React/Vue/Angular source code.

**Spec**: `.claude/specs/06-source-code-extractor.md`

### Task 3.1: Tailwind Config Parser
Parse `tailwind.config.js` → extract colors, spacing, typography, borderRadius.

### Task 3.2: CSS Variable Parser
Parse `:root { --var: value }` from any CSS file.

### Task 3.3: SCSS Variable Parser
Parse `$variable: value;` patterns.

### Task 3.4: React Component Analyzer
Use AST parsing to detect component patterns, props interfaces, style usage.

---

## Phase 4: Semi Design Doc Site

**Goal**: Multi-page interactive doc site at semi.design quality level.

**Spec**: `.claude/specs/07-doc-site.md`

### Task 4.1: Static Site Structure (Next.js or Astro)
### Task 4.2: Live Code Editor (Sandpack)
### Task 4.3: Component Gallery with Interactive Preview
### Task 4.4: Token Reference with Copy-to-Clipboard
### Task 4.5: Theme Editor UI
### Task 4.6: Search

---

## Phase 5: Theme Package + Ecosystem

**Goal**: npm-publishable theme package, Figma sync.

**Spec**: `.claude/specs/08-theme-package.md`

### Task 5.1: npm Package Generator
### Task 5.2: Figma Tokens Bidirectional Sync
### Task 5.3: MCP Server Integration

---

## Execution Guide for Claude Code

Each phase has a detailed spec in `.claude/specs/`. To work on a task:

1. Read the relevant spec file
2. Check current code in referenced files
3. Write tests FIRST (TDD approach)
4. Implement changes
5. Verify with test commands in spec
6. Update this plan's status checkboxes

# Design System Generation Upgrade — Design Document

**Date:** 2026-02-27
**Status:** Draft — Awaiting Approval

---

## Problem Statement

UX Master v4 currently generates design system outputs as flat files in a single `output/` folder. The documentation output is a single-file HTML page, far from the interactive, navigable guideline site that teams need (like semi.design). Developers working on multiple projects need isolated, manageable, and upgradable design system outputs.

### Current Pain Points

1. **No project isolation** — All outputs dumped into `output/` with ad-hoc naming
2. **Only 4 component templates** — Button, Card, Input, Badge (P0: syntax errors in generated code)
3. **Documentation is a single HTML file** — No sidebar navigation, no interactive previews, not semi.design quality
4. **No `serve` command** — Can't preview design system locally
5. **MCP doesn't integrate** design system browsing/generation

---

## Decisions Made

| Decision | Choice |
|----------|--------|
| Output structure | **Central registry** at `~/.uxmaster/projects/<slug>/` |
| Guideline site | **Custom static site** (semi.design inspired) |
| Phase 1 scope | Getting Started + Design Tokens + Component Gallery |

---

## Architecture Overview

```
~/.uxmaster/
├── config.json                    # Global settings
└── projects/
    ├── hexabox/
    │   ├── manifest.json          # Project metadata
    │   ├── harvest-raw.json       # Merged harvests
    │   ├── harvests/              # Per-page harvests
    │   ├── tokens/
    │   │   ├── semi-theme.css     # CSS variables
    │   │   └── figma-tokens.json  # Figma export
    │   ├── components/            # Generated React components
    │   │   ├── button/
    │   │   ├── card/
    │   │   └── ...
    │   └── site/                  # Generated guideline site
    │       ├── index.html         # Landing / Getting Started
    │       ├── tokens.html        # Design Tokens page
    │       ├── components.html    # Component Gallery
    │       ├── css/
    │       │   └── style.css      # Site styles
    │       └── js/
    │           └── app.js         # Interactions
    └── another-project/
        └── ...
```

---

## Proposed Changes

### Component 1: Project Registry Upgrade

#### [MODIFY] [project_registry.py](file:///Users/todyle/Library/Mobile%20Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master/scripts/project_registry.py)

- Change `OUTPUT_DIR` default from `./output` to `~/.uxmaster/projects/`
- Add `build()` method that orchestrates: token mapping → component generation → site generation
- Add `serve()` method that starts local HTTP server for a project's `site/` directory
- Add `export()` method to copy/create a standalone npm-ready package (Phase 2 prep)
- Ensure backward compatibility by accepting custom `output_dir`

---

### Component 2: Design System Site Generator (New)

#### [NEW] [site_generator.py](file:///Users/todyle/Library/Mobile%20Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master/scripts/site_generator.py)

New script that generates a multi-page static site inspired by semi.design:

**Page 1: `index.html` — Getting Started**
- Project overview (name, source URL, extraction date)
- Quick Start: how to install/use the CSS tokens
- Code snippets for importing tokens into React/Vue/HTML projects
- Sidebar navigation (shared across all pages)

**Page 2: `tokens.html` — Design Tokens**
- **Colors:** Interactive swatches with copy-on-click, organized by semantic group (primary, success, warning, danger, neutral, background, text, border)
- **Typography:** Live specimens showing each font at each size/weight
- **Spacing:** Visual bars showing spacing scale
- **Shadows:** Live shadow previews on cards
- **Borders:** Radius preview with live rendering
- Full token reference table with CSS variable name, value, and copy button

**Page 3: `components.html` — Component Gallery**
- Card grid showing each generated component
- For each component: visual preview (rendered with CSS variables), variant showcase, code snippet with copy
- Component status indicators (stable, beta, planned)

**Shared UI Elements (semi.design inspired):**
- Collapsible sidebar navigation with section anchors
- Dark mode toggle
- Responsive layout (desktop sidebar → mobile hamburger)
- Semi Design typography and color system for the site itself
- Search tokens by name (JS-powered filter)

**Technical approach:**
- Python generates complete static HTML/CSS/JS files
- Uses Jinja2-style string templates embedded in the script
- Zero external dependencies at build time
- Generated site is self-contained (no CDN, no node_modules)
- Site CSS uses CSS custom properties for its own theming

---

### Component 3: CLI Enhancement

#### [MODIFY] [harvester_cli.py](file:///Users/todyle/Library/Mobile%20Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master/scripts/harvester_cli.py)

Add new subcommands:

```bash
# Full pipeline: extract → map → index → generate → build site
uxmaster quick https://example.com --name "My Project"

# List all projects in registry
uxmaster projects list

# Open/serve design system site for a project
uxmaster serve hexabox          # starts localhost:3939

# Rebuild site for existing project
uxmaster build hexabox

# Show project info
uxmaster projects info hexabox

# Delete a project
uxmaster projects delete hexabox
```

---

### Component 4: Component Generator Fix (P0)

#### [MODIFY] [component_generator.py](file:///Users/todyle/Library/Mobile%20Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master/scripts/component_generator.py)

- Fix syntax errors in generated TSX (missing `{` in forwardRef destructure)
- Fix duplicate naming conflict (exported `Button` shadows imported `Button`)
- Ensure all generated components pass `npx tsc --noEmit`
- Expand from 4 to 10+ component templates (Phase 1): Button, Card, Input, Badge, Tag, Avatar, Modal, Table, Tabs, Tooltip

---

### Component 5: MCP Integration

#### [MODIFY] [server.py](file:///Users/todyle/Library/Mobile%20Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master/mcp/server.py)

Add MCP tools for design system management:
- `list_design_systems` — List all projects in registry
- `get_design_tokens` — Return tokens for a specific project
- `build_design_system` — Trigger full pipeline for a URL
- `get_component_code` — Return generated component code

---

## Phase Plan

### Phase 1 (This Implementation)
1. ✅ Project Registry upgrade (central `~/.uxmaster/projects/`)
2. ✅ Site Generator — 3 pages (Getting Started, Tokens, Components)
3. ✅ CLI commands (`projects list`, `serve`, `build`)
4. ✅ Component Generator P0 fix (syntax errors)

### Phase 2 (Future)
- Component Detail Pages (each component gets its own page with API docs)
- Theme Customizer (live token editor)
- Dark Mode design system preview
- npm package export
- 20+ component templates
- MCP tools integration

---

## Verification Plan

### Automated Tests

**1. Existing tests (must still pass):**
```bash
cd /Users/todyle/Library/Mobile\ Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master
python3 -m pytest tests/test_project_registry.py -v
python3 -m pytest tests/test_design_doc.py -v
python3 -m pytest tests/test_generator.py -v
```

**2. New test: `tests/test_site_generator.py`**
- Test that `generate_site()` produces `index.html`, `tokens.html`, `components.html`
- Test that each page has valid HTML structure (`<!DOCTYPE html>`, `<html>`, `</html>`)
- Test that token values appear in `tokens.html`
- Test that component names appear in `components.html`
- Test sidebar navigation links are present
- Test dark mode toggle exists

**3. New test: `tests/test_project_registry_v2.py`**
- Test `build()` orchestrates all steps
- Test `serve()` starts HTTP server
- Test default registry path is `~/.uxmaster/projects/`

**4. Component syntax validation:**
```bash
# After generating components, validate TypeScript compiles
npx tsc --noEmit output/hexabox-components/button/component.tsx
```

### Manual Verification
1. Run `python3 scripts/harvester_cli.py quick https://hexabox.dexignlab.com --name hexabox`
2. Run `python3 scripts/harvester_cli.py serve hexabox`
3. Open browser at `http://localhost:3939`
4. Verify: sidebar navigation works, color swatches are clickable, typography specimens render correctly, component gallery shows previews
5. Test dark mode toggle
6. Test responsive layout (resize browser to mobile width)

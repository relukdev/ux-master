# AGENTS.md — UX Master AI Configuration

**Cross-platform agent configuration** for Google Antigravity, OpenAI Codex, OpenCode, Cursor, Claude, and compatible AI tools.

## The UX Master

UX Master is an **AI-powered design system extraction and generation platform**. The agent's role: extract design tokens from websites, map them to Semi Design, generate production-ready components, and document everything. Think of it as "Figma Tokens Studio" meets "Semi Design" — fully automated.

## 5 Core Directives

1. **Extract first** — harvester_v4.js (browser) and extractor.py (AST) are the source of truth
2. **Map to Semi** — all tokens must conform to Semi Design CSS variables (--semi-*)
3. **Generate with intent** — React TypeScript components use forwardRef, proper JSX, no syntax errors
4. **Test everything** — pytest for logic, tsc --noEmit for generated code
5. **Never break the data** — CSVs in data/ (UX Laws, Design Tests) are read-only

## Commands

**Full pipeline:**
```bash
python3 scripts/harvester_cli.py quick https://example.com --framework semi
```

**Individual steps:**
```bash
# Extract tokens from browser
python3 scripts/harvester_browser.py --url https://example.com --output ./output

# Map raw tokens to Semi Design spec
python3 scripts/token_mapper.py -i output/harvest.json --project myproject

# Build indexed design system
python3 scripts/design_system_indexer.py --input output/harvest.json --name "MyApp" --output output/

# Generate components
python3 scripts/component_generator.py --input output/design-system.json --all --output ./components

# Generate documentation
python3 scripts/design_doc_generator.py -i output/harvest.json -o output/design-system.html

# Search codebase
python3 scripts/search.py "color" --filter tokens
```

**Testing:**
```bash
pytest tests/ -v
python3 scripts/test_harvester_v4.py
npx tsc --noEmit  # Validate generated components
```

## Project Structure

```
scripts/
├── harvester_v4.js              # Browser JS injection (120+ tokens)
├── harvester_browser.py         # Playwright automation
├── extractor.py                 # CSS/file extraction
├── token_mapper.py              # Raw tokens → Semi Design
├── design_system_indexer.py     # Indexed design system build
├── component_generator.py       # React/Vue component gen
├── design_doc_generator.py      # HTML documentation
├── harvester_cli.py             # Unified CLI orchestrator
├── figma_bridge.py              # Figma Tokens Studio bridge
├── harvest_session.py           # Multi-page merge
├── project_registry.py          # Multi-project management
├── search.py                    # Full-text search utility
└── test_harvester_v4.py         # Harvester tests

data/
├── ux_laws.csv                  # 48 UX Laws reference
├── design_tests.csv             # 37 Design Tests
└── semi_design_spec.json        # Semi Design token spec

mcp/
└── mcp-config.json              # MCP server configuration

tests/
├── test_harvester.py
├── test_token_mapper.py
├── test_component_generator.py
└── test_design_doc.py

.claude/
├── plans/MASTER_PLAN.md         # Full roadmap
└── specs/                       # Detailed specifications
```

## Code Style

**Python 3.x:**
- No external dependencies except Playwright (optional for browser automation)
- PEP 8, type hints encouraged
- Doc strings in English, comments can be bilingual

**Generated React/TypeScript:**
- Must use `forwardRef` for component forwarding
- Proper JSX formatting, no syntax errors
- All Semi Design CSS variables follow `--semi-*` naming convention
- Must compile: `npx tsc --noEmit`

**Semi Design Compliance:**
- Reference: https://github.com/DouyinFE/semi-design
- Token spec: `packages/semi-theme-default/scss/global.scss`
- Component patterns: 60+ components in `packages/semi-ui/`

## Testing Requirements

1. **Unit tests** — pytest for token mapping, color accuracy, component generation
2. **Type checking** — TypeScript validation on all generated code
3. **Integration** — Full pipeline end-to-end on reference sites
4. **Manual** — Visual inspection of generated components in browser

Test before commit:
```bash
pytest tests/ -v && npx tsc --noEmit
```

## Git Workflow

- **Conventional commits**: `fix:`, `feat:`, `docs:`, `refactor:`, `test:`
- **Branches**: feature-*, bugfix-*, hotfix-* from main
- **Code review** before merge to main
- **Never push** directly to main
- Tag releases: `v0.1.0`, `v0.2.0`, etc.

## Current Priorities (P0 → P2)

**P0 (Critical):**
- Fix `component_generator.py` — generated code has syntax errors, won't compile
- Fix `token_mapper.py` — color accuracy issues (neutrals, semantic colors)

**P1 (High):**
- Expand component templates from 4 to 20+
- Upgrade `design_doc_generator.py` to semi.design quality
- Improve Figma bridge integration

**P2 (Medium):**
- Performance optimization for large harvests
- Better error messaging and logging
- Extended CSS variable support

## Boundaries — What AI Must NOT Do

- ❌ Modify `data/ux_laws.csv` or `data/design_tests.csv` without explicit approval
- ❌ Push to main branch directly (PR + review required)
- ❌ Change build or deployment configs without review
- ❌ Commit generated code to version control (output/ is .gitignored)
- ❌ Run production harvests without confirming the target URL
- ❌ Modify Semi Design token spec without referencing upstream

## For Full Skill Details

See **SKILL.md** in root directory for detailed capability matrix, agent persona, and extended best practices.

---

**Last Updated:** 2026-02-26
**Version:** 1.0
**Maintainer:** UX Master

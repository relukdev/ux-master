# CLAUDE.md — UX Master Design System Platform

## Project Overview

UX Master is an AI-powered design system extraction and generation platform combining **Design Intelligence** (48 UX Laws, 37 Design Tests, 1032+ patterns) with **Design System Automation** (Harvester v4, Token Mapping, Component Generation). One command transforms any website or codebase into a complete, production-ready design system based on Semi Design architecture.

## Unified Skill

The full UX Master skill is at `.skills/skills/ux-master/SKILL.md` — read this for the complete workflow, persona ("The UX Master"), 5 Core Directives, and both design intelligence and harvester pipelines.

Cross-platform configs also available:
- `AGENTS.md` — For Antigravity, Codex, OpenCode, Cursor
- `GEMINI.md` — For Gemini CLI

## Architecture

```
scripts/
├── harvester_v4.js          # Browser JS injection — extracts 120+ tokens from DOM
├── harvester_browser.py     # Playwright automation — opens browser, injects harvester
├── extractor.py             # CSS/local file extraction (non-browser)
├── token_mapper.py          # Maps raw harvest → Semi Design CSS variables
├── design_system_indexer.py # Builds indexed design system (Semi architecture)
├── component_generator.py   # Generates React/Semi/Vue components from tokens
├── design_doc_generator.py  # Generates HTML documentation page
├── harvester_cli.py         # Unified CLI orchestrator
├── figma_bridge.py          # Figma Tokens Studio integration
├── harvest_session.py       # Multi-page harvest merge
├── project_registry.py      # Multi-project management
├── search.py                # BM25 search — 1032+ patterns across 16 domains
└── uxm.py                   # Unified orchestrator (cross-platform entry point)

data/                        # 16 domains: UX Laws, Design Tests, styles, colors, typography...
mcp/                         # MCP server config (8 tools, Figma/Stitch/VSCode integrations)
.skills/skills/ux-master/    # Unified skill + references + helper scripts
```

## Key Commands

```bash
# === FULL PIPELINE ===
python3 scripts/harvester_cli.py quick https://example.com --framework semi
python3 scripts/uxm.py https://example.com --project myapp   # Unified orchestrator

# === DESIGN INTELLIGENCE ===
python3 scripts/search.py "fintech dashboard" --design-system -p "ProjectName"
python3 scripts/search.py "mobile app" --domain ux-laws -n 5
python3 scripts/search.py "checkout flow" --domain design-tests

# === INDIVIDUAL PIPELINE STEPS ===
python3 scripts/harvester_browser.py --url https://example.com --output ./output
python3 scripts/token_mapper.py -i output/harvest.json --project myproject
python3 scripts/design_system_indexer.py --input output/harvest.json --name "MyApp" --output output/
python3 scripts/component_generator.py --input output/design-system.json --all --output ./components
python3 scripts/design_doc_generator.py -i output/harvest.json -o output/design-system.html

# === VALIDATION & TESTING ===
python3 -m pytest tests/ -v
python3 scripts/test_harvester_v4.py
python3 .skills/skills/ux-master/scripts/validate_tokens.py -i output/design-system.css
npx tsc --noEmit  # Validate generated TypeScript
```

## Key References

- **Unified Skill**: `.skills/skills/ux-master/SKILL.md`
- **Master Plan**: `.claude/plans/MASTER_PLAN.md`
- **Detailed Specs**: `.claude/specs/` (8 spec files)
- **Semi Design Source**: https://github.com/DouyinFE/semi-design
- **Semi Design Tokens**: `packages/semi-theme-default/scss/global.scss`
- **Pipeline Guide**: `.skills/skills/ux-master/references/pipeline-guide.md`
- **Token Spec**: `.skills/skills/ux-master/references/token-spec.md`
- **Troubleshooting**: `.skills/skills/ux-master/references/troubleshooting.md`
- **MCP Config**: `mcp/mcp-config.json` (8 tools)

## Current Priorities

See `.claude/plans/MASTER_PLAN.md` for full roadmap:

1. **P0**: Fix `component_generator.py` — syntax errors in generated JSX
2. **P0**: Fix `token_mapper.py` — color accuracy (neutrals, semantic colors)
3. **P1**: Expand component templates to 22+ (from current 4)
4. **P1**: Upgrade `design_doc_generator.py` to semi.design quality
5. **P2**: npm theme package generator, Figma bidirectional sync

## Coding Standards

- Python 3.x, no external deps except Playwright (optional)
- Generated React code: TypeScript, `forwardRef`, proper JSX, `cn()` utility
- All CSS variables: `--semi-*` naming convention
- Test every generated component: `npx tsc --noEmit`
- Doc strings English, comments bilingual OK

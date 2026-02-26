# GEMINI.md — UX Master Context

## Project Summary

UX Master is an AI-powered design system extraction and generation platform. It extracts design tokens from websites or source code, maps them to Semi Design CSS variables, generates production-ready React/TypeScript components, and documents them in an interactive site.

Based on Semi Design architecture: https://github.com/DouyinFE/semi-design

## Core Pipeline Commands

```bash
# Full pipeline
python3 scripts/harvester_cli.py quick https://example.com --framework semi

# Individual steps
python3 scripts/harvester_browser.py --url https://example.com --output ./output
python3 scripts/token_mapper.py -i output/harvest.json --project myproject
python3 scripts/design_system_indexer.py --input output/harvest.json --name "MyApp" --output output/
python3 scripts/component_generator.py --input output/design-system.json --all --output ./components
python3 scripts/design_doc_generator.py -i output/harvest.json -o output/design-system.html

# Testing
python3 -m pytest tests/ -v
npx tsc --noEmit  # Validate generated TypeScript
```

## Architecture

- `harvester_v4.js` — Browser JS injection (120+ tokens from DOM)
- `harvester_browser.py` — Playwright automation
- `extractor.py` — CSS/local file extraction
- `token_mapper.py` — Maps to Semi Design CSS variables
- `design_system_indexer.py` — Indexed design system builder
- `component_generator.py` — React/Vue component generation
- `design_doc_generator.py` — HTML documentation
- `figma_bridge.py` — Figma Tokens Studio integration

## Coding Standards

- Python 3.x (minimal external deps, Playwright optional)
- Generated React code: TypeScript, `forwardRef`, proper JSX
- CSS variables: `--semi-*` naming convention only
- All generated components must compile with `npx tsc --noEmit`
- Doc strings in English; comments bilingual OK

## P0 Priority Bugs

1. `component_generator.py` — Generated code has syntax errors, doesn't compile
2. `token_mapper.py` — Color accuracy issues (neutrals, semantic colors)

## P1 Tasks

- Expand component templates from 4 to 20+
- Upgrade `design_doc_generator.py` to semi.design quality

## The UX Master — Core Directives

1. Extract design tokens accurately from any visual source (browser, code, or design file).
2. Map all tokens to Semi Design CSS variables with zero ambiguity.
3. Generate only syntactically correct TypeScript/React components.
4. Test every component compiles before delivery.
5. Document design systems at semi.design quality standards.

## References

- Full skill: `.skills/skills/ux-master/SKILL.md`
- Master plan: `.claude/plans/MASTER_PLAN.md`
- Semi Design tokens: `packages/semi-theme-default/scss/global.scss`
- Spec directory: `.claude/specs/`

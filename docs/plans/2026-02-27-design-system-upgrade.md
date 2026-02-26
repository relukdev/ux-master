# Design System Generation Upgrade — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use sp-executing-plans to implement this plan task-by-task.

**Goal:** Upgrade UX Master to generate per-project design systems in a central registry (`~/.uxmaster/projects/`) with a semi.design-quality interactive guideline site.

**Architecture:** Extend `ProjectRegistry` to use `~/.uxmaster/projects/` as default, add a new `SiteGenerator` that produces a 3-page static site (Getting Started, Design Tokens, Component Gallery), fix P0 component generator syntax bugs, and add CLI commands (`projects list`, `serve`, `build`).

**Tech Stack:** Python 3.x, HTML/CSS/JS (generated static site), http.server (local serving)

---

## Task 1: Fix Component Generator P0 Syntax Bugs

The `generate_semi_component()` and `generate_react_component()` functions produce invalid TSX due to malformed destructure syntax on lines 55 and 99.

**Files:**
- Modify: `scripts/component_generator.py:55,99`
- Test: `tests/test_component_syntax.py` (new)

**Step 1: Write the failing test**

Create `tests/test_component_syntax.py`:

```python
#!/usr/bin/env python3
"""Tests that generated components have valid syntax."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from component_generator import generate_semi_component, generate_react_component


class TestComponentSyntax(unittest.TestCase):
    """Generated components must have valid JSX/TSX syntax."""

    def test_semi_component_has_opening_brace_in_destructure(self):
        """The forwardRef callback must have ({ before destructured props."""
        code = generate_semi_component(
            name="Button", interface_name="Button",
            semi_component="Button", props="children: React.ReactNode;",
            prop_destructure="children",
            style="{}", source="test", timestamp="2026-01-01"
        )
        # Must have >((  { destructure pattern, not >((destructure
        self.assertIn(">(({ ", code.replace("\n", " "))
        # Must NOT have double closing braces/parens issues
        self.assertNotIn("}});", code)

    def test_react_component_has_opening_brace_in_destructure(self):
        """The forwardRef callback must have ({ before destructured props."""
        code = generate_react_component(
            name="Button", interface_name="Button",
            element_type="button", props="children: React.ReactNode;",
            prop_destructure="children",
            base_classes='"btn"', source="test", timestamp="2026-01-01"
        )
        self.assertIn(">(({ ", code.replace("\n", " "))
        self.assertNotIn("}});", code)

    def test_semi_component_no_name_collision(self):
        """Exported component must not shadow imported Semi component."""
        code = generate_semi_component(
            name="HxButton", interface_name="HxButton",
            semi_component="Button", props="children: React.ReactNode;",
            prop_destructure="children",
            style="{}", source="test", timestamp="2026-01-01"
        )
        self.assertIn("export const HxButton", code)
        self.assertIn('import { Button }', code)

    def test_generated_component_is_valid_tsx_structure(self):
        """Basic TSX structure validation."""
        code = generate_semi_component(
            name="TestCard", interface_name="TestCard",
            semi_component="Card", props="children: React.ReactNode;",
            prop_destructure="children",
            style="{}", source="test", timestamp="2026-01-01"
        )
        self.assertIn("export interface TestCardProps", code)
        self.assertIn("export const TestCard", code)
        self.assertIn("React.forwardRef", code)
        self.assertIn('.displayName = "TestCard"', code)


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run test to verify it fails**

```bash
cd "/Users/todyle/Library/Mobile Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master"
python3 -m pytest tests/test_component_syntax.py -v
```
Expected: FAIL (current code produces `>((children, className, ...props}}, ref)` — missing `{`)

**Step 3: Fix the syntax bugs**

In `scripts/component_generator.py`, fix two lines:

Line 55 — change:
```python
f'>(({prop_destructure}, className, ...props}}, ref) => {{',
```
to:
```python
f'>(( {{ {prop_destructure}, className, ...props }}, ref) => {{',
```

Line 99 — same fix:
```python
f'>(( {{ {prop_destructure}, className, ...props }}, ref) => {{',
```

Also fix closing brace on lines 68 and 110 — change `'}});'` to `'});'`.

**Step 4: Run test to verify it passes**

```bash
python3 -m pytest tests/test_component_syntax.py -v
```
Expected: PASS

**Step 5: Run existing tests to verify no regressions**

```bash
python3 -m pytest tests/test_generator.py -v
```

**Step 6: Commit**

```bash
git add scripts/component_generator.py tests/test_component_syntax.py
git commit -m "fix(component-gen): fix TSX syntax — missing brace in forwardRef destructure"
```

---

## Task 2: Upgrade Project Registry to Central Location

Change default output directory from `./output` to `~/.uxmaster/projects/` and add `build()` and `serve()` methods.

**Files:**
- Modify: `scripts/project_registry.py`
- Modify: `tests/test_project_registry.py` (add new tests)

**Step 1: Write failing tests**

Add to `tests/test_project_registry.py`:

```python
class TestRegistryDefaults(unittest.TestCase):
    """Central registry defaults."""

    def test_default_output_dir_is_uxmaster(self):
        """Default output should be ~/.uxmaster/projects/."""
        reg = ProjectRegistry()
        expected = Path.home() / ".uxmaster" / "projects"
        self.assertEqual(reg.output_dir, expected)

    def test_custom_output_dir_still_works(self):
        """Backward compat: custom output_dir is respected."""
        tmp = Path(tempfile.mkdtemp())
        try:
            reg = ProjectRegistry(output_dir=tmp)
            self.assertEqual(reg.output_dir, tmp)
        finally:
            shutil.rmtree(tmp)


class TestRegistryServe(unittest.TestCase):
    """HTTP serving for project sites."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.registry = ProjectRegistry(output_dir=self.tmp_dir)
        self.registry.create("Test", "https://test.com")
        # Create a dummy site
        site_dir = self.tmp_dir / "test" / "site"
        site_dir.mkdir(parents=True)
        (site_dir / "index.html").write_text("<html><body>Hello</body></html>")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_get_site_dir(self):
        site_dir = self.registry.get_site_dir("test")
        self.assertTrue(site_dir.exists())
        self.assertTrue((site_dir / "index.html").exists())

    def test_get_site_dir_nonexistent(self):
        site_dir = self.registry.get_site_dir("nope")
        self.assertFalse(site_dir.exists())
```

**Step 2: Run to verify they fail**

```bash
python3 -m pytest tests/test_project_registry.py::TestRegistryDefaults -v
python3 -m pytest tests/test_project_registry.py::TestRegistryServe -v
```

**Step 3: Implement changes**

In `scripts/project_registry.py`:
- Change `OUTPUT_DIR` from `Path(__file__).parent.parent / "output"` to `Path.home() / ".uxmaster" / "projects"`
- Add `get_site_dir(self, slug)` method → returns `self.output_dir / slug / "site"`
- Add `serve(self, slug, port=3939)` method using `http.server`

**Step 4: Run tests**

```bash
python3 -m pytest tests/test_project_registry.py -v
```

**Step 5: Commit**

```bash
git add scripts/project_registry.py tests/test_project_registry.py
git commit -m "feat(registry): use ~/.uxmaster/projects/ as central registry"
```

---

## Task 3: Create Site Generator

New script that generates a 3-page semi.design-inspired static site from design-system.json.

**Files:**
- Create: `scripts/site_generator.py`
- Create: `tests/test_site_generator.py`

**Step 1: Write failing tests**

Create `tests/test_site_generator.py`:

```python
#!/usr/bin/env python3
"""Tests for site_generator.py — Design System Guideline Site."""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from site_generator import SiteGenerator

SAMPLE_DESIGN_SYSTEM = {
    "name": "TestApp Design System",
    "colors": {
        "primary": "#4F46E5",
        "success": "#10B981",
        "warning": "#F59E0B",
        "danger": "#EF4444",
    },
    "typography": {
        "font-weight-regular": "400",
        "font-weight-bold": "700",
    },
    "spacing": {
        "tight": "8px",
        "base": "16px",
        "loose": "24px",
    },
    "borders": {
        "radius-sm": "3px",
        "radius-md": "6px",
    },
    "shadows": {
        "sm": "0 0 1px rgba(0,0,0,0.1)",
    },
    "components": {},
}

SAMPLE_META = {
    "name": "TestApp",
    "url": "https://testapp.com",
    "slug": "testapp",
    "created_at": "2026-01-01T00:00:00Z",
}

SAMPLE_TOKENS = {
    "--semi-color-primary": "#4F46E5",
    "--semi-color-success": "#10B981",
}


class TestSiteGeneratorOutput(unittest.TestCase):
    """Site generator produces correct file structure."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.gen = SiteGenerator(
            design_system=SAMPLE_DESIGN_SYSTEM,
            tokens=SAMPLE_TOKENS,
            meta=SAMPLE_META,
            output_dir=self.tmp_dir,
        )
        self.gen.generate()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_index_html_exists(self):
        self.assertTrue((self.tmp_dir / "index.html").exists())

    def test_tokens_html_exists(self):
        self.assertTrue((self.tmp_dir / "tokens.html").exists())

    def test_components_html_exists(self):
        self.assertTrue((self.tmp_dir / "components.html").exists())

    def test_css_exists(self):
        self.assertTrue((self.tmp_dir / "css" / "style.css").exists())

    def test_js_exists(self):
        self.assertTrue((self.tmp_dir / "js" / "app.js").exists())


class TestSiteContent(unittest.TestCase):
    """Generated pages have correct content."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.gen = SiteGenerator(
            design_system=SAMPLE_DESIGN_SYSTEM,
            tokens=SAMPLE_TOKENS,
            meta=SAMPLE_META,
            output_dir=self.tmp_dir,
        )
        self.gen.generate()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def _read(self, filename):
        return (self.tmp_dir / filename).read_text()

    def test_index_has_project_name(self):
        self.assertIn("TestApp", self._read("index.html"))

    def test_index_has_valid_html(self):
        html = self._read("index.html")
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("</html>", html)

    def test_index_has_sidebar_nav(self):
        html = self._read("index.html")
        self.assertIn("sidebar", html.lower())

    def test_tokens_has_color_values(self):
        html = self._read("tokens.html")
        self.assertIn("#4F46E5", html)
        self.assertIn("#10B981", html)

    def test_tokens_has_spacing_values(self):
        html = self._read("tokens.html")
        self.assertIn("8px", html)
        self.assertIn("16px", html)

    def test_tokens_has_copy_functionality(self):
        html = self._read("tokens.html")
        self.assertIn("copy", html.lower())

    def test_components_has_component_section(self):
        html = self._read("components.html")
        self.assertIn("component", html.lower())

    def test_all_pages_have_dark_mode_toggle(self):
        for page in ["index.html", "tokens.html", "components.html"]:
            html = self._read(page)
            self.assertIn("dark", html.lower(), f"{page} missing dark mode")

    def test_all_pages_have_navigation_links(self):
        for page in ["index.html", "tokens.html", "components.html"]:
            html = self._read(page)
            self.assertIn("tokens.html", html, f"{page} missing tokens link")
            self.assertIn("components.html", html, f"{page} missing components link")


class TestSiteMinimalInput(unittest.TestCase):
    """Handles minimal input without crashing."""

    def test_empty_design_system(self):
        tmp_dir = Path(tempfile.mkdtemp())
        try:
            gen = SiteGenerator(
                design_system={},
                tokens={},
                meta={"name": "Empty", "slug": "empty"},
                output_dir=tmp_dir,
            )
            gen.generate()
            self.assertTrue((tmp_dir / "index.html").exists())
        finally:
            shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run to verify they fail**

```bash
python3 -m pytest tests/test_site_generator.py -v
```
Expected: ImportError (site_generator doesn't exist)

**Step 3: Implement `scripts/site_generator.py`**

Create the full `SiteGenerator` class that produces:
- `index.html` — Getting Started page with sidebar, quick start guide
- `tokens.html` — Design tokens with interactive color swatches, typography specimens, spacing bars
- `components.html` — Component gallery with card previews
- `css/style.css` — Semi.design-inspired styles (sidebar layout, dark mode vars)
- `js/app.js` — Sidebar toggle, dark mode toggle, copy-to-clipboard, token search

Key implementation details:
- Use Python string templates (no Jinja2 dependency)
- All CSS/JS is embedded inline or in local files (no CDN)
- Semi.design-inspired sidebar layout with collapsible navigation
- Color swatches use CSS custom properties from the design system
- Click-to-copy on all token values

**Step 4: Run tests**

```bash
python3 -m pytest tests/test_site_generator.py -v
```

**Step 5: Commit**

```bash
git add scripts/site_generator.py tests/test_site_generator.py
git commit -m "feat(site-gen): add multi-page design system guideline site generator"
```

---

## Task 4: Add CLI Commands (projects, serve, build)

Add `projects list`, `serve`, and `build` subcommands to the CLI.

**Files:**
- Modify: `scripts/harvester_cli.py`

**Step 1: Add `projects` subcommand to `create_parser()`**

Add three new subparsers:
- `projects` — with sub-subcommands: `list`, `info <slug>`, `delete <slug>`
- `serve` — `serve <slug> [--port 3939]`
- `build` — `build <slug>` (regenerate site for existing project)

**Step 2: Add handler methods to `HarvesterCLI`**

- `projects_list()` — calls `ProjectRegistry().list_all()`, prints table
- `projects_info(slug)` — calls `ProjectRegistry().get(slug)`, prints details
- `projects_delete(slug)` — calls `ProjectRegistry().delete(slug)`
- `serve(slug, port)` — calls `ProjectRegistry().serve(slug, port)`
- `build(slug)` — loads project data, runs SiteGenerator, outputs to `project/site/`

**Step 3: Update `quick()` to use registry**

Modify `quick()` to:
1. Accept `--name` argument (default: derive from URL)
2. Create project in registry
3. Run full pipeline into project directory
4. Generate site
5. Print serve command hint

**Step 4: Smoke test CLI commands**

```bash
# Test projects list
python3 scripts/harvester_cli.py projects list

# Test help
python3 scripts/harvester_cli.py serve --help
python3 scripts/harvester_cli.py build --help
```

**Step 5: Commit**

```bash
git add scripts/harvester_cli.py
git commit -m "feat(cli): add projects/serve/build commands"
```

---

## Task 5: Integration Test — End-to-End Pipeline

Use the existing HexaBox harvest data to test the full pipeline.

**Files:**
- Test: manual verification

**Step 1: Build design system from existing harvest**

```bash
cd "/Users/todyle/Library/Mobile Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master"

# Create project in registry
python3 scripts/project_registry.py --create "HexaBox" --url "https://hexabox.dexignlab.com"

# Add existing harvest
python3 scripts/project_registry.py --add-harvest hexabox -i output/hexabox-harvest.json
```

**Step 2: Run site generator**

```bash
python3 scripts/harvester_cli.py build hexabox
```

**Step 3: Serve and verify in browser**

```bash
python3 scripts/harvester_cli.py serve hexabox
# Opens http://localhost:3939
```

Verify in browser:
1. ✅ Sidebar navigation is visible and links work
2. ✅ Getting Started page shows project name "HexaBox"
3. ✅ Tokens page shows color swatches with correct hex values
4. ✅ Tokens page shows typography specimens
5. ✅ Components page shows generated component cards
6. ✅ Dark mode toggle works
7. ✅ Copy-to-clipboard works on token values
8. ✅ Responsive: sidebar collapses on mobile width

**Step 4: Run all tests**

```bash
python3 -m pytest tests/ -v --ignore=tests/automation
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: complete design system generation upgrade v4.1"
```

---

## Task 6: MCP Integration (Minimal)

Add design system tools to existing MCP server.

**Files:**
- Modify: `mcp/server.py`

**Step 1: Add tools**

Add to the existing MCP server:
- `list_design_systems` — returns list of projects from registry
- `get_design_tokens` — returns CSS tokens for a project slug
- `build_design_system` — triggers full pipeline for a project

**Step 2: Run MCP tests**

```bash
python3 -m pytest tests/test_mcp_server.py -v
```

**Step 3: Commit**

```bash
git add mcp/server.py
git commit -m "feat(mcp): add design system management tools"
```

---

## Verification Summary

| Test File | Command | What it verifies |
|-----------|---------|-----------------|
| `tests/test_component_syntax.py` | `python3 -m pytest tests/test_component_syntax.py -v` | Generated TSX has valid syntax |
| `tests/test_project_registry.py` | `python3 -m pytest tests/test_project_registry.py -v` | Registry CRUD + central path + serve |
| `tests/test_site_generator.py` | `python3 -m pytest tests/test_site_generator.py -v` | Site pages exist, have correct content |
| `tests/test_generator.py` | `python3 -m pytest tests/test_generator.py -v` | Template generator still works |
| `tests/test_design_doc.py` | `python3 -m pytest tests/test_design_doc.py -v` | Design doc generator still works |
| All tests | `python3 -m pytest tests/ -v --ignore=tests/automation` | Full regression |
| Manual | `python3 scripts/harvester_cli.py serve hexabox` → browser | Visual verification of guideline site |

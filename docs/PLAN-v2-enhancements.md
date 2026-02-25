# PLAN: Semi-Sync Harvester v2 — 3 Enhancements

## Enhancement 1: Multi-Project Registry

**Problem:** Output hiện tại chỉ lưu vào `output/haravan/`. Khi dev làm nhiều dự án → cần lưu, quản lý, và tái sử dụng từng design system riêng.

### Proposed Changes

#### [NEW] [project_registry.py](file:///Users/todyle/Library/Mobile Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master/scripts/project_registry.py)

```python
class ProjectRegistry:
    """Manages multiple harvested design systems."""
    
    # Storage: output/<project-slug>/
    #   ├── manifest.json        # Project metadata + pages scanned
    #   ├── harvest-raw.json     # Merged raw harvest
    #   ├── semi-theme-override.css
    #   ├── figma-tokens.json
    #   ├── design-system.html   # Doc site (Enhancement 3)
    #   └── HaravanDashboard.tsx # React component
    
    def create(name, url) -> ProjectInfo
    def get(slug) -> ProjectInfo
    def list_all() -> list[ProjectInfo]
    def add_page_harvest(slug, page_harvest) -> MergedTokens
    def delete(slug)
```

CLI integration:
```bash
# Create/update project
python3 scripts/project_registry.py --create "Haravan" --url "https://showcase.myharavan.com"

# List all projects  
python3 scripts/project_registry.py --list

# Get specific project info
python3 scripts/project_registry.py --get haravan

# Token mapper now takes --project
python3 scripts/token_mapper.py -i harvest.json --project haravan
```

---

## Enhancement 2: Multi-Page Scanner

**Problem:** Scan 1 trang → thiếu data (vd: không thấy success/danger colors, form styles). Scan N trang → complete design system.

### Proposed Changes

#### [NEW] [harvest_session.py](file:///Users/todyle/Library/Mobile Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master/scripts/harvest_session.py)

```python
def merge_harvests(harvests: list[dict]) -> dict:
    """Merge multiple page harvests into consolidated tokens."""
    # Strategy:
    #   - Colors: take most frequent value (voting system)
    #   - Typography: take from body/main page
    #   - Geometry: weighted average / mode
    #   - Surfaces: union of all found surfaces
    
def calculate_confidence(harvests) -> dict:
    """Score each token by how many pages it appeared on."""
    # confidence = appearances / total_pages
```

Updated `/harvest` workflow:

```
/harvest <URL> --pages dashboard,products,orders,settings
# OR
/harvest <URL> --scan-depth 4

AI Workflow:
1. Navigate to base URL → user authenticates
2. Scan page 1 (dashboard) → harvest
3. Navigate to page 2 (products) → harvest  
4. Navigate to page 3 (orders) → harvest
5. Merge all harvests → consolidated tokens
6. Generate output with confidence scores
```

---

## Enhancement 3: Design System Documentation Site

**Problem:** Output hiện tại là CSS + JSON files. Cần 1 trang web đẹp để dev/designer xem design system.

### Proposed Changes

#### [NEW] [design_doc_generator.py](file:///Users/todyle/Library/Mobile Documents/com~apple~CloudDocs/Code/AgentSkills/ux-master/scripts/design_doc_generator.py)

Single-file HTML output (`design-system.html`), inspired by Semi Design site:

**Sections:**
1. **Introduction** — Project name, source URL, extraction dates
2. **🎨 Color Palette** — Interactive swatches with hex values + copy button
3. **🔤 Typography** — Font specimens (headings, body, muted)
4. **📐 Geometry** — Border radius preview + shadow specimens  
5. **🧱 Components Preview** — Button, Card, Input, Tag samples using CSS vars
6. **📋 Token Reference** — Full table of `--semi-*` variables
7. **⚙️ Usage** — Install instructions, CSS import, React setup

**Tech:** Pure HTML + CSS + vanilla JS. No build step. Dark mode toggle. Responsive.

---

## File Summary

| Enhancement | File | Action |
|-------------|------|--------|
| 1 | `scripts/project_registry.py` | NEW |
| 1 | `tests/test_project_registry.py` | NEW |
| 2 | `scripts/harvest_session.py` | NEW |
| 2 | `tests/test_harvest_session.py` | NEW |
| 3 | `scripts/design_doc_generator.py` | NEW |
| 3 | `tests/test_design_doc.py` | NEW |
| All | `SKILL.md` | MODIFY |

---

## Verification Plan

### Automated Tests

```bash
# All unit tests
cd /tmp/ux-test && python3 -m pytest test_project_registry.py test_harvest_session.py test_design_doc.py -v

# Generate doc site and validate HTML
python3 scripts/design_doc_generator.py --project haravan
# → opens design-system.html in browser
```

### Browser Integration Test

1. Dùng AI browser mở `design-system.html` → verify render đẹp
2. Test dark mode toggle
3. Test color swatch copy button
4. Test responsive layout

### E2E: Multi-page Haravan scan

1. Scan 3 trang: dashboard, products list, orders list
2. Verify merged tokens có nhiều thông tin hơn scan 1 trang
3. Generate doc site → verify hiển thị đủ

# Design System Extraction Plan — Phased Approach

> Hướng dẫn chi tiết cách MasterDesign Agent thu thập và xây dựng Design System hoàn chỉnh từ một trang web.

---

## Component Checklist

### 🔴 MUST HAVE (Phase 1) — Đủ để rebuild page

| # | Category | Tokens / Components | Source Pages |
|---|----------|---------------------|--------------|
| 1 | **Color System** | primary + shades, semantic (success/warning/danger/info), neutral scale (10 shades), link color, disabled color | Dashboard, Any |
| 2 | **Surface System** | app_bg, card_bg, sidebar_bg, header_bg, modal_bg, hover_bg, selected_bg, input_bg | Dashboard, Settings |
| 3 | **Typography Scale** | font-family (heading + body), 6 sizes (xs→2xl), 4 weights (regular→bold), line-heights, letter-spacings | Any |
| 4 | **Spacing System** | 8 spacing values (4px→48px) from actual paddings/margins/gaps | Dashboard |
| 5 | **Border System** | border-color, border-width, border-radius (sm/md/lg/xl/full) | Any |
| 6 | **Shadow System** | shadow-sm, shadow-md, shadow-lg (from cards, dropdowns, modals) | Dashboard, Popup |
| 7 | **Button** | primary, secondary, outline, danger, ghost, disabled — sizes (sm/md/lg) | Any |
| 8 | **Input / Form** | text input, select, checkbox, radio, textarea — border, focus ring, error state | Settings, Form |
| 9 | **Card** | padding, radius, shadow, border, header/body/footer structure | Dashboard |
| 10 | **Table** | header bg, row hover, border style, cell padding, stripe pattern | Report, Orders |
| 11 | **Layout Metrics** | sidebar width, header height, content max-width, content padding, grid gap | Dashboard |
| 12 | **Navigation** | sidebar item height, active bg, hover bg, icon size, indent, divider | Dashboard |

> **Phase 1 goal:** 80+ tokens, 6+ component samples → người dùng thấy WOW.

---

### 🟡 SHOULD HAVE (Phase 2) — Nâng cấp thành design system hoàn chỉnh

| # | Category | Tokens / Components |
|---|----------|---------------------|
| 13 | **Tag / Badge** | color variants, sizes, border-radius |
| 14 | **Avatar** | sizes (sm/md/lg), border, fallback bg |
| 15 | **Tooltip** | bg, text color, arrow, shadow, max-width |
| 16 | **Dropdown / Select** | option hover, selected bg, divider, animation |
| 17 | **Modal / Dialog** | overlay bg opacity, modal radius, header/body/footer padding |
| 18 | **Tabs** | active tab indicator, tab padding, border-bottom |
| 19 | **Breadcrumb** | separator, link color, current color |
| 20 | **Pagination** | active bg, hover bg, size, border-radius |
| 21 | **Toast / Notification** | variants (success/error/warning/info), position, icon |
| 22 | **Icon System** | default size, color mapping, stroke-width (if Lucide/Heroicons) |
| 23 | **Transition System** | duration (fast/normal/slow), easing curves |

---

### 🟢 NICE TO HAVE (Phase 3) — Polish & edge cases

| # | Category | Tokens / Components |
|---|----------|---------------------|
| 24 | **Bottom Sheet** (mobile) | handle bar, snap points, overlay |
| 25 | **Skeleton Loader** | base-color, animation-color, border-radius |
| 26 | **Progress Bar** | height, colors, border-radius |
| 27 | **Stepper / Wizard** | step circle size, line connector, active/completed colors |
| 28 | **Charts** | chart color scale (6+ colors), axis color, grid line color |
| 29 | **Data Viz** | KPI card variants, metric typography, delta colors |
| 30 | **Dark Mode** | full alternate surface/text/border/shadow palette |

---

## Smart Harvesting Strategy

### Page Priority Order

```
1. Dashboard          → layout, sidebar, cards, KPI, navigation (richest page)
2. List/Table page    → table styles, pagination, filters, tags, badges
3. Form/Settings      → inputs, selects, checkboxes, radio, textarea, buttons
4. Detail/Modal page  → modal, tabs, breadcrumb, tooltips
5. Report/Analytics   → charts, data viz, progress bars
```

### Batch Extraction Techniques

1. **Full-DOM Scan** — Upgraded harvester scans ALL elements, not just specific selectors. Extracts unique (property, value) pairs and counts frequencies.
2. **Computed Style Histogram** — For colors/sizes, build frequency histogram. Top values = design tokens. Noise eliminated.
3. **Component Blueprint** — For each component type (button, input, table), extract the complete style profile: dimensions, colors, borders, padding, margin, font, transitions.
4. **Spacing Inference** — Collect all padding/margin/gap values across page → derive spacing scale (4, 8, 12, 16, 20, 24, 32, 40, 48).
5. **Shadow Collection** — Every unique box-shadow → categorize by depth (sm/md/lg).
6. **State Extraction** — Programmatically trigger :hover/:focus/:active states to capture interactive styles.

### Browser Discovery Protocol

Khi data không đủ (ví dụ: thiếu success/danger colors, modal styles):

1. AI mở browser → navigate đến URL đã cho
2. Click vào các menu items để tìm trang Report, Settings, Orders
3. Inject harvester v3 vào mỗi trang
4. Merge all harvests → consolidated design system
5. Nếu vẫn thiếu: mở DevTools, inspect tooltip/dropdown/modal → trigger và capture

---

## Execution Plan

### Phase 1: MUST HAVE (Đợt 1)

**Files to create/modify:**

| File | Action | Purpose |
|------|--------|---------|
| `scripts/harvester_v3.js` | NEW | Full-DOM scan, component blueprints, spacing inference |
| `scripts/token_mapper.py` | MODIFY | Map v3 harvest format (components, spacing, layout) |
| `scripts/design_doc_generator.py` | MODIFY | Add component gallery with real extracted styles |
| `tests/test_harvester_v3.py` | NEW | Validate v3 harvest output structure |

**New harvest output structure (v3):**

```json
{
  "meta": { "url": "", "timestamp": "", "title": "", "page_type": "dashboard" },
  "colors": { "primary": "", "success": "", "warning": "", "danger": "", "info": "", "link": "", "disabled": "" },
  "neutrals": { "50": "", "100": "", "200": "", ..., "900": "" },
  "surfaces": { "app_bg": "", "card_bg": "", "sidebar_bg": "", "header_bg": "", "modal_bg": "", "hover_bg": "", "selected_bg": "", "input_bg": "" },
  "typography": { "heading_family": "", "body_family": "", "sizes": { "xs": "", "sm": "", "base": "", "lg": "", "xl": "", "2xl": "" }, "weights": {}, "line_heights": {} },
  "spacing": { "scale": ["4px", "8px", "12px", "16px", "20px", "24px", "32px", "48px"] },
  "borders": { "color": "", "width": "", "radius": { "sm": "", "md": "", "lg": "", "xl": "", "full": "" } },
  "shadows": { "sm": "", "md": "", "lg": "" },
  "layout": { "sidebar_width": "", "header_height": "", "content_max_width": "", "content_padding": "", "grid_gap": "" },
  "components": {
    "button": { "primary": {}, "secondary": {}, "outline": {}, "danger": {}, "sizes": {} },
    "input": { "default": {}, "focus": {}, "error": {} },
    "card": { "default": {} },
    "table": { "header": {}, "row": {}, "cell": {} },
    "nav_item": { "default": {}, "active": {}, "hover": {} },
    "tag": { "variants": {} }
  }
}
```

### Phase 2 & 3

Sẽ mở rộng harvester để capture thêm modal, dropdown, tooltip, tabs, dark mode, chart colors. Upgraded `design_doc_generator.py` sẽ render tất cả component samples.

---

## Verification

1. Chạy harvester v3 trên Haravan dashboard
2. So sánh token count: v2 (~20 tokens) vs v3 (80+ tokens)
3. Generate design-system.html → verify component gallery có đủ 12 categories
4. Browser test: dark mode, copy, responsive

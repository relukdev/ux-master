# Spec 03: Fix Doc Generator Display

## Problem

`scripts/design_doc_generator.py` generates an HTML page with display issues:
- Color Palette section shows border radius values instead of actual color swatches
- Missing interactive component previews
- No copy-to-clipboard on tokens

## Root Cause

In `_build_color_section()` (line 204-224), the function iterates over tokens but doesn't filter by color-related tokens, so border/geometry tokens appear in the color section.

## Fix Steps

### Step 1: Separate Token Categories Properly

In `generate_doc_html()`, categorize tokens before rendering:

```python
def categorize_tokens(tokens):
    categories = {
        "brand": {},      # --semi-color-primary-*, secondary-*, tertiary-*
        "semantic": {},    # --semi-color-success-*, warning-*, danger-*, info-*
        "neutral": {},     # --semi-color-neutral-*
        "background": {},  # --semi-color-bg-*
        "text": {},        # --semi-color-text-*
        "fill": {},        # --semi-color-fill-*
        "border": {},      # --semi-color-border, --semi-border-*
        "shadow": {},      # --semi-shadow-*
        "typography": {},  # --semi-font-*
        "spacing": {},     # --semi-spacing-*
        "sizing": {},      # --semi-height-*, --semi-width-*
    }
    
    for key, value in tokens.items():
        if key.startswith("--semi-color-primary") or key.startswith("--semi-color-secondary"):
            categories["brand"][key] = value
        elif key.startswith("--semi-color-success") or key.startswith("--semi-color-warning"):
            categories["semantic"][key] = value
        # ... etc
    
    return categories
```

### Step 2: Better Color Swatch Rendering

```python
def _build_color_swatch(name, hex_value, label=None):
    """Render a single color swatch with hex label."""
    text_color = "#FFFFFF" if luminance(hex_value) < 128 else "#000000"
    return f'''
    <div class="swatch" style="background-color: {hex_value}; color: {text_color}">
        <div class="swatch-name">{label or name}</div>
        <div class="swatch-value">{hex_value}</div>
        <button class="copy-btn" onclick="navigator.clipboard.writeText('{hex_value}')">Copy</button>
    </div>
    '''
```

### Step 3: Add Component Preview Section

Embed live HTML previews of components using the extracted tokens:

```python
def _build_live_component_preview(tokens):
    """Generate HTML that renders button/card/input with extracted tokens."""
    primary = tokens.get("--semi-color-primary", "#0F79F3")
    radius = tokens.get("--semi-border-radius-medium", "6px")
    font = tokens.get("--semi-font-family-regular", "Inter, sans-serif")
    
    return f'''
    <section id="components">
        <h2>Component Preview</h2>
        <div class="component-grid">
            <div class="component-card">
                <h3>Button</h3>
                <div class="preview">
                    <button style="background:{primary}; color:#fff; 
                        border-radius:{radius}; font-family:{font};
                        padding:8px 16px; border:none; cursor:pointer">
                        Primary Button
                    </button>
                    <button style="background:transparent; color:{primary};
                        border:1px solid {primary}; border-radius:{radius};
                        font-family:{font}; padding:8px 16px; cursor:pointer">
                        Outline Button
                    </button>
                </div>
            </div>
            <!-- Card, Input, Badge previews -->
        </div>
    </section>
    '''
```

## Files to Modify

- `scripts/design_doc_generator.py`
  - `generate_doc_html()` — add token categorization
  - `_build_color_section()` — fix to only show colors
  - `_build_components_section()` — add live HTML preview
  - `_get_css()` — add styles for swatches and previews

## Verification

```bash
# Generate doc for Fila
python3 scripts/design_doc_generator.py \
  -i output/fila/harvest-v4-raw.json \
  -o /tmp/test-doc.html

# Open in browser and verify:
# 1. Color Palette shows actual color swatches (not border radius)
# 2. Each swatch shows hex value
# 3. Component Preview section shows styled buttons, cards, inputs
# 4. Copy button works on token values
open /tmp/test-doc.html
```

## Acceptance Criteria

- [ ] Color Palette section shows colored rectangles with hex labels
- [ ] Brand, semantic, neutral colors in separate groups
- [ ] Component Preview shows at least button, card, input with extracted tokens
- [ ] Copy-to-clipboard works for hex values and CSS variable names
- [ ] Dark mode toggle still works correctly
- [ ] Page renders well on both desktop and mobile

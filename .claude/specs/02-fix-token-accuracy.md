# Spec 02: Fix Token Accuracy

## Problem

Token extraction produces inaccurate results:
1. Neutral scale has near-identical shades (no visual gradient)
2. Semantic colors capture background tint instead of strong base color
3. Color histogram sampling misses significant colors

## Root Causes

### Issue 1: Neutral Scale — All Light Colors

In `harvester_v4.js`, function `extractNeutralScale()` (line 814-839):

```javascript
// Problem: Only considers colors that appear 2+ times AND pass isNeutral()
// On a light-themed admin dashboard, ALL neutral colors are light (lum > 200)
// Result: 50→900 all map to shades between #E7EFFD and #FFFFFF
```

**Fix**: Generate missing dark neutrals by deriving them from the lightest/darkest detected:
```javascript
function extractNeutralScale(histogram) {
    // ... existing detection ...
    
    // If all neutrals are in the same luminance range, generate a full scale
    if (neutrals.length > 0) {
        const lightest = neutrals[0].lum;
        const darkest = neutrals[neutrals.length - 1].lum;
        
        if (lightest - darkest < 100) {
            // Detected neutrals are all similar — generate synthetic scale
            // Use body text color as anchor for dark end
            const bodyColor = normalizeColor(gs(document.body).color);
            const headingColor = /* find darkest heading color */;
            
            // Build scale from white → detected neutrals → body text → dark
            return generateSyntheticNeutralScale(neutrals, bodyColor, headingColor);
        }
    }
}
```

### Issue 2: Semantic Colors Capture Background

In `extractSemanticColors()` (line 329-443):

```javascript
// Problem: For elements like <span class="badge-success">
// backgroundColor = #EAFBF2 (light tint)  ← this gets mapped as "base"
// color = #00B69B (strong green)           ← this is the actual semantic color
```

**Fix**: Prefer the stronger/more saturated color as "base":
```javascript
// Instead of:
colors[name] = {
    base: bg !== "#000000" ? bg : fg,  // ❌ Always picks bg first
    
// Use:
const bgSaturation = analyzeColorPsychology(bg)?.s || 0;
const fgSaturation = analyzeColorPsychology(fg)?.s || 0;
colors[name] = {
    base: fgSaturation > bgSaturation ? fg : bg,  // ✅ Pick more saturated
    tint: fgSaturation > bgSaturation ? bg : fg,   // New: background tint
```

### Issue 3: Text Color Mapping Inverted

Body text `#919AA3` is a muted gray — this should be `text-2` (secondary), not `text-0` (primary). Heading color `#475569` is darker — this should be `text-0`.

**Fix in `token_mapper.py`**:
```python
# Compare luminance to determine text hierarchy
text_primary = raw_text.get("primary")
text_secondary = raw_text.get("secondary")

if text_primary and text_secondary:
    lum_p = luminance(text_primary)
    lum_s = luminance(text_secondary)
    
    # Darker = more prominent = text-0
    if lum_p > lum_s:
        text_primary, text_secondary = text_secondary, text_primary
```

## Files to Modify

| File | Function | Issue |
|------|----------|-------|
| `scripts/harvester_v4.js` | `extractNeutralScale()` | Generate full 50→900 gradient |
| `scripts/harvester_v4.js` | `extractSemanticColors()` | Prefer saturated color as base |
| `scripts/token_mapper.py` | `_map_text_system()` | Fix text hierarchy ordering |
| `scripts/token_mapper.py` | `_map_v3_neutrals()` | Handle light-only neutral sets |
| `scripts/design_system_indexer.py` | `to_semi_tokens()` | Validate color mapping |

## Verification

```bash
# 1. Harvest 5 different admin templates
urls=(
  "https://templates.envytheme.com/fila/project-management.html"
  "https://demos.adminmart.com/premium/bootstrap/modernize-bootstrap/package/html/main/index.html"
  "https://themesbrand.com/velzon/html/default/dashboard-analytics.html"
  "https://demo.dashboardpack.com/architectui-html-free/"
  "https://demo.themeselection.com/materio-bootstrap-html-admin-template/html/vertical-menu-template/dashboards-crm.html"
)

for url in "${urls[@]}"; do
  python3 scripts/harvester_cli.py quick "$url" --framework semi
done

# 2. Manually inspect output/*/design-system.css for each:
# - Primary color matches visual (open URL in browser, compare)
# - Neutral scale has distinct 50→900 gradient
# - Text colors: text-0 is darkest, text-3 is lightest
# - Success is green, Warning is orange/yellow, Danger is red
```

## Acceptance Criteria

- [ ] Neutral scale 50→900 shows visually distinct gradient (50 = near-white, 900 = near-black)
- [ ] Semantic colors (success, warning, danger) use the strong/saturated variant as base
- [ ] Text hierarchy: text-0 is darkest (headings), text-3 is lightest (disabled/muted)
- [ ] Primary color matches the most prominent brand/action color on the page
- [ ] Works correctly on both light and dark themed sites

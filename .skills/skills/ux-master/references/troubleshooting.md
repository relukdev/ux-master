# UX Master Troubleshooting Guide

Common issues and fixes for each stage of the pipeline.

## Table of Contents

1. [Browser Harvesting Issues](#browser-harvesting-issues)
2. [Token Mapping Issues](#token-mapping-issues)
3. [Component Generation Issues](#component-generation-issues)
4. [Documentation Generation Issues](#documentation-generation-issues)
5. [Theme Package Issues](#theme-package-issues)

---

## Browser Harvesting Issues

### Playwright not installed

**Symptom**: `ModuleNotFoundError: No module named 'playwright'`

**Fix**:
```bash
pip install playwright --break-system-packages
python3 -m playwright install chromium
```

### Page requires authentication

**Symptom**: Harvest returns mostly default/placeholder tokens.

**Fix**: Use `--cookies` flag or pre-authenticate:
```bash
# Option 1: Pass cookies file
python3 scripts/harvester_browser.py --url "..." --cookies cookies.json

# Option 2: Use non-headless mode and log in manually
python3 scripts/harvester_browser.py --url "..." --no-headless
```

### SPA content not loaded

**Symptom**: Missing tokens because page content loads asynchronously.

**Fix**: Increase wait time:
```bash
python3 scripts/harvester_browser.py --url "..." --wait 5000
```

### Harvest JSON is empty or minimal

**Symptom**: `harvest-v4-raw.json` has very few tokens.

**Causes & fixes**:
- Page uses iframes → harvester can't penetrate cross-origin iframes
- Page is mostly images → no CSS to extract
- JavaScript errors prevented harvester from running → check browser console

---

## Token Mapping Issues

### Neutral scale all same shade

**Symptom**: `--semi-color-neutral-50` through `--semi-color-neutral-900` are all similar light colors (e.g., #E7EFFD to #FFFFFF).

**Cause**: Light-themed sites only have light neutral colors visible in computed styles.

**Fix**: Manually inspect and provide synthetic darkening:
```python
# In the harvest JSON, check visualAnalysis.colors.neutrals
# If all luminance values are > 200, the scale needs synthetic dark end

# Quick fix: manually set dark end based on text color
# text-0 color is usually a good anchor for neutral-800/900
```

Or post-process the tokens:
```bash
# After token_mapper.py runs, check output
grep "neutral" output/myproject/design-system.css

# If all values are light, manually replace:
# --semi-color-neutral-700: #374151;
# --semi-color-neutral-800: #1F2937;
# --semi-color-neutral-900: #111827;
```

### Semantic colors are background tint instead of strong color

**Symptom**: `--semi-color-success` is `#EAFBF2` (light green tint) instead of `#00B69B` (strong green).

**Cause**: Harvester picked the background of a success badge instead of its text/icon color.

**Fix**: Check the harvest JSON:
```json
"semantic": {
  "success": {
    "base": "#EAFBF2",  // ← This is wrong, it's the bg
    "fg": "#00B69B"      // ← This should be the base
  }
}
```

Swap them: the more saturated color should be `base`. You can fix this in the harvest JSON before running token_mapper, or fix the CSS output directly.

### Text hierarchy inverted

**Symptom**: `--semi-color-text-0` is lighter than `--semi-color-text-3`.

**Rule**: text-0 = darkest (headings), text-3 = lightest (disabled).

**Fix**: Compare luminance and swap:
```css
/* Before (wrong) */
--semi-color-text-0: #919AA3;  /* Light gray — this should be text-2 */
--semi-color-text-2: #475569;  /* Dark gray — this should be text-0 */

/* After (correct) */
--semi-color-text-0: #475569;  /* Darkest */
--semi-color-text-2: #919AA3;  /* Lighter */
```

### Primary color is wrong

**Symptom**: Primary is detected as the page background or a non-brand color.

**Cause**: Color histogram ranked a ubiquitous non-brand color higher.

**Fix**: Visually inspect the source site and override:
```bash
# In the harvest JSON, set:
# visualAnalysis.colors.semantic.primary.base = "#CORRECT_HEX"
# Then re-run token_mapper.py
```

---

## Component Generation Issues

### TypeScript compilation errors

**Symptom**: `npx tsc --noEmit` reports errors.

**Common errors and fixes**:

#### Wrong HTML tag casing
```tsx
// ❌ Error: Property 'BUTTON' does not exist
<BUTTON ref={ref}>
// ✅ Fix
<button ref={ref}>
```

#### Broken forwardRef destructuring
```tsx
// ❌ Error: Unexpected token
>((variant, size, ...props}, ref) => {
// ✅ Fix
>(({ variant, size, ...props }, ref) => {
```

#### Invalid className template
```tsx
// ❌ Error: Unterminated string literal
className={cn(
    "inline-flex items-center
    font-medium"

// ✅ Fix: All strings must be on one line or properly concatenated
className={cn(
    "inline-flex items-center font-medium",
)}
```

#### Wrong HTMLElement type
```tsx
// ❌ Error: Cannot find name 'HTMLBUTTONElement'
React.forwardRef<HTMLBUTTONElement, ...>
// ✅ Fix
React.forwardRef<HTMLButtonElement, ...>
```

### Missing cn() utility

**Symptom**: `Cannot find module '@/lib/utils'`

**Fix**: Create the utility file:
```typescript
// components/_shared/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Or a simple version without dependencies:
```typescript
export function cn(...args: any[]): string {
  return args
    .flat()
    .filter(Boolean)
    .map(arg => {
      if (typeof arg === 'string') return arg;
      if (typeof arg === 'object') {
        return Object.entries(arg)
          .filter(([, v]) => v)
          .map(([k]) => k)
          .join(' ');
      }
      return '';
    })
    .join(' ')
    .trim();
}
```

### Components don't render correctly

**Symptom**: Components display but with wrong styles.

**Fix**: Verify the CSS variables are loaded. The generated `design-system.css` must be imported in the app:
```tsx
// In your app entry point:
import './design-system.css';
```

---

## Documentation Generation Issues

### Color swatches show wrong values

**Symptom**: Color palette section displays border-radius or spacing values as colors.

**Cause**: Token categorization bug — non-color tokens mixed into color section.

**Fix**: The doc generator should filter tokens by prefix. Verify:
- Brand colors: `--semi-color-primary*`, `--semi-color-secondary*`, `--semi-color-tertiary*`
- Semantic: `--semi-color-success*`, `--semi-color-warning*`, `--semi-color-danger*`
- Not colors: `--semi-border-*`, `--semi-spacing-*`, `--semi-font-*`

### No component previews

**Symptom**: Doc page has token reference but no live component samples.

**Fix**: Ensure the doc generator has access to both the harvest JSON and the tokens. The component preview section uses inline HTML styled with the extracted tokens.

### Dark mode toggle broken

**Symptom**: Toggle exists but doesn't change anything.

**Fix**: The dark mode CSS must use `body[theme-mode="dark"]` selector, matching Semi Design convention.

---

## Theme Package Issues

### `npm pack` fails

**Symptom**: Error when trying to pack the theme.

**Fix**: Verify `package.json` has required fields:
- `name` must be lowercase, no spaces
- `version` must be valid semver
- `files` array must list existing directories

### Theme doesn't apply with Semi Design

**Symptom**: Importing the theme has no visual effect.

**Fix**:
1. Verify the SCSS file uses correct `$` variable names matching Semi's expectations
2. Ensure `index.js` exports the correct structure
3. Check that `semi-theme-default` isn't overriding your custom theme (load order matters)

### Figma tokens don't import

**Symptom**: Tokens Studio can't parse `figma-tokens.json`.

**Fix**: Verify the JSON structure matches Tokens Studio format:
```json
{
  "color": {
    "primary": {
      "value": "#0F79F3",
      "type": "color"
    }
  }
}
```

Each token needs both `value` and `type` fields.

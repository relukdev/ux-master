# UX Master Pipeline Guide

Complete command reference and architecture for the design system generation pipeline.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Full Pipeline Commands](#full-pipeline-commands)
3. [Browser Harvesting (URL Input)](#browser-harvesting)
4. [Source Code Extraction](#source-code-extraction)
5. [Token Mapping](#token-mapping)
6. [Design System Indexing](#design-system-indexing)
7. [Component Generation](#component-generation)
8. [Documentation Generation](#documentation-generation)
9. [Theme Package Generation](#theme-package-generation)
10. [Multi-Page Harvesting](#multi-page-harvesting)
11. [Merging Multiple Sources](#merging-multiple-sources)

---

## Quick Start

The fastest way to run the full pipeline on a URL:

```bash
cd <project-root>
python3 scripts/harvester_cli.py quick <URL> --framework semi
```

This runs: harvest → index → generate components → generate docs in one shot. Output goes to `output/<auto-detected-slug>/`.

For more control, run each step individually as described below.

---

## Full Pipeline Commands

### Step-by-step for URL input:

```bash
PROJECT="myproject"
URL="https://example.com"

# 1. Extract tokens from live page
python3 scripts/harvester_browser.py --url "$URL" --output ./output/$PROJECT

# 2. Map to Semi Design tokens
python3 scripts/token_mapper.py \
  -i output/$PROJECT/harvest-v4-raw.json \
  --project $PROJECT

# 3. Build design system index
python3 scripts/design_system_indexer.py \
  --input output/$PROJECT/harvest-v4-raw.json \
  --name "$PROJECT" \
  --output output/$PROJECT/

# 4. Generate React components
python3 scripts/component_generator.py \
  --input output/$PROJECT/design-system.json \
  --all \
  --output output/$PROJECT/components/

# 5. Generate documentation
python3 scripts/design_doc_generator.py \
  -i output/$PROJECT/harvest-v4-raw.json \
  -o output/$PROJECT/design-system.html

# 6. Validate TypeScript compilation
cd output/$PROJECT/components && npx tsc --noEmit 2>&1
```

### Step-by-step for source code input:

```bash
PROJECT="myproject"
SOURCE_DIR="/path/to/source"

# 1. Extract from source files
python3 scripts/extractor.py \
  --directory "$SOURCE_DIR" \
  --output ./output/$PROJECT

# 2-6: Same as URL pipeline above
```

---

## Browser Harvesting

### Prerequisites

Playwright must be installed:
```bash
pip install playwright --break-system-packages
python3 -m playwright install chromium
```

### Command

```bash
python3 scripts/harvester_browser.py \
  --url "https://example.com" \
  --output ./output/myproject \
  [--headless]           # Run without visible browser (default: true)
  [--wait 3000]          # Wait ms after page load before extracting
  [--viewport 1920x1080] # Browser viewport size
```

### What It Extracts

The harvester injects `harvester_v4.js` into the page, which runs a comprehensive DOM analysis:

- **Color Histogram**: Scans all computed styles, counts color frequency
- **Semantic Colors**: Detects primary (buttons, links), success/warning/danger (badges, alerts)
- **Neutral Scale**: Extracts background and text grays, generates 10-step gradient
- **Typography**: Font families from body/headings, font sizes, weights, line heights
- **Spacing**: Analyzes padding/margin patterns across elements
- **Geometry**: Border radii, box shadows
- **Layout**: Grid/flex patterns, container widths

### Output Format

`harvest-v4-raw.json`:
```json
{
  "_version": 4,
  "_timestamp": "2025-02-25T10:30:00Z",
  "_url": "https://example.com",
  "visualAnalysis": {
    "colors": {
      "histogram": [...],
      "semantic": {
        "primary": { "base": "#0F79F3", "confidence": 0.95 },
        "success": { "base": "#00B69B", "confidence": 0.85 },
        "warning": { "base": "#F59E0B", "confidence": 0.80 },
        "danger":  { "base": "#EF4444", "confidence": 0.90 }
      },
      "neutrals": { "50": "#FAFAFA", ..., "900": "#1C1F23" }
    },
    "typography": {
      "fontFamilies": ["Inter", "-apple-system", "sans-serif"],
      "headingFamily": ["Poppins", "sans-serif"],
      "sizes": { "body": "14px", "h1": "32px", ... },
      "weights": { "regular": 400, "semibold": 600, "bold": 700 }
    },
    "spacing": { "base": "16px", "scale": [0, 2, 4, 8, 12, 16, 20, 24, 32, 40] },
    "geometry": {
      "borderRadius": { "small": "3px", "medium": "6px", "large": "12px" },
      "shadows": { "sm": "...", "md": "...", "lg": "..." }
    }
  }
}
```

---

## Source Code Extraction

### Command

```bash
python3 scripts/extractor.py \
  --directory /path/to/project \
  --output ./output/myproject
```

### What It Parses

| Source File | What's Extracted |
|---|---|
| `tailwind.config.js/ts` | colors, spacing, borderRadius, fontFamily, screens |
| `*.css` | CSS custom properties (`--var: value`) |
| `*.scss` / `*.sass` | SCSS variables (`$var: value`) |
| `*.tsx` / `*.jsx` | Component names, variant/size props, style patterns |
| `tokens.json` | Design token standard format |
| `package.json` | Stack detection (Tailwind? Semi? MUI?) |

---

## Token Mapping

### Command

```bash
python3 scripts/token_mapper.py \
  -i output/myproject/harvest-v4-raw.json \
  --project myproject
```

### What It Does

Maps raw harvest data to the full Semi Design token specification (~200 CSS variables). Key mappings:

- Histogram primary color → `--semi-color-primary` + 6 derived states
- Body font → `--semi-font-family-regular`
- Heading sizes → `--semi-font-size-header-1` through `--semi-font-size-header-6`
- Border radius medium → `--semi-border-radius-medium`
- Neutral scale → `--semi-color-bg-0` through `--semi-color-bg-4`

### Output

- `design-system.css` — CSS file with all `--semi-*` custom properties
- `tokens.json` — Machine-readable token dictionary

---

## Design System Indexing

### Command

```bash
python3 scripts/design_system_indexer.py \
  --input output/myproject/harvest-v4-raw.json \
  --name "MyProject" \
  --output output/myproject/
```

### What It Does

Structures raw tokens into a comprehensive design system JSON following Semi Design architecture. Includes:

- Color system with brand, semantic, neutral, surface, text, fill categories
- Typography system with scale, families, weights
- Spacing system with named scale (tight → super-loose)
- Component architecture specs
- Dark mode token overrides

### Output

`design-system.json` — Full design system specification used by the component generator.

---

## Component Generation

### Command

```bash
python3 scripts/component_generator.py \
  --input output/myproject/design-system.json \
  --all \
  --output output/myproject/components/ \
  [--framework react]  # react (default), semi, vue
  [--component button] # Generate single component
```

### Output Structure

```
components/
├── _shared/
│   ├── utils.ts       # cn() utility
│   └── types.ts       # Shared types
├── button/
│   ├── Button.tsx      # Component code
│   └── index.ts        # Re-export
├── input/
├── card/
├── ... (22 components)
└── index.ts            # Barrel export
```

### Validation

Always validate after generation:
```bash
# Add tsconfig if not present
cat > output/myproject/components/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "paths": { "@/*": ["./*"] }
  },
  "include": ["**/*.tsx", "**/*.ts"]
}
EOF

# Check compilation
cd output/myproject/components && npx tsc --noEmit
```

---

## Documentation Generation

### Command

```bash
python3 scripts/design_doc_generator.py \
  -i output/myproject/harvest-v4-raw.json \
  -o output/myproject/design-system.html
```

### Features

The generated HTML page includes:
- **Color Palette**: Swatches for brand, semantic, neutral, surface colors
- **Typography**: Rendered specimens with actual fonts
- **Component Preview**: Live-styled buttons, cards, inputs using extracted tokens
- **Token Reference**: Full table with CSS variable names and values
- **Copy-to-Clipboard**: Click any token value to copy
- **Dark/Light Toggle**: Switch between themes
- **Responsive**: Works on mobile and desktop

---

## Theme Package Generation

After all tokens are mapped, generate an npm-publishable package:

### package.json template:
```json
{
  "name": "semi-theme-{{projectSlug}}",
  "version": "1.0.0",
  "description": "Semi Design theme extracted from {{projectName}} by UX Master",
  "main": "index.js",
  "files": ["scss/", "css/", "tokens/"],
  "peerDependencies": {
    "@douyinfe/semi-ui": ">=2.0.0"
  },
  "keywords": ["semi-design", "theme", "design-system", "ux-master"],
  "author": "Generated by UX Master Harvester v4"
}
```

### global.scss template:
```scss
// Semi Design Theme Override — Generated by UX Master
// Source: {{sourceUrl}}
// Generated: {{timestamp}}

// === Brand Colors ===
$color-primary: {{primaryColor}};
$color-secondary: {{secondaryColor}};
$color-tertiary: {{tertiaryColor}};

// === Semantic Colors ===
$color-success: {{successColor}};
$color-warning: {{warningColor}};
$color-danger: {{dangerColor}};
$color-info: {{infoColor}};

// === Typography ===
$font-family-regular: {{fontFamily}};

// === Spacing ===
$spacing-base: {{spacingBase}};

// === Border Radius ===
$border-radius-medium: {{borderRadiusMedium}};

// Generate CSS custom properties
:root {
  --semi-color-primary: #{$color-primary};
  // ... all tokens
}
```

### index.js template:
```javascript
module.exports = {
  name: '{{projectSlug}}',
  import: './scss/global.scss',
  tokens: require('./tokens/style-dictionary.json'),
};
```

### Figma Tokens format:
```json
{
  "color": {
    "primary": { "value": "{{primaryColor}}", "type": "color" },
    "secondary": { "value": "{{secondaryColor}}", "type": "color" }
  },
  "fontFamily": {
    "regular": { "value": "{{fontFamily}}", "type": "fontFamilies" }
  }
}
```

---

## Multi-Page Harvesting

For better accuracy, harvest multiple pages and merge:

```bash
# Harvest multiple pages
python3 scripts/harvester_cli.py extract \
  --url "https://example.com" \
  --crawl \
  --max-pages 5 \
  --generate
```

Or manually:
```bash
python3 scripts/harvest_session.py \
  --urls "https://example.com" "https://example.com/about" "https://example.com/products" \
  --output output/myproject/
```

Multi-page harvesting increases confidence scores and catches tokens that only appear on specific pages.

---

## Merging Multiple Sources

Combine browser harvest with source code extraction:

```bash
# Browser harvest
python3 scripts/harvester_browser.py --url "https://example.com" --output ./output/myproject

# Source code extraction
python3 scripts/extractor.py --directory ./src --output ./output/myproject-source

# Merge (source code values override browser values when both exist)
python3 scripts/design_system_indexer.py \
  --multi output/myproject/harvest-v4-raw.json output/myproject-source/harvest.json \
  --merge \
  --name "MyProject" \
  --output output/myproject/
```

Source code tokens have higher confidence (exact values from config files) than browser-extracted tokens (computed/approximated).

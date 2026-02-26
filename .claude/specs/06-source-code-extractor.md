# Spec 06: Source Code Extractor

## Goal

Extract design tokens directly from source code (React, Vue, Tailwind, SCSS, CSS variables) — complementing the browser-based harvester.

## Input → Output

```
Input (any of):
├── tailwind.config.js    → colors, spacing, breakpoints, borderRadius, fonts
├── globals.css / *.css   → CSS custom properties (--var: value)
├── _variables.scss       → $variable: value
├── tokens.json           → Design token standard format
├── src/components/*.tsx   → Component patterns, props, style usage
└── package.json          → Dependency detection (Tailwind? Semi? MUI?)

Output:
├── harvest-source.json   → Same format as harvester_v4.js output
└── (mergeable with browser harvest for higher confidence)
```

## Implementation

### Module: `scripts/source_extractor.py`

```python
class SourceExtractor:
    """Extract design tokens from source code files."""
    
    def __init__(self, directory: Path):
        self.directory = directory
        self.tokens = {}
        self.components = []
    
    def extract(self) -> dict:
        """Run all extractors and return unified harvest format."""
        self._detect_stack()
        self._extract_css_variables()
        self._extract_tailwind_config()
        self._extract_scss_variables()
        self._extract_component_patterns()
        return self._to_harvest_format()
```

### Tailwind Config Parser

```python
def _extract_tailwind_config(self):
    """Parse tailwind.config.js/ts for design tokens."""
    config_paths = [
        "tailwind.config.js", "tailwind.config.ts",
        "tailwind.config.cjs", "tailwind.config.mjs"
    ]
    
    for path in config_paths:
        full = self.directory / path
        if full.exists():
            content = full.read_text()
            self.tokens["tailwind"] = {
                "colors": self._parse_tw_colors(content),
                "spacing": self._parse_tw_spacing(content),
                "borderRadius": self._parse_tw_radius(content),
                "fontFamily": self._parse_tw_fonts(content),
                "screens": self._parse_tw_screens(content),
            }
            break

def _parse_tw_colors(self, content):
    """Extract color definitions from Tailwind config."""
    # Match patterns like: colors: { primary: '#0F79F3', ... }
    # Also handle: colors: { primary: { DEFAULT: '#0F79F3', dark: '#0C60C2' } }
    # Use regex or simple JS eval for object extraction
```

### CSS Variable Parser

```python
def _extract_css_variables(self):
    """Parse :root { --var: value } from CSS files."""
    css_files = list(self.directory.rglob("*.css"))
    
    for css_file in css_files:
        content = css_file.read_text()
        # Match: --variable-name: value;
        pattern = r'--([a-zA-Z0-9-]+)\s*:\s*([^;]+);'
        for match in re.finditer(pattern, content):
            name = f"--{match.group(1)}"
            value = match.group(2).strip()
            self.tokens.setdefault("css_vars", {})[name] = value
```

### SCSS Variable Parser

```python
def _extract_scss_variables(self):
    """Parse $variable: value; from SCSS files."""
    scss_files = list(self.directory.rglob("*.scss")) + list(self.directory.rglob("*.sass"))
    
    for scss_file in scss_files:
        content = scss_file.read_text()
        pattern = r'\$([a-zA-Z0-9-_]+)\s*:\s*([^;]+);'
        for match in re.finditer(pattern, content):
            name = match.group(1)
            value = match.group(2).strip()
            self.tokens.setdefault("scss_vars", {})[name] = value
```

### Component Pattern Detector

```python
def _extract_component_patterns(self):
    """Detect React/Vue component patterns from JSX/TSX files."""
    tsx_files = list(self.directory.rglob("*.tsx")) + list(self.directory.rglob("*.jsx"))
    
    for file in tsx_files[:50]:  # Limit for performance
        content = file.read_text()
        
        # Detect component names
        # export const Button = ...
        # export default function Card() ...
        comp_pattern = r'export\s+(?:default\s+)?(?:const|function)\s+(\w+)'
        for match in re.finditer(comp_pattern, content):
            self.components.append({
                "name": match.group(1),
                "file": str(file.relative_to(self.directory)),
                "has_variants": "variant" in content.lower(),
                "has_sizes": "size" in content.lower(),
                "uses_tailwind": "className" in content and ("bg-" in content or "text-" in content),
                "uses_css_modules": ".module.css" in content or ".module.scss" in content,
            })
```

### Merge with Browser Harvest

```python
def merge_harvests(browser_harvest: dict, source_harvest: dict) -> dict:
    """Merge browser + source code extractions for higher accuracy."""
    merged = browser_harvest.copy()
    
    # Source code tokens have higher confidence for exact values
    if "tailwind" in source_harvest:
        tw = source_harvest["tailwind"]
        if tw.get("colors", {}).get("primary"):
            merged["visualAnalysis"]["colors"]["semantic"]["primary"]["base"] = tw["colors"]["primary"]
            merged["visualAnalysis"]["colors"]["semantic"]["primary"]["confidence"] = 0.99
    
    # CSS variables are definitive
    if "css_vars" in source_harvest:
        merged["sourceTokens"] = source_harvest["css_vars"]
    
    return merged
```

## CLI

```bash
# Extract from source directory
python3 scripts/source_extractor.py --directory ./src -o output/source-harvest.json

# Merge with browser harvest
python3 scripts/source_extractor.py \
  --directory ./src \
  --merge output/browser-harvest.json \
  -o output/merged-harvest.json
```

## Acceptance Criteria

- [ ] Parses `tailwind.config.js` colors, spacing, fonts, screens
- [ ] Parses CSS custom properties from any `.css` file
- [ ] Parses SCSS variables from `.scss` files
- [ ] Detects React component patterns and variant names
- [ ] Output matches harvest JSON format (mergeable with browser harvest)
- [ ] Works on at least 3 real open-source projects

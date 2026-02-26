# Spec 07: Semi Design Doc Site

## Goal

Generate a multi-page interactive documentation site for the extracted design system, matching the quality of [semi.design](https://semi.design/en-US).

## Target Output

```
output/{project}/site/
├── index.html              # Landing page with overview
├── tokens/
│   ├── colors.html         # Color system with swatches
│   ├── typography.html     # Font specimens
│   ├── spacing.html        # Spacing scale visualization
│   └── shadows.html        # Shadow & elevation
├── components/
│   ├── button.html         # Button with live preview + API table
│   ├── card.html
│   ├── input.html
│   └── ...                 # One page per component
├── theme/
│   └── editor.html         # Live token editor
├── assets/
│   ├── style.css           # Site styles
│   ├── app.js              # Interactivity (theme switching, search, copy)
│   └── sandpack.js         # Live code editor
└── design-system.css       # The extracted tokens CSS
```

## Page Template Structure

Each page:
1. **Sidebar navigation** — all pages listed, current highlighted
2. **Header** — project name, search, theme toggle
3. **Content area** — page-specific content
4. **TOC sidebar** — table of contents for current page

## Key Features

### Live Code Editor (Sandpack-like)

Use inline `<iframe>` or `contenteditable` + eval to render component previews:

```html
<div class="live-editor">
  <div class="code-panel">
    <textarea id="code-editor">&lt;Button variant="primary"&gt;Click me&lt;/Button&gt;</textarea>
  </div>
  <div class="preview-panel" id="preview">
    <!-- Rendered preview here -->
  </div>
</div>
```

### Props API Table (Auto-generated)

From component `spec.json`:
```html
<table class="api-table">
  <thead><tr><th>Prop</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
  <tbody>
    <tr><td>variant</td><td>"primary" | "secondary" | "outline"</td><td>"primary"</td><td>Visual style</td></tr>
    <tr><td>size</td><td>"sm" | "md" | "lg"</td><td>"md"</td><td>Component size</td></tr>
  </tbody>
</table>
```

### Token Copy-to-Clipboard

```javascript
document.querySelectorAll('.token-value').forEach(el => {
  el.addEventListener('click', () => {
    navigator.clipboard.writeText(el.textContent);
    el.classList.add('copied');
    setTimeout(() => el.classList.remove('copied'), 1500);
  });
});
```

### Theme Editor

Interactive UI to modify CSS variables in real-time:
```javascript
function updateToken(varName, value) {
  document.documentElement.style.setProperty(varName, value);
  // Update preview components
  document.querySelectorAll('.preview-panel').forEach(p => p.style.setProperty(varName, value));
}
```

## Implementation

### Generator: `scripts/doc_site_generator.py`

```python
class DocSiteGenerator:
    def __init__(self, tokens, harvest, components, project_name):
        self.tokens = tokens
        self.harvest = harvest
        self.components = components
        self.project_name = project_name
    
    def generate(self, output_dir: Path):
        self._generate_index(output_dir)
        self._generate_token_pages(output_dir / "tokens")
        self._generate_component_pages(output_dir / "components")
        self._generate_theme_editor(output_dir / "theme")
        self._copy_assets(output_dir / "assets")
        self._generate_design_system_css(output_dir)
```

## Acceptance Criteria

- [ ] Multi-page site with sidebar navigation
- [ ] Color page shows 10-shade swatches for each color group
- [ ] Typography page shows rendered text specimens
- [ ] Component pages show live preview + props API table
- [ ] Token values have click-to-copy
- [ ] Theme editor changes propagate to all previews
- [ ] Search across tokens and components
- [ ] Dark/light mode toggle
- [ ] Mobile responsive
- [ ] No external dependencies (single-file CSS + JS)

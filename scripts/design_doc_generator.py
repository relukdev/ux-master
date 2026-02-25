#!/usr/bin/env python3
"""
Design System Documentation Generator — Single-file HTML output.

Generates a beautiful, self-contained HTML page documenting a harvested
design system with interactive color swatches, typography specimens,
geometry previews, component samples, and token reference table.

Usage:
    from design_doc_generator import generate_doc_html
    html = generate_doc_html(tokens, harvest, meta)
    
    # Or via CLI:
    python3 design_doc_generator.py --project haravan
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone


def generate_doc_html(tokens: dict, harvest: dict = None, meta: dict = None, confidence: dict = None) -> str:
    """Generate a single-file HTML design system documentation page.
    
    Args:
        tokens: Semi Design CSS variable tokens dict
        harvest: Raw harvest data (for additional context)
        meta: Project metadata (name, url, etc.)
        confidence: Optional confidence scores from multi-page scan
    """
    meta = meta or {}
    harvest = harvest or {}
    project_name = meta.get("name", meta.get("title", "Design System"))
    source_url = meta.get("url", "")
    timestamp = meta.get("updated_at", meta.get("timestamp", datetime.now(timezone.utc).isoformat()))
    page_count = meta.get("page_count", meta.get("harvest_count", 1))

    # Categorize tokens
    brand_colors = {}
    semantic_colors = {}
    surface_colors = {}
    text_colors = {}
    typography_tokens = {}
    geometry_tokens = {}
    shadow_tokens = {}

    for var, val in sorted(tokens.items()):
        if "primary" in var:
            brand_colors[var] = val
        elif any(s in var for s in ("success", "warning", "danger")):
            semantic_colors[var] = val
        elif "bg-" in var or "border" in var:
            surface_colors[var] = val
        elif "text-" in var:
            text_colors[var] = val
        elif "font-" in var:
            typography_tokens[var] = val
        elif "shadow" in var:
            shadow_tokens[var] = val
        elif "radius" in var:
            geometry_tokens[var] = val
        else:
            geometry_tokens[var] = val

    # Build HTML sections
    color_swatches_html = _build_color_section("Brand Colors", brand_colors)
    color_swatches_html += _build_color_section("Semantic Colors", semantic_colors)
    color_swatches_html += _build_color_section("Surface Colors", surface_colors)
    color_swatches_html += _build_color_section("Text Colors", text_colors)

    typography_html = _build_typography_section(typography_tokens, harvest)
    geometry_html = _build_geometry_section(geometry_tokens, shadow_tokens)
    components_html = _build_components_section(tokens)
    token_table_html = _build_token_table(tokens, confidence)
    usage_html = _build_usage_section(project_name)

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_esc(project_name)} — Design System</title>
    <style>
{_get_css(tokens)}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <div class="header-left">
                <h1 class="header-title">{_esc(project_name)}</h1>
                <span class="header-badge">Design System</span>
            </div>
            <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">
                <span class="toggle-icon" id="themeIcon">☀️</span>
            </button>
        </div>
    </header>

    <main class="main">
        <!-- Section 1: Introduction -->
        <section class="section" id="introduction">
            <h2 class="section-title">Introduction</h2>
            <div class="intro-grid">
                <div class="intro-card">
                    <div class="intro-label">Project</div>
                    <div class="intro-value">{_esc(project_name)}</div>
                </div>
                <div class="intro-card">
                    <div class="intro-label">Source</div>
                    <div class="intro-value"><a href="{_esc(source_url)}" target="_blank" rel="noopener">{_esc(source_url or 'N/A')}</a></div>
                </div>
                <div class="intro-card">
                    <div class="intro-label">Pages Scanned</div>
                    <div class="intro-value">{page_count}</div>
                </div>
                <div class="intro-card">
                    <div class="intro-label">Tokens Extracted</div>
                    <div class="intro-value">{len(tokens)}</div>
                </div>
                <div class="intro-card">
                    <div class="intro-label">Last Updated</div>
                    <div class="intro-value">{_esc(timestamp[:10] if timestamp else 'N/A')}</div>
                </div>
            </div>
        </section>

        <!-- Section 2: Color Palette -->
        <section class="section" id="colors">
            <h2 class="section-title">🎨 Color Palette</h2>
            {color_swatches_html}
        </section>

        <!-- Section 3: Typography -->
        <section class="section" id="typography">
            <h2 class="section-title">🔤 Typography</h2>
            {typography_html}
        </section>

        <!-- Section 4: Geometry -->
        <section class="section" id="geometry">
            <h2 class="section-title">📐 Geometry</h2>
            {geometry_html}
        </section>

        <!-- Section 5: Components Preview -->
        <section class="section" id="components">
            <h2 class="section-title">🧱 Components Preview</h2>
            {components_html}
        </section>

        <!-- Section 6: Token Reference -->
        <section class="section" id="tokens">
            <h2 class="section-title">📋 Token Reference</h2>
            {token_table_html}
        </section>

        <!-- Section 7: Usage -->
        <section class="section" id="usage">
            <h2 class="section-title">⚙️ Usage</h2>
            {usage_html}
        </section>
    </main>

    <footer class="footer">
        <p>Generated by <strong>UX Master — Semi-Sync Harvester</strong></p>
    </footer>

    <div class="toast" id="toast">Copied!</div>

    <script>
{_get_js()}
    </script>
</body>
</html>"""

    return html


def _esc(s: str) -> str:
    """HTML-escape a string."""
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _build_color_section(title: str, colors: dict) -> str:
    """Build HTML for a color group."""
    if not colors:
        return ""
    
    swatches = []
    for var, val in colors.items():
        label = var.replace("--semi-color-", "").replace("-", " ").title()
        swatches.append(f"""
            <div class="swatch" onclick="copyColor('{_esc(val)}')">
                <div class="swatch-color" style="background: {_esc(val)}"></div>
                <div class="swatch-info">
                    <div class="swatch-name">{_esc(label)}</div>
                    <code class="swatch-value">{_esc(val)}</code>
                </div>
            </div>""")

    return f"""
        <h3 class="subsection-title">{_esc(title)}</h3>
        <div class="swatch-grid">{"".join(swatches)}
        </div>"""


def _build_typography_section(typo_tokens: dict, harvest: dict) -> str:
    """Build typography specimen section."""
    font_family = ""
    font_size = ""
    for var, val in typo_tokens.items():
        if "family" in var:
            font_family = val
        elif "size" in var:
            font_size = val

    # Also check harvest for additional typography info
    typo_harvest = harvest.get("typography", {})
    if not font_family:
        font_family = typo_harvest.get("font_family", "system-ui, sans-serif")
    if not font_size:
        font_size = typo_harvest.get("body_size", "14px")

    return f"""
        <div class="type-specimens">
            <div class="type-specimen">
                <div class="type-label">Font Family</div>
                <div class="type-sample" style="font-family: {_esc(font_family)}">{_esc(font_family.split(',')[0].strip())}</div>
                <code>{_esc(font_family)}</code>
            </div>
            <div class="type-specimen">
                <div class="type-label">Heading</div>
                <div class="type-heading-sample" style="font-family: {_esc(font_family)}">The quick brown fox jumps over the lazy dog</div>
            </div>
            <div class="type-specimen">
                <div class="type-label">Body ({_esc(font_size)})</div>
                <div class="type-body-sample" style="font-family: {_esc(font_family)}; font-size: {_esc(font_size)}">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
                </div>
            </div>
            <div class="type-specimen">
                <div class="type-label">Muted</div>
                <div class="type-muted-sample" style="font-family: {_esc(font_family)}; font-size: {_esc(font_size)}">
                    Secondary text, captions, and supplementary information.
                </div>
            </div>
        </div>"""


def _build_geometry_section(geometry_tokens: dict, shadow_tokens: dict) -> str:
    """Build geometry preview section."""
    items = []
    
    for var, val in geometry_tokens.items():
        label = var.replace("--semi-", "").replace("-", " ").title()
        items.append(f"""
            <div class="geo-item">
                <div class="geo-preview" style="border-radius: {_esc(val)}"></div>
                <div class="geo-info">
                    <div class="geo-label">{_esc(label)}</div>
                    <code>{_esc(val)}</code>
                </div>
            </div>""")

    for var, val in shadow_tokens.items():
        label = var.replace("--semi-", "").replace("-", " ").title()
        items.append(f"""
            <div class="geo-item">
                <div class="geo-preview geo-shadow" style="box-shadow: {_esc(val)}"></div>
                <div class="geo-info">
                    <div class="geo-label">{_esc(label)}</div>
                    <code>{_esc(val)}</code>
                </div>
            </div>""")

    return f"""
        <div class="geo-grid">{"".join(items)}
        </div>"""


def _build_components_section(tokens: dict) -> str:
    """Build component preview section using CSS variables."""
    primary = tokens.get("--semi-color-primary", "#2463EB")
    primary_hover = tokens.get("--semi-color-primary-hover", primary)
    bg = tokens.get("--semi-color-bg-1", "#FFFFFF")
    border = tokens.get("--semi-color-border", "#E5E7EB")
    text0 = tokens.get("--semi-color-text-0", "#111827")
    text1 = tokens.get("--semi-color-text-1", "#4B5563")
    radius = tokens.get("--semi-border-radius-medium", "8px")
    card_radius = tokens.get("--semi-border-radius-large", "16px")
    shadow = tokens.get("--semi-shadow-elevated", "0 1px 3px rgba(0,0,0,0.1)")
    success = tokens.get("--semi-color-success", "#10B981")
    danger = tokens.get("--semi-color-danger", "#EF4444")
    warning = tokens.get("--semi-color-warning", "#F59E0B")

    return f"""
        <div class="component-grid">
            <!-- Buttons -->
            <div class="component-card">
                <h4>Buttons</h4>
                <div class="component-row">
                    <button class="comp-btn comp-btn-primary" style="background:{primary}; border-radius:{radius}; color:#fff">Primary</button>
                    <button class="comp-btn comp-btn-outline" style="border: 1px solid {border}; border-radius:{radius}; color:{text0}; background:transparent">Secondary</button>
                    <button class="comp-btn comp-btn-danger" style="background:{danger}; border-radius:{radius}; color:#fff">Danger</button>
                </div>
            </div>

            <!-- Card -->
            <div class="component-card">
                <h4>Card</h4>
                <div class="comp-card-preview" style="background:{bg}; border-radius:{card_radius}; box-shadow:{shadow}; border:1px solid {border}">
                    <div class="comp-card-title" style="color:{text0}">Card Title</div>
                    <div class="comp-card-body" style="color:{text1}">Card content with the extracted design tokens applied.</div>
                </div>
            </div>

            <!-- Input -->
            <div class="component-card">
                <h4>Input</h4>
                <input type="text" class="comp-input" placeholder="Enter text..." style="border: 1px solid {border}; border-radius:{radius}; color:{text0}">
            </div>

            <!-- Tags -->
            <div class="component-card">
                <h4>Tags</h4>
                <div class="component-row">
                    <span class="comp-tag" style="background:{primary}20; color:{primary}; border-radius:{radius}">Primary</span>
                    <span class="comp-tag" style="background:{success}20; color:{success}; border-radius:{radius}">Success</span>
                    <span class="comp-tag" style="background:{warning}20; color:{warning}; border-radius:{radius}">Warning</span>
                    <span class="comp-tag" style="background:{danger}20; color:{danger}; border-radius:{radius}">Danger</span>
                </div>
            </div>
        </div>"""


def _build_token_table(tokens: dict, confidence: dict = None) -> str:
    """Build full token reference table."""
    rows = []
    for var, val in sorted(tokens.items()):
        # Determine category
        if "color" in var or "bg-" in var or "text-" in var or "border" in var:
            cat = "Color"
            preview = f'<span class="token-color-preview" style="background:{_esc(val)}"></span>'
        elif "radius" in var:
            cat = "Geometry"
            preview = ""
        elif "shadow" in var:
            cat = "Shadow"
            preview = ""
        elif "font" in var:
            cat = "Typography"
            preview = ""
        else:
            cat = "Other"
            preview = ""

        rows.append(f"""
                <tr>
                    <td><code>{_esc(var)}</code></td>
                    <td>{preview} {_esc(val)}</td>
                    <td>{cat}</td>
                </tr>""")

    return f"""
        <div class="table-wrapper">
            <table class="token-table">
                <thead>
                    <tr>
                        <th>Variable</th>
                        <th>Value</th>
                        <th>Category</th>
                    </tr>
                </thead>
                <tbody>{"".join(rows)}
                </tbody>
            </table>
        </div>"""


def _build_usage_section(project_name: str) -> str:
    """Build usage/install instructions section."""
    slug = project_name.lower().replace(" ", "-")
    return f"""
        <div class="usage-blocks">
            <div class="usage-block">
                <h4>1. CSS Import</h4>
                <pre><code>/* Import the theme override in your main CSS/entry */
@import './semi-theme-override.css';

/* Or in HTML */
&lt;link rel="stylesheet" href="semi-theme-override.css"&gt;</code></pre>
            </div>
            <div class="usage-block">
                <h4>2. React Setup (Semi Design)</h4>
                <pre><code>// Install Semi UI
npm install @douyinfe/semi-ui

// Import theme override AFTER Semi default styles
import '@douyinfe/semi-ui/dist/css/semi.min.css';
import './semi-theme-override.css';</code></pre>
            </div>
            <div class="usage-block">
                <h4>3. Figma Tokens</h4>
                <pre><code>// Import figma-tokens.json into Tokens Studio plugin
// File → Import → Select figma-tokens.json
// Apply {_esc(project_name)} theme set</code></pre>
            </div>
        </div>"""


def _get_css(tokens: dict) -> str:
    """Generate the embedded CSS for the doc page."""
    primary = tokens.get("--semi-color-primary", "#2463EB")
    
    return f"""
        :root {{
            --doc-primary: {primary};
            --doc-bg: #FAFBFC;
            --doc-surface: #FFFFFF;
            --doc-text: #111827;
            --doc-text-secondary: #6B7280;
            --doc-border: #E5E7EB;
            --doc-code-bg: #F3F4F6;
            --doc-radius: 12px;
            --doc-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}

        [data-theme="dark"] {{
            --doc-bg: #0F172A;
            --doc-surface: #1E293B;
            --doc-text: #F1F5F9;
            --doc-text-secondary: #94A3B8;
            --doc-border: #334155;
            --doc-code-bg: #1E293B;
            --doc-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, system-ui, 'Segoe UI', Roboto, 'Inter', sans-serif;
            background: var(--doc-bg);
            color: var(--doc-text);
            line-height: 1.6;
            transition: background 0.3s, color 0.3s;
        }}

        .header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: var(--doc-surface);
            border-bottom: 1px solid var(--doc-border);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }}

        .header-inner {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .header-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .header-title {{
            font-size: 20px;
            font-weight: 700;
        }}

        .header-badge {{
            background: var(--doc-primary);
            color: #fff;
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 100px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .theme-toggle {{
            background: var(--doc-code-bg);
            border: 1px solid var(--doc-border);
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.2s;
        }}

        .theme-toggle:hover {{
            border-color: var(--doc-primary);
        }}

        .main {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 32px 24px;
        }}

        .section {{
            margin-bottom: 48px;
        }}

        .section-title {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--doc-border);
        }}

        .subsection-title {{
            font-size: 16px;
            font-weight: 600;
            margin: 16px 0 12px;
            color: var(--doc-text-secondary);
        }}

        /* Intro Grid */
        .intro-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
        }}

        .intro-card {{
            background: var(--doc-surface);
            border: 1px solid var(--doc-border);
            border-radius: var(--doc-radius);
            padding: 16px;
            box-shadow: var(--doc-shadow);
        }}

        .intro-label {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--doc-text-secondary);
            margin-bottom: 4px;
        }}

        .intro-value {{
            font-size: 15px;
            font-weight: 500;
            word-break: break-all;
        }}

        .intro-value a {{
            color: var(--doc-primary);
            text-decoration: none;
        }}

        /* Color Swatches */
        .swatch-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 12px;
        }}

        .swatch {{
            background: var(--doc-surface);
            border: 1px solid var(--doc-border);
            border-radius: var(--doc-radius);
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.15s, box-shadow 0.15s;
        }}

        .swatch:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        .swatch-color {{
            height: 72px;
            width: 100%;
        }}

        .swatch-info {{
            padding: 10px 12px;
        }}

        .swatch-name {{
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 2px;
        }}

        .swatch-value {{
            font-size: 11px;
            color: var(--doc-text-secondary);
        }}

        /* Typography */
        .type-specimens {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .type-specimen {{
            background: var(--doc-surface);
            border: 1px solid var(--doc-border);
            border-radius: var(--doc-radius);
            padding: 20px;
        }}

        .type-label {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--doc-text-secondary);
            margin-bottom: 8px;
        }}

        .type-sample {{
            font-size: 32px;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .type-heading-sample {{
            font-size: 28px;
            font-weight: 700;
        }}

        .type-body-sample {{
            line-height: 1.6;
        }}

        .type-muted-sample {{
            color: var(--doc-text-secondary);
            line-height: 1.6;
        }}

        /* Geometry */
        .geo-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 12px;
        }}

        .geo-item {{
            background: var(--doc-surface);
            border: 1px solid var(--doc-border);
            border-radius: var(--doc-radius);
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .geo-preview {{
            width: 48px;
            height: 48px;
            background: var(--doc-primary);
            flex-shrink: 0;
        }}

        .geo-shadow {{
            background: var(--doc-surface);
            border-radius: 8px;
        }}

        .geo-label {{
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 2px;
        }}

        .geo-info code {{
            font-size: 11px;
            color: var(--doc-text-secondary);
        }}

        /* Components */
        .component-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 16px;
        }}

        .component-card {{
            background: var(--doc-surface);
            border: 1px solid var(--doc-border);
            border-radius: var(--doc-radius);
            padding: 20px;
        }}

        .component-card h4 {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--doc-text-secondary);
        }}

        .component-row {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .comp-btn {{
            padding: 8px 16px;
            border: none;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: opacity 0.2s;
        }}

        .comp-btn:hover {{ opacity: 0.9; }}

        .comp-card-preview {{
            padding: 16px;
        }}

        .comp-card-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .comp-card-body {{
            font-size: 14px;
            line-height: 1.5;
        }}

        .comp-input {{
            width: 100%;
            padding: 10px 12px;
            font-size: 14px;
            background: var(--doc-bg);
            outline: none;
            transition: border-color 0.2s;
        }}

        .comp-input:focus {{
            border-color: var(--doc-primary) !important;
        }}

        .comp-tag {{
            display: inline-block;
            padding: 4px 10px;
            font-size: 12px;
            font-weight: 500;
        }}

        /* Token Table */
        .table-wrapper {{
            overflow-x: auto;
            border: 1px solid var(--doc-border);
            border-radius: var(--doc-radius);
        }}

        .token-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .token-table th {{
            background: var(--doc-code-bg);
            padding: 10px 16px;
            text-align: left;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--doc-border);
        }}

        .token-table td {{
            padding: 8px 16px;
            border-bottom: 1px solid var(--doc-border);
            vertical-align: middle;
        }}

        .token-table tr:last-child td {{
            border-bottom: none;
        }}

        .token-table tr:hover {{
            background: var(--doc-code-bg);
        }}

        .token-color-preview {{
            display: inline-block;
            width: 16px;
            height: 16px;
            border-radius: 4px;
            vertical-align: middle;
            margin-right: 8px;
            border: 1px solid var(--doc-border);
        }}

        /* Usage */
        .usage-blocks {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .usage-block {{
            background: var(--doc-surface);
            border: 1px solid var(--doc-border);
            border-radius: var(--doc-radius);
            padding: 20px;
        }}

        .usage-block h4 {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
        }}

        .usage-block pre {{
            background: var(--doc-code-bg);
            border-radius: 8px;
            padding: 16px;
            overflow-x: auto;
            font-size: 13px;
            line-height: 1.5;
        }}

        code {{
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 24px;
            font-size: 13px;
            color: var(--doc-text-secondary);
            border-top: 1px solid var(--doc-border);
        }}

        /* Toast */
        .toast {{
            position: fixed;
            bottom: -60px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--doc-text);
            color: var(--doc-bg);
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            transition: bottom 0.3s;
            z-index: 999;
        }}

        .toast.show {{
            bottom: 24px;
        }}

        /* Responsive */
        @media (max-width: 640px) {{
            .intro-grid {{ grid-template-columns: 1fr 1fr; }}
            .swatch-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .component-grid {{ grid-template-columns: 1fr; }}
            .geo-grid {{ grid-template-columns: 1fr; }}
        }}
    """


def _get_js() -> str:
    """Generate embedded JavaScript."""
    return """
        function toggleTheme() {
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            document.getElementById('themeIcon').textContent = next === 'dark' ? '🌙' : '☀️';
            localStorage.setItem('theme', next);
        }

        function copyColor(value) {
            navigator.clipboard.writeText(value).then(() => {
                const toast = document.getElementById('toast');
                toast.textContent = 'Copied: ' + value;
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2000);
            });
        }

        // Restore saved theme
        (function() {
            const saved = localStorage.getItem('theme');
            if (saved) {
                document.documentElement.setAttribute('data-theme', saved);
                document.getElementById('themeIcon').textContent = saved === 'dark' ? '🌙' : '☀️';
            }
        })();
    """


# ============ CLI ============

if __name__ == "__main__":
    import argparse

    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

    parser = argparse.ArgumentParser(description="Generate Design System Documentation HTML")
    parser.add_argument("--project", "-p", help="Project slug (reads from output/<slug>/)")
    parser.add_argument("--input", "-i", help="Direct input: harvest JSON file")
    parser.add_argument("--tokens", "-t", help="Direct input: Semi tokens JSON file")
    parser.add_argument("--output", "-o", help="Output HTML file path")
    parser.add_argument("--open", action="store_true", help="Open in browser after generating")

    args = parser.parse_args()

    if args.project:
        from project_registry import ProjectRegistry
        from token_mapper import map_to_semi_tokens

        registry = ProjectRegistry()
        manifest = registry.get(args.project)
        if not manifest:
            print(f"Error: Project '{args.project}' not found")
            sys.exit(1)

        harvest = registry.get_merged_harvest(args.project)
        if not harvest:
            # Fallback: try harvest-raw.json
            harvest_path = registry.get_project_dir(args.project) / "harvest-raw.json"
            if harvest_path.exists():
                with open(harvest_path) as f:
                    harvest = json.load(f)
            else:
                print(f"Error: No harvest data for project '{args.project}'")
                sys.exit(1)

        tokens = map_to_semi_tokens(harvest)
        meta = {**manifest, **harvest.get("meta", {})}
        output_path = args.output or str(registry.get_project_dir(args.project) / "design-system.html")

    elif args.input:
        from token_mapper import map_to_semi_tokens

        with open(args.input) as f:
            harvest = json.load(f)
        tokens = map_to_semi_tokens(harvest)
        meta = harvest.get("meta", {})
        output_path = args.output or "design-system.html"

    else:
        print("Error: Specify --project or --input")
        parser.print_help()
        sys.exit(1)

    html = generate_doc_html(tokens, harvest, meta)

    with open(output_path, "w") as f:
        f.write(html)
    print(f"[OK] Design system doc written to {output_path}")

    if args.open:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(output_path)}")

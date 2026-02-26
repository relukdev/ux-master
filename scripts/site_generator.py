#!/usr/bin/env python3
"""
Design System Guideline Site Generator

Generates a multi-page static site inspired by semi.design for documenting
a harvested design system. Output is fully self-contained (no CDN, no node_modules).

Pages:
  - index.html      — Getting Started (overview, quick start)
  - tokens.html     — Design Tokens (colors, typography, spacing, shadows)
  - components.html — Component Gallery (card grid, code snippets)

Usage:
    from site_generator import SiteGenerator
    gen = SiteGenerator(design_system, tokens, meta, output_dir)
    gen.generate()

Author: UX Master AI
Version: 4.1.0
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class SiteGenerator:
    """Generate a semi.design-inspired static guideline site."""

    def __init__(
        self,
        design_system: dict,
        tokens: dict,
        meta: dict,
        output_dir: Path,
        components: Optional[Dict[str, Dict[str, str]]] = None,
    ):
        self.ds = design_system
        self.tokens = tokens
        self.meta = meta
        self.output_dir = Path(output_dir)
        self.components = components or {}
        self.project_name = meta.get("name", "Design System")
        self.project_slug = meta.get("slug", "project")
        self.project_url = meta.get("url", "")

    def generate(self):
        """Generate complete site."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "css").mkdir(exist_ok=True)
        (self.output_dir / "js").mkdir(exist_ok=True)

        # Write pages
        self._write("index.html", self._page_index())
        self._write("tokens.html", self._page_tokens())
        self._write("components.html", self._page_components())
        self._write("css/style.css", self._css())
        self._write("js/app.js", self._js())

    def _write(self, path: str, content: str):
        filepath = self.output_dir / path
        filepath.write_text(content, encoding="utf-8")

    # ── HTML Shell ──────────────────────────────────────────────

    def _shell(self, title: str, active: str, body: str) -> str:
        """Wrap body in full HTML shell with sidebar."""
        nav_items = [
            ("index.html", "Getting Started", "getting-started"),
            ("tokens.html", "Design Tokens", "tokens"),
            ("components.html", "Components", "components"),
        ]

        nav_html = ""
        for href, label, key in nav_items:
            cls = ' class="active"' if key == active else ""
            nav_html += f'        <a href="{href}"{cls}>{label}</a>\n'

        return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — {self._esc(self.project_name)}</title>
  <link rel="stylesheet" href="css/style.css">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2 class="sidebar-title">{self._esc(self.project_name)}</h2>
      <span class="sidebar-badge">Design System</span>
    </div>
    <nav class="sidebar-nav">
{nav_html}    </nav>
    <div class="sidebar-footer">
      <button class="dark-mode-toggle" id="darkToggle" title="Toggle dark mode">
        <span class="icon-sun">☀️</span>
        <span class="icon-moon">🌙</span>
      </button>
      <span class="sidebar-version">UX Master v4.1</span>
    </div>
  </aside>

  <button class="menu-toggle" id="menuToggle" aria-label="Toggle menu">☰</button>

  <main class="main-content">
{body}
  </main>

  <script src="js/app.js"></script>
</body>
</html>"""

    # ── Page: Getting Started ───────────────────────────────────

    def _page_index(self) -> str:
        url_html = ""
        if self.project_url:
            url_html = f'<p class="source-url">Source: <a href="{self._esc(self.project_url)}" target="_blank">{self._esc(self.project_url)}</a></p>'

        created = self.meta.get("created_at", "")
        if created:
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                created = dt.strftime("%B %d, %Y")
            except Exception:
                pass

        colors_count = len(self.ds.get("colors", {}))
        typo_count = len(self.ds.get("typography", {}))
        spacing_count = len(self.ds.get("spacing", {}))
        token_count = len(self.tokens)
        comp_count = len(self.components)

        body = f"""
    <section class="hero">
      <h1>{self._esc(self.project_name)} Design System</h1>
      <p class="hero-desc">
        Extracted design tokens and components powered by UX Master v4.
        Use these tokens to maintain visual consistency across your project.
      </p>
      {url_html}
    </section>

    <section class="stats-grid">
      <div class="stat-card">
        <div class="stat-number">{token_count}</div>
        <div class="stat-label">CSS Tokens</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{colors_count}</div>
        <div class="stat-label">Colors</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{spacing_count}</div>
        <div class="stat-label">Spacing</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{comp_count}</div>
        <div class="stat-label">Components</div>
      </div>
    </section>

    <section class="content-section">
      <h2>Quick Start</h2>
      <p>Import the design system CSS variables into your project:</p>

      <div class="code-block">
        <div class="code-header">
          <span>CSS</span>
          <button class="copy-btn" data-copy="css-import">Copy</button>
        </div>
        <pre><code id="css-import">@import url('./{self.project_slug}/tokens/semi-theme.css');

/* Or copy the CSS variables directly into your :root */
:root {{
  /* See Design Tokens page for all available variables */
}}</code></pre>
      </div>

      <div class="code-block">
        <div class="code-header">
          <span>React / TypeScript</span>
          <button class="copy-btn" data-copy="react-import">Copy</button>
        </div>
        <pre><code id="react-import">// Import the design system tokens
import './{self.project_slug}/tokens/semi-theme.css';

// Use components
import {{ Button }} from './{self.project_slug}/components/button';</code></pre>
      </div>
    </section>

    <section class="content-section">
      <h2>Architecture</h2>
      <p>This design system follows the <strong>Semi Design</strong> architecture
         with CSS custom properties (variables) for all design tokens.</p>
      <ul>
        <li><strong>Tokens:</strong> CSS variables with <code>--semi-*</code> naming</li>
        <li><strong>Components:</strong> React + TypeScript with <code>forwardRef</code></li>
        <li><strong>Figma:</strong> Compatible with Figma Tokens Studio</li>
      </ul>
    </section>
"""
        return self._shell(f"Getting Started", "getting-started", body)

    # ── Page: Design Tokens ─────────────────────────────────────

    def _page_tokens(self) -> str:
        body = """
    <section class="content-section">
      <h1>Design Tokens</h1>
      <p>All design tokens extracted from the source, mapped to Semi Design CSS variables.</p>
    </section>
"""
        # Colors
        colors = self.ds.get("colors", {})
        if colors:
            body += '    <section class="content-section" id="colors">\n'
            body += '      <h2>Colors</h2>\n'
            body += '      <div class="token-search-box"><input type="text" id="colorSearch" placeholder="Search colors..." class="search-input"></div>\n'
            body += '      <div class="color-grid" id="colorGrid">\n'
            for name, value in colors.items():
                body += f"""        <div class="color-swatch" data-name="{self._esc(name)}">
          <div class="swatch-preview" style="background-color: {self._esc(value)}"></div>
          <div class="swatch-info">
            <span class="swatch-name">{self._esc(name)}</span>
            <span class="swatch-value" data-copyable>{self._esc(value)}</span>
          </div>
        </div>
"""
            body += '      </div>\n'
            body += '    </section>\n\n'

        # Also show semi token colors
        color_tokens = {k: v for k, v in self.tokens.items() if "color" in k.lower()}
        if color_tokens:
            body += '    <section class="content-section" id="css-color-tokens">\n'
            body += '      <h2>CSS Color Variables</h2>\n'
            body += '      <div class="color-grid">\n'
            for name, value in color_tokens.items():
                body += f"""        <div class="color-swatch">
          <div class="swatch-preview" style="background-color: {self._esc(value)}"></div>
          <div class="swatch-info">
            <span class="swatch-name">{self._esc(name)}</span>
            <span class="swatch-value" data-copyable>{self._esc(value)}</span>
          </div>
        </div>
"""
            body += '      </div>\n'
            body += '    </section>\n\n'

        # Typography
        typo = self.ds.get("typography", {})
        if typo:
            body += '    <section class="content-section" id="typography">\n'
            body += '      <h2>Typography</h2>\n'
            body += '      <div class="typo-grid">\n'
            for name, value in typo.items():
                body += f"""        <div class="typo-item">
          <span class="typo-name">{self._esc(name)}</span>
          <span class="typo-value" data-copyable>{self._esc(value)}</span>
        </div>
"""
            body += '      </div>\n'
            body += '    </section>\n\n'

        # Spacing
        spacing = self.ds.get("spacing", {})
        if spacing:
            body += '    <section class="content-section" id="spacing">\n'
            body += '      <h2>Spacing</h2>\n'
            body += '      <div class="spacing-list">\n'
            for name, value in spacing.items():
                # Parse px value for bar width
                try:
                    px = int(value.replace("px", ""))
                except (ValueError, AttributeError):
                    px = 16
                body += f"""        <div class="spacing-item">
          <span class="spacing-name">{self._esc(name)}</span>
          <div class="spacing-bar" style="width: {px}px"></div>
          <span class="spacing-value" data-copyable>{self._esc(value)}</span>
        </div>
"""
            body += '      </div>\n'
            body += '    </section>\n\n'

        # Shadows
        shadows = self.ds.get("shadows", {})
        if shadows:
            body += '    <section class="content-section" id="shadows">\n'
            body += '      <h2>Shadows</h2>\n'
            body += '      <div class="shadow-grid">\n'
            for name, value in shadows.items():
                body += f"""        <div class="shadow-card" style="box-shadow: {self._esc(value)}">
          <span class="shadow-name">{self._esc(name)}</span>
          <span class="shadow-value" data-copyable>{self._esc(value)}</span>
        </div>
"""
            body += '      </div>\n'
            body += '    </section>\n\n'

        # Borders
        borders = self.ds.get("borders", {})
        if borders:
            body += '    <section class="content-section" id="borders">\n'
            body += '      <h2>Borders & Radius</h2>\n'
            body += '      <div class="border-grid">\n'
            for name, value in borders.items():
                if "radius" in name:
                    body += f"""        <div class="border-item">
          <div class="radius-preview" style="border-radius: {self._esc(value)}"></div>
          <span class="border-name">{self._esc(name)}</span>
          <span class="border-value" data-copyable>{self._esc(value)}</span>
        </div>
"""
            body += '      </div>\n'
            body += '    </section>\n\n'

        # Full Token Reference Table
        if self.tokens:
            body += '    <section class="content-section" id="token-table">\n'
            body += '      <h2>Token Reference</h2>\n'
            body += '      <div class="token-search-box"><input type="text" id="tokenSearch" placeholder="Search tokens..." class="search-input"></div>\n'
            body += '      <table class="token-table" id="tokenTable">\n'
            body += '        <thead><tr><th>Variable</th><th>Value</th><th></th></tr></thead>\n'
            body += '        <tbody>\n'
            for name, value in sorted(self.tokens.items()):
                body += f'          <tr><td><code>{self._esc(name)}</code></td><td data-copyable>{self._esc(value)}</td><td><button class="copy-btn-sm" data-copy-text="{self._esc(name)}: {self._esc(value)}">📋</button></td></tr>\n'
            body += '        </tbody>\n'
            body += '      </table>\n'
            body += '    </section>\n'

        return self._shell("Design Tokens", "tokens", body)

    # ── Page: Components ────────────────────────────────────────

    def _page_components(self) -> str:
        body = """
    <section class="content-section">
      <h1>Component Gallery</h1>
      <p>Generated React components using the design system tokens.</p>
    </section>
"""
        if not self.components:
            body += """
    <section class="content-section">
      <div class="empty-state">
        <p>No components generated yet.</p>
        <p>Run <code>uxmaster build &lt;project&gt;</code> to generate components.</p>
      </div>
    </section>
"""
        else:
            body += '    <section class="content-section">\n'
            body += '      <div class="component-grid">\n'

            for comp_name, files in sorted(self.components.items()):
                code = files.get("component.tsx", files.get("component.vue", ""))
                # Truncate for preview
                preview_code = code[:500] + ("..." if len(code) > 500 else "")

                body += f"""        <div class="component-card">
          <div class="component-header">
            <h3>{self._esc(comp_name.capitalize())}</h3>
            <span class="component-status">Stable</span>
          </div>
          <div class="component-preview">
            <div class="preview-box">
              <div class="preview-element preview-{self._esc(comp_name)}">
                {self._esc(comp_name.capitalize())}
              </div>
            </div>
          </div>
          <div class="component-code">
            <div class="code-header">
              <span>component.tsx</span>
              <button class="copy-btn" data-copy="code-{self._esc(comp_name)}">Copy</button>
            </div>
            <pre><code id="code-{self._esc(comp_name)}">{self._esc(preview_code)}</code></pre>
          </div>
        </div>
"""
            body += '      </div>\n'
            body += '    </section>\n'

        return self._shell("Components", "components", body)

    # ── CSS ─────────────────────────────────────────────────────

    def _css(self) -> str:
        # Get primary color for theming, with fallback
        primary = self.ds.get("colors", {}).get("primary", "#4F46E5")

        return f"""/* Design System Guideline Site — Generated by UX Master v4.1 */

:root {{
  --site-primary: {primary};
  --site-bg: #ffffff;
  --site-bg-alt: #f8f9fc;
  --site-text: #1e293b;
  --site-text-secondary: #64748b;
  --site-border: #e2e8f0;
  --site-sidebar-bg: #f1f5f9;
  --site-sidebar-width: 260px;
  --site-code-bg: #1e293b;
  --site-code-text: #e2e8f0;
  --site-radius: 8px;
  --site-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
  --site-shadow-lg: 0 4px 16px rgba(0,0,0,0.1);
  --site-font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

[data-theme="dark"] {{
  --site-bg: #0f172a;
  --site-bg-alt: #1e293b;
  --site-text: #e2e8f0;
  --site-text-secondary: #94a3b8;
  --site-border: #334155;
  --site-sidebar-bg: #1e293b;
  --site-code-bg: #0f172a;
  --site-shadow: 0 1px 3px rgba(0,0,0,0.3);
  --site-shadow-lg: 0 4px 16px rgba(0,0,0,0.4);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: var(--site-font);
  background: var(--site-bg);
  color: var(--site-text);
  line-height: 1.6;
  display: flex;
  min-height: 100vh;
}}

/* Sidebar */
.sidebar {{
  width: var(--site-sidebar-width);
  background: var(--site-sidebar-bg);
  border-right: 1px solid var(--site-border);
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  z-index: 100;
  transition: transform 0.3s ease;
}}

.sidebar-header {{
  padding: 24px 20px 16px;
  border-bottom: 1px solid var(--site-border);
}}

.sidebar-title {{
  font-size: 18px;
  font-weight: 700;
  color: var(--site-text);
  margin-bottom: 4px;
}}

.sidebar-badge {{
  display: inline-block;
  padding: 2px 8px;
  background: var(--site-primary);
  color: white;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}}

.sidebar-nav {{
  flex: 1;
  padding: 12px 8px;
  overflow-y: auto;
}}

.sidebar-nav a {{
  display: block;
  padding: 10px 16px;
  color: var(--site-text-secondary);
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s ease;
  margin-bottom: 2px;
}}

.sidebar-nav a:hover {{
  background: var(--site-border);
  color: var(--site-text);
}}

.sidebar-nav a.active {{
  background: var(--site-primary);
  color: white;
}}

.sidebar-footer {{
  padding: 16px 20px;
  border-top: 1px solid var(--site-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.sidebar-version {{
  font-size: 12px;
  color: var(--site-text-secondary);
}}

.dark-mode-toggle {{
  background: var(--site-border);
  border: none;
  border-radius: 20px;
  padding: 4px 12px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}}

.dark-mode-toggle:hover {{
  background: var(--site-primary);
}}

[data-theme="light"] .icon-moon {{ display: none; }}
[data-theme="dark"] .icon-sun {{ display: none; }}

.menu-toggle {{
  display: none;
  position: fixed;
  top: 16px;
  left: 16px;
  z-index: 200;
  background: var(--site-primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 20px;
  cursor: pointer;
}}

/* Main Content */
.main-content {{
  flex: 1;
  margin-left: var(--site-sidebar-width);
  max-width: 900px;
  padding: 40px 48px 80px;
}}

/* Hero */
.hero {{
  margin-bottom: 32px;
}}

.hero h1 {{
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 12px;
  background: linear-gradient(135deg, var(--site-primary), var(--site-text));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}

.hero-desc {{
  font-size: 16px;
  color: var(--site-text-secondary);
  line-height: 1.7;
  max-width: 600px;
}}

.source-url {{
  margin-top: 8px;
  font-size: 13px;
  color: var(--site-text-secondary);
}}

.source-url a {{
  color: var(--site-primary);
}}

/* Stats */
.stats-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
  margin-bottom: 40px;
}}

.stat-card {{
  background: var(--site-bg-alt);
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius);
  padding: 20px;
  text-align: center;
}}

.stat-number {{
  font-size: 28px;
  font-weight: 700;
  color: var(--site-primary);
}}

.stat-label {{
  font-size: 13px;
  color: var(--site-text-secondary);
  margin-top: 4px;
  font-weight: 500;
}}

/* Content Sections */
.content-section {{
  margin-bottom: 40px;
}}

.content-section h1 {{
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
}}

.content-section h2 {{
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--site-border);
}}

.content-section p {{
  color: var(--site-text-secondary);
  margin-bottom: 16px;
  line-height: 1.7;
}}

.content-section ul {{
  padding-left: 20px;
  margin-bottom: 16px;
}}

.content-section li {{
  margin-bottom: 8px;
  color: var(--site-text-secondary);
}}

.content-section code {{
  background: var(--site-bg-alt);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-family: 'Fira Code', monospace;
}}

/* Code Block */
.code-block {{
  border-radius: var(--site-radius);
  overflow: hidden;
  margin-bottom: 20px;
  border: 1px solid var(--site-border);
}}

.code-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: var(--site-bg-alt);
  border-bottom: 1px solid var(--site-border);
  font-size: 12px;
  font-weight: 600;
  color: var(--site-text-secondary);
}}

.code-block pre {{
  background: var(--site-code-bg);
  color: var(--site-code-text);
  padding: 16px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.6;
  font-family: 'Fira Code', monospace;
}}

.copy-btn, .copy-btn-sm {{
  background: var(--site-primary);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 10px;
  font-size: 11px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.2s;
}}

.copy-btn:hover, .copy-btn-sm:hover {{
  opacity: 0.85;
}}

.copy-btn-sm {{
  padding: 2px 6px;
  font-size: 10px;
}}

/* Color Grid */
.color-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}}

.color-swatch {{
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius);
  overflow: hidden;
  transition: box-shadow 0.2s;
  cursor: pointer;
}}

.color-swatch:hover {{
  box-shadow: var(--site-shadow-lg);
}}

.swatch-preview {{
  height: 80px;
  width: 100%;
}}

.swatch-info {{
  padding: 10px 12px;
  background: var(--site-bg);
}}

.swatch-name {{
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--site-text);
  margin-bottom: 2px;
}}

.swatch-value {{
  font-size: 12px;
  color: var(--site-text-secondary);
  font-family: 'Fira Code', monospace;
  cursor: pointer;
}}

.swatch-value:hover {{
  color: var(--site-primary);
}}

/* Search */
.token-search-box {{
  margin-bottom: 16px;
}}

.search-input {{
  width: 100%;
  padding: 10px 16px;
  border: 1px solid var(--site-border);
  border-radius: 6px;
  background: var(--site-bg);
  color: var(--site-text);
  font-size: 14px;
  font-family: var(--site-font);
  outline: none;
  transition: border-color 0.2s;
}}

.search-input:focus {{
  border-color: var(--site-primary);
}}

/* Typography Grid */
.typo-grid {{
  display: grid;
  gap: 8px;
}}

.typo-item {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--site-bg-alt);
  border-radius: 6px;
  border: 1px solid var(--site-border);
}}

.typo-name {{
  font-weight: 600;
  font-size: 13px;
}}

.typo-value {{
  font-family: 'Fira Code', monospace;
  font-size: 13px;
  color: var(--site-text-secondary);
  cursor: pointer;
}}

/* Spacing */
.spacing-list {{
  display: grid;
  gap: 8px;
}}

.spacing-item {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: var(--site-bg-alt);
  border-radius: 6px;
  border: 1px solid var(--site-border);
}}

.spacing-name {{
  width: 120px;
  font-weight: 600;
  font-size: 13px;
  flex-shrink: 0;
}}

.spacing-bar {{
  height: 12px;
  background: var(--site-primary);
  border-radius: 3px;
  min-width: 4px;
  opacity: 0.7;
}}

.spacing-value {{
  font-family: 'Fira Code', monospace;
  font-size: 13px;
  color: var(--site-text-secondary);
  flex-shrink: 0;
  cursor: pointer;
}}

/* Shadows */
.shadow-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}}

.shadow-card {{
  padding: 24px;
  border-radius: var(--site-radius);
  background: var(--site-bg);
  border: 1px solid var(--site-border);
  text-align: center;
}}

.shadow-name {{
  display: block;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}}

.shadow-value {{
  font-size: 11px;
  color: var(--site-text-secondary);
  font-family: 'Fira Code', monospace;
  cursor: pointer;
}}

/* Borders */
.border-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}}

.border-item {{
  text-align: center;
  padding: 16px;
  background: var(--site-bg-alt);
  border-radius: 6px;
  border: 1px solid var(--site-border);
}}

.radius-preview {{
  width: 60px;
  height: 60px;
  background: var(--site-primary);
  margin: 0 auto 12px;
  opacity: 0.7;
}}

.border-name {{
  display: block;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 2px;
}}

.border-value {{
  font-size: 12px;
  color: var(--site-text-secondary);
  font-family: 'Fira Code', monospace;
  cursor: pointer;
}}

/* Token Table */
.token-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  margin-top: 12px;
}}

.token-table th {{
  text-align: left;
  padding: 10px 12px;
  background: var(--site-bg-alt);
  border-bottom: 2px solid var(--site-border);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--site-text-secondary);
}}

.token-table td {{
  padding: 8px 12px;
  border-bottom: 1px solid var(--site-border);
}}

.token-table td code {{
  font-size: 12px;
  color: var(--site-primary);
}}

.token-table tr:hover {{
  background: var(--site-bg-alt);
}}

/* Component Gallery */
.component-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 20px;
}}

.component-card {{
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius);
  overflow: hidden;
  transition: box-shadow 0.2s;
}}

.component-card:hover {{
  box-shadow: var(--site-shadow-lg);
}}

.component-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--site-border);
}}

.component-header h3 {{
  font-size: 16px;
  font-weight: 600;
}}

.component-status {{
  padding: 2px 8px;
  background: #dcfce7;
  color: #166534;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}}

.component-preview {{
  padding: 24px;
  background: var(--site-bg-alt);
  border-bottom: 1px solid var(--site-border);
}}

.preview-box {{
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60px;
}}

.preview-element {{
  padding: 8px 20px;
  background: var(--site-primary);
  color: white;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
}}

.component-code pre {{
  max-height: 200px;
  overflow-y: auto;
}}

/* Empty State */
.empty-state {{
  text-align: center;
  padding: 60px 20px;
  color: var(--site-text-secondary);
}}

/* Responsive */
@media (max-width: 768px) {{
  .sidebar {{
    transform: translateX(-100%);
  }}

  .sidebar.open {{
    transform: translateX(0);
  }}

  .menu-toggle {{
    display: block;
  }}

  .main-content {{
    margin-left: 0;
    padding: 80px 20px 40px;
  }}

  .stats-grid {{
    grid-template-columns: repeat(2, 1fr);
  }}

  .component-grid {{
    grid-template-columns: 1fr;
  }}

  .color-grid {{
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }}
}}
"""

    # ── JavaScript ──────────────────────────────────────────────

    def _js(self) -> str:
        return """// Design System Guideline Site — Generated by UX Master v4.1

// Dark mode toggle
const darkToggle = document.getElementById('darkToggle');
if (darkToggle) {
  // Load preference
  const saved = localStorage.getItem('uxm-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);

  darkToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('uxm-theme', next);
  });
}

// Mobile menu toggle
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
if (menuToggle && sidebar) {
  menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside
  document.addEventListener('click', (e) => {
    if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
      sidebar.classList.remove('open');
    }
  });
}

// Copy to clipboard
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    // Flash feedback
    const toast = document.createElement('div');
    toast.textContent = 'Copied!';
    toast.style.cssText = `
      position: fixed; bottom: 20px; right: 20px;
      background: #10b981; color: white; padding: 8px 16px;
      border-radius: 6px; font-size: 13px; font-weight: 600;
      z-index: 9999; animation: fadeOut 1.5s forwards;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 1500);
  });
}

// Copy buttons
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.getAttribute('data-copy');
    const el = document.getElementById(id);
    if (el) copyToClipboard(el.textContent);
  });
});

document.querySelectorAll('.copy-btn-sm').forEach(btn => {
  btn.addEventListener('click', () => {
    const text = btn.getAttribute('data-copy-text');
    if (text) copyToClipboard(text);
  });
});

// Click-to-copy on values
document.querySelectorAll('[data-copyable]').forEach(el => {
  el.addEventListener('click', () => {
    copyToClipboard(el.textContent);
  });
});

// Color search
const colorSearch = document.getElementById('colorSearch');
const colorGrid = document.getElementById('colorGrid');
if (colorSearch && colorGrid) {
  colorSearch.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    colorGrid.querySelectorAll('.color-swatch').forEach(swatch => {
      const name = swatch.getAttribute('data-name') || '';
      swatch.style.display = name.toLowerCase().includes(q) ? '' : 'none';
    });
  });
}

// Token table search
const tokenSearch = document.getElementById('tokenSearch');
const tokenTable = document.getElementById('tokenTable');
if (tokenSearch && tokenTable) {
  tokenSearch.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase();
    tokenTable.querySelectorAll('tbody tr').forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(q) ? '' : 'none';
    });
  });
}

// Fade out animation
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeOut {
    0% { opacity: 1; transform: translateY(0); }
    70% { opacity: 1; }
    100% { opacity: 0; transform: translateY(-10px); }
  }
`;
document.head.appendChild(style);
"""

    # ── Utilities ───────────────────────────────────────────────

    @staticmethod
    def _esc(s: str) -> str:
        """HTML-escape a string."""
        if not isinstance(s, str):
            s = str(s)
        return (
            s.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )


# ============ CLI ============

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Design System Guideline Site")
    parser.add_argument("--design-system", "-d", required=True, help="design-system.json path")
    parser.add_argument("--tokens", "-t", help="semi-theme-override.css JSON or CSS tokens file")
    parser.add_argument("--meta", "-m", help="manifest.json path")
    parser.add_argument("--components", "-c", help="Components directory (with sub-folders)")
    parser.add_argument("--output", "-o", default="./site", help="Output directory for site")

    args = parser.parse_args()

    # Load design system
    with open(args.design_system, 'r') as f:
        design_system = json.load(f)

    # Load tokens
    tokens = {}
    if args.tokens:
        with open(args.tokens, 'r') as f:
            content = f.read()
            # Try JSON first, then parse CSS
            try:
                tokens = json.loads(content)
            except json.JSONDecodeError:
                # Parse CSS variables
                import re
                for match in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+)', content):
                    tokens[match.group(1)] = match.group(2).strip()

    # Load meta
    meta = {"name": "Design System", "slug": "project"}
    if args.meta:
        with open(args.meta, 'r') as f:
            meta = json.load(f)

    # Load components
    components = {}
    if args.components:
        comp_dir = Path(args.components)
        if comp_dir.exists():
            for sub in sorted(comp_dir.iterdir()):
                if sub.is_dir():
                    files = {}
                    for f in sub.iterdir():
                        if f.is_file():
                            files[f.name] = f.read_text()
                    if files:
                        components[sub.name] = files

    gen = SiteGenerator(
        design_system=design_system,
        tokens=tokens,
        meta=meta,
        output_dir=Path(args.output),
        components=components,
    )
    gen.generate()
    print(f"[OK] Site generated at {args.output}/")
    print(f"  → {args.output}/index.html")
    print(f"  → {args.output}/tokens.html")
    print(f"  → {args.output}/components.html")

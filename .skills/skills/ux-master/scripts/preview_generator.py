#!/usr/bin/env python3
"""
Token Preview Generator — Creates a visual HTML preview of extracted tokens.

Generates a single-page HTML that shows:
1. Brand color swatches with all states
2. Semantic color swatches
3. Neutral scale gradient
4. Typography specimens
5. Component previews (button, card, input) using extracted tokens

Used in the semi-auto workflow to confirm tokens with the user before
generating the full component library.

Usage:
    python3 preview_generator.py --input design-system.css --output preview.html
    python3 preview_generator.py --input tokens.json --format json --output preview.html
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


def parse_css_tokens(css_content: str) -> dict:
    tokens = {}
    pattern = r'(--semi-[a-zA-Z0-9-]+)\s*:\s*([^;]+);'
    for match in re.finditer(pattern, css_content):
        tokens[match.group(1)] = match.group(2).strip()
    return tokens


def parse_json_tokens(json_content: str) -> dict:
    data = json.loads(json_content)
    tokens = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if key.startswith("--semi-"):
                tokens[key] = str(value)
            elif isinstance(value, dict):
                for subkey, subval in value.items():
                    if isinstance(subval, str):
                        tokens[f"--semi-{key}-{subkey}"] = subval
    return tokens


def hex_luminance(hex_str: str) -> float:
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) < 6:
        return 128
    r, g, b = (int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return 0.299 * r + 0.587 * g + 0.114 * b


def text_color_for(hex_bg: str) -> str:
    return "#FFFFFF" if hex_luminance(hex_bg) < 128 else "#000000"


def generate_preview_html(tokens: dict, project_name: str = "Design System") -> str:
    """Generate a visual preview HTML page."""

    # Extract key tokens with defaults
    primary = tokens.get("--semi-color-primary", "#0F79F3")
    secondary = tokens.get("--semi-color-secondary", "#FF6900")
    tertiary = tokens.get("--semi-color-tertiary", "#7C3AED")
    success = tokens.get("--semi-color-success", "#00B69B")
    warning = tokens.get("--semi-color-warning", "#F59E0B")
    danger = tokens.get("--semi-color-danger", "#EF4444")
    info = tokens.get("--semi-color-info", "#3B82F6")

    bg0 = tokens.get("--semi-color-bg-0", "#FFFFFF")
    bg1 = tokens.get("--semi-color-bg-1", "#FFFFFF")
    text0 = tokens.get("--semi-color-text-0", "#1C1F23")
    text1 = tokens.get("--semi-color-text-1", "#475569")
    text2 = tokens.get("--semi-color-text-2", "#919AA3")
    border = tokens.get("--semi-color-border", "#E5E7EB")

    font = tokens.get("--semi-font-family-regular", '"Inter", -apple-system, sans-serif')
    font_size = tokens.get("--semi-font-size-regular", "14px")
    radius = tokens.get("--semi-border-radius-medium", "6px")

    # Build neutral scale swatches
    neutral_html = ""
    for i in range(0, 1000, 50):
        key = f"--semi-color-neutral-{i}"
        if key in tokens and tokens[key].startswith("#"):
            val = tokens[key]
            tc = text_color_for(val)
            neutral_html += f'<div class="swatch" style="background:{val};color:{tc}"><span>{i}</span><span>{val}</span></div>\n'

    # Build all CSS variables for preview
    css_vars = "\n".join(f"  {k}: {v};" for k, v in sorted(tokens.items()))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{project_name} — Token Preview</title>
<style>
:root {{
{css_vars}
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: {font};
  font-size: {font_size};
  color: {text0};
  background: {bg0};
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}}
h1 {{ font-size: 28px; margin-bottom: 8px; }}
h2 {{ font-size: 20px; margin: 32px 0 16px; color: {text0}; border-bottom: 2px solid {border}; padding-bottom: 8px; }}
h3 {{ font-size: 16px; margin: 16px 0 8px; color: {text1}; }}
.subtitle {{ color: {text2}; margin-bottom: 32px; }}
.color-row {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }}
.color-card {{
  width: 140px; border-radius: {radius}; overflow: hidden;
  border: 1px solid {border}; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}
.color-card .preview {{ height: 80px; display: flex; align-items: flex-end; padding: 8px; }}
.color-card .label {{ padding: 8px; font-size: 12px; background: {bg1}; }}
.color-card .label .hex {{ color: {text2}; }}
.swatch {{
  display: inline-flex; flex-direction: column; align-items: center; justify-content: center;
  width: 80px; height: 60px; font-size: 11px; gap: 2px; border-radius: 4px;
  border: 1px solid rgba(0,0,0,0.1);
}}
.neutral-row {{ display: flex; gap: 4px; margin-bottom: 16px; }}
.typo-specimen {{ margin: 8px 0; }}
.typo-specimen span {{ color: {text2}; font-size: 12px; }}
.component-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }}
.component-card {{
  border: 1px solid {border}; border-radius: {radius}; padding: 24px;
  background: {bg1};
}}
.component-card h3 {{ margin-top: 0; }}
.btn {{
  display: inline-flex; align-items: center; justify-content: center;
  padding: 8px 16px; border: none; border-radius: {radius};
  font-family: {font}; font-size: {font_size}; font-weight: 500;
  cursor: pointer; margin: 4px;
}}
.btn-primary {{ background: {primary}; color: {text_color_for(primary)}; }}
.btn-secondary {{ background: {secondary}; color: {text_color_for(secondary)}; }}
.btn-outline {{ background: transparent; color: {primary}; border: 1px solid {primary}; }}
.btn-danger {{ background: {danger}; color: white; }}
.btn-sm {{ padding: 4px 12px; font-size: 12px; }}
.btn-lg {{ padding: 12px 24px; font-size: 16px; }}
.input-demo {{
  width: 100%; padding: 8px 12px; border: 1px solid {border};
  border-radius: {radius}; font-family: {font}; font-size: {font_size};
  color: {text0}; background: {bg0}; outline: none;
}}
.input-demo:focus {{ border-color: {primary}; box-shadow: 0 0 0 2px {primary}33; }}
.card-demo {{
  border: 1px solid {border}; border-radius: {radius}; padding: 16px;
  background: {bg1}; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 99px; font-size: 12px; font-weight: 500; }}
.badge-success {{ background: {success}22; color: {success}; }}
.badge-warning {{ background: {warning}22; color: {warning}; }}
.badge-danger {{ background: {danger}22; color: {danger}; }}
.token-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.token-table th {{ text-align: left; padding: 8px; background: {bg1}; border-bottom: 2px solid {border}; }}
.token-table td {{ padding: 8px; border-bottom: 1px solid {border}; }}
.token-table .color-dot {{ display: inline-block; width: 14px; height: 14px; border-radius: 50%; vertical-align: middle; margin-right: 6px; border: 1px solid rgba(0,0,0,0.1); }}
footer {{ margin-top: 48px; padding-top: 16px; border-top: 1px solid {border}; color: {text2}; font-size: 12px; }}
</style>
</head>
<body>

<h1>{project_name}</h1>
<p class="subtitle">Design Token Preview — Generated by UX Master</p>

<h2>Brand Colors</h2>
<div class="color-row">
  <div class="color-card">
    <div class="preview" style="background:{primary};color:{text_color_for(primary)}">Primary</div>
    <div class="label">--semi-color-primary<br><span class="hex">{primary}</span></div>
  </div>
  <div class="color-card">
    <div class="preview" style="background:{secondary};color:{text_color_for(secondary)}">Secondary</div>
    <div class="label">--semi-color-secondary<br><span class="hex">{secondary}</span></div>
  </div>
  <div class="color-card">
    <div class="preview" style="background:{tertiary};color:{text_color_for(tertiary)}">Tertiary</div>
    <div class="label">--semi-color-tertiary<br><span class="hex">{tertiary}</span></div>
  </div>
</div>

<h2>Semantic Colors</h2>
<div class="color-row">
  <div class="color-card">
    <div class="preview" style="background:{success};color:{text_color_for(success)}">Success</div>
    <div class="label">--semi-color-success<br><span class="hex">{success}</span></div>
  </div>
  <div class="color-card">
    <div class="preview" style="background:{warning};color:{text_color_for(warning)}">Warning</div>
    <div class="label">--semi-color-warning<br><span class="hex">{warning}</span></div>
  </div>
  <div class="color-card">
    <div class="preview" style="background:{danger};color:{text_color_for(danger)}">Danger</div>
    <div class="label">--semi-color-danger<br><span class="hex">{danger}</span></div>
  </div>
  <div class="color-card">
    <div class="preview" style="background:{info};color:{text_color_for(info)}">Info</div>
    <div class="label">--semi-color-info<br><span class="hex">{info}</span></div>
  </div>
</div>

<h2>Neutral Scale</h2>
<div class="neutral-row">
{neutral_html}
</div>

<h2>Typography</h2>
<div class="typo-specimen">
  <div style="font-size:32px;font-weight:700;color:{text0}">Heading 1 — The quick brown fox</div>
  <span>32px / Bold / {font}</span>
</div>
<div class="typo-specimen">
  <div style="font-size:24px;font-weight:600;color:{text0}">Heading 3 — The quick brown fox</div>
  <span>24px / Semibold</span>
</div>
<div class="typo-specimen">
  <div style="font-size:{font_size};color:{text1}">Body text — The quick brown fox jumps over the lazy dog. This is how body text appears with the extracted typography tokens.</div>
  <span>{font_size} / Regular</span>
</div>
<div class="typo-specimen">
  <div style="font-size:12px;color:{text2}">Caption text — Supporting text in a lighter color for descriptions and metadata</div>
  <span>12px / Regular / text-2</span>
</div>

<h2>Component Previews</h2>
<div class="component-grid">
  <div class="component-card">
    <h3>Button</h3>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
      <button class="btn btn-primary">Primary</button>
      <button class="btn btn-secondary">Secondary</button>
      <button class="btn btn-outline">Outline</button>
      <button class="btn btn-danger">Danger</button>
    </div>
    <div style="margin-top:8px">
      <button class="btn btn-primary btn-sm">Small</button>
      <button class="btn btn-primary">Medium</button>
      <button class="btn btn-primary btn-lg">Large</button>
    </div>
  </div>

  <div class="component-card">
    <h3>Input</h3>
    <div style="display:flex;flex-direction:column;gap:8px;margin-top:12px">
      <input class="input-demo" placeholder="Enter your email...">
      <input class="input-demo" value="john@example.com">
      <input class="input-demo" disabled placeholder="Disabled input" style="opacity:0.5;cursor:not-allowed">
    </div>
  </div>

  <div class="component-card">
    <h3>Card</h3>
    <div class="card-demo" style="margin-top:12px">
      <div style="font-weight:600;margin-bottom:4px">Card Title</div>
      <div style="color:{text2};font-size:13px;margin-bottom:12px">This is a card component using the extracted shadow and border tokens.</div>
      <button class="btn btn-primary btn-sm">Action</button>
    </div>
  </div>

  <div class="component-card">
    <h3>Badges</h3>
    <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
      <span class="badge badge-success">Active</span>
      <span class="badge badge-warning">Pending</span>
      <span class="badge badge-danger">Error</span>
      <span class="badge" style="background:{primary}22;color:{primary}">Info</span>
    </div>
  </div>
</div>

<h2>Token Reference</h2>
<table class="token-table">
  <thead><tr><th>Token</th><th>Value</th><th>Preview</th></tr></thead>
  <tbody>
"""

    # Add top tokens to table
    important_tokens = [
        "--semi-color-primary", "--semi-color-secondary", "--semi-color-tertiary",
        "--semi-color-success", "--semi-color-warning", "--semi-color-danger",
        "--semi-color-bg-0", "--semi-color-bg-1", "--semi-color-bg-2",
        "--semi-color-text-0", "--semi-color-text-1", "--semi-color-text-2",
        "--semi-color-border", "--semi-font-family-regular",
        "--semi-font-size-regular", "--semi-border-radius-medium",
    ]

    for key in important_tokens:
        if key in tokens:
            val = tokens[key]
            preview = ""
            if val.startswith("#") or val.startswith("rgb"):
                preview = f'<span class="color-dot" style="background:{val}"></span>'
            html += f'    <tr><td><code>{key}</code></td><td>{val}</td><td>{preview}</td></tr>\n'

    html += f"""
  </tbody>
</table>

<footer>
  Generated by UX Master Harvester v4 — {datetime.now().strftime('%Y-%m-%d %H:%M')}
</footer>

</body>
</html>"""

    return html


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate token preview HTML")
    parser.add_argument("--input", "-i", required=True, help="Token file (CSS or JSON)")
    parser.add_argument("--output", "-o", required=True, help="Output HTML file")
    parser.add_argument("--format", "-f", choices=["css", "json", "auto"], default="auto")
    parser.add_argument("--name", "-n", default="Design System", help="Project name")
    args = parser.parse_args()

    path = Path(args.input)
    content = path.read_text()

    fmt = args.format
    if fmt == "auto":
        fmt = "json" if path.suffix == ".json" else "css"

    tokens = parse_json_tokens(content) if fmt == "json" else parse_css_tokens(content)

    if not tokens:
        print(f"No tokens found in {path}")
        sys.exit(1)

    html = generate_preview_html(tokens, args.name)
    Path(args.output).write_text(html)
    print(f"Preview generated: {args.output} ({len(tokens)} tokens)")


if __name__ == "__main__":
    main()

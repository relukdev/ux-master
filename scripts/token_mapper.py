#!/usr/bin/env python3
"""
Semi Token Compiler — Maps raw CSSOM harvest data to Semi Design tokens.

Converts browser-extracted computed styles into:
1. Semi Design CSS variable overrides (--semi-*)
2. Figma Tokens Studio JSON
3. Human-readable markdown summary

Usage:
    from token_mapper import map_to_semi_tokens, generate_css_override, generate_figma_tokens
    tokens = map_to_semi_tokens(raw_harvest_json)
    css = generate_css_override(tokens, meta)
    figma_json = generate_figma_tokens(tokens, meta)
"""
import json
import re
import colorsys


# ============ COLOR UTILITIES ============

def rgb_to_hex(color_str: str) -> str:
    """Convert rgb()/rgba() string to uppercase HEX. Pass-through if already hex."""
    if not color_str:
        return ""

    color_str = color_str.strip()

    # Already hex
    if color_str.startswith("#"):
        return color_str.upper()

    # Parse rgb(r, g, b) or rgba(r, g, b, a)
    match = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', color_str)
    if match:
        r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
        return f"#{r:02X}{g:02X}{b:02X}"

    return color_str


def hex_to_rgb(hex_str: str) -> tuple:
    """Convert hex color to (r, g, b) tuple."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def darken(hex_color: str, factor: float) -> str:
    """Darken a hex color by a factor (0.0 = no change, 1.0 = black)."""
    r, g, b = hex_to_rgb(hex_color)
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return f"#{r:02X}{g:02X}{b:02X}"


def lighten(hex_color: str, factor: float) -> str:
    """Lighten a hex color by a factor (0.0 = no change, 1.0 = white)."""
    r, g, b = hex_to_rgb(hex_color)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02X}{g:02X}{b:02X}"


def derive_shades(hex_color: str) -> dict:
    """Generate hover, active, and light variants from a base color."""
    return {
        "hover": darken(hex_color, 0.1),
        "active": darken(hex_color, 0.2),
        "light": lighten(hex_color, 0.85),
    }


# ============ SEMI TOKEN MAPPING ============

# Mapping table: harvest key path → Semi Design CSS variable
MAPPING = {
    # Colors
    ("colors", "primary"):      "--semi-color-primary",
    ("colors", "success"):      "--semi-color-success",
    ("colors", "warning"):      "--semi-color-warning",
    ("colors", "danger"):       "--semi-color-danger",
    # Surfaces
    ("surfaces", "app_bg"):     "--semi-color-bg-0",
    ("surfaces", "card_bg"):    "--semi-color-bg-1",
    ("surfaces", "sidebar_bg"): "--semi-color-bg-2",
    ("surfaces", "border"):     "--semi-color-border",
    # Typography
    ("typography", "title_color"):  "--semi-color-text-0",
    ("typography", "body_color"):   "--semi-color-text-1",
    ("typography", "muted_color"):  "--semi-color-text-2",
    ("typography", "font_family"):  "--semi-font-family-regular",
    ("typography", "body_size"):    "--semi-font-size-regular",
    # Geometry
    ("geometry", "button_radius"):  "--semi-border-radius-medium",
    ("geometry", "card_radius"):    "--semi-border-radius-large",
    ("geometry", "card_shadow"):    "--semi-shadow-elevated",
}

# Which tokens are colors (need hex conversion)
COLOR_TOKENS = {
    "--semi-color-primary", "--semi-color-success", "--semi-color-warning",
    "--semi-color-danger", "--semi-color-bg-0", "--semi-color-bg-1",
    "--semi-color-bg-2", "--semi-color-border", "--semi-color-text-0",
    "--semi-color-text-1", "--semi-color-text-2",
}


def map_to_semi_tokens(raw: dict) -> dict:
    """Map raw harvest JSON to Semi Design CSS variables."""
    tokens = {}

    for (section, key), semi_var in MAPPING.items():
        value = raw.get(section, {}).get(key)
        if value:
            if semi_var in COLOR_TOKENS:
                value = rgb_to_hex(value)
            tokens[semi_var] = value

    # Auto-derive hover/active/light for primary
    if "--semi-color-primary" in tokens:
        primary_hex = tokens["--semi-color-primary"]
        shades = derive_shades(primary_hex)
        tokens["--semi-color-primary-hover"] = shades["hover"]
        tokens["--semi-color-primary-active"] = shades["active"]
        tokens["--semi-color-primary-light-default"] = shades["light"]

    # Auto-derive for semantic colors
    for sem in ("success", "warning", "danger"):
        base_var = f"--semi-color-{sem}"
        if base_var in tokens:
            shades = derive_shades(tokens[base_var])
            tokens[f"{base_var}-hover"] = shades["hover"]
            tokens[f"{base_var}-active"] = shades["active"]

    return tokens


# ============ OUTPUT GENERATORS ============

def generate_css_override(tokens: dict, meta: dict = None) -> str:
    """Generate CSS theme override file for Semi Design."""
    meta = meta or {}
    url = meta.get("url", "unknown")
    title = meta.get("title", "")
    timestamp = meta.get("timestamp", "")

    lines = [
        f"/* Semi-Sync Harvester — Theme Override */",
        f"/* Source: {url} */",
        f"/* Title: {title} */",
        f"/* Extracted: {timestamp} */",
        f"/* Auto-generated by UX Master Skill */",
        "",
        "body {"
    ]

    # Group by category
    categories = {
        "Brand Colors": [],
        "Semantic Colors": [],
        "Surface Colors": [],
        "Text Colors": [],
        "Typography": [],
        "Geometry": [],
        "Shadows": [],
    }

    for var, val in sorted(tokens.items()):
        if "primary" in var:
            categories["Brand Colors"].append((var, val))
        elif any(s in var for s in ("success", "warning", "danger")):
            categories["Semantic Colors"].append((var, val))
        elif "bg-" in var or "border" in var:
            categories["Surface Colors"].append((var, val))
        elif "text-" in var:
            categories["Text Colors"].append((var, val))
        elif "font-" in var:
            categories["Typography"].append((var, val))
        elif "shadow" in var:
            categories["Shadows"].append((var, val))
        elif "radius" in var:
            categories["Geometry"].append((var, val))
        else:
            categories["Geometry"].append((var, val))

    for cat_name, items in categories.items():
        if items:
            lines.append(f"  /* {cat_name} */")
            for var, val in items:
                lines.append(f"  {var}: {val};")
            lines.append("")

    lines.append("}")
    return "\n".join(lines)


def generate_figma_tokens(tokens: dict, meta: dict = None) -> str:
    """Generate Figma Tokens Studio compatible JSON."""
    meta = meta or {}
    figma = {}

    for var, val in tokens.items():
        # Strip --semi- prefix for Figma key
        key = var.replace("--", "").replace("semi-", "semi-")

        # Determine token type
        if "color" in var or "bg-" in var or "text-" in var or "border" in var:
            token_type = "color"
        elif "radius" in var:
            token_type = "borderRadius"
        elif "shadow" in var:
            token_type = "boxShadow"
        elif "font-family" in var:
            token_type = "fontFamilies"
        elif "font-size" in var:
            token_type = "fontSizes"
        else:
            token_type = "other"

        figma[key] = {"value": val, "type": token_type}

    result = {
        "_metadata": {
            "source": meta.get("url", ""),
            "title": meta.get("title", ""),
            "generated_by": "UX Master — Semi-Sync Harvester",
            "timestamp": meta.get("timestamp", ""),
        },
        **figma
    }

    return json.dumps(result, indent=2, ensure_ascii=False)


def generate_summary(tokens: dict, meta: dict = None) -> str:
    """Generate human-readable markdown summary."""
    meta = meta or {}
    url = meta.get("url", "unknown")
    title = meta.get("title", "")
    total = len(tokens)

    lines = [
        f"# Semi-Sync Harvest Report",
        "",
        f"**Source:** {url}",
        f"**Title:** {title}",
        f"**Total Tokens Extracted:** {total}",
        "",
        "## Token Mapping",
        "",
        "| Semi Variable | Value |",
        "|---|---|",
    ]

    for var, val in sorted(tokens.items()):
        lines.append(f"| `{var}` | `{val}` |")

    lines.extend([
        "",
        "## Usage",
        "",
        "1. **CSS Override:** Import `semi-theme-override.css` to override Semi Design defaults",
        "2. **Figma Tokens:** Import `figma-tokens.json` into Tokens Studio → Semi Figma Plugin",
        "3. **React Components:** Use `@douyinfe/semi-ui` with the CSS override, components auto-inherit theme",
    ])

    return "\n".join(lines)


# ============ CLI ============

if __name__ == "__main__":
    import argparse
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Semi Token Compiler")
    parser.add_argument("--input", "-i", help="Input JSON file (harvester output)")
    parser.add_argument("--output", "-o", default=None, help="Output CSS file")
    parser.add_argument("--figma", "-f", default=None, help="Output Figma tokens file")
    parser.add_argument("--project", "-p", default=None, help="Project slug (saves to output/<slug>/)")
    parser.add_argument("--summary", "-s", action="store_true", help="Print markdown summary")
    parser.add_argument("--test", action="store_true", help="Run with sample data")

    args = parser.parse_args()

    if args.test:
        sample = {
            "meta": {"url": "https://example.com", "timestamp": "test", "title": "Test"},
            "colors": {"primary": "rgb(23, 92, 211)", "success": "rgb(16, 185, 129)"},
            "surfaces": {"app_bg": "rgb(244, 246, 248)", "card_bg": "rgb(255, 255, 255)"},
            "typography": {"font_family": "Inter, sans-serif", "body_size": "14px",
                           "title_color": "rgb(15, 23, 42)", "body_color": "rgb(71, 85, 105)"},
            "geometry": {"button_radius": "4px", "card_shadow": "0px 1px 3px rgba(0,0,0,0.1)"}
        }
        tokens = map_to_semi_tokens(sample)
        print(generate_css_override(tokens, sample["meta"]))
        print("\n---\n")
        print(generate_summary(tokens, sample["meta"]))
        sys.exit(0)

    if args.input:
        with open(args.input, "r") as f:
            raw = json.load(f)
    else:
        raw = json.load(sys.stdin)

    meta = raw.get("meta", {})
    tokens = map_to_semi_tokens(raw)

    # Resolve output paths (project-aware)
    if args.project:
        from project_registry import ProjectRegistry
        registry = ProjectRegistry()
        project_dir = registry.get_project_dir(args.project)
        project_dir.mkdir(parents=True, exist_ok=True)
        css_path = args.output or str(project_dir / "semi-theme-override.css")
        figma_path = args.figma or str(project_dir / "figma-tokens.json")

        # Auto-register harvest with project
        manifest = registry.get(args.project)
        if manifest:
            registry.add_page_harvest(args.project, raw)
    else:
        css_path = args.output or "semi-theme-override.css"
        figma_path = args.figma or "figma-tokens.json"

    # Write CSS
    css = generate_css_override(tokens, meta)
    with open(css_path, "w") as f:
        f.write(css)
    print(f"[OK] CSS written to {css_path}")

    # Write Figma JSON
    figma = generate_figma_tokens(tokens, meta)
    with open(figma_path, "w") as f:
        f.write(figma)
    print(f"[OK] Figma tokens written to {figma_path}")

    # Summary
    if args.summary:
        print("\n" + generate_summary(tokens, meta))

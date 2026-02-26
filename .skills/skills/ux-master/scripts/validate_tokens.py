#!/usr/bin/env python3
"""
Token Validator — Checks extracted design tokens for common issues.

Validates:
1. Neutral scale has distinct gradients (not all same shade)
2. Text hierarchy is correct (text-0 darkest → text-3 lightest)
3. Semantic colors use strong saturated base (not background tint)
4. Primary color is a plausible brand color (not white/black/gray)
5. All required Semi Design tokens are present

Usage:
    python3 validate_tokens.py --input design-system.css
    python3 validate_tokens.py --input tokens.json --format json
"""

import json
import re
import sys
import colorsys
from pathlib import Path


def hex_to_rgb(hex_str: str) -> tuple:
    """Convert hex color to (r, g, b) tuple."""
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    if len(hex_str) < 6:
        return (0, 0, 0)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def luminance(hex_str: str) -> float:
    """Calculate relative luminance (0-255 scale)."""
    r, g, b = hex_to_rgb(hex_str)
    return 0.299 * r + 0.587 * g + 0.114 * b


def saturation(hex_str: str) -> float:
    """Calculate HSL saturation (0-1 scale)."""
    r, g, b = hex_to_rgb(hex_str)
    _, s, _ = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return s


def parse_css_tokens(css_content: str) -> dict:
    """Parse CSS custom properties from CSS content."""
    tokens = {}
    pattern = r'(--semi-[a-zA-Z0-9-]+)\s*:\s*([^;]+);'
    for match in re.finditer(pattern, css_content):
        tokens[match.group(1)] = match.group(2).strip()
    return tokens


def parse_json_tokens(json_content: str) -> dict:
    """Parse tokens from JSON format."""
    data = json.loads(json_content)
    if isinstance(data, dict):
        # Flat dict or nested
        tokens = {}
        for key, value in data.items():
            if key.startswith("--semi-"):
                tokens[key] = value
            elif isinstance(value, dict):
                for subkey, subval in value.items():
                    if isinstance(subval, str):
                        tokens[f"--semi-{key}-{subkey}"] = subval
        return tokens
    return {}


class TokenValidator:
    """Validate design tokens for common issues."""

    REQUIRED_TOKENS = [
        "--semi-color-primary",
        "--semi-color-bg-0",
        "--semi-color-bg-1",
        "--semi-color-text-0",
        "--semi-color-text-1",
        "--semi-color-border",
        "--semi-font-family-regular",
        "--semi-font-size-regular",
        "--semi-border-radius-medium",
    ]

    def __init__(self, tokens: dict):
        self.tokens = tokens
        self.issues = []
        self.warnings = []
        self.passed = []

    def validate_all(self) -> dict:
        """Run all validations and return report."""
        self._check_required_tokens()
        self._check_neutral_scale()
        self._check_text_hierarchy()
        self._check_semantic_colors()
        self._check_primary_color()
        self._check_background_levels()

        return {
            "total_tokens": len(self.tokens),
            "issues": self.issues,
            "warnings": self.warnings,
            "passed": self.passed,
            "score": self._calculate_score(),
        }

    def _check_required_tokens(self):
        """Check all required Semi Design tokens are present."""
        missing = [t for t in self.REQUIRED_TOKENS if t not in self.tokens]
        if missing:
            self.issues.append({
                "type": "missing_tokens",
                "message": f"Missing {len(missing)} required tokens",
                "details": missing,
            })
        else:
            self.passed.append("All required tokens present")

    def _check_neutral_scale(self):
        """Check neutral scale has distinct gradient."""
        neutrals = {}
        for key, value in self.tokens.items():
            if "neutral" in key and value.startswith("#"):
                match = re.search(r'neutral-(\d+)', key)
                if match:
                    neutrals[int(match.group(1))] = value

        if len(neutrals) < 3:
            self.warnings.append({
                "type": "insufficient_neutrals",
                "message": "Less than 3 neutral scale values found",
            })
            return

        lum_values = [(k, luminance(v)) for k, v in sorted(neutrals.items())]

        # Check range
        lum_range = max(l for _, l in lum_values) - min(l for _, l in lum_values)
        if lum_range < 100:
            self.issues.append({
                "type": "flat_neutral_scale",
                "message": f"Neutral scale lacks contrast (luminance range: {lum_range:.0f}, need >100)",
                "details": {str(k): f"{v} (lum={luminance(v):.0f})" for k, v in sorted(neutrals.items())},
                "fix": "Manually add dark neutrals (700=#374151, 800=#1F2937, 900=#111827)",
            })
        else:
            self.passed.append(f"Neutral scale has good contrast (range: {lum_range:.0f})")

    def _check_text_hierarchy(self):
        """Check text-0 is darkest, text-3 is lightest."""
        text_tokens = {}
        for i in range(4):
            key = f"--semi-color-text-{i}"
            if key in self.tokens and self.tokens[key].startswith("#"):
                text_tokens[i] = self.tokens[key]

        if len(text_tokens) < 2:
            return

        lums = {k: luminance(v) for k, v in text_tokens.items()}

        # text-0 should have lowest luminance (darkest)
        if 0 in lums and max(lums.keys()) in lums:
            if lums[0] > lums[max(lums.keys())]:
                self.issues.append({
                    "type": "inverted_text_hierarchy",
                    "message": "Text hierarchy inverted: text-0 is lighter than text-3",
                    "details": {f"text-{k}": f"{v} (lum={lums[k]:.0f})" for k, v in text_tokens.items()},
                    "fix": "Swap text-0 and text-3 values (text-0 should be darkest)",
                })
            else:
                self.passed.append("Text hierarchy correct (text-0 darkest)")

    def _check_semantic_colors(self):
        """Check semantic colors are saturated (not background tints)."""
        semantics = {
            "success": "--semi-color-success",
            "warning": "--semi-color-warning",
            "danger": "--semi-color-danger",
        }

        for name, key in semantics.items():
            if key in self.tokens and self.tokens[key].startswith("#"):
                sat = saturation(self.tokens[key])
                lum = luminance(self.tokens[key])

                if sat < 0.3 and lum > 200:
                    self.warnings.append({
                        "type": "weak_semantic_color",
                        "message": f"{name} color ({self.tokens[key]}) looks like a background tint (low saturation: {sat:.2f})",
                        "fix": f"Use a more saturated {name} color (saturation should be > 0.5)",
                    })
                else:
                    self.passed.append(f"{name} color is properly saturated ({sat:.2f})")

    def _check_primary_color(self):
        """Check primary color is a plausible brand color."""
        key = "--semi-color-primary"
        if key not in self.tokens:
            return

        value = self.tokens[key]
        if not value.startswith("#"):
            return

        lum = luminance(value)
        sat = saturation(value)

        if lum > 240:
            self.issues.append({
                "type": "primary_too_light",
                "message": f"Primary color ({value}) is nearly white (luminance: {lum:.0f})",
                "fix": "Check source site for the actual brand color",
            })
        elif lum < 15:
            self.issues.append({
                "type": "primary_too_dark",
                "message": f"Primary color ({value}) is nearly black (luminance: {lum:.0f})",
                "fix": "Check source site for the actual brand color",
            })
        elif sat < 0.2:
            self.warnings.append({
                "type": "primary_desaturated",
                "message": f"Primary color ({value}) has low saturation ({sat:.2f}), may be a gray",
                "fix": "Verify this is the intended brand color",
            })
        else:
            self.passed.append(f"Primary color looks good ({value}, sat={sat:.2f})")

    def _check_background_levels(self):
        """Check background levels have proper ordering."""
        bgs = {}
        for i in range(5):
            key = f"--semi-color-bg-{i}"
            if key in self.tokens and self.tokens[key].startswith("#"):
                bgs[i] = self.tokens[key]

        if len(bgs) >= 2:
            lums = {k: luminance(v) for k, v in bgs.items()}
            # In light mode, bg-0 should be lightest (highest luminance)
            if 0 in lums and 4 in lums:
                if lums[0] < lums[4]:
                    self.warnings.append({
                        "type": "bg_ordering",
                        "message": "Background levels may be inverted (bg-0 is darker than bg-4)",
                    })
                else:
                    self.passed.append("Background levels ordered correctly")

    def _calculate_score(self) -> int:
        """Calculate overall quality score (0-100)."""
        total_checks = len(self.issues) + len(self.warnings) + len(self.passed)
        if total_checks == 0:
            return 50

        score = 100
        score -= len(self.issues) * 15
        score -= len(self.warnings) * 5
        return max(0, min(100, score))

    def print_report(self):
        """Print formatted validation report."""
        report = self.validate_all()

        print(f"\n{'='*60}")
        print(f"  Token Validation Report")
        print(f"  Total tokens: {report['total_tokens']}")
        print(f"  Score: {report['score']}/100")
        print(f"{'='*60}\n")

        if report['passed']:
            print("✅ PASSED:")
            for p in report['passed']:
                print(f"   • {p}")
            print()

        if report['warnings']:
            print("⚠️  WARNINGS:")
            for w in report['warnings']:
                print(f"   • {w['message']}")
                if 'fix' in w:
                    print(f"     Fix: {w['fix']}")
            print()

        if report['issues']:
            print("❌ ISSUES:")
            for i in report['issues']:
                print(f"   • {i['message']}")
                if 'fix' in i:
                    print(f"     Fix: {i['fix']}")
                if 'details' in i and isinstance(i['details'], list):
                    for d in i['details'][:5]:
                        print(f"       - {d}")
            print()

        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate design tokens")
    parser.add_argument("--input", "-i", required=True, help="Token file (CSS or JSON)")
    parser.add_argument("--format", "-f", choices=["css", "json", "auto"], default="auto")
    parser.add_argument("--json-output", "-o", help="Write report as JSON")
    args = parser.parse_args()

    path = Path(args.input)
    content = path.read_text()

    fmt = args.format
    if fmt == "auto":
        fmt = "json" if path.suffix == ".json" else "css"

    if fmt == "json":
        tokens = parse_json_tokens(content)
    else:
        tokens = parse_css_tokens(content)

    if not tokens:
        print(f"❌ No tokens found in {path}")
        sys.exit(1)

    validator = TokenValidator(tokens)
    report = validator.print_report()

    if args.json_output:
        Path(args.json_output).write_text(json.dumps(report, indent=2))
        print(f"Report saved to {args.json_output}")

    sys.exit(0 if report['score'] >= 70 else 1)


if __name__ == "__main__":
    main()

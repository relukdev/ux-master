#!/usr/bin/env python3
"""Tests for design_doc_generator.py — CSS extraction and quality."""
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from design_doc_generator import generate_doc_html, generate_doc_files

SAMPLE_TOKENS = {
    "--semi-color-primary": "#2463EB",
    "--semi-color-success": "#10B981",
    "--semi-color-warning": "#F59E0B",
    "--semi-color-danger": "#EF4444",
    "--semi-color-border": "#E5E7EB",
    "--semi-color-text-0": "#111827",
    "--semi-color-text-1": "#4B5563",
    "--semi-color-bg-1": "#FFFFFF",
    "--semi-border-radius-medium": "8px",
    "--semi-border-radius-large": "16px",
    "--semi-shadow-elevated": "0 1px 3px rgba(0,0,0,0.1)",
    "--semi-font-family-regular": "Inter, sans-serif",
    "--semi-font-size-regular": "14px",
}

SAMPLE_META = {"name": "TestApp", "url": "https://test.com"}


class TestNoInlineStyles(unittest.TestCase):
    """Components section must not have inline style= attributes."""

    def setUp(self):
        self.html = generate_doc_html(SAMPLE_TOKENS, {}, SAMPLE_META)
        # Extract components section
        self.comp_section = self.html.split("Components Preview")[1].split("Token Reference")[0]

    def test_no_style_attributes_in_components(self):
        """Only allowed style= is on the .comp-preview root container."""
        styles = re.findall(r'style="[^"]*"', self.comp_section)
        # Only the root comp-preview uses style for custom properties
        self.assertLessEqual(len(styles), 1, f"Found {len(styles)} inline styles")
        if styles:
            self.assertIn("--cp-", styles[0], "Root style should set custom properties")


class TestCSSComponentClasses(unittest.TestCase):
    """CSS must contain all required component classes."""

    def setUp(self):
        self.html = generate_doc_html(SAMPLE_TOKENS, {}, SAMPLE_META)

    def test_btn_classes(self):
        for cls in ["comp-btn-primary", "comp-btn-outline", "comp-btn-danger", "comp-btn-sm", "comp-btn-lg"]:
            self.assertIn(cls, self.html, f"Missing CSS class: {cls}")

    def test_tag_variants(self):
        for variant in ["primary", "success", "warning", "danger", "info"]:
            self.assertIn(f"comp-tag--{variant}", self.html, f"Missing tag variant: {variant}")

    def test_nav_classes(self):
        self.assertIn("comp-nav-item", self.html)
        self.assertIn("comp-nav-item--active", self.html)

    def test_table_classes(self):
        self.assertIn("comp-table-wrap", self.html)
        self.assertIn("comp-table", self.html)

    def test_form_classes(self):
        self.assertIn("comp-select", self.html)
        self.assertIn("comp-card-demo", self.html)


class TestCSSQuality(unittest.TestCase):
    """CSS follows frontend-design best practices."""

    def setUp(self):
        self.html = generate_doc_html(SAMPLE_TOKENS, {}, SAMPLE_META)

    def test_reduced_motion(self):
        self.assertIn("prefers-reduced-motion", self.html)

    def test_css_custom_properties(self):
        self.assertIn("var(--cp-", self.html)

    def test_color_mix_for_tags(self):
        self.assertIn("color-mix", self.html)

    def test_hover_states(self):
        self.assertIn(":hover", self.html)

    def test_active_states(self):
        self.assertIn(":active", self.html)

    def test_focus_input_state(self):
        self.assertIn("comp-input:focus", self.html)

    def test_transition_properties(self):
        self.assertIn("transition:", self.html)


class TestMultiFileOutput(unittest.TestCase):
    """generate_doc_files() produces correct file structure."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.result = generate_doc_files(SAMPLE_TOKENS, {}, SAMPLE_META, str(self.tmp_dir))

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_creates_html(self):
        self.assertTrue((self.tmp_dir / "design-system.html").exists())

    def test_creates_css(self):
        self.assertTrue((self.tmp_dir / "design-system.css").exists())

    def test_creates_js(self):
        self.assertTrue((self.tmp_dir / "design-system.js").exists())

    def test_html_links_css(self):
        html = (self.tmp_dir / "design-system.html").read_text()
        self.assertIn('<link rel="stylesheet" href="design-system.css">', html)

    def test_html_links_js(self):
        html = (self.tmp_dir / "design-system.html").read_text()
        self.assertIn('<script src="design-system.js">', html)

    def test_html_no_inline_style_tag(self):
        html = (self.tmp_dir / "design-system.html").read_text()
        self.assertNotIn("<style>", html)

    def test_css_has_content(self):
        css = (self.tmp_dir / "design-system.css").read_text()
        self.assertGreater(len(css), 1000)
        self.assertIn(".comp-btn-primary", css)

    def test_js_has_content(self):
        js = (self.tmp_dir / "design-system.js").read_text()
        self.assertIn("toggleTheme", js)

    def test_return_dict(self):
        self.assertIn("html", self.result)
        self.assertIn("css", self.result)
        self.assertIn("js", self.result)


class TestBackwardCompatibility(unittest.TestCase):
    """Single-file mode still works as before."""

    def test_embedded_html_has_style_tag(self):
        html = generate_doc_html(SAMPLE_TOKENS, {}, SAMPLE_META)
        self.assertIn("<style>", html)

    def test_embedded_html_has_script_tag(self):
        html = generate_doc_html(SAMPLE_TOKENS, {}, SAMPLE_META)
        self.assertIn("<script>", html)

    def test_valid_html_structure(self):
        html = generate_doc_html(SAMPLE_TOKENS, {}, SAMPLE_META)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("</html>", html)

    def test_project_name_in_output(self):
        html = generate_doc_html(SAMPLE_TOKENS, {}, SAMPLE_META)
        self.assertIn("TestApp", html)


if __name__ == "__main__":
    unittest.main()

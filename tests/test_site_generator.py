#!/usr/bin/env python3
"""Tests for site_generator.py — Design System Guideline Site."""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from site_generator import SiteGenerator

SAMPLE_DESIGN_SYSTEM = {
    "name": "TestApp Design System",
    "colors": {
        "primary": "#4F46E5",
        "success": "#10B981",
        "warning": "#F59E0B",
        "danger": "#EF4444",
    },
    "typography": {
        "font-weight-regular": "400",
        "font-weight-bold": "700",
    },
    "spacing": {
        "tight": "8px",
        "base": "16px",
        "loose": "24px",
    },
    "borders": {
        "radius-sm": "3px",
        "radius-md": "6px",
    },
    "shadows": {
        "sm": "0 0 1px rgba(0,0,0,0.1)",
    },
    "components": {},
}

SAMPLE_META = {
    "name": "TestApp",
    "url": "https://testapp.com",
    "slug": "testapp",
    "created_at": "2026-01-01T00:00:00Z",
}

SAMPLE_TOKENS = {
    "--semi-color-primary": "#4F46E5",
    "--semi-color-success": "#10B981",
    "--semi-color-warning": "#F59E0B",
    "--semi-color-danger": "#EF4444",
    "--semi-font-family-regular": "Inter, sans-serif",
    "--semi-font-size-regular": "14px",
    "--semi-border-radius-medium": "6px",
}

SAMPLE_COMPONENTS = {
    "button": {
        "component.tsx": "export const Button = () => {};",
        "index.ts": "export { Button } from './button';",
    },
    "card": {
        "component.tsx": "export const Card = () => {};",
        "index.ts": "export { Card } from './card';",
    },
}


class TestSiteGeneratorOutput(unittest.TestCase):
    """Site generator produces correct file structure."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.gen = SiteGenerator(
            design_system=SAMPLE_DESIGN_SYSTEM,
            tokens=SAMPLE_TOKENS,
            meta=SAMPLE_META,
            output_dir=self.tmp_dir,
            components=SAMPLE_COMPONENTS,
        )
        self.gen.generate()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_index_html_exists(self):
        self.assertTrue((self.tmp_dir / "index.html").exists())

    def test_tokens_html_exists(self):
        self.assertTrue((self.tmp_dir / "tokens.html").exists())

    def test_components_html_exists(self):
        self.assertTrue((self.tmp_dir / "components.html").exists())

    def test_css_exists(self):
        self.assertTrue((self.tmp_dir / "css" / "style.css").exists())

    def test_js_exists(self):
        self.assertTrue((self.tmp_dir / "js" / "app.js").exists())


class TestSiteContent(unittest.TestCase):
    """Generated pages have correct content."""

    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.gen = SiteGenerator(
            design_system=SAMPLE_DESIGN_SYSTEM,
            tokens=SAMPLE_TOKENS,
            meta=SAMPLE_META,
            output_dir=self.tmp_dir,
            components=SAMPLE_COMPONENTS,
        )
        self.gen.generate()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def _read(self, filename):
        return (self.tmp_dir / filename).read_text()

    def test_index_has_project_name(self):
        self.assertIn("TestApp", self._read("index.html"))

    def test_index_has_valid_html(self):
        html = self._read("index.html")
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("</html>", html)

    def test_index_has_sidebar(self):
        html = self._read("index.html")
        self.assertIn("sidebar", html.lower())

    def test_tokens_has_color_values(self):
        html = self._read("tokens.html")
        self.assertIn("#4F46E5", html)
        self.assertIn("#10B981", html)

    def test_tokens_has_spacing_values(self):
        html = self._read("tokens.html")
        self.assertIn("8px", html)
        self.assertIn("16px", html)

    def test_tokens_has_copy_functionality(self):
        js = self._read("js/app.js")
        self.assertIn("copy", js.lower())

    def test_components_page_has_component_names(self):
        html = self._read("components.html")
        self.assertIn("button", html.lower())
        self.assertIn("card", html.lower())

    def test_all_pages_have_dark_mode(self):
        for page in ["index.html", "tokens.html", "components.html"]:
            html = self._read(page)
            self.assertIn("dark", html.lower(), f"{page} missing dark mode")

    def test_all_pages_have_navigation_links(self):
        for page in ["index.html", "tokens.html", "components.html"]:
            html = self._read(page)
            self.assertIn("tokens.html", html, f"{page} missing tokens link")
            self.assertIn("components.html", html, f"{page} missing components link")

    def test_all_pages_have_responsive_meta(self):
        for page in ["index.html", "tokens.html", "components.html"]:
            html = self._read(page)
            self.assertIn("viewport", html, f"{page} missing viewport meta")


class TestSiteMinimalInput(unittest.TestCase):
    """Handles minimal input without crashing."""

    def test_empty_design_system(self):
        tmp_dir = Path(tempfile.mkdtemp())
        try:
            gen = SiteGenerator(
                design_system={},
                tokens={},
                meta={"name": "Empty", "slug": "empty"},
                output_dir=tmp_dir,
            )
            gen.generate()
            self.assertTrue((tmp_dir / "index.html").exists())
            self.assertTrue((tmp_dir / "tokens.html").exists())
            self.assertTrue((tmp_dir / "components.html").exists())
        finally:
            shutil.rmtree(tmp_dir)

    def test_no_components(self):
        tmp_dir = Path(tempfile.mkdtemp())
        try:
            gen = SiteGenerator(
                design_system=SAMPLE_DESIGN_SYSTEM,
                tokens=SAMPLE_TOKENS,
                meta=SAMPLE_META,
                output_dir=tmp_dir,
            )
            gen.generate()
            html = (tmp_dir / "components.html").read_text()
            self.assertIn("<!DOCTYPE html>", html)
        finally:
            shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    unittest.main()

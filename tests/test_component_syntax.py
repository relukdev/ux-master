#!/usr/bin/env python3
"""Tests that generated components have valid syntax."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from component_generator import generate_semi_component, generate_react_component


class TestSemiComponentSyntax(unittest.TestCase):
    """Semi Design component generation produces valid TSX."""

    def _generate(self, name="TestButton", semi_component="Button"):
        return generate_semi_component(
            name=name, interface_name=name,
            semi_component=semi_component,
            props="children: React.ReactNode;",
            prop_destructure="children",
            style="{}", source="test", timestamp="2026-01-01"
        )

    def test_forwardref_has_opening_brace(self):
        """forwardRef callback must destructure with ({ ... })."""
        code = self._generate()
        # Normalize whitespace for checking
        flat = " ".join(code.split())
        self.assertIn("(( {", flat, "Missing opening brace in destructure")

    def test_no_double_closing_brace_paren(self):
        """Must not have }});  — should be });"""
        code = self._generate()
        self.assertNotIn("}});", code, "Double closing }}) found")

    def test_valid_forwardref_closing(self):
        """forwardRef must close with });"""
        code = self._generate()
        self.assertIn("});", code)

    def test_no_name_collision_different_name(self):
        """Exported name != imported Semi component name avoids collision."""
        code = self._generate(name="HxButton", semi_component="Button")
        self.assertIn("export const HxButton", code)
        self.assertIn('import { Button }', code)

    def test_has_required_structure(self):
        """Component must have interface, export, forwardRef, displayName."""
        code = self._generate(name="TestCard", semi_component="Card")
        self.assertIn("export interface TestCardProps", code)
        self.assertIn("export const TestCard", code)
        self.assertIn("React.forwardRef", code)
        self.assertIn('.displayName = "TestCard"', code)


class TestReactComponentSyntax(unittest.TestCase):
    """React + Tailwind component generation produces valid TSX."""

    def _generate(self, name="TestButton"):
        return generate_react_component(
            name=name, interface_name=name,
            element_type="button",
            props="children: React.ReactNode;",
            prop_destructure="children",
            base_classes='"btn"',
            source="test", timestamp="2026-01-01"
        )

    def test_forwardref_has_opening_brace(self):
        code = self._generate()
        flat = " ".join(code.split())
        self.assertIn("(( {", flat, "Missing opening brace in destructure")

    def test_no_double_closing_brace_paren(self):
        code = self._generate()
        self.assertNotIn("}});", code, "Double closing }}) found")

    def test_valid_forwardref_closing(self):
        code = self._generate()
        self.assertIn("});", code)

    def test_has_required_structure(self):
        code = self._generate(name="TestInput")
        self.assertIn("export interface TestInputProps", code)
        self.assertIn("export const TestInput", code)
        self.assertIn("React.forwardRef", code)
        self.assertIn('.displayName = "TestInput"', code)


if __name__ == "__main__":
    unittest.main()

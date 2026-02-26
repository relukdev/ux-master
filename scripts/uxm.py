#!/usr/bin/env python3
"""
UX Master — Unified Orchestrator

Cross-platform entry point that works with any AI coding tool:
Claude Code, Antigravity, Gemini CLI, OpenCode, Cursor, etc.

Runs the full pipeline: Extract → Map → Index → Generate → Document → Package

Usage:
    # From URL
    python3 scripts/uxm.py https://example.com --project myapp

    # From source directory
    python3 scripts/uxm.py --source ./src --project myapp

    # Validate existing tokens
    python3 scripts/uxm.py --validate output/myapp/design-system.css

    # Preview tokens
    python3 scripts/uxm.py --preview output/myapp/design-system.css --name "MyApp"

    # Search design patterns
    python3 scripts/uxm.py --search "fintech dashboard" --domain ux-laws

Author: UX Master AI
Version: 4.0.0
"""

import argparse
import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
SKILL_SCRIPTS = PROJECT_ROOT / ".skills" / "skills" / "ux-master" / "scripts"


def run_cmd(cmd: list, desc: str = "", check: bool = True) -> subprocess.CompletedProcess:
    """Run a command with status output."""
    print(f"\n{'='*60}")
    print(f"  {desc or ' '.join(cmd[:3])}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, capture_output=False, text=True, cwd=str(PROJECT_ROOT))
    if check and result.returncode != 0:
        print(f"  ⚠️  Command exited with code {result.returncode}")
    return result


def pipeline_url(url: str, project: str, framework: str = "semi", crawl: bool = False, max_pages: int = 1):
    """Run full pipeline from URL."""
    output_dir = PROJECT_ROOT / "output" / project
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  UX Master v4 — Design System Pipeline                       ║
║  Source: {url[:50]:<50} ║
║  Project: {project:<49} ║
║  Framework: {framework:<47} ║
╚══════════════════════════════════════════════════════════════╝
""")

    # Phase 1: Extract
    extract_cmd = [
        sys.executable, str(SCRIPTS_DIR / "harvester_browser.py"),
        "--url", url, "--output", str(output_dir)
    ]
    if crawl:
        extract_cmd.extend(["--crawl", "--max-pages", str(max_pages)])
    run_cmd(extract_cmd, f"Phase 1/6: Extracting tokens from {url}")

    harvest_file = output_dir / "harvest-v4-raw.json"
    if not harvest_file.exists():
        # Try alternate names
        for alt in ["harvest.json", "harvest-raw.json"]:
            alt_path = output_dir / alt
            if alt_path.exists():
                harvest_file = alt_path
                break
        else:
            print(f"  ❌ No harvest file found in {output_dir}")
            return False

    # Phase 2: Map to Semi Design tokens
    run_cmd([
        sys.executable, str(SCRIPTS_DIR / "token_mapper.py"),
        "-i", str(harvest_file), "--project", project
    ], "Phase 2/6: Mapping to Semi Design tokens")

    # Phase 3: Build design system index
    run_cmd([
        sys.executable, str(SCRIPTS_DIR / "design_system_indexer.py"),
        "--input", str(harvest_file),
        "--name", project,
        "--output", str(output_dir)
    ], "Phase 3/6: Building design system index")

    # Phase 4: Generate components
    ds_file = output_dir / "design-system.json"
    if ds_file.exists():
        run_cmd([
            sys.executable, str(SCRIPTS_DIR / "component_generator.py"),
            "--input", str(ds_file),
            "--all",
            "--output", str(output_dir / "components"),
            "--framework", framework
        ], f"Phase 4/6: Generating {framework} components")
    else:
        print(f"  ⚠️  Skipping component generation — {ds_file} not found")

    # Phase 5: Generate documentation
    run_cmd([
        sys.executable, str(SCRIPTS_DIR / "design_doc_generator.py"),
        "-i", str(harvest_file),
        "-o", str(output_dir / "design-system.html")
    ], "Phase 5/6: Generating documentation site")

    # Phase 6: Validate tokens
    css_file = output_dir / "design-system.css"
    if css_file.exists() and SKILL_SCRIPTS.exists():
        run_cmd([
            sys.executable, str(SKILL_SCRIPTS / "validate_tokens.py"),
            "-i", str(css_file)
        ], "Phase 6/6: Validating tokens")

    # Summary
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ Pipeline Complete!                                        ║
║                                                              ║
║  Output directory: {str(output_dir):<40} ║
║                                                              ║
║  Files generated:                                            ║
║  • harvest-v4-raw.json  — Raw extraction data                ║
║  • design-system.json   — Indexed design system              ║
║  • design-system.css    — CSS variables (Semi spec)          ║
║  • design-system.html   — Interactive documentation          ║
║  • components/          — React TypeScript components        ║
╚══════════════════════════════════════════════════════════════╝
""")
    return True


def pipeline_source(source_dir: str, project: str, framework: str = "semi"):
    """Run pipeline from source code directory."""
    output_dir = PROJECT_ROOT / "output" / project
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  UX Master v4 — Source Code Extraction                       ║
║  Source: {source_dir[:50]:<50} ║
║  Project: {project:<49} ║
╚══════════════════════════════════════════════════════════════╝
""")

    # Extract from source
    run_cmd([
        sys.executable, str(SCRIPTS_DIR / "extractor.py"),
        "--directory", source_dir,
        "--output", str(output_dir)
    ], f"Extracting tokens from {source_dir}")

    # Continue with standard pipeline
    harvest_file = output_dir / "harvest.json"
    if not harvest_file.exists():
        for alt in ["harvest-v4-raw.json", "harvest-raw.json"]:
            alt_path = output_dir / alt
            if alt_path.exists():
                harvest_file = alt_path
                break

    if harvest_file.exists():
        run_cmd([
            sys.executable, str(SCRIPTS_DIR / "token_mapper.py"),
            "-i", str(harvest_file), "--project", project
        ], "Mapping to Semi Design tokens")

        run_cmd([
            sys.executable, str(SCRIPTS_DIR / "design_system_indexer.py"),
            "--input", str(harvest_file),
            "--name", project,
            "--output", str(output_dir)
        ], "Building design system index")

        ds_file = output_dir / "design-system.json"
        if ds_file.exists():
            run_cmd([
                sys.executable, str(SCRIPTS_DIR / "component_generator.py"),
                "--input", str(ds_file), "--all",
                "--output", str(output_dir / "components"),
                "--framework", framework
            ], f"Generating {framework} components")

        run_cmd([
            sys.executable, str(SCRIPTS_DIR / "design_doc_generator.py"),
            "-i", str(harvest_file),
            "-o", str(output_dir / "design-system.html")
        ], "Generating documentation")

    print(f"\n✅ Source extraction complete → {output_dir}")
    return True


def validate_tokens(token_file: str):
    """Validate design tokens."""
    if SKILL_SCRIPTS.exists():
        run_cmd([
            sys.executable, str(SKILL_SCRIPTS / "validate_tokens.py"),
            "-i", token_file
        ], f"Validating {token_file}")
    else:
        print("⚠️  Validation script not found at .skills/skills/ux-master/scripts/")


def preview_tokens(token_file: str, name: str = "Design System"):
    """Generate token preview HTML."""
    if SKILL_SCRIPTS.exists():
        output_path = Path(token_file).parent / "preview.html"
        run_cmd([
            sys.executable, str(SKILL_SCRIPTS / "preview_generator.py"),
            "-i", token_file,
            "-o", str(output_path),
            "-n", name
        ], f"Generating preview for {name}")
        print(f"\n📄 Preview: {output_path}")
    else:
        print("⚠️  Preview script not found at .skills/skills/ux-master/scripts/")


def search_patterns(query: str, domain: str = None, n: int = 5):
    """Search design patterns."""
    cmd = [sys.executable, str(SCRIPTS_DIR / "search.py"), query]
    if domain:
        cmd.extend(["--domain", domain])
    cmd.extend(["-n", str(n)])
    run_cmd(cmd, f"Searching: {query}")


def show_info():
    """Show platform info."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║  UX Master v4 — Unified Design System Intelligence          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🎯 Harvester v4    — Extract 120+ tokens from any website  ║
║  🔄 Token Mapper    — Map to Semi Design CSS variables      ║
║  ⚛️  Component Gen   — 22 React/Semi/Vue components         ║
║  📄 Doc Generator   — Interactive documentation site        ║
║  📐 48 UX Laws      — Behavioral psychology design rules    ║
║  ✅ 37 Design Tests  — TDD for design validation            ║
║  🔍 BM25 Search     — 1032+ patterns across 16 domains     ║
║  🎨 Figma Bridge    — Bidirectional token sync              ║
║  🤖 MCP Server      — Claude/Cursor/AI integration          ║
║                                                              ║
║  Platform Support:                                           ║
║  Claude Code • Antigravity • Gemini CLI • OpenCode          ║
║  Cursor • Windsurf • Codex • Any Python 3.x environment     ║
║                                                              ║
║  Config Files:                                               ║
║  • CLAUDE.md   — Claude Code                                ║
║  • AGENTS.md   — Antigravity, Codex, OpenCode, Cursor       ║
║  • GEMINI.md   — Gemini CLI                                 ║
║  • SKILL.md    — Full skill definition                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def main():
    parser = argparse.ArgumentParser(
        description="UX Master v4 — Unified Design System Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/uxm.py https://linear.app --project linear
  python3 scripts/uxm.py --source ./src --project myapp
  python3 scripts/uxm.py --validate output/myapp/design-system.css
  python3 scripts/uxm.py --preview output/myapp/design-system.css --name "MyApp"
  python3 scripts/uxm.py --search "fintech dashboard" --domain ux-laws
  python3 scripts/uxm.py --info
        """
    )

    parser.add_argument("url", nargs="?", help="Website URL to extract from")
    parser.add_argument("--source", "-s", help="Source code directory to extract from")
    parser.add_argument("--project", "-p", default="default", help="Project name/slug")
    parser.add_argument("--framework", "-f", default="semi", choices=["semi", "react", "vue"],
                        help="Component framework (default: semi)")
    parser.add_argument("--crawl", action="store_true", help="Multi-page crawl")
    parser.add_argument("--max-pages", type=int, default=5, help="Max pages to crawl")
    parser.add_argument("--validate", help="Validate a token CSS/JSON file")
    parser.add_argument("--preview", help="Generate preview HTML from tokens")
    parser.add_argument("--name", "-n", default="Design System", help="Project display name")
    parser.add_argument("--search", help="Search design patterns")
    parser.add_argument("--domain", "-d", help="Search domain (ux-laws, design-tests, style, etc.)")
    parser.add_argument("--info", action="store_true", help="Show platform info")

    args = parser.parse_args()

    if args.info:
        show_info()
    elif args.validate:
        validate_tokens(args.validate)
    elif args.preview:
        preview_tokens(args.preview, args.name)
    elif args.search:
        search_patterns(args.search, args.domain)
    elif args.source:
        pipeline_source(args.source, args.project, args.framework)
    elif args.url:
        pipeline_url(args.url, args.project, args.framework, args.crawl, args.max_pages)
    else:
        show_info()
        parser.print_help()


if __name__ == "__main__":
    main()

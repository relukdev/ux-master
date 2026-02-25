#!/usr/bin/env python3
"""
Harvest Session — Merge multiple page harvests into consolidated tokens.

When scanning multiple pages of the same site, each page may reveal different
tokens (e.g., success/danger colors only on order pages, form styles on settings).
This module merges them using voting/frequency strategies and calculates
confidence scores for each token.
"""
import json
from collections import Counter


def merge_harvests(harvests: list) -> dict:
    """Merge multiple page harvests into a single consolidated harvest.

    Strategy:
      - meta: use first harvest's meta, add page_count
      - colors: most frequent value per key (voting)
      - surfaces: union of all found, most frequent value per key
      - typography: first non-empty value per key (body page wins)
      - geometry: most frequent value per key (mode)
    """
    if not harvests:
        return {}
    if len(harvests) == 1:
        return harvests[0]

    merged = {
        "meta": _merge_meta(harvests),
        "colors": _merge_section(harvests, "colors"),
        "surfaces": _merge_section(harvests, "surfaces"),
        "typography": _merge_section(harvests, "typography"),
        "geometry": _merge_section(harvests, "geometry"),
    }
    return merged


def calculate_confidence(harvests: list) -> dict:
    """Score each token by how many pages it appeared on.

    Returns dict of {section: {key: confidence_float}} where
    confidence = appearances / total_pages.
    """
    if not harvests:
        return {}

    total = len(harvests)
    sections = ("colors", "surfaces", "typography", "geometry")
    result = {}

    for section in sections:
        key_counts = Counter()
        for h in harvests:
            for key in h.get(section, {}):
                key_counts[key] += 1
        result[section] = {key: round(count / total, 2) for key, count in key_counts.items()}

    return result


def merge_with_confidence(harvests: list) -> dict:
    """Merge harvests and attach confidence scores."""
    merged = merge_harvests(harvests)
    confidence = calculate_confidence(harvests)
    merged["_confidence"] = confidence
    return merged


def _merge_meta(harvests: list) -> dict:
    """Merge meta from multiple harvests."""
    first_meta = harvests[0].get("meta", {})
    return {
        "url": first_meta.get("url", ""),
        "timestamp": first_meta.get("timestamp", ""),
        "title": first_meta.get("title", ""),
        "page_count": len(harvests),
        "pages": [h.get("meta", {}).get("url", "") for h in harvests],
    }


def _merge_section(harvests: list, section: str) -> dict:
    """Merge a section using most-frequent-value voting."""
    key_values = {}

    for h in harvests:
        for key, val in h.get(section, {}).items():
            if val:
                key_values.setdefault(key, []).append(val)

    merged = {}
    for key, values in key_values.items():
        counter = Counter(values)
        merged[key] = counter.most_common(1)[0][0]

    return merged


# ============ CLI ============

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Merge multiple harvest JSON files")
    parser.add_argument("files", nargs="+", help="Harvest JSON files to merge")
    parser.add_argument("--output", "-o", default=None, help="Output merged JSON file")
    parser.add_argument("--confidence", action="store_true", help="Include confidence scores")

    args = parser.parse_args()

    harvests = []
    for fp in args.files:
        with open(fp, "r") as f:
            harvests.append(json.load(f))

    if args.confidence:
        result = merge_with_confidence(harvests)
    else:
        result = merge_harvests(harvests)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"[OK] Merged {len(harvests)} harvests → {args.output}")
    else:
        print(output)

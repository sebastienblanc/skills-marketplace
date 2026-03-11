#!/usr/bin/env python3
"""
generate_skills_json.py
-----------------------
Scans all skills/*/SKILL.md files, parses YAML frontmatter, and writes
docs/skills.json for the GitHub Pages marketplace UI.

Usage:
    python scripts/generate_skills_json.py
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"
OUTPUT = ROOT / "docs" / "skills.json"


def parse_frontmatter(text: str) -> dict:
    """Extract and parse YAML frontmatter delimited by '---'."""
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    raw = match.group(1)

    # Minimal YAML parser for the simple structure we use
    result = {}
    current_key = None
    multiline_buf = []

    def flush_multiline():
        if current_key and multiline_buf:
            result[current_key] = " ".join(multiline_buf).strip()
            multiline_buf.clear()

    for line in raw.splitlines():
        # Top-level key: value
        top = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if top and not line.startswith(" "):
            flush_multiline()
            key, val = top.group(1), top.group(2).strip()
            if val == ">":
                current_key = key
            elif val == "":
                # nested block (like metadata:)
                current_key = key
                result[key] = {}
            else:
                result[key] = val
                current_key = None
            continue

        # Nested key under metadata
        nested = re.match(r"^\s{2}(\w[\w-]*):\s*(.*)", line)
        if nested and isinstance(result.get(current_key), dict):
            result[current_key][nested.group(1)] = nested.group(2).strip()
            continue

        # Continuation of multiline value
        if current_key and not isinstance(result.get(current_key), dict):
            stripped = line.strip()
            if stripped:
                multiline_buf.append(stripped)
            current_key = current_key  # keep same key

    flush_multiline()
    return result


def skill_from_path(skill_dir: Path):
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        print(f"  ⚠ Skipping {skill_dir.name}: no SKILL.md found", file=sys.stderr)
        return None

    text = skill_file.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if not fm:
        print(f"  ⚠ Skipping {skill_dir.name}: frontmatter not found", file=sys.stderr)
        return None

    meta = fm.get("metadata", {}) if isinstance(fm.get("metadata"), dict) else {}

    tags_raw = meta.get("tags", "")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    has_reference = (skill_dir / "references" / "REFERENCE.md").exists()

    return {
        "name": fm.get("name", skill_dir.name),
        "description": fm.get("description", ""),
        "license": fm.get("license", ""),
        "author": meta.get("author", ""),
        "tags": tags,
        "icon": meta.get("icon", "🛠️"),
        "difficulty": meta.get("difficulty", ""),
        "hasReference": has_reference,
    }


def main():
    if not SKILLS_DIR.exists():
        print(f"Error: skills directory not found at {SKILLS_DIR}", file=sys.stderr)
        sys.exit(1)

    skills = []
    for entry in sorted(SKILLS_DIR.iterdir()):
        if entry.is_dir():
            print(f"Processing {entry.name}…")
            s = skill_from_path(entry)
            if s:
                skills.append(s)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(skills, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Generated {OUTPUT.relative_to(ROOT)} with {len(skills)} skill(s).")


if __name__ == "__main__":
    main()

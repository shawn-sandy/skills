#!/usr/bin/env python3
"""Fallback Agent Skills spec checker (subset skills-ref validates).

Rules per https://agentskills.io/specification:
- SKILL.md exists with --- delimited YAML frontmatter
- name: 1-64 chars, lowercase kebab (no leading/trailing/double hyphen),
  matches the parent directory name
- description: present, 1-1024 chars
- compatibility: at most 500 chars when present
- no Claude-only leftovers: disable-model-invocation key anywhere,
  CLAUDE_PLUGIN_ROOT anywhere in the skill directory
"""
import glob
import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].split("\n"):
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip('"')
    return fields


def main(root):
    errors = []
    dirs = sorted(d for d in glob.glob(os.path.join(root, "*")) if os.path.isdir(d))
    if not dirs:
        errors.append(f"no skill directories under {root}/")
    for d in dirs:
        rel = os.path.basename(d)
        path = os.path.join(d, "SKILL.md")
        if not os.path.isfile(path):
            errors.append(f"{rel}: missing SKILL.md")
            continue
        fm = frontmatter(open(path).read())
        if fm is None:
            errors.append(f"{rel}: missing or unterminated frontmatter")
            continue
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not (1 <= len(name) <= 64 and NAME_RE.match(name)):
            errors.append(f"{rel}: invalid name {name!r}")
        if name != rel:
            errors.append(f"{rel}: name {name!r} does not match directory")
        if not (1 <= len(desc) <= 1024):
            errors.append(f"{rel}: description length {len(desc)} outside 1-1024")
        if "disable-model-invocation" in fm:
            errors.append(f"{rel}: carries Claude-only key disable-model-invocation")
        if len(fm.get("compatibility", "")) > 500:
            errors.append(f"{rel}: compatibility exceeds 500 chars")
        for f in glob.glob(os.path.join(d, "**", "*"), recursive=True):
            if os.path.isfile(f):
                try:
                    if "CLAUDE_PLUGIN_ROOT" in open(f, errors="replace").read():
                        errors.append(f"{rel}: {os.path.relpath(f, d)} references CLAUDE_PLUGIN_ROOT")
                except OSError:
                    pass
    for e in errors:
        print(f"FAIL {e}")
    if not errors:
        print(f"OK: {len(dirs)} skills pass spec checks")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "skills"))

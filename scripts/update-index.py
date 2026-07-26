#!/usr/bin/env python3
"""Regenerate the skill index table in README.md from skills/*/SKILL.md frontmatter."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
START, END = "<!-- INDEX:START — updated as skills are added -->", "<!-- INDEX:END -->"

rows = ["| Skill | Description |", "|---|---|"]
for path in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
    text = open(path).read()
    name = re.search(r"^name:\s*(.+)$", text, re.M).group(1).strip()
    desc = re.search(r"^description:\s*(.+)$", text, re.M).group(1).strip().strip('"')
    rows.append(f"| [{name}](skills/{name}) | {desc} |")

readme = open(README).read()
if START not in readme or END not in readme:
    sys.exit("README.md is missing the INDEX markers")
head, rest = readme.split(START, 1)
_, tail = rest.split(END, 1)
open(README, "w").write(head + START + "\n" + "\n".join(rows) + "\n" + END + tail)
print(f"README index updated: {len(rows) - 2} skills")

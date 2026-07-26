#!/usr/bin/env bash
# Spec-compliance sweep across every skills/*/ directory.
# Prefers the official skills-ref validator (agentskills/agentskills);
# falls back to the bundled checker implementing the same rules.
set -euo pipefail
cd "$(dirname "$0")/.."

if command -v skills-ref >/dev/null 2>&1; then
  fail=0
  for d in skills/*/; do
    skills-ref validate "$d" || fail=1
  done
  exit "$fail"
fi

exec python3 tests/validate_frontmatter.py skills

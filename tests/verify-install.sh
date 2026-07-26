#!/usr/bin/env bash
# Objective smoke test: one command installs every published skill.
# Installs the repo (local checkout by default, or a repo slug/URL as $1)
# into a throwaway project via the skills CLI for the claude-code target,
# then asserts every skills/*/ directory landed. Cleans up after itself.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
repo="${1:-$root}"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
cd "$tmp"

npx -y skills add "$repo" --agent claude-code --skill '*' -y --copy

missing=0
for d in "$root"/skills/*/; do
  name="$(basename "$d")"
  if [ ! -f "$tmp/.claude/skills/$name/SKILL.md" ]; then
    echo "MISSING: $name"
    missing=1
  fi
done
if [ "$missing" -eq 0 ]; then
  echo "OK: all $(ls -d "$root"/skills/*/ | wc -l | tr -d ' ') skills installed from $repo"
fi
exit "$missing"

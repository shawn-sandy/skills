# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A platform-agnostic [Agent Skills](https://agentskills.io) marketplace installed via `npx skills`. Skills here must run on ~70 agents, not just Claude Code. There is no application code and no build step — markdown content plus a shell and stdlib-Python validation harness. No package manager.

Published skills live in `skills/<name>/SKILL.md` at the repo root, **not** under `.claude/`. Skills may be extracted from `shawn-sandy/agentics` or authored natively here; either way they must pass the portability gate below.

## Commands

```bash
bash tests/validate-all.sh                    # spec sweep — required before opening a PR
python3 tests/validate_frontmatter.py skills  # the same checker, invoked directly
python3 scripts/update-index.py               # regenerate the README skill table
bash tests/verify-install.sh                  # npx install smoke test — slow, needs network
```

Run only `validate-all.sh` locally. `verify-install.sh` hits npm on every run; let CI run it.

## Portability gate

These break non-Claude agents or fail the validator. Never introduce them under `skills/`:

- `disable-model-invocation` in frontmatter.
- The literal string `CLAUDE_PLUGIN_ROOT` anywhere in a skill directory — the validator greps every file in the dir, so even documenting the variable fails.
- `claude` or `anthropic` as a substring of a skill `name` (`claudemd-optimizer` fails).
- Sibling-skill invocation, subagent spawning, plugin hooks or slash commands, plan-mode steps, `$ARGUMENTS`, hardcoded absolute paths.

A skill's directory name must equal its `name:` exactly, in kebab-case. Prefer gerunds (`reviewing-skills`) over verbs (`review-skill`).

## SKILL.md shape

```yaml
---
name: <kebab-case, equals the directory name>
description: "<capability sentence plus a 'Use when ...' trigger>"
allowed-tools: Read, Bash, Grep
license: MIT
metadata:
  author: shawn-sandy
  version: "1.0"
---
```

`description` is third person, one paragraph, no newlines, 1024 chars max. Body has no H1, uses imperative voice, and stays under 500 lines; overflow goes to `references/`, which must be exactly one level deep.

When authoring or reviewing a skill, read `skills/reviewing-skills/references/best-practices.md` first — it holds the full rules and is not loaded automatically.

## Claude plugin marketplace

The repo is also a Claude Code plugin marketplace: `.claude-plugin/marketplace.json`
lists one plugin whose `source` is `"./"`, so the repo root *is* the plugin body and
`.claude-plugin/plugin.json` describes it. Skills are auto-discovered from `skills/` —
never list them individually in either manifest, or the two files drift as skills are
added. Keep `version` in step across both files and bump on release.

Validate with `claude plugin validate .` after editing either manifest. It warns that
root `CLAUDE.md` is not loaded as plugin context; that is expected — this file is repo
guidance, not shipped context.

## Generated files

The README skill table between `<!-- INDEX:START -->` and `<!-- INDEX:END -->` is generated. Run `python3 scripts/update-index.py` after changing any skill's `name` or `description`, and never hand-edit the table. The generator writes each description straight into a Markdown table cell, so a `|` anywhere in a `description` adds a column and corrupts that row — keep pipe characters out of descriptions.

## Releases

Bump a skill's `metadata.version` when its body changes materially. Tag the repo (`v0.1.0` style) on release.

## Known limitation

`skills-ref` is not installed locally or in CI, so `validate-all.sh` always falls back to `tests/validate_frontmatter.py`, a deliberate subset of the full spec check. Passing locally does not prove full spec compliance.

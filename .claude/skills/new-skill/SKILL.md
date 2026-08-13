---
name: new-skill
description: Scaffold a new published skill under skills/ with spec-compliant frontmatter, then validate it and regenerate the README index.
disable-model-invocation: true
---

Scaffold a new marketplace skill named `$ARGUMENTS`.

This skill lives in `.claude/skills/` and is Claude Code tooling for this repo. The `disable-model-invocation` key is correct here and must never be copied into a published skill under `skills/` — the validator rejects it there.

## 0. Load the authoring rules

Read `skills/reviewing-skills/references/best-practices.md` before writing anything. It holds the full spec rules and is not loaded automatically, so a skill written without it can pass the bundled checker and still violate the spec.

## 1. Check the name

Reject and ask for a different name if any of these fail:

- Not kebab-case matching `^[a-z0-9]+(-[a-z0-9]+)*$`, or over 64 chars.
- Contains `claude` or `anthropic` as a substring anywhere.
- `skills/<name>/` already exists.

Suggest a gerund form (`reviewing-tests`, not `review-test`) if the name is a bare verb phrase.

## 2. Ask what the skill does

Get from the user, in one batched question if possible:

- The capability, in one sentence.
- When an agent should reach for it — the "Use when …" trigger.
- Which tools it needs, for `allowed-tools`.

Write the `description` as a single third-person paragraph, no newlines, 1024 chars max: capability sentence first, then a `Use when …` clause. No `|` characters — `scripts/update-index.py` writes the description straight into a Markdown table cell, and a pipe silently adds a column. Add a scope-exclusion clause when the trigger could collide with an existing skill — check `skills/*/SKILL.md` descriptions for overlap before settling on wording.

## 3. Write skills/<name>/SKILL.md

```yaml
---
name: <name>
description: "<capability sentence. Use when ...>"
allowed-tools: <comma-separated>
license: MIT
metadata:
  author: shawn-sandy
  version: "1.0"
---
```

Body rules: no H1, imperative voice, under 500 lines. No `$ARGUMENTS`, no absolute paths, no plan-mode steps, no spawning subagents or calling sibling skills. Avoid time-sensitive phrasing such as "currently" or "as of 2024". Fully qualify any MCP tool as `ServerName:tool_name`.

`CLAUDE_PLUGIN_ROOT` must not appear anywhere under `skills/<name>/`. The validator greps every file in the directory for that literal, so a skill that merely documents the variable fails — never copy this rule's wording into the skill itself.

Move anything over ~500 lines into `skills/<name>/references/<topic>.md` — exactly one level deep, with a table of contents if the reference exceeds 100 lines.

## 4. Validate and index

```bash
bash tests/validate-all.sh
python3 scripts/update-index.py
```

Both must succeed. `validate-all.sh` prints `FAIL <reason>` lines and exits non-zero on any violation — fix the skill rather than the validator. Then confirm `git diff README.md` shows the new row inside the `INDEX:START`/`INDEX:END` block.

Report the created path and the validator output. Do not commit.

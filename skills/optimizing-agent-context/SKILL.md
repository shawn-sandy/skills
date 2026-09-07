---
name: optimizing-agent-context
description: "Optimizes what a project loads into every coding-agent session. Counts which skills, plugins, slash commands, and subagents past sessions actually invoked, prunes the rest from the load set, then tightens CLAUDE.md against the same data by deleting dead references, replacing ignored always-do rules with hooks, and pinning the skills that carry the dev cycle in a short table. Use when the user asks to optimize their agent setup or project context, prune unused skills or plugins, audit skill usage, or slim down CLAUDE.md."
allowed-tools: AskUserQuestion, Bash, Edit, Glob, Grep, Read, Write
license: MIT
compatibility: Reads Claude Code session logs under ~/.claude/projects, the enabledPlugins block of .claude/settings.json, and CLAUDE.md with .claude/rules (Claude Code conventions); the bundled counter needs Python 3; runs on any agent that can edit files.
metadata:
  author: shawn-sandy
  version: "1.0"
---

Two things load into every session before any work starts: the description of every enabled
skill, capped to a fixed share of the context window, and the project CLAUDE.md, re-read on
every turn. Both fill up with entries nobody uses and rules nobody follows, and a fresh session
has no way to tell which skill the team reaches for at each stage. Measure what ran, cut what
did not, then make CLAUDE.md say only what changes behavior.

> **Freedom level: Rigid** — run the steps in order. Never delete a file, flip a plugin flag,
> or edit CLAUDE.md before the confirmation in Step 5.
> **Operational rules** — Count before cutting: every removal cites a row, a missing row, or a
> rule check from Step 1. The project settings file and CLAUDE.md are shared with
> collaborators; say so before editing them. Keep the user's wording for any rule that
> survives. Report the context-budget gain as expected, not measured: the harness does not
> expose whether skill descriptions were being truncated.

## When not to use

Not for judging one skill's quality (that is a SKILL.md review), and not for a scored
CLAUDE.md audit on its own; the `agentic-memory-management` skill in this marketplace does
that without session history. This skill uses what past sessions did to decide what stays
loaded and what CLAUDE.md still needs to say.

## Step 1 — Count what actually ran

Run the bundled counter from the project root. The path is relative to this skill's directory.

```bash
python3 scripts/count_usage.py --since YYYY-MM-DD
```

With no path argument it finds the log directories for the project's main checkout and its
worktrees under `~/.claude/projects/` (the checkout path with every non-alphanumeric character
replaced by `-`). From inside a worktree it resolves the main checkout through git, so the
whole project's history counts. Pass a log directory explicitly when the logs live elsewhere.
Drop `--since` to count everything on disk.

The output has four tables and a rollup:

| Table | Signal | Where it comes from |
|-------|--------|---------------------|
| Slash commands typed by the user | What the team reaches for on purpose | `<command-name>` tags in user turns |
| Skills invoked by the agent | What the agent picks on its own | `Skill` tool calls |
| MCP tools called | Whether an MCP plugin earns its place | tool names starting `mcp__` |
| Subagents spawned | Which project agents ever ran | `Agent` tool calls |
| Rollup by plugin prefix | Per-plugin total, commands plus skills | the part before `:` in each name |

Read the `sessions` column, not `calls`: one session can loop a tool hundreds of times.
Any enabled plugin, command file, or agent file absent from every table had zero invocations.

Then check every CLAUDE.md rule of the form "always use NAME when touching PATH", one flag
per rule:

```bash
python3 scripts/count_usage.py --follows src/components/=component-skill --follows src/api/=api-review
```

Each check prints how many sessions edited a file under PATH and how many of those used NAME
(invoked it, typed it, read its file, or named it in a shell command). That ratio is the
rule's real effect.

## Step 2 — Inventory what loads

```bash
python3 -c 'import json; [print(v, k) for k, v in json.load(open(".claude/settings.json")).get("enabledPlugins", {}).items()]'
python3 -c 'import json, os; [print(v, k) for k, v in json.load(open(os.path.expanduser("~/.claude/settings.json"))).get("enabledPlugins", {}).items()]'
ls .claude/commands .claude/agents 2>/dev/null
wc -lc CLAUDE.md .claude/rules/*.md 2>/dev/null
grep -n skillListingBudgetFraction ~/.claude/settings.json
```

Keep both plugin lists side by side; Step 3's settings rule depends on whether a plugin is
enabled at one level or both. CLAUDE.md's byte count is paid on every turn, so note it before
and after. The last line shows the description budget cap, if one is set.

## Step 3 — Classify every loaded entry

Sort each plugin, command file, and agent file into one bucket:

| Bucket | Test | Action |
|--------|------|--------|
| Carries the cycle | Top row for its stage in Step 1, or used in a meaningful share of sessions | Keep; give it a row in the Step 6 table |
| Unused | No row in any Step 1 table | Remove |
| Superseded | Has rows, but another entry covers the same stage in far more sessions | Remove; name the winner in the table's Not column |
| Keep anyway | No rows, but written for this codebase and worth enforcing with a hook | Keep at most one or two, and say why in the report |

Apply these rules when deciding how to remove a plugin:

- Settings precedence is local, then project, then user. A plugin also `true` in the user
  file gets an explicit `false` in the project file; deleting the key would fall back to the
  user-level `true`. A plugin enabled only in the project file gets its key deleted.
- Two plugins, or a plugin and a built-in, exposing the same bare command name resolve
  ambiguously when typed. Disable the duplicate so the bare name resolves to one thing;
  prefixed names keep working.
- Zero-use command files that wrap scripts already documented elsewhere (package scripts,
  README) are duplication with a maintenance cost and nothing else.
- A plugin that ships only hooks (no skills, commands, or MCP server) leaves no trace in
  the Step 1 tables while doing real work on every tool call. Look inside its directory
  under `~/.claude/plugins/cache/` for a `hooks/` folder before calling it unused.
- Grep every name about to go: `grep -rn '<name>' CLAUDE.md .claude/rules README.md docs/`.
  A line advertising a removed command is removed with it, and CLAUDE.md hits feed Step 4.

## Step 4 — Tighten CLAUDE.md against the data

Read CLAUDE.md and every `.claude/rules/*.md` once, with the Step 1 output beside them.
Mark each block with one finding:

| Finding | Test | Action |
|---------|------|--------|
| Dead reference | Names a command, agent, plugin, or script that Step 3 removes or that no longer exists | Delete the line |
| Ignored rule | An always-use-NAME rule whose Step 1 check shows NAME used in a minority of matching sessions | Delete it, or replace it with a hook and delete the prose |
| Duplicate | Restates a package script, a lint or formatter config, or a `.claude/rules/` file | Delete; leave at most one pointer |
| Default-restating | Removing it would not change what the agent does ("write clear code", "add tests") | Delete |
| Path-specific block | Applies to one directory or file type only | Move to `.claude/rules/<topic>.md` with `paths:` frontmatter; leave nothing behind |
| Missing stage map | No section says which skill carries each dev-cycle stage | Add the Workflow Skills table in Step 6 |

A pointer in CLAUDE.md steers but does not enforce. In the audit this skill was distilled
from, an existing instruction to invoke a skill before component work was followed in roughly
one session in seven. Where a skill must run, a hook is the enforcement path; the prose then
costs context for nothing.

Path-scoped rule file shape:

```md
---
paths:
  - "src/components/**"
---

# Component rules

- Rule that applies only under this path
```

## Step 5 — Confirm before cutting

Show the complete change list in one message: files to delete, settings keys to delete, keys
to flip to `false`, doc lines to drop, CLAUDE.md lines to delete or move with the finding
behind each, and the proposed table rows with the Step 1 numbers behind each. Then use
`AskUserQuestion` to settle three points and wait for the answers:

1. Project settings (shared, checked in) or local settings (this machine only)? Default to
   project so every collaborator loads the same set.
2. Any entry in the Unused bucket the user wants kept regardless?
3. For each ignored rule: delete, or convert to a hook? Default to delete when no hook path
   exists in the project yet.

Do not proceed on silence.

## Step 6 — Apply

```bash
git rm -r .claude/commands            # or list the individual files
git rm .claude/agents/<unused>.md
```

Edit the `enabledPlugins` block per the Step 3 rules. Touch the user-level settings file only
when a name collision requires it, and say in the report that the edit lives outside the repo.

Apply the Step 4 findings to CLAUDE.md: delete marked lines, write each path-specific block to
its `.claude/rules/` file, and add a Workflow Skills section directly after the section that
lists project commands or scripts. Use this shape:

```markdown
## Workflow Skills

These skills carry the dev cycle; reach for them at the matching stage without being asked.

| Stage  | Use                                | Not                    |
| ------ | ---------------------------------- | ---------------------- |
| Commit | `/<plugin>:<commit-skill>`         | a bare `git commit -m` |
| Review | `/<review-skill>` before every PR  | ad-hoc review prose    |
```

One row per stage the audit surfaced; branch, commit, review, ship, cleanup, plans, sharing,
and recap are the usual set. Fill Use from the top Step 1 row for that stage and Not with the
substitute the agent reached for instead. Leave the how out: each skill's own description
carries it, so the table does not drift when a plugin updates.

Remove doc lines that advertise deleted commands. Add a changelog entry if the project keeps one.

## Step 7 — Verify

```bash
ls .claude/commands 2>/dev/null; ls .claude/agents
python3 -c 'import json; s = json.load(open(".claude/settings.json")); print(sorted(k for k, v in s.get("enabledPlugins", {}).items() if v))'
awk '/^## Workflow Skills/{p=1; print; next} p && /^## /{exit} p' CLAUDE.md
wc -lc CLAUDE.md .claude/rules/*.md
grep -rnE '/<removed-name>\b|<removed-name>\.md' CLAUDE.md .claude/rules README.md docs/ --exclude='<this-plan>*' || echo "no dead references"
```

Expected: only the kept files list, only the kept plugin keys print, the whole Workflow Skills
section prints with one row per stage, CLAUDE.md is smaller than the Step 2 measurement, and
no removed name appears as a slash command or a file outside the plan that documents the
removal. The grep matches `/name` and `name.md` only, so a longer hyphenated word that happens
to contain the name does not count. Run the project's markdown lint and formatter check on the
touched files when it has them.

Then open a fresh session in the repository and type `/`. None of the removed names should
autocomplete; every skill named in the table should. Ask that session to commit a scratch
change and confirm it reaches for the table's commit skill rather than a bare `git commit`.
That is the end-to-end check of the table.

## Report

```text
## Agent Context Audit

Sessions counted: <n> (<first date> to <last date>)
Load set kept: <plugins>; <command and agent files>
Load set removed: <n> command files, <n> agent files, <n> plugin keys deleted, <n> flipped to false
CLAUDE.md: <bytes before> to <bytes after>; <n> lines deleted, <n> blocks moved to .claude/rules/, <n> rules converted to hooks
Pinned: <n>-row Workflow Skills table
Not measured: context-budget gain (the description cap is set; truncation is not observable)
Follow-ups: <hooks still to wire; other plans or docs that referenced deleted files>
```

---
name: verify
description: Runtime-verify a change to a published skill in this repo by driving its script as a CLI and running its SKILL.md steps as a fresh agent. Repo-local tooling, not a published skill.
---

Verification here means running the skill, not running `tests/validate-all.sh` (CI does that).

## Script surface

Skill scripts are stdlib Python with no build step. Drive them as a user would:

```bash
python3 skills/<name>/scripts/<script>.py --help
python3 skills/<name>/scripts/<script>.py <args>
```

Real session logs live under `~/.claude/projects/<cwd with non-alphanumerics replaced by ->*/`.
For deterministic runs, write a fixture `.jsonl` in the scratchpad: one JSON object per line with
`type` (user or assistant), `timestamp`, and `message.content` as a list of blocks (`text`,
`tool_use` with `name` and `input`, `tool_result`).

Gotchas seen: zsh expands a bare `=word` argument as a command lookup, so quote it (`'=word'`).
Default log discovery keyed on the cwd finds only the current worktree's sessions when run from
inside a worktree; run from the main checkout to see the whole project.

## SKILL.md surface

Copy the skill into a throwaway project and run a fresh agent against it:

```bash
T=<scratchpad>/verify-agent; mkdir -p "$T/.claude/skills"; cp -R skills/<name> "$T/.claude/skills/"
cd "$T" && env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT claude -p "<ask it to run one step of the skill>" \
  --allowedTools "Skill,Read,Glob,Grep,Bash(python3 *),Bash(ls *)" --max-turns 12
```

Also run the SKILL.md's own shell commands verbatim inside a real target project and compare what
they print with what the SKILL.md says to expect.

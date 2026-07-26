---
status: proposal
type: feature
created: 2026-07-26
repo-name: skills
---

# Proposal: Publish a platform-agnostic skills marketplace as `shawn-sandy/skills`

> This is a proposal for review, not an execution plan. It grounds the current
> state of the Agent Skills ecosystem (spec, CLI, registry) and of the author's
> existing Claude Code marketplaces, and proposes publishing a curated,
> standards-compliant skills repo instead of building new marketplace
> infrastructure. The load-bearing decisions are resolved (see Locked
> decisions); execution is handed off (see Next step).

## TL;DR

The platform-agnostic skills marketplace already exists as public
infrastructure: the Agent Skills open standard (agentskills.io) is the format,
and Vercel's `npx skills` CLI + skills.sh registry is the distribution layer
for 70+ agents. Building another one would duplicate a solved layer. The
opportunity is to extract a curated flagship set (~10–15) of the ~73
self-authored skills currently locked inside Claude-Code-only plugin
packaging, publish them as `shawn-sandy/skills` in the standard layout, and
let the existing agentics marketplaces consume them back via `git-subdir` so
nothing drifts.

## Context

- The idea: "set up a platform-agnostic skills marketplace" — skills that
  install and run on Claude Code, OpenAI Codex CLI, Cursor, Gemini CLI,
  GitHub Copilot, and peers, distributed openly.
- The author already operates two self-authored, auto-updating Claude Code
  marketplaces: **agentics-kit** (18 installed plugins, sourced from the
  `shawn-sandy/agentics` monorepo — 13 plugin dirs, ~73 distinct skill
  directories under `kit/plugins/`) and **agentic-acss-plugins** (2 plugins).
  20 of the 56 plugins installed on this machine are self-authored.
- All of it is packaged in Claude-Code-proprietary form:
  `.claude-plugin/marketplace.json` (git-subdir sources), plugin anatomy with
  `commands/`, `agents/`, `hooks/`, and Claude-specific frontmatter
  (`disable-model-invocation`).
- `~/devbox/skills` (this directory) is empty and not yet a git repo — the
  intended home for the new project.
- The machine already carries evidence of the target ecosystem in use:
  `~/.claude/skills/find-skills` and `agent-browser` are symlinks into
  `~/.agents/skills/`, the install location used by `npx skills`.

External ground truth (fetched 2026-07-26):

- **Agent Skills standard** — released by Anthropic 2025-12-18, published at
  agentskills.io, stewarded through the Agentic AI Foundation. A skill is a
  directory whose `SKILL.md` carries YAML frontmatter (`name` ≤64 chars
  kebab-case matching the directory, `description` ≤1024 chars; optional
  `license`, `compatibility` ≤500, `metadata` map, experimental
  `allowed-tools`) plus optional `scripts/`, `references/`, `assets/`.
  Progressive disclosure: metadata (~100 tokens) at startup, body (<5000
  tokens recommended, <500 lines) on activation, resources on demand.
  Validated with `skills-ref validate`. Roughly 40 platforms had adopted the
  standard by mid-2026, including every launch target named above.
- **`npx skills` CLI** (github.com/vercel-labs/skills, MIT) — installs skills
  from any public GitHub repo into 70+ agents' native directories
  (`.claude/skills/`, `.agents/skills/`, `~/.cursor/skills/`, …). Expects
  `skills/<name>/SKILL.md` (flat) or `skills/<category>/<name>/SKILL.md`
  (two-level catalog). Commands: `add`, `find`, `use`, `list`, `update`,
  `remove`, `init`.
- **skills.sh** — public directory and leaderboard (~1M installs tracked),
  identifies skills as `owner/repo/skill-name`, listing driven by install
  telemetry; no documented submission gate.
- Adjacent marketplaces (SkillsRouter, OpenClaw Bazaar) already compete on
  hosting/curation — further evidence the infrastructure layer is saturated.

## Core finding

> The marketplace does not need to be built — the Agent Skills standard plus
> `npx skills`/skills.sh already is the platform-agnostic marketplace; the
> real work is extracting the author's ~73 Claude-locked skills into a
> curated, spec-compliant public repo that the existing ecosystem can
> discover, install, and rank.

## Side-by-side

| Dimension | Current setup (agentics-kit, agentic-acss-plugins) | Target (Agent Skills + `npx skills`) |
|---|---|---|
| Format | `SKILL.md` inside Claude plugin anatomy | `SKILL.md` per open spec, `skills-ref` validated |
| Reach | Claude Code only | ~40 platforms / 70+ agents |
| Registry | Self-hosted `.claude-plugin/marketplace.json` | skills.sh, auto-listed via install telemetry |
| Install UX | `/plugin marketplace add shawn-sandy/agentics` | `npx skills add shawn-sandy/skills` |
| Identity | plugin name within marketplace | `shawn-sandy/skills/<skill-name>` |
| Claude-only surfaces (commands, agents, hooks) | Supported | Out of scope — remain in existing plugins |
| Ranking/discovery | none public | leaderboard by installs (all-time, trending, 8-week) |

## Locked & resolved decisions

Resolved in the 2026-07-26 review:

1. **Form factor: registry + CLI — adopt, don't build.** Publish onto the
   existing `npx skills`/skills.sh ecosystem rather than building a new
   registry, CLI, or website. Propagates to every workstream: no backend, no
   hosting, no submission pipeline.
2. **Launch platforms: Claude Code, Codex CLI, Cursor, Gemini CLI/Copilot.**
   All are Agent Skills adopters and `npx skills` targets, so multi-platform
   support costs nothing beyond spec compliance — no per-platform adapters.
3. **Audience: open-source community, free.** License everything permissively
   (MIT recommended, matching `vercel-labs/skills`); no payment or account
   infrastructure.
4. **Repo strategy: new curated repo at `~/devbox/skills`.** The agentics
   monorepo and both live marketplaces stay untouched; zero risk to the 18
   auto-updating installed plugins.
5. **Curation: flagship set of ~10–15 skills.** Hand-picked for portability
   and value; quality drives leaderboard installs more than volume. The full
   portability triage of all ~73 is execution work (Appendix A is the
   checklist).
6. **Source of truth: the new repo is canonical for extracted skills.**
   agentics consumes them back via its existing `git-subdir` plugin-source
   mechanism — one copy, no sync script, no drift.
7. **Name: `shawn-sandy/skills`.** Matches ecosystem convention
   (`vercel-labs/skills`, `anthropics/skills`) and yields the shortest
   install command.

## Workstreams

### A — Repo scaffold and standard compliance

- Initialize `~/devbox/skills` as a git repo with the `npx skills` flat
  layout: `skills/<name>/SKILL.md` (+ optional `references/`, `scripts/`,
  `assets/` per skill).
- Root `README.md` with per-agent install commands, `LICENSE` (MIT),
  skill index table.
- CI: run `skills-ref validate` on every skill directory on push — the spec
  ships a reference validator; use it rather than a hand-rolled linter.
- Seam: this repo holds only spec-compliant skills. Anything needing
  `commands/`, `agents/`, or `hooks/` stays a Claude plugin in agentics.

### B — Extraction and portability adaptation

- Select the flagship set from the ~73 candidates using the Appendix A
  checklist (no Claude-only tool dependencies, no
  `${CLAUDE_PLUGIN_ROOT}`-style paths, body <500 lines or split into
  `references/`).
- Per-skill adaptation: keep `name`/`description` (already spec-shaped);
  keep `allowed-tools` where used (spec-experimental); drop
  `disable-model-invocation` (Claude-only — fold its intent into the
  description); add `compatibility` only where a skill genuinely requires
  specific tooling; add `license` and `metadata.author`.
- Rewrite descriptions to trigger well across agents (what + when + keywords,
  per the spec's guidance) rather than relying on Claude Code's skill picker.

### C — Back-integration with agentics

- For each extracted skill, point the corresponding agentics plugin's
  `marketplace.json` source at `shawn-sandy/skills` via `git-subdir` and
  delete the monorepo copy, so the new repo is the single source.
- Claude-only wrappers (slash commands, subagents, hooks) remain in the
  monorepo and reference the skill content that now ships from the new repo.

### D — Publish and discover

- Push to GitHub public; verify `npx skills add shawn-sandy/skills` end-to-end
  on all four launch platforms (project and global scopes).
- skills.sh listing follows automatically from install telemetry — no
  submission step; README badges and a short announcement drive the first
  installs that make the repo visible.
- A browsable web directory is deliberately out of scope (YAGNI): skills.sh
  already provides search, pages, and ranking.

## Risks & tensions

- **Cross-agent behavior variance.** Skills written against Claude Code
  habits (tool names like `AskUserQuestion`, `Agent` teams, `Skill` chaining)
  degrade on other agents. Mitigation: the Appendix A triage excludes
  hard-dependent skills from the flagship set; soft dependencies get a
  `compatibility` note.
- **Ecosystem dependency.** `npx skills`/skills.sh is Vercel-operated and
  telemetry-ranked. Mitigation: the repo is plain git in an open format —
  any current or future index (SkillsRouter, OpenClaw Bazaar, agent-native
  installers) can consume it; there is no lock-in to the CLI.
- **Two-repo identity confusion.** `shawn-sandy/agentics-kit` (older, 47
  SKILL.md) and `shawn-sandy/agentics` (current monorepo) already overlap;
  adding `shawn-sandy/skills` makes three homes for skill content. Mitigation:
  decision 6 makes canonicity explicit; see open question on deprecating the
  older repo.
- **Back-integration churn.** Workstream C touches live, auto-updating
  marketplaces. Mitigation: extract-and-repoint one plugin at a time, after
  the new repo is published and verified — never batch-migrate.

## Open questions (decisions only)

- **Deprecate `shawn-sandy/agentics-kit` (the older 47-skill repo)?**
  Non-blocking for this proposal, but the three-repo overlap is real.
  Recommendation: archive it once workstream C lands.
- **Category layout now or later?** `npx skills` supports
  `skills/<category>/<name>/` two-level catalogs. Recommendation: launch flat
  (~10–15 skills need no taxonomy); revisit past ~25 skills.

## Roadmap

| Phase | Work | Size | Depends on |
|---|---|---|---|
| 1 | Scaffold repo (git init, layout, README, LICENSE, `skills-ref` CI) | S | — |
| 2 | Triage ~73 skills against Appendix A; pick flagship ~10–15 | M | — |
| 3 | Extract + adapt flagship set; validate; test installs on 4 platforms | M | 1, 2 |
| 4 | Publish to GitHub; verify `npx skills add`; confirm skills.sh listing | S | 3 |
| 5 | Back-integrate agentics via `git-subdir`, one plugin at a time | M | 4 |
| 6 | Expand set, add categories if >25 skills, ongoing curation | M (recurring) | 4 |

## Appendix A — Portability triage checklist

A skill qualifies for `shawn-sandy/skills` when all of the following hold;
otherwise it stays Claude-plugin-only or gets adapted first.

1. Frontmatter is spec-valid: kebab-case `name` matching its directory,
   keyword-rich `description` ≤1024 chars (`skills-ref validate` passes).
2. No hard dependency on Claude-only runtime surfaces: `AskUserQuestion`,
   `Agent`/subagent types, `Skill` cross-invocation, plugin slash commands,
   hooks, `${CLAUDE_PLUGIN_ROOT}` paths.
3. No `disable-model-invocation` reliance (field is Claude-specific).
4. Body under ~500 lines / <5000 tokens; overflow moved to `references/`
   with one-level-deep relative links.
5. Scripts, if any, are self-contained with documented dependencies
   (declared in `compatibility` when non-trivial).
6. Instructions reference generic capabilities (read files, run shell,
   fetch web) rather than agent-brand tool names, except inside a clearly
   marked Claude-specific section.

## Appendix B — Field mapping: current Claude Code skills → Agent Skills spec

| Current usage (agentics skills) | Spec disposition |
|---|---|
| `name` | Keep — already compliant shape |
| `description` | Keep; rewrite for cross-agent triggering (what + when + keywords) |
| `allowed-tools` | Keep — spec-recognized (experimental); support varies by agent |
| `disable-model-invocation` | Remove — Claude-only; encode intent in description |
| `references/` subdirectories | Keep — spec-native optional directory |
| `commands/`, `agents/`, `hooks/`, `hooks.json` | Do not migrate — remain in Claude plugins (workstream C) |
| `.claude-plugin/marketplace.json`, `git-subdir` sources | Unchanged in agentics; gains pointers to the new repo |

## Appendix C — Inventory snapshot (2026-07-26)

- Registered marketplaces on this machine: 11; installed plugins: 56, of
  which 20 self-authored (18 agentics-kit + 2 agentic-acss-plugins — the only
  two with `autoUpdate: true`).
- `shawn-sandy/agentics` monorepo: 13 plugin dirs, ~73 distinct skill
  directories under `kit/plugins/`.
- `shawn-sandy/agentics-kit` (older): 14 plugins declared, 47 SKILL.md.
- Standalone `~/.claude/skills`: ~24 skills, including two symlinks into
  `~/.agents/skills/` (`npx skills` install location — the target ecosystem
  is already in local use).
- `~/devbox/skills`: empty, not a git repo — the new project home.

Sources: [agentskills.io/specification](https://agentskills.io/specification) ·
[github.com/agentskills/agentskills](https://github.com/agentskills/agentskills) ·
[github.com/vercel-labs/skills](https://github.com/vercel-labs/skills) ·
[skills.sh](https://www.skills.sh/) ·
[Vercel changelog: introducing skills](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)

## Next step

Convert to an execution plan:
`/plan-agent:implementation-plan author an execution plan from the proposal at docs/proposals/publish-agent-skills-marketplace.md`

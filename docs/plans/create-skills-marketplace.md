---
status: in-progress
type: feature
created: 2026-07-26
glance: Sixty self-authored skills currently reach only Claude Code; publishing a curated flagship set in the open Agent Skills format puts them one install command away from 70-plus coding agents. Done means npx skills add shawn-sandy/skills works on four platforms, CI validates every skill against the spec, and one agentics plugin proves the canonical-source model.
workflow: true
---

# Plan: Publish shawn-sandy/skills — a cross-platform skills marketplace repo

## Objective

Ship shawn-sandy/skills: a public, spec-compliant repository of 10–15 flagship skills extracted from the agentics monorepo, installable on Claude Code, OpenAI Codex CLI, Cursor, and Gemini CLI with a single npx skills add shawn-sandy/skills command.

## Context

The decision-complete proposal at docs/proposals/publish-agent-skills-marketplace.md settled the strategy on 2026-07-26: adopt the existing Agent Skills ecosystem (the open SKILL.md standard at agentskills.io plus Vercel's npx skills CLI and the skills.sh registry) rather than building marketplace infrastructure. The author's 60 skills live inside Claude-Code-only plugin packaging in the shawn-sandy/agentics monorepo (13 plugins under kit/plugins/); this plan extracts a curated flagship set into a new canonical repo at ~/devbox/skills, published as shawn-sandy/skills.

Two known risks, both mitigated in the steps: cross-agent behavior variance (skills written against Claude Code habits may degrade elsewhere — the triage checklist excludes hard-dependent skills, and descriptions are rewritten for cross-agent triggering), and live-marketplace churn (the agentics marketplaces auto-update on this machine — back-integration is piloted on a single plugin before any wider rollout, which stays out of scope here).

## Steps

1. Initialize ~/devbox/skills as a git repository with the ecosystem layout: git init, a root README.md with per-agent install commands, a skill index, and the demotion policy (a skill that grows Claude-only dependencies moves back to its agentics plugin and is removed here in the same release), an MIT LICENSE, a .gitignore, and the skills/ directory, committed together with the existing docs/ content Why: the npx skills CLI only discovers skills in a repo shaped skills/name/SKILL.md, and the proposal and this plan should travel in the repo's history from the first commit Verify: git log shows the initial commit and the tree contains README.md, LICENSE, and skills/.
2. Triage all 60 monorepo skills (find ~/devbox/agentics/kit/plugins -maxdepth 4 -name SKILL.md) against the portability checklist in the proposal's Appendix A and record every verdict in docs/triage.md, marking 10–15 as the flagship set Why: curation is the locked strategy — an auditable include/exclude record keeps the launch set defensible and makes later expansion mechanical instead of a judgment call each time Verify: docs/triage.md lists all 60 skills, each with an include or exclude reason, and the include count is between 10 and 15.
3. Extract each flagship skill into skills/name/SKILL.md (copying its references/ directory when present), keeping original skill names — identity on skills.sh is owner/repo/skill-name, so the shawn-sandy/skills namespace disambiguates, and a rename happens only if triage finds an exact-name clash with a widely installed skill — and adapting frontmatter per the proposal's Appendix B: keep name, description, and allowed-tools; drop disable-model-invocation; add license MIT plus metadata author shawn-sandy and version 1.0; rewrite each description to state what the skill does and when to use it with keywords that trigger across agents Why: spec-compliant frontmatter and keyword-rich descriptions are what make the same file activate correctly on Claude Code, Codex, Cursor, and Gemini rather than only on Claude Code's skill picker Verify: every skills/name/ directory passes the spec validator with zero errors and each name field matches its directory.
4. Add the runnable checks: tests/validate-all.sh runs the official skills-ref validator across every skills directory and falls back to a bundled frontmatter checker implementing the same rules when skills-ref is unavailable, tests/verify-install.sh installs the repo into a temporary project via npx skills add, asserts every flagship skill lands, and removes the temporary directory afterward, and .github/workflows/validate.yml runs both scripts on push and pull request Why: a marketplace repo is only trustworthy if every future commit is machine-checked against the spec — manual review does not scale past the launch set Verify: both scripts exit 0 locally, and deliberately corrupting one skill's name field makes tests/validate-all.sh exit non-zero.
5. Publish the repository as public github.com/shawn-sandy/skills with gh repo create shawn-sandy/skills --public --source . --push, then tag the launch commit v0.1.0 and push the tag Why: public GitHub availability is the entire distribution mechanism — the npx skills CLI installs straight from the repo and skills.sh indexes it automatically from install telemetry, with no submission step — and the tag marks the launch state for humans and changelogs Verify: gh repo view shawn-sandy/skills succeeds, the v0.1.0 tag exists on the remote, and the Actions tab shows the validate workflow green on main.
6. Verify cross-platform installs from the published repo: in a scratch directory, run npx skills add shawn-sandy/skills with explicit agent flags forcing the claude-code, codex, cursor, and gemini-cli targets (so the agents need not be installed locally) and assert the files land in each agent's expected directory, with a runtime activation spot-check on Claude Code only Why: platform-agnostic is this plan's core claim and must be observed on real agent install layouts, not assumed from spec compliance — forced targets keep the check honest without installing three extra agent CLIs Verify: each agent's install path (such as .claude/skills/ and .agents/skills/) contains the flagship skills, npx skills list reports them, and a flagship skill activates in a Claude Code session.
7. Pilot the back-integration on one affected plugin in ~/devbox/agentics: sync its extracted skills from shawn-sandy/skills via git subtree pull or a documented copy step, or repoint the plugin's git-subdir source to the new repo when the plugin ships no commands, agents, or hooks, then bump that plugin's version in .claude-plugin/marketplace.json, keeping the repoint to a single commit so git revert plus /plugin update is the instant rollback Why: the locked decision makes the new repo canonical, but the agentics marketplaces auto-update on this machine — proving the model on one plugin, with a one-commit rollback, avoids batch-breaking 18 live plugins Verify: reinstalling that plugin via /plugin update in Claude Code loads skill content that now originates from shawn-sandy/skills.

## Files

- README.md (new) — per-agent install commands and the skill index
- LICENSE (new) — MIT
- .gitignore (new) — node_modules, scratch artifacts
- docs/triage.md (new) — include/exclude verdict for all 60 candidate skills
- skills/ (new) — 10–15 extracted flagship skill directories, each with SKILL.md
- tests/validate-all.sh (new) — spec-validation sweep across every skill
- tests/verify-install.sh (new) — end-to-end install smoke test
- .github/workflows/validate.yml (new) — CI running both checks
- ../agentics/.claude-plugin/marketplace.json (modified) — pilot plugin repoint and version bump

## Acceptance Criteria

- [ ] npx skills add shawn-sandy/skills installs the flagship set from a clean scratch project for Claude Code, Codex CLI, Cursor, and Gemini CLI targets
- [ ] Every skills directory passes the Agent Skills spec validator with zero errors
- [ ] docs/triage.md records an include or exclude verdict for all 60 candidate skills
- [ ] The repository is public at github.com/shawn-sandy/skills with the validate workflow green on main
- [ ] bash tests/verify-install.sh exits 0 against the published repository
- [ ] The pilot plugin reinstalls cleanly in Claude Code with its skill content sourced from shawn-sandy/skills
- [ ] No published skill carries disable-model-invocation or CLAUDE_PLUGIN_ROOT references
- [ ] Every published skill's name field matches its directory name
- [ ] The v0.1.0 tag exists on the published repository

## Tests

Tier 1 — steps create runnable skill content, shell test scripts, and CI configuration
- Objective: one command installs the flagship set cross-platform. File: tests/verify-install.sh; Type: smoke; Asserts: npx skills add into a fresh temporary project installs every flagship skill for the claude-code target, and the temporary directory is removed afterward; Run: bash tests/verify-install.sh
- Integration: spec-compliance sweep. File: tests/validate-all.sh; Targets: every skills/name/SKILL.md frontmatter; Key cases: name matches its directory, description within 1024 characters, no Claude-only keys remain; Run: bash tests/validate-all.sh

## Verification

From a clean scratch directory, run bash tests/verify-install.sh against the published repository and confirm it exits 0. Then run npx skills add shawn-sandy/skills for each of the four launch targets and inspect the agent install paths: the flagship skills must be present under .claude/skills/ (Claude Code) and the respective directories for Codex, Cursor, and Gemini CLI, and npx skills list must report them. Confirm the GitHub Actions validate workflow is green on main. Finally, run /plugin update for the pilot plugin in Claude Code and confirm its skill loads with content originating from shawn-sandy/skills. The skills.sh listing follows install telemetry and may lag — it is expected, not required, for completion.

## Next Steps

- Roll out back-integration to the remaining agentics plugins
  Extends the pilot from step 7 to every plugin whose skills were extracted.
  ```text
  In the shawn-sandy/agentics repo, complete the back-integration started
  with the pilot plugin: for each plugin whose skills now live canonically
  in github.com/shawn-sandy/skills, sync or repoint the skill content
  (git subtree pull, or git-subdir source repoint for pure-skill plugins),
  bump each plugin's version in .claude-plugin/marketplace.json, and update
  the CHANGELOG. Migrate one plugin per commit. Verify by running
  /plugin update in Claude Code for every migrated plugin and confirming
  each skill still loads.
  ```
- Expand the flagship set and introduce categories
  The flat skills/ layout is right up to roughly 25 skills; the CLI also supports skills/category/name/ two-level catalogs.
  ```text
  In the shawn-sandy/skills repo, review docs/triage.md for excluded skills
  whose blockers are fixable, adapt the next batch to the Agent Skills spec
  (same rules as the flagship set), and restructure skills/ into
  skills/<category>/<name>/ once the count passes 25. Update README.md's
  index and keep tests/validate-all.sh green. Verify with
  bash tests/verify-install.sh.
  ```
- Archive the legacy shawn-sandy/agentics-kit repository
  The proposal flags the older 47-skill repo as overlapping identity; wish-list until the rollout lands.
  ```text
  Archive the github.com/shawn-sandy/agentics-kit repository: confirm no
  marketplace in ~/.claude/plugins/known_marketplaces.json still points at
  it, add a README notice directing users to shawn-sandy/agentics and
  shawn-sandy/skills, then archive it via gh repo archive. Verify the repo
  shows as archived on GitHub and Claude Code plugin updates still succeed.
  ```

## Unresolved Questions

- Which plugin pilots the back-integration in step 7? Recommendation: the smallest plugin whose skills all pass triage, decided when docs/triage.md exists.

## Resources

- docs/proposals/publish-agent-skills-marketplace.md — the decision-complete proposal behind this plan, including the Appendix A portability checklist and Appendix B field mapping
- https://agentskills.io/specification — SKILL.md frontmatter and directory rules, progressive disclosure limits, skills-ref validator
- https://github.com/vercel-labs/skills — npx skills CLI: expected repo layout and per-agent install paths
- https://www.skills.sh/ — registry and leaderboard; owner/repo/skill identity, telemetry-driven listing

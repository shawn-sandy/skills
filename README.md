# skills

A curated set of agent skills by [Shawn Sandy](https://github.com/shawn-sandy),
published in the open [Agent Skills](https://agentskills.io) format. Every
skill here works on any platform that supports the standard — Claude Code,
OpenAI Codex CLI, Cursor, Gemini CLI, GitHub Copilot, and 70+ other agents.

## Install

Install any skill (or all of them) with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
# interactive picker
npx skills add shawn-sandy/skills

# a single skill
npx skills add shawn-sandy/skills/<skill-name>

# install globally (all detected agents)
npx skills add shawn-sandy/skills -g
```

The CLI detects your installed agents and copies each skill into the right
location (`.claude/skills/`, `.agents/skills/`, `~/.cursor/skills/`, ...).

## Skills

<!-- INDEX:START — updated as skills are added -->
| Skill | Description |
|---|---|
| [agentic-memory-management](skills/agentic-memory-management) | Audits and optimizes CLAUDE.md project memory files. Checks adherence to Claude Code best practices and produces actionable fixes. Use when the user asks to audit, optimize, or diagnose a CLAUDE.md. |
| [code-review-agent](skills/code-review-agent) | Reviews code for bugs, security issues, and breaking changes. Produces prioritized findings on quality, vulnerabilities, and regressions. Use when asked to review code or check a PR diff. |
| [code-testing-agent](skills/code-testing-agent) | Suggests purpose-driven tests tied to actual behavior. Writes test files covering untested paths and behavior gaps in the codebase. Use when the user asks to suggest tests or find untested behavior. |
| [deep-grill](skills/deep-grill) | Stress-tests plan decisions node-by-node with focused questions. Walks each decision point surfacing assumptions and weak spots. Use when the user asks to deep grill or stress-test a plan. |
| [plan-status](skills/plan-status) | Writes lifecycle status into a plan's frontmatter, one file or a directory. Inspects codebase and git history for accurate dates. Use when asked to check or update plan status. |
| [planning-skills](skills/planning-skills) | Scaffolds a new skill with SKILL.md and supporting files. Walks a structured workflow covering frontmatter, body, references, and scripts. Use when the user asks to plan or scaffold a new skill. |
| [reviewing-skills](skills/reviewing-skills) | Scores SKILL.md files across 5 quality dimensions. Audits against the Agent Skills open standard's authoring best practices and optionally generates a fix. Use when the user asks to review, audit, or score a skill. |
| [reviewing-tests](skills/reviewing-tests) | Audits tests for quality, coverage, and code alignment. Identifies gaps, redundant tests, and misaligned assertions. Use when the user asks to review, audit, or improve a test suite. |
| [running-tests](skills/running-tests) | Detects the test framework and runs scoped tests. Reports pass/fail results with output and identifies failing assertions. Use when the user asks to run tests, check if tests pass, or verify changes. |
| [security-scrub](skills/security-scrub) | Scans code and diffs for secrets and sensitive data. Detects credentials, tokens, and PII to prevent leaks before sharing. Use when the user asks to check for secrets or review a diff for leaks. |
| [tdd-fix](skills/tdd-fix) | Fixes bugs via TDD with up to 10 red-green iterations. Writes a failing test then autonomously iterates until the bug is resolved. Use when the user asks to TDD-fix a bug or run a red-green cycle. |
| [wcag-compliance-reviewer](skills/wcag-compliance-reviewer) | Reviews HTML/CSS and React code for WCAG 2.2 Level AA violations. Provides targeted fixes for each accessibility issue found. Use when the user asks to check WCAG compliance or audit accessibility. |
<!-- INDEX:END -->

## Layout

```
skills/<name>/SKILL.md    # one directory per skill, per the Agent Skills spec
tests/validate-all.sh     # spec-compliance sweep (CI)
tests/verify-install.sh   # end-to-end install smoke test
docs/                     # proposal, plan, and triage records behind this repo
```

## Portability policy

Skills in this repo must pass the portability checklist in
[docs/proposals/publish-agent-skills-marketplace.md](docs/proposals/publish-agent-skills-marketplace.md)
(Appendix A): spec-valid frontmatter, no platform-only runtime dependencies,
bodies within the progressive-disclosure budget, self-contained scripts.

**Demotion policy:** a skill that grows platform-only dependencies (hooks,
subagents, plugin commands) moves back to its source plugin in
[shawn-sandy/agentics](https://github.com/shawn-sandy/agentics) and is removed
from this repo in the same release, with a deprecation note in the commit.

## License

[MIT](LICENSE)

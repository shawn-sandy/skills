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

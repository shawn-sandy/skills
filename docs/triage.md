# Skill Portability Triage

Verdict for every skill in shawn-sandy/agentics kit/plugins/ against the
portability checklist in docs/proposals/publish-agent-skills-marketplace.md
Appendix A. Generated from signal extraction on 2026-07-26; verdicts are
editorial. Soft signals (AskUserQuestion mentions, disable-model-invocation
keys) do not exclude a skill: the former degrades to asking in chat, the
latter is stripped during extraction.

Included: 12 of 60.

| Plugin | Skill | Verdict | Reason |
|---|---|---|---|
| artifact-tools | diff-artifact | exclude | hard dependency: plugin-root paths |
| artifact-tools | plan-artifact | exclude | hard dependency: plugin-root paths |
| artifact-tools | prompt-artifact | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| artifact-tools | session-artifact | exclude | hard dependency: plugin-root paths |
| code-review | code-review-agent | include | clean signals; universal code-review workflow |
| code-testing-agent | code-testing-agent | include | clean signals; universal test-writing workflow |
| code-testing-agent | reviewing-tests | include | clean signals; test-quality review applies on any agent |
| code-testing-agent | running-tests | include | clean signals; runner-detection workflow is generic |
| code-testing-agent | tdd-fix | include | portable after dropping disable-model-invocation; one prose mention of a sibling skill softened in extraction |
| code-testing-agent | tdd-loop | exclude | needs adaptation: ExitPlanMode step and plan-mode rules woven into the loop |
| content-tools | artifact-to-post | exclude | Claude-artifact concept at its core; rethink for generic HTML sources |
| git-agent | branch-agent | exclude | needs adaptation: plan-mode gating and disable-model-invocation semantics |
| git-agent | commit-agent | exclude | needs adaptation: plan-mode gating; references marketplace versioning |
| git-agent | create-issue | exclude | hard dependency: invokes sibling skills |
| git-agent | merge | exclude | needs adaptation: ExitPlanMode step 0 and plan-mode gating |
| git-agent | pr-agent | exclude | needs adaptation: plan-mode gating |
| git-agent | ship-autonomous | exclude | needs adaptation: plan-mode gating; 415 lines near budget |
| git-agent | ship | exclude | needs adaptation: plan-mode gating |
| memory-tools | agentic-memory-management | include | conditional plan-mode note degrades safely; ships with a compatibility note (audits CLAUDE.md files) |
| memory-tools | path-rules-advisor | exclude | output format is .claude/rules/; Claude Code specific |
| plan-agent | build-proposal | exclude | hard dependency: spawns subagents; invokes sibling skills |
| plan-agent | build | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| plan-agent | deep-grill | include | portable after dropping disable-model-invocation; plan interviews are platform-neutral |
| plan-agent | documenting-plans | exclude | hard dependency: invokes sibling skills |
| plan-agent | finalize-plan | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| plan-agent | implementation-plan | exclude | hard dependency: plugin-root paths; spawns subagents; invokes sibling skills; plugin hooks |
| plan-agent | markdown-to-html | exclude | hard dependency: spawns subagents; invokes sibling skills |
| plan-agent | plan-status | include | clean; edits plan frontmatter with generic file operations |
| plan-agent | plans-library | exclude | hard dependency: invokes sibling skills |
| plan-agent | plans-open | exclude | hard dependency: invokes sibling skills |
| plan-agent | prototype | exclude | hard dependency: plugin-root paths; invokes sibling skills; plugin hooks |
| plan-agent | review-plan | exclude | hard dependency: invokes sibling skills |
| plan-agent | setup-sites | exclude | needs adaptation: plan-mode step; otherwise portable GitHub Pages scaffold |
| plan-agent | write-prompt | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| product-plans | plan-review-agents | exclude | hard dependency: spawns subagents |
| settings-sync | settings-backup | exclude | targets ~/.claude settings specifically; narrow cross-platform value |
| settings-sync | settings-restore | exclude | targets ~/.claude settings specifically; narrow cross-platform value |
| skill-reviewer | auditing-allowed-tools | exclude | hard dependency: plugin-root paths; spawns subagents |
| skill-reviewer | optimizing-skill-frontmatter | exclude | needs adaptation: ExitPlanMode step 0 |
| skill-reviewer | planning-skills | include | clean; skill-design guidance now targets a cross-platform standard |
| skill-reviewer | reviewing-skills | include | clean; SKILL.md review is the Agent Skills spec's own artifact |
| social-media-tools | export-session | exclude | hard dependency: plugin-root paths |
| social-media-tools | media-library | exclude | consumes sibling share-* skill outputs (docs/media/social) |
| social-media-tools | save-artifact | exclude | hard dependency: invokes sibling skills |
| social-media-tools | security-scrub | include | clean; secret/PII scanning is universally valuable |
| social-media-tools | share-blog | exclude | hard dependency: plugin-root paths |
| social-media-tools | share-code | exclude | hard dependency: plugin-root paths |
| social-media-tools | share-explanation | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| social-media-tools | share-github | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| social-media-tools | share-init | exclude | hard dependency: plugin-root paths |
| social-media-tools | share-project | exclude | hard dependency: plugin-root paths |
| social-media-tools | share-react | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| social-media-tools | share-scan | exclude | needs adaptation: plan-mode/Claude-specific step |
| social-media-tools | share-selection | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| social-media-tools | share-session | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| social-media-tools | share-video | exclude | hard dependency: plugin-root paths |
| social-media-tools | social-share | exclude | hard dependency: plugin-root paths; invokes sibling skills |
| social-media-tools | write-guide | exclude | hard dependency: plugin-root paths |
| team-defaults | sync-rules | exclude | hard dependency: plugin-root paths |
| wcag-compliance-reviewer | wcag-compliance-reviewer | include | zero platform flags; accessibility review is fully generic |

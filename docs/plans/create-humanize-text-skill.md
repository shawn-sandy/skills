---
status: completed
type: feature
created: 2026-08-12
issue: https://github.com/shawn-sandy/skills/issues/1
glance: AI-drafted text carries recognizable tells — stock vocabulary, formulaic structure, promotional tone — that flag it instantly to readers and reviewers. Done means a spec-valid humanize-text skill installs from this repo with one command, and running it on an AI-flavored sample produces a category-tagged findings report plus a rewrite with the tells gone and the facts intact.
---

# Plan: Create the humanize-text skill — rewrite AI-sounding text into natural prose

## Objective

Ship skills/humanize-text/: a portable Agent Skill that detects the documented signs of AI writing in any text and rewrites it to read naturally, using Wikipedia's "Signs of AI writing" guide as the pattern source.

## Context

Wikipedia editors maintain a field guide to AI-generated prose (https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) covering stock vocabulary ("delve", "testament", "underscore"), copula avoidance ("serves as" instead of "is"), negative parallelisms ("not just X, but Y"), rule-of-three padding, promotional puffery ("vibrant", "rich tapestry"), vague attributions ("experts argue"), and formatting tells (title-case headings, em-dash overuse, excessive boldface). The guide's key insight: these patterns cluster — density across categories, not any single word, is the signal. The skill encodes that as detection guidance rather than a naive word blacklist.

The new skill follows this repo's established conventions: one directory under skills/ with spec-valid SKILL.md frontmatter per the Agent Skills standard (agentskills.io), pattern detail split into a references/ file so the skill body stays inside the progressive-disclosure budget (the security-scrub skill is the in-repo model), no platform-only dependencies per the portability policy, and a README index row produced by scripts/update-index.py — the index table is generated output and is never hand-edited.

Scope guard: the skill improves writing quality by removing tells while preserving the author's facts, quotes, code blocks, and meaning. It is an editing aid, not a detector-evasion tool, and its SKILL.md states that boundary.

## Steps

1. [x] Author skills/humanize-text/references/ai-writing-signs.md — a detection-and-rewrite catalog distilled from the Wikipedia guide with one section per sign category (stock vocabulary with era-grouped word lists, phrasing and structure, tone and content, formatting and punctuation), each entry pairing the tell with a concrete rewrite strategy, plus a voice-targets section giving rewrite guidance for the three optional tones (casual, formal, punchy) Why: the catalog is the single source of truth the skill loads at runtime, and splitting it into references/ keeps SKILL.md small enough to stay inside the spec's progressive-disclosure budget Verify: the file exists and grep finds all four category headings, the voice-targets section, and representative flagged terms from the guide (delve, testament, underscore, "serves as", "not just").
2. [x] Author skills/humanize-text/SKILL.md with spec-valid frontmatter (name humanize-text, a cross-agent trigger description, allowed-tools Read/Grep/Edit/Write, license MIT, metadata author shawn-sandy and version 1.0) and a numbered workflow: load the references catalog, scan the input text (inline or file path) for tells and classify findings by category with line references, rewrite at balanced depth — always substitute clear tells, restructure sentences only where a category clusters densely — preserving facts/quotes/code and honoring an optional voice target (casual, formal, punchy; default preserves the existing voice), then emit a structured HUMANIZE REPORT block (per-category findings with the tell and its fix, a density note, and the rewrite) — including a review-only mode for when the user asks to flag rather than rewrite Why: SKILL.md is the entry point the Agent Skills spec requires, and an explicit scan-classify-rewrite-report loop with a machine-checkable report keeps behavior consistent and composable across the 70+ agents this repo targets Verify: python3 tests/validate_frontmatter.py skills exits 0 with no humanize-text errors, and the SKILL.md body documents the HUMANIZE REPORT block and the three voice targets.
3. [x] Regenerate the README skill index with python3 scripts/update-index.py Why: the table between the INDEX markers is generated output — repo policy forbids hand-editing it Verify: git diff README.md shows exactly one new table row linking skills/humanize-text with the frontmatter description.
4. [x] Run the repo's CI gates locally: bash tests/validate-all.sh and bash tests/verify-install.sh Why: these are the marketplace repo's merge gates — a skill that fails either never ships Verify: both scripts exit 0 and the install test's summary counts humanize-text among the installed skills.
5. [x] Exercise the skill end-to-end on a planted sample: feed a deliberately AI-flavored paragraph (stock vocabulary, a negative parallelism, promotional adjectives, em-dash overuse) through the humanize-text workflow and inspect the output Why: spec compliance proves the skill installs, not that it works — the objective is met only when a real rewrite removes the tells without changing the facts Verify: the findings report names each planted tell with its category, and the rewrite contains none of the planted flagged terms while every factual claim survives.

## Files

- skills/humanize-text/SKILL.md (new) — skill entry point: frontmatter, scan-classify-rewrite-report workflow, report format
- skills/humanize-text/references/ai-writing-signs.md (new) — detection-and-rewrite catalog distilled from the Wikipedia guide
- README.md (generated) — index row added by scripts/update-index.py

## Acceptance Criteria

- [x] bash tests/validate-all.sh exits 0 with skills/humanize-text/ present
- [x] bash tests/verify-install.sh exits 0 and its output counts humanize-text among the installed skills
- [x] The README index row for humanize-text was produced by scripts/update-index.py, not a hand edit
- [x] references/ai-writing-signs.md contains all four category sections (stock vocabulary, phrasing and structure, tone and content, formatting and punctuation) plus the voice-targets section
- [x] Running the skill on an AI-flavored sample paragraph yields a structured HUMANIZE REPORT block with category-tagged findings and a rewrite free of the planted tells with facts intact
- [x] No file under skills/humanize-text/ carries disable-model-invocation or CLAUDE_PLUGIN_ROOT references

## Tests

Tier 1 — steps create runnable skill content that ships to 70+ agents
- Objective: the humanize-text skill is spec-valid and installs cross-platform. File: tests/verify-install.sh; Type: smoke; Asserts: a clean npx skills add of this repo lands skills/humanize-text/SKILL.md in the throwaway project's .claude/skills/; Run: bash tests/verify-install.sh
- Integration: spec-compliance sweep. File: tests/validate-all.sh; Targets: skills/humanize-text/SKILL.md frontmatter; Key cases: name matches directory, description within 1024 chars, no Claude-only keys; Run: bash tests/validate-all.sh

## Verification

From the repo root, run bash tests/validate-all.sh and bash tests/verify-install.sh — both must exit 0 and the install test's summary must count the new skill. Confirm git diff README.md shows the humanize-text index row and nothing else outside the INDEX markers.

Then the end-to-end check: in an agent session with the skill installed, paste a sample paragraph planted with known tells (for example: "This vibrant framework serves as a testament to modern engineering — it doesn't just compile code, it delves into every module, underscoring a rich tapestry of optimizations"), ask to humanize it, and confirm the response contains (a) a structured HUMANIZE REPORT block naming each planted tell with its category and fix and (b) a rewrite in which none of the planted flagged terms appear while the paragraph's factual claims are unchanged. Repeat once with an explicit voice target ("humanize this, punchy") and confirm the rewrite shifts register while still clearing the tells.

## Next Steps

- Sync the new skill into the agentics plugin mirror
  The skills repo is canonical; the agentics monorepo syncs from it.
  ```text
  In the shawn-sandy/agentics repo, sync the humanize-text skill from
  github.com/shawn-sandy/skills into the plugin whose theme fits (or confirm
  it should stay marketplace-only), bump that plugin's version in
  .claude-plugin/marketplace.json, and add a CHANGELOG entry. Verify by
  running /plugin update in Claude Code and confirming the skill loads.
  ```
- Era-vocabulary refresh cadence (wish list)
  The Wikipedia guide notes flagged vocabulary shifts by model generation.
  ```text
  In the shawn-sandy/skills repo, review
  skills/humanize-text/references/ai-writing-signs.md against the current
  revision of https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
  and add any newly documented vocabulary or pattern tells to the catalog,
  keeping the era grouping. Verify bash tests/validate-all.sh still exits 0.
  ```

## Resources

- Wikipedia: Signs of AI writing — https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing (pattern source for the references catalog; consulted 2026-08-12)
- Agent Skills specification — https://agentskills.io/specification (frontmatter and layout rules the validators enforce)
- skills/security-scrub/ — in-repo model for the SKILL.md + references/ split and frontmatter shape

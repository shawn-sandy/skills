---
name: humanize-text
description: "Rewrites AI-sounding text into natural prose, flagging stock vocabulary, formulaic structure, and promotional tone. Use when asked to humanize text or make writing sound less like AI."
allowed-tools: Read, Grep, Edit, Write
license: MIT
metadata:
  author: shawn-sandy
  version: "1.0"
---

# humanize-text

Detect the documented signs of AI-generated writing in any text and rewrite it
to read naturally. Emits a structured `HUMANIZE REPORT` block that callers can
check before using the rewrite.

## Overview

Five steps, run in order. Input is either inline text or a file path. The
default mode rewrites; the user can ask for **review-only** (flag findings,
change nothing) or name a **voice target** (casual, formal, punchy).

**Boundary:** this skill is an editing aid. It removes the stylistic tells of
AI drafting while preserving the author's facts, quotes, code blocks, and
meaning. It is not a tool for evading AI-disclosure requirements — if the
context requires disclosing AI assistance, say so.

## Step 1 — Load rules

`Read` the `references/ai-writing-signs.md` file adjacent to this SKILL.md. It
carries the four sign categories (stock vocabulary, phrasing and structure,
tone and content, formatting and punctuation), the rewrite strategy for each
tell, the voice-target guidance, and the density scoring rules.

## Step 2 — Resolve input and mode

- **Inline text** — the text the user pasted or quoted is the input.
- **File path** — `Read` the file; its full contents are the input.
- **Mode** — `rewrite` unless the user asked to only flag, review, or check
  the text ("just tell me what sounds like AI") → `review-only`.
- **Voice** — `preserved` unless the user named a target: `casual`, `formal`,
  or `punchy`.

## Step 3 — Scan and classify

Walk the input against each category's tell table. Record every finding with
its category, the line or sentence it sits in, the matched text, and the
planned fix. Then apply the density principle from the rules file: score the
text LOW / MEDIUM / HIGH by how many categories fire and how tightly findings
cluster. A lone common word in natural prose is a weak signal — do not flag
isolated hits in text that otherwise reads human.

## Step 4 — Rewrite (skip in review-only mode)

Apply fixes at **balanced depth**:

- Always substitute clear tells — stock vocabulary, copula avoidance,
  puffery, weasel attributions — using each entry's rewrite strategy.
- Restructure sentences only where the density score says a category clusters
  (MEDIUM restructures the worst sentences; HIGH also varies rhythm, breaks
  parallel triads, and rebuilds formulaic paragraphs).

Hard rules, regardless of depth or voice:

- Never change facts, names, numbers, dates, or quoted material.
- Never touch code blocks, commands, or identifiers.
- Never invent specifics the source did not contain.
- Honor the voice target from `references/ai-writing-signs.md`; `preserved`
  means the author's register survives untouched apart from the tells.

For file input, apply the rewrite to the file with `Edit` after emitting the
report.

## Step 5 — Emit the HUMANIZE REPORT

Output exactly this block (fill in the brackets), then the rewrite:

```
HUMANIZE REPORT
---
Mode: [rewrite | review-only]
Voice: [preserved | casual | formal | punchy]
Density: [LOW | MEDIUM | HIGH] — <n> findings across <m> categories
Findings:
  - [category] line <n>: "<matched text>" → <fix applied or proposed>
---
```

- In `rewrite` mode, follow the block with the full rewritten text (or, for
  file input, a note that the file was edited in place plus a summary of what
  changed).
- In `review-only` mode, stop after the block — propose fixes in the findings
  lines but change nothing.
- No findings → `Findings: none`, density LOW, and the text returned
  unchanged with a note that it already reads naturally.

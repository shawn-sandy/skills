#!/usr/bin/env python3
"""Count which slash commands, skills, MCP tools, and subagents actually ran
across Claude Code session logs (JSONL), so unused entries in the load set
stand out. Prints distinct sessions and total calls per name, then a rollup
by plugin prefix (the part before ':' in a command or skill name).

Usage:
  count_usage.py [--since YYYY-MM-DD] [--follows PATH=NAME ...] [PATH ...]

PATH is a .jsonl file or a directory searched recursively for them. With no
PATH, scans ~/.claude/projects/<encoded cwd>*/ — the log directories Claude
Code keeps for the current project and its worktrees.

--follows PATH=NAME checks one CLAUDE.md rule of the form "use NAME when
touching PATH": it reports how many sessions edited a file whose path contains
PATH and how many of those used NAME (invoked it as a skill, typed it as a
command, read a file whose path contains NAME, or ran a shell command that
mentions NAME). Edits made through shell redirection count as edits. Stdlib only.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

CMD_RE = re.compile(r"<command-name>/?([^<]+)</command-name>")
CATEGORIES = ("commands", "skills", "mcp", "subagents")
EDIT_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")
# ponytail: a shell command "touches" a path when it also carries a write operator;
# refine per-command if false positives from `ls foo > out` ever matter.
# A ">" preceded by a digit or "&" is stderr plumbing (2>&1), and ">/dev/null" writes nothing.
SHELL_WRITE_RE = re.compile(r"((?<![0-9&])>(?!&|\s*/dev/null)|\btee\b|\bsed -i|\bmv\b|\bcp\b|\brm\b)")


def default_paths():
    # Claude Code names a project's log dir by replacing every
    # non-alphanumeric character of its absolute path with '-'.
    encoded = re.sub(r"[^A-Za-z0-9]", "-", os.getcwd())
    return glob.glob(os.path.expanduser(f"~/.claude/projects/{encoded}*"))


def jsonl_files(paths):
    """Yield (session_id, path). A session's own log is <root>/<id>.jsonl and
    its subagent logs sit under <root>/<id>/..., so the first path segment
    below the scanned root names the session either way."""
    for p in paths:
        if os.path.isdir(p):
            for f in glob.glob(os.path.join(p, "**", "*.jsonl"), recursive=True):
                head = os.path.relpath(f, p).split(os.sep)[0]
                yield (head[:-6] if head.endswith(".jsonl") else head), f
        elif p.endswith(".jsonl") and os.path.isfile(p):
            yield os.path.basename(p)[:-6], p


def blocks(event):
    content = (event.get("message") or {}).get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    return [b for b in content or [] if isinstance(b, dict)]


def scan(files, since):
    tally = {c: collections.defaultdict(lambda: [0, set()]) for c in CATEGORIES}
    per_session = collections.defaultdict(lambda: {"edits": set(), "touched": set()})
    sessions = set()
    first = last = None

    def hit(category, name, session):
        row = tally[category][name]
        row[0] += 1
        row[1].add(session)

    for session, path in files:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    event = json.loads(line)
                except ValueError:
                    continue  # partial or corrupt line; skip it, keep counting
                stamp = str(event.get("timestamp") or "")[:10]
                if stamp and stamp < since:
                    continue
                if stamp:
                    first = min(first or stamp, stamp)
                    last = max(last or stamp, stamp)
                sessions.add(session)
                kind = event.get("type")
                for block in blocks(event):
                    # Slash commands the user typed. Only user text blocks count,
                    # so tool results that quote a transcript do not inflate it.
                    if kind == "user" and block.get("type") == "text":
                        for name in CMD_RE.findall(block.get("text") or ""):
                            hit("commands", name.strip(), session)
                            per_session[session]["touched"].add(name.strip())
                    if kind == "assistant" and block.get("type") == "tool_use":
                        tool = block.get("name") or ""
                        args = block.get("input") or {}
                        if tool == "Skill":
                            skill = str(args.get("skill", "?"))
                            hit("skills", skill, session)
                            per_session[session]["touched"].add(skill)
                        elif tool.startswith("mcp__"):
                            hit("mcp", tool, session)
                        elif tool in ("Agent", "Task"):
                            hit("subagents", str(args.get("subagent_type", "(default)")), session)
                        elif tool in EDIT_TOOLS:
                            per_session[session]["edits"].add(str(args.get("file_path") or args.get("notebook_path") or ""))
                        elif tool == "Read":
                            per_session[session]["touched"].add(str(args.get("file_path") or ""))
                        elif tool == "Bash":
                            command = str(args.get("command") or "")
                            per_session[session]["touched"].add(command)
                            if SHELL_WRITE_RE.search(command):
                                per_session[session]["edits"].add(command)
    return tally, per_session, sessions, first, last


def print_table(title, rows):
    print(f"\n## {title}")
    if not rows:
        print("(none)")
        return
    print(f"{'sessions':>8} {'calls':>6}  name")
    for name, (calls, sessions) in sorted(rows.items(), key=lambda kv: (-len(kv[1][1]), -kv[1][0], kv[0])):
        print(f"{len(sessions):>8} {calls:>6}  {name}")


def print_rule_check(spec, per_session):
    path_sub, _, name = spec.partition("=")
    if not path_sub or not name:
        sys.exit(f"error: --follows expects PATH=NAME, got {spec!r}")
    editing = {s for s, d in per_session.items() if any(path_sub in p for p in d["edits"])}
    followed = {s for s in editing if any(name in item for item in per_session[s]["touched"])}
    share = f"{100 * len(followed) // len(editing)}%" if editing else "n/a"
    print(f"\n## Rule check: use {name} when touching {path_sub}")
    print(f"{len(editing)} sessions edited a matching file; {len(followed)} of those used {name} ({share}).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help=".jsonl files or directories of them")
    ap.add_argument("--since", default="", metavar="YYYY-MM-DD", help="ignore events dated before this day")
    ap.add_argument("--follows", action="append", default=[], metavar="PATH=NAME",
                    help="check the rule 'use NAME when touching PATH'; repeatable")
    args = ap.parse_args()

    files = sorted(set(jsonl_files(args.paths or default_paths())))
    if not files:
        sys.exit("error: no .jsonl session logs found; pass a log directory as PATH")

    tally, per_session, sessions, first, last = scan(files, args.since)
    print(f"# Skill usage across {len(sessions)} sessions, {len(files)} log files ({first or '?'} to {last or '?'})")
    print_table("Slash commands typed by the user", tally["commands"])
    print_table("Skills invoked by the agent", tally["skills"])
    print_table("MCP tools called", tally["mcp"])
    print_table("Subagents spawned", tally["subagents"])

    # Plugin rollup: 'git-agent:commit-agent' belongs to plugin 'git-agent'.
    by_plugin = collections.defaultdict(lambda: [0, set()])
    for category in ("commands", "skills"):
        for name, (calls, sessions_hit) in tally[category].items():
            plugin = name.split(":", 1)[0] if ":" in name else "(project-local or built-in)"
            by_plugin[plugin][0] += calls
            by_plugin[plugin][1] |= sessions_hit
    print_table("Rollup by plugin prefix (commands + skills)", by_plugin)
    print("\nAny enabled plugin, command file, or agent file missing from these tables had zero invocations.")

    for spec in args.follows:
        print_rule_check(spec, per_session)


if __name__ == "__main__":
    main()

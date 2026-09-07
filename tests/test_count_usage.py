#!/usr/bin/env python3
"""Regression tests for skills/optimizing-agent-context/scripts/count_usage.py.

Run: python3 -B -m unittest tests/test_count_usage.py
"""
import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True  # keep __pycache__ out of the skill directory
SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "skills" / "optimizing-agent-context" / "scripts" / "count_usage.py"
_spec = importlib.util.spec_from_file_location("count_usage", SCRIPT)
cu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cu)


def event(kind, content, stamp="2026-09-01T10:00:00Z"):
    return json.dumps({"type": kind, "timestamp": stamp, "message": {"role": kind, "content": content}})


class ScanTolerance(unittest.TestCase):
    def test_well_formed_json_that_is_not_an_event_is_skipped(self):
        good = event("user", [{"type": "text", "text": "<command-name>/demo:cmd</command-name>"}])
        junk = [
            "null", "42", "[1, 2]", "{broken json",
            json.dumps({"type": "user", "timestamp": "2026-09-01", "message": "not-a-dict"}),
            json.dumps({"type": "assistant", "timestamp": "2026-09-01", "message": {"content": 42}}),
        ]
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "s.jsonl"), "w") as fh:
                fh.write("\n".join(junk + [good]) + "\n")
            tally, per_session, sessions, first, last = cu.scan(list(cu.jsonl_files([d])), "")
        self.assertEqual(tally["commands"]["demo:cmd"][0], 1)
        self.assertEqual(sessions, {"s"})


class ShellWriteRegex(unittest.TestCase):
    def test_redirects_into_files_count_as_writes(self):
        for cmd in ["cmd 2> error.log", "cmd 1> out.txt", "cmd &> both.log", "cat > x.ts <<EOF", "echo hi >> log"]:
            self.assertTrue(cu.SHELL_WRITE_RE.search(cmd), cmd)

    def test_descriptor_plumbing_is_not_a_write(self):
        for cmd in ["cmd 2>&1 | head", "grep x dir 2>/dev/null", "ls >/dev/null", "cat f"]:
            self.assertFalse(cu.SHELL_WRITE_RE.search(cmd), cmd)


if __name__ == "__main__":
    unittest.main()

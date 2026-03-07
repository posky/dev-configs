#!/usr/bin/env python3

import json
import os
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("manage_issues.py")


def make_exec(path, content):
    path.write_text(textwrap.dedent(content))
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


def fake_git(path):
    make_exec(
        path,
        """\
        #!/usr/bin/env python3
        import os, sys
        if sys.argv[1:] == ["remote", "get-url", "origin"] and os.environ.get("GIT_REMOTE_URL"):
            print(os.environ["GIT_REMOTE_URL"])
            raise SystemExit(0)
        raise SystemExit(1)
        """,
    )


def fake_gh(path):
    make_exec(
        path,
        """\
        #!/usr/bin/env python3
        import json, os, pathlib, sys

        def next_payload(env):
            state_path = pathlib.Path(env["GH_STATE"])
            state = json.loads(state_path.read_text()) if state_path.exists() else {"index": 0}
            payloads = json.loads(env.get("GH_PAYLOADS", "[{}]"))
            payload = payloads[min(state["index"], len(payloads) - 1)]
            state["index"] += 1
            state_path.write_text(json.dumps(state))
            return payload

        args = sys.argv[1:]
        log_path = pathlib.Path(os.environ["GH_LOG"])
        calls = json.loads(log_path.read_text()) if log_path.exists() else []
        calls.append(args)
        log_path.write_text(json.dumps(calls))
        if args[:2] == ["auth", "status"]:
            raise SystemExit(0 if os.environ.get("GH_AUTH_OK", "1") == "1" else 1)
        if args[:2] == ["label", "list"]:
            mode = os.environ.get("GH_LABEL_MODE", "ok")
            if mode == "fail":
                raise SystemExit(1)
            print(os.environ.get("GH_LABELS", "[]"))
            raise SystemExit(0)
        if args[:2] == ["issue", "list"] or args[:2] == ["issue", "view"]:
            print(next_payload(os.environ))
            raise SystemExit(0)
        if args[:2] == ["issue", "create"]:
            if os.environ.get("GH_CREATE_FAIL") == "1":
                print("HTTP 403", file=sys.stderr)
                raise SystemExit(1)
            print(os.environ.get("GH_CREATE_STDOUT", "https://github.com/octo/demo/issues/12"))
            raise SystemExit(0)
        if args[:2] == ["issue", "edit"]:
            if os.environ.get("GH_EDIT_FAIL") == "1":
                raise SystemExit(1)
            print("edited")
            raise SystemExit(0)
        if args and args[0] == "api":
            mode = os.environ.get("GH_API_MODE", "ok")
            if mode == "fail":
                print(os.environ.get("GH_API_STDERR", ""), file=sys.stderr, end="")
                raise SystemExit(1)
            if mode == "invalid_json":
                print("{")
                raise SystemExit(0)
            print(next_payload(os.environ))
            raise SystemExit(0)
        raise SystemExit(2)
        """,
    )


class ManageIssuesTests(unittest.TestCase):
    def run_case(self, args, payloads=None, labels=None, remote="git@github.com:octo/demo.git", auth_ok=True, api_mode="ok", api_stderr=""):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)
        gh_log = root / "gh-log.json"
        gh_state = root / "gh-state.json"
        git_path = root / "fake-git.py"
        gh_path = root / "fake-gh.py"
        body_path = root / "body.md"
        body_path.write_text("Body from file")
        fake_git(git_path)
        fake_gh(gh_path)
        env = os.environ.copy()
        env.update(
            {
                "PYTHONPATH": str(SCRIPT.parent),
                "GIT_BIN": str(git_path),
                "GH_BIN": str(gh_path),
                "GH_LOG": str(gh_log),
                "GH_STATE": str(gh_state),
                "GIT_REMOTE_URL": remote,
                "GH_AUTH_OK": "1" if auth_ok else "0",
                "GH_API_MODE": api_mode,
                "GH_API_STDERR": api_stderr,
                "GH_PAYLOADS": json.dumps(payloads or ["{}"]),
                "GH_LABELS": json.dumps(labels or []),
                "BODY_FILE": str(body_path),
            }
        )
        completed = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False, env=env)
        body = json.loads(completed.stdout)
        calls = json.loads(gh_log.read_text()) if gh_log.exists() else []
        return completed, body, calls, body_path

    def test_list_and_view(self):
        completed, body, calls, _ = self.run_case(
            ["list", "--label", "bug", "--milestone", "v1", "--author", "octo", "--assignee", "@me", "--search", "crash", "--limit", "5"],
            payloads=['[{"number":1}]'],
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(body["action"], "list")
        self.assertTrue(any(call[:2] == ["auth", "status"] for call in calls))

        completed, body, _, _ = self.run_case(["view", "7", "--comments"], payloads=['{"number":7,"comments":[{}]}'])
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(body["data"]["number"], 7)

    def test_create_with_explicit_and_auto_metadata(self):
        payloads = ['[{"name":"bug"},{"name":"docs"}]', '{"number":12,"title":"Bug"}']
        labels = [{"name": "bug"}, {"name": "docs"}]
        completed, body, calls, _ = self.run_case(
            ["create", "--title", "Bug Sprint 1", "--label", "bug"],
            payloads=payloads,
            labels=labels,
        )
        self.assertEqual(completed.returncode, 0)
        create_call = next(call for call in calls if call[:2] == ["issue", "create"])
        self.assertIn("--label", create_call)

        payloads = ['[{"name":"bug"},{"name":"docs"}]', '[{"title":"Sprint 1"}]', '{"number":12,"title":"Bug Sprint 1"}']
        completed, body, calls, _ = self.run_case(
            ["create", "--title", "Bug Sprint 1"],
            payloads=payloads,
            labels=labels,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(body["data"]["applied_labels"], ["bug"])
        self.assertEqual(body["data"]["applied_milestone"], "Sprint 1")

    def test_create_body_file_and_ambiguous_milestone_warning(self):
        labels = [{"name": "bug"}]
        payloads = ['[{"name":"bug"}]', '[{"title":"Sprint 1"},{"title":"Sprint 2"}]', '{"number":12}']
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        body_path = Path(temp_dir.name) / "body.md"
        body_path.write_text("Body from file")
        completed, body, calls, _ = self.run_case(
            ["create", "--title", "bug sprint 1 sprint 2", "--body-file", str(body_path)],
            payloads=payloads,
            labels=labels,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(body["warnings"][0]["code"], "ambiguous_milestone")

        completed, body, _, _ = self.run_case(["create", "--title", "bug", "--body-file", "/missing/file"], labels=labels)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "body_file_unreadable")

    def test_edit_and_validation_failures(self):
        payloads = ['{"number":7,"title":"Edited"}']
        labels = [{"name": "bug"}, {"name": "docs"}]
        completed, body, calls, _ = self.run_case(
            ["edit", "7", "--add-label", "docs", "--remove-label", "bug", "--milestone", "Sprint 1"],
            payloads=['[{"name":"bug"},{"name":"docs"}]', '[{"title":"Sprint 1"}]', '{"number":7,"title":"Edited"}'],
            labels=labels,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(body["data"]["title"], "Edited")

        cases = [
            (["edit", "0", "--title", "x"], "invalid_issue_number", payloads),
            (["create"], "empty_title", payloads),
            (["edit", "7"], "missing_update_fields", payloads),
            (["edit", "7", "--milestone", "x", "--remove-milestone"], "invalid_milestone_change", payloads),
            (["create", "--title", "x", "--label", "missing"], "unknown_label", ['[{"name":"bug"},{"name":"docs"}]']),
            (["edit", "7", "--milestone", "missing"], "unknown_milestone", ['[{"title":"Sprint 1"}]']),
        ]
        for args, code, case_payloads in cases:
            with self.subTest(code=code):
                completed, body, _, _ = self.run_case(args, payloads=case_payloads, labels=labels)
                self.assertEqual(completed.returncode, 1)
                self.assertFalse(body["ok"])
                self.assertEqual(body["code"], code)

    def test_paginated_metadata_and_alt_remote(self):
        labels_page1 = [{"name": f"label-{index}"} for index in range(1, 101)]
        labels_page2 = [{"name": f"label-{index}"} for index in range(101, 106)]
        completed, body, _, _ = self.run_case(
            ["create", "--title", "Needs page two", "--label", "label-105"],
            payloads=[json.dumps(labels_page1), json.dumps(labels_page2), '{"number":12,"title":"Needs page two"}'],
            remote="ssh://git@github.com/octo/demo.git",
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(body["repo"], "octo/demo")

    def test_sub_issue_actions_and_failures(self):
        completed, body, calls, _ = self.run_case(["list-sub-issues", "7", "--per-page", "2", "--page", "3"], payloads=['[{"id":1}]'])
        self.assertEqual(completed.returncode, 0)
        api_call = next(call for call in calls if call and call[0] == "api")
        self.assertTrue(api_call[-1].endswith("/sub_issues?per_page=2&page=3"))

        completed, body, calls, _ = self.run_case(["get-parent", "7"], payloads=['{"id":2}'])
        self.assertEqual(completed.returncode, 0)

        completed, body, calls, _ = self.run_case(["add-sub-issue", "7", "--sub-issue-id", "11", "--replace-parent"], payloads=['{"ok":true}'])
        self.assertEqual(completed.returncode, 0)
        api_call = next(call for call in calls if call and call[0] == "api")
        self.assertIn("sub_issue_id=11", api_call)
        self.assertIn("replace_parent=true", api_call)

        completed, body, calls, _ = self.run_case(["remove-sub-issue", "7", "--sub-issue-id", "11"], payloads=['{"ok":true}'])
        self.assertEqual(completed.returncode, 0)

        cases = [
            (["list-sub-issues", "7", "--per-page", "0"], "invalid_pagination"),
            (["add-sub-issue", "0", "--sub-issue-id", "1"], "invalid_parent_issue_number"),
            (["remove-sub-issue", "7", "--sub-issue-id", "0"], "invalid_sub_issue_id"),
        ]
        for args, code in cases:
            with self.subTest(code=code):
                completed, body, _, _ = self.run_case(args)
                self.assertEqual(completed.returncode, 1)
                self.assertEqual(body["code"], code)

    def test_auth_repo_and_api_failures(self):
        completed, body, _, _ = self.run_case(["list"], auth_ok=False)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_auth_invalid")

        completed, body, _, _ = self.run_case(["list"], remote="https://example.com/nope.git")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "repo_unresolved")

        completed, body, _, _ = self.run_case(["list", "--repo", "bad/repo/name"])
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "invalid_repo")

        completed, body, _, _ = self.run_case(["list-sub-issues", "7"], api_mode="fail", api_stderr="HTTP 403")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_forbidden")

        completed, body, _, _ = self.run_case(["get-parent", "7"], api_mode="invalid_json")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_api_invalid_json")

        completed, body, _, _ = self.run_case(["view", "7"], payloads=["{"], api_mode="ok")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_issue_view_invalid_json")


if __name__ == "__main__":
    unittest.main()

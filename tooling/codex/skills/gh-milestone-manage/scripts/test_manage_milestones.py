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

SCRIPT = Path(__file__).with_name("manage_milestones.py")


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

        args = sys.argv[1:]
        log_path = pathlib.Path(os.environ["GH_LOG"])
        calls = json.loads(log_path.read_text()) if log_path.exists() else []
        calls.append(args)
        log_path.write_text(json.dumps(calls))
        if args[:2] == ["auth", "status"]:
            raise SystemExit(0 if os.environ.get("GH_AUTH_OK", "1") == "1" else 1)
        if args and args[0] == "api":
            mode = os.environ.get("GH_API_MODE", "ok")
            if mode == "fail":
                print(os.environ.get("GH_API_STDERR", ""), file=sys.stderr, end="")
                raise SystemExit(1)
            if mode == "invalid_json":
                print("{")
                raise SystemExit(0)
            state_path = pathlib.Path(os.environ["GH_STATE"])
            state = json.loads(state_path.read_text()) if state_path.exists() else {"index": 0}
            payloads = json.loads(os.environ.get("GH_API_PAYLOADS", "[{}]"))
            payload = payloads[min(state["index"], len(payloads) - 1)]
            state["index"] += 1
            state_path.write_text(json.dumps(state))
            print(payload)
            raise SystemExit(0)
        raise SystemExit(2)
        """,
    )


class ManageMilestonesTests(unittest.TestCase):
    def run_case(self, args, payloads=None, remote="git@github.com:octo/demo.git", auth_ok=True, mode="ok", stderr=""):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)
        gh_log = root / "gh-log.json"
        gh_state = root / "gh-state.json"
        git_path = root / "fake-git.py"
        gh_path = root / "fake-gh.py"
        fake_git(git_path)
        fake_gh(gh_path)
        env = os.environ.copy()
        env["GIT_BIN"] = str(git_path)
        env["GH_BIN"] = str(gh_path)
        env["GH_LOG"] = str(gh_log)
        env["GH_STATE"] = str(gh_state)
        env["GIT_REMOTE_URL"] = remote
        env["GH_AUTH_OK"] = "1" if auth_ok else "0"
        env["GH_API_MODE"] = mode
        env["GH_API_STDERR"] = stderr
        env["GH_API_PAYLOADS"] = json.dumps(payloads or ["{}"])
        completed = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False, env=env)
        body = json.loads(completed.stdout)
        calls = json.loads(gh_log.read_text()) if gh_log.exists() else []
        return completed, body, calls

    def test_success_commands(self):
        cases = [
            (["list"], ["[{\"number\": 1}]"], "list", None),
            (["get", "7"], ["{\"number\": 7}"], "get", 7),
            (["create", "--title", "Sprint", "--due-on", "2026-03-07"], ["{\"number\": 8}"], "create", None),
            (["update", "7", "--description", "Refined"], ["{\"number\": 7}"], "update", 7),
            (["close", "7"], ["{\"number\": 7, \"state\": \"closed\"}"], "close", 7),
            (["reopen", "7"], ["{\"number\": 7, \"state\": \"open\"}"], "reopen", 7),
            (["delete", "7", "--confirm-delete"], ["{\"number\": 7, \"title\": \"Sprint\"}", "{}"], "delete", 7),
        ]
        for args, payloads, action, number in cases:
            with self.subTest(action=action):
                completed, body, calls = self.run_case(args, payloads=payloads)
                self.assertEqual(completed.returncode, 0)
                self.assertTrue(body["ok"])
                self.assertEqual(body["action"], action)
                if number is not None:
                    self.assertEqual(body["milestone_number"], number)
                if action == "delete":
                    api_calls = [call for call in calls if call and call[0] == "api"]
                    self.assertEqual(api_calls[-2][-1], "repos/octo/demo/milestones/7")
                    self.assertEqual(api_calls[-1][2], "DELETE")

    def test_repo_override_and_due_on_normalization(self):
        completed, body, calls = self.run_case(
            ["create", "--repo", "acme/app", "--title", "Release", "--due-on", "2026-03-07T10:30:00+09:00"],
            payloads=["{\"number\": 9}"],
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(body["repo"], "acme/app")
        api_call = next(call for call in calls if call and call[0] == "api")
        self.assertIn("due_on=2026-03-07T01:30:00Z", api_call)

    def test_invalid_repo_and_repo_inference_failure(self):
        completed, body, _ = self.run_case(["list", "--repo", "bad"], remote="")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "invalid_repo")
        completed, body, _ = self.run_case(["list"], remote="https://example.com/nope.git")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "repo_unresolved")

    def test_validation_failures(self):
        cases = [
            (["get", "0"], "invalid_milestone_number"),
            (["list", "--state", "draft"], "invalid_state"),
            (["list", "--sort", "title"], "invalid_sort"),
            (["list", "--direction", "sideways"], "invalid_direction"),
            (["list", "--per-page", "0"], "invalid_per_page"),
            (["list", "--page", "0"], "invalid_page"),
            (["create"], "empty_title"),
            (["create", "--title", "   "], "empty_title"),
            (["create", "--title", "x", "--due-on", "bad"], "invalid_due_on"),
            (["create", "--title", "x", "--due-on", "2026-03-07T10:30:00"], "invalid_due_on"),
            (["update", "4"], "missing_update_fields"),
            (["delete", "4"], "delete_confirmation_required"),
        ]
        for args, code in cases:
            with self.subTest(code=code):
                completed, body, _ = self.run_case(args)
                self.assertEqual(completed.returncode, 1)
                self.assertEqual(body["code"], code)

    def test_auth_failure(self):
        completed, body, calls = self.run_case(["list"], auth_ok=False)
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_auth_invalid")
        self.assertEqual(len([call for call in calls if call[:2] == ["auth", "status"]]), 1)

    def test_gh_api_failure_and_invalid_json(self):
        completed, body, _ = self.run_case(["list"], mode="fail")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_api_failed")
        completed, body, _ = self.run_case(["list"], mode="fail", stderr="HTTP 403: Forbidden")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_api_forbidden")
        completed, body, _ = self.run_case(["list"], mode="fail", stderr="HTTP 401: Unauthorized")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_api_unauthorized")
        completed, body, _ = self.run_case(["list"], mode="invalid_json")
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(body["code"], "gh_api_invalid_json")


if __name__ == "__main__":
    unittest.main()

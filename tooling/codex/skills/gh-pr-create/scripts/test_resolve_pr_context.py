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

SCRIPT_PATH = Path(__file__).with_name("resolve_pr_context.py")


def run_git(repo_root, *args):
    subprocess.run(["git", "-C", str(repo_root), *args], check=True, capture_output=True, text=True)


def write_fake_gh(path):
    path.write_text(
        textwrap.dedent(
            """\
            #!/usr/bin/env python3
            import json
            import os
            import sys

            args = sys.argv[1:]
            if args[:2] == ["auth", "status"]:
                if os.environ.get("GH_AUTH_OK", "1") == "1":
                    print("ok")
                    raise SystemExit(0)
                print("auth failed", file=sys.stderr)
                raise SystemExit(1)
            if args[:2] == ["issue", "view"]:
                payload = json.loads(os.environ.get("GH_FIXTURES", "{}")).get(args[2])
                if payload is None:
                    print("missing issue", file=sys.stderr)
                    raise SystemExit(1)
                print(json.dumps(payload))
                raise SystemExit(0)
            if args[:2] == ["label", "list"]:
                mode = os.environ.get("GH_LABEL_MODE", "ok")
                if mode == "fail":
                    print("label lookup failed", file=sys.stderr)
                    raise SystemExit(1)
                if mode == "invalid_json":
                    print("{")
                    raise SystemExit(0)
                print(os.environ.get("GH_LABEL_FIXTURES", "[]"))
                raise SystemExit(0)
            print("unsupported gh invocation", file=sys.stderr)
            raise SystemExit(2)
            """
        )
    )
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


def write_fake_git(path):
    path.write_text(
        textwrap.dedent(
            """\
            #!/usr/bin/env python3
            import os
            import subprocess
            import sys

            args = sys.argv[1:]
            if "--name-only" in args and os.environ.get("GIT_DIFF_FAIL") == "1":
                print("diff failed", file=sys.stderr)
                raise SystemExit(1)
            completed = subprocess.run(["git", *args], check=False)
            raise SystemExit(completed.returncode)
            """
        )
    )
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


class ResolvePrContextTests(unittest.TestCase):
    def make_repo(self):
        temp_dir = tempfile.TemporaryDirectory()
        repo_root = Path(temp_dir.name)
        run_git(repo_root, "init", "-b", "develop")
        run_git(repo_root, "config", "user.name", "Test User")
        run_git(repo_root, "config", "user.email", "test@example.com")
        (repo_root / "README.md").write_text("test\n")
        run_git(repo_root, "add", "README.md")
        run_git(repo_root, "commit", "-m", "initial")
        run_git(repo_root, "checkout", "-b", "feature/test")
        run_git(repo_root, "branch", "main")
        run_git(repo_root, "remote", "add", "origin", "https://example.com/repo.git")
        run_git(repo_root, "update-ref", "refs/remotes/origin/feature/test", "HEAD")
        run_git(repo_root, "branch", "--set-upstream-to=origin/feature/test", "feature/test")
        fake_gh = repo_root / "fake-gh.py"
        fake_git = repo_root / "fake-git.py"
        write_fake_gh(fake_gh)
        write_fake_git(fake_git)
        return temp_dir, repo_root, fake_gh, fake_git

    def commit_file(self, repo_root, relative_path, contents):
        target = repo_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents)
        run_git(repo_root, "add", str(relative_path))
        run_git(repo_root, "commit", "-m", f"add {relative_path}")

    def run_resolver(
        self,
        repo_root,
        fake_gh,
        fake_git,
        request_text,
        fixtures=None,
        labels=None,
        auth_ok=True,
        extra_args=None,
        label_mode="ok",
        git_diff_fail=False,
    ):
        request_file = repo_root / "request.txt"
        request_file.write_text(request_text)
        env = os.environ.copy()
        env["GH_BIN"] = str(fake_gh)
        env["GIT_BIN"] = str(fake_git)
        env["GH_FIXTURES"] = json.dumps(fixtures or {})
        env["GH_LABEL_FIXTURES"] = json.dumps(labels or [])
        env["GH_LABEL_MODE"] = label_mode
        env["GH_AUTH_OK"] = "1" if auth_ok else "0"
        env["GIT_DIFF_FAIL"] = "1" if git_diff_fail else "0"
        command = [sys.executable, str(SCRIPT_PATH), "--repo-root", str(repo_root), "--request-file", str(request_file)]
        if extra_args:
            command.extend(extra_args)
        completed = subprocess.run(command, check=False, capture_output=True, text=True, env=env)
        return completed, json.loads(completed.stdout)

    def test_parses_close_related_and_majority_milestone(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        fixtures = {
            "12": {"milestone": {"title": "Sprint A"}, "title": "One", "url": "u1", "state": "OPEN"},
            "34": {"milestone": {"title": "Sprint A"}, "title": "Two", "url": "u2", "state": "OPEN"},
            "56": {"milestone": {"title": "Sprint B"}, "title": "Three", "url": "u3", "state": "OPEN"},
        }
        completed, payload = self.run_resolver(repo_root, fake_gh, fake_git, "Implements !#12 and #34 plus #56", fixtures=fixtures)
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(payload["close_issues"], [12])
        self.assertEqual(payload["related_issues"], [34, 56])
        self.assertEqual(payload["milestone"], "Sprint A")
        self.assertEqual(payload["labels"], [])
        self.assertEqual(payload["warnings"], [])
        self.assertTrue(payload["has_upstream"])

    def test_selects_labels_from_request_and_changed_paths(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        self.commit_file(repo_root, Path("docs/guide.md"), "docs\n")
        self.commit_file(repo_root, Path("backend/service.py"), "print('ok')\n")
        completed, payload = self.run_resolver(
            repo_root,
            fake_gh,
            fake_git,
            "docs update !#12",
            fixtures={"12": {"milestone": None, "title": "Docs cleanup", "url": "u1", "state": "OPEN"}},
            labels=[{"name": "docs", "description": "Documentation"}, {"name": "backend", "description": "Backend scope"}],
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(payload["labels"], ["backend", "docs"])
        self.assertEqual(payload["warnings"], [])

    def test_label_lookup_failure_warns_and_succeeds(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        completed, payload = self.run_resolver(repo_root, fake_gh, fake_git, "No issue refs", label_mode="fail")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(payload["labels"], [])
        self.assertEqual(payload["warnings"][0]["code"], "label_lookup_failed")

    def test_label_lookup_invalid_json_warns_and_succeeds(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        completed, payload = self.run_resolver(repo_root, fake_gh, fake_git, "No issue refs", label_mode="invalid_json")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(payload["labels"], [])
        self.assertEqual(payload["warnings"][0]["code"], "label_lookup_invalid_json")

    def test_changed_paths_failure_warns_and_keeps_text_match(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        completed, payload = self.run_resolver(
            repo_root,
            fake_gh,
            fake_git,
            "docs update",
            labels=[{"name": "docs", "description": "Documentation"}],
            git_diff_fail=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(payload["labels"], ["docs"])
        self.assertEqual(payload["warnings"][0]["code"], "changed_paths_unavailable")

    def test_close_issue_wins_and_tie_break_prefers_close_milestone(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        fixtures = {
            "10": {"milestone": {"title": "Sprint X"}, "title": "One", "url": "u1", "state": "OPEN"},
            "20": {"milestone": {"title": "Sprint Y"}, "title": "Two", "url": "u2", "state": "OPEN"},
            "30": {"milestone": {"title": "Sprint X"}, "title": "Three", "url": "u3", "state": "OPEN"},
            "40": {"milestone": {"title": "Sprint Y"}, "title": "Four", "url": "u4", "state": "OPEN"},
        }
        completed, payload = self.run_resolver(repo_root, fake_gh, fake_git, "Refs #10 and !#20 and #30 and #40 and #20 again", fixtures=fixtures)
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(payload["close_issues"], [20])
        self.assertEqual(payload["related_issues"], [10, 30, 40])
        self.assertEqual(payload["milestone"], "Sprint Y")

    def test_multiple_templates_require_choice(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        template_dir = repo_root / ".github" / "PULL_REQUEST_TEMPLATE"
        template_dir.mkdir(parents=True)
        (template_dir / "feature.md").write_text("feature\n")
        (template_dir / "bugfix.md").write_text("bugfix\n")
        completed, payload = self.run_resolver(repo_root, fake_gh, fake_git, "No issue refs")
        self.assertEqual(completed.returncode, 0)
        self.assertTrue(payload["needs_template_choice"])
        self.assertEqual(payload["template_candidates"], [".github/PULL_REQUEST_TEMPLATE/bugfix.md", ".github/PULL_REQUEST_TEMPLATE/feature.md"])

    def test_explicit_template_selects_candidate(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        github_dir = repo_root / ".github"
        github_dir.mkdir()
        (github_dir / "pull_request_template.md").write_text("default\n")
        completed, payload = self.run_resolver(
            repo_root,
            fake_gh,
            fake_git,
            "No issue refs",
            extra_args=["--template", ".github/pull_request_template.md", "--base", "main"],
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(payload["selected_template"], ".github/pull_request_template.md")
        self.assertEqual(payload["base_branch"], "main")

    def test_explicit_template_must_be_candidate(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        github_dir = repo_root / ".github"
        github_dir.mkdir()
        (github_dir / "pull_request_template.md").write_text("default\n")
        (github_dir / "not-a-template.md").write_text("notes\n")
        completed, payload = self.run_resolver(
            repo_root,
            fake_gh,
            fake_git,
            "No issue refs",
            extra_args=["--template", ".github/not-a-template.md"],
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(payload["errors"][0]["code"], "template_not_candidate")

    def test_invalid_auth_fails_early(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        completed, payload = self.run_resolver(
            repo_root,
            fake_gh,
            fake_git,
            "Refs #1",
            fixtures={"1": {"milestone": None, "title": "One", "url": "u1", "state": "OPEN"}},
            auth_ok=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(payload["errors"][0]["code"], "gh_auth_invalid")

    def test_missing_base_branch_fails(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        completed, payload = self.run_resolver(
            repo_root,
            fake_gh,
            fake_git,
            "No issue refs",
            extra_args=["--base", "release"],
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(payload["errors"][0]["code"], "missing_base_branch")

    def test_missing_issue_lookup_fails(self):
        temp_dir, repo_root, fake_gh, fake_git = self.make_repo()
        self.addCleanup(temp_dir.cleanup)
        completed, payload = self.run_resolver(repo_root, fake_gh, fake_git, "Refs #77", fixtures={})
        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(payload["errors"][0]["code"], "issue_lookup_failed")

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

import unittest
from pathlib import Path
from unittest.mock import patch

import label_selection


class Completed:
    def __init__(self, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout


class LabelSelectionTests(unittest.TestCase):
    def test_select_labels_matches_request_issue_and_paths(self):
        labels = [
            {"name": "api", "description": "API changes"},
            {"name": "docs", "description": "Documentation"},
            {"name": "bug", "description": "Bug fixes"},
        ]
        issue_payloads = {12: {"title": "API cleanup"}}
        selected = label_selection.select_labels(
            "Update docs for #12",
            issue_payloads,
            labels,
            ["docs/guide.md", "src/api/index.ts"],
        )
        self.assertEqual(selected, ["api", "docs"])

    def test_select_labels_ignores_description_only_matches(self):
        labels = [{"name": "enhancement", "description": "docs changes"}]
        selected = label_selection.select_labels("Update docs", {}, labels, ["docs/guide.md"])
        self.assertEqual(selected, [])

    @patch("label_selection.run_command")
    def test_fetch_labels_returns_warning_on_lookup_failure(self, run_command):
        run_command.return_value = Completed(returncode=1)
        labels, warnings = label_selection.fetch_labels(Path("/tmp/repo"))
        self.assertEqual(labels, [])
        self.assertEqual(warnings[0]["code"], "label_lookup_failed")

    @patch("label_selection.run_command")
    def test_fetch_labels_returns_warning_on_invalid_json(self, run_command):
        run_command.return_value = Completed(returncode=0, stdout="{invalid")
        labels, warnings = label_selection.fetch_labels(Path("/tmp/repo"))
        self.assertEqual(labels, [])
        self.assertEqual(warnings[0]["code"], "label_lookup_invalid_json")

    @patch("label_selection.run_command")
    def test_resolve_labels_keeps_request_match_when_paths_fail(self, run_command):
        run_command.side_effect = [
            Completed(returncode=0, stdout='[{"name":"docs","description":"Documentation"}]'),
            Completed(returncode=1),
        ]
        labels, warnings = label_selection.resolve_labels(Path("/tmp/repo"), "develop", "Update docs", {})
        self.assertEqual(labels, ["docs"])
        self.assertEqual(warnings[0]["code"], "changed_paths_unavailable")


if __name__ == "__main__":
    unittest.main()

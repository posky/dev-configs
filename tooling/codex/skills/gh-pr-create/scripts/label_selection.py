#!/usr/bin/env python3

import json
import os
import re
import subprocess
from pathlib import Path

WORD_PATTERN = re.compile(r"[^\w]+", re.UNICODE)
PATH_SPLIT_PATTERN = re.compile(r"[\\/]+")
MIN_TOKEN_LENGTH = 2


def tool_path(env_name, default_name):
    return os.environ.get(env_name, default_name)


def run_command(command, cwd):
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)


def warning(code, message):
    return {"code": code, "message": message}


def normalize_phrase(text):
    cleaned = WORD_PATTERN.sub(" ", text.casefold().replace("-", " ").replace("_", " ").replace(".", " "))
    return " ".join(part for part in cleaned.split() if len(part) >= MIN_TOKEN_LENGTH)


def fetch_labels(repo_root):
    gh = tool_path("GH_BIN", "gh")
    completed = run_command(
        [gh, "label", "list", "--json", "name,description", "--limit", "100", "--sort", "name", "--order", "asc"],
        repo_root,
    )
    if completed.returncode != 0:
        return [], [warning("label_lookup_failed", "Repository labels could not be loaded.")]
    try:
        payload = json.loads(completed.stdout or "[]")
    except json.JSONDecodeError:
        return [], [warning("label_lookup_invalid_json", "Repository labels returned invalid JSON.")]
    if not isinstance(payload, list):
        return [], [warning("label_lookup_invalid_json", "Repository labels returned invalid JSON.")]
    labels = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        description = item.get("description")
        if isinstance(name, str) and name.strip():
            labels.append({"name": name, "description": description or ""})
    return labels, []


def collect_changed_paths(repo_root, base_branch):
    git = tool_path("GIT_BIN", "git")
    completed = run_command([git, "-C", str(repo_root), "diff", "--name-only", f"{base_branch}...HEAD"], repo_root)
    if completed.returncode != 0:
        return [], [warning("changed_paths_unavailable", "Changed file paths could not be loaded.")]
    paths = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    return paths, []


def build_text_evidence(request_text, issue_payloads):
    phrases = [normalize_phrase(request_text)]
    for payload in issue_payloads.values():
        title = payload.get("title")
        if isinstance(title, str) and title.strip():
            phrases.append(normalize_phrase(title))
    return f" {' '.join(part for part in phrases if part)} "


def build_path_evidence(changed_paths):
    phrases = set()
    for changed_path in changed_paths:
        parts = PATH_SPLIT_PATTERN.split(changed_path)
        for part in parts:
            normalized = normalize_phrase(Path(part).stem or part)
            if normalized:
                phrases.add(normalized)
    return phrases


def select_labels(request_text, issue_payloads, labels, changed_paths):
    text_evidence = build_text_evidence(request_text, issue_payloads)
    path_evidence = build_path_evidence(changed_paths)
    selected = []
    for label in labels:
        label_name = label["name"]
        label_phrase = normalize_phrase(label_name)
        if not label_phrase:
            continue
        phrase_match = f" {label_phrase} " in text_evidence
        path_match = label_phrase in path_evidence
        if phrase_match or path_match:
            selected.append(label_name)
    return sorted(set(selected), key=str.casefold)


def resolve_labels(repo_root, base_branch, request_text, issue_payloads):
    labels, warnings = fetch_labels(repo_root)
    if not labels:
        return [], warnings
    changed_paths, path_warnings = collect_changed_paths(repo_root, base_branch)
    selected = select_labels(request_text, issue_payloads, labels, changed_paths)
    return selected, warnings + path_warnings

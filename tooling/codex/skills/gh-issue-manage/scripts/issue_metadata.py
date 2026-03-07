#!/usr/bin/env python3

import json
import re

from gh_common import failure, gh_failure, run, tool

ACCEPT_HEADER = "Accept: application/vnd.github+json"
VERSION_HEADER = "X-GitHub-Api-Version: 2022-11-28"
WORD_PATTERN = re.compile(r"[^\w]+", re.UNICODE)
MIN_TOKEN_LENGTH = 2


def warning(code, message):
    return {"code": code, "message": message}

def normalize_phrase(text):
    cleaned = WORD_PATTERN.sub(" ", text.casefold().replace("-", " ").replace("_", " "))
    return " ".join(part for part in cleaned.split() if len(part) >= MIN_TOKEN_LENGTH)


def build_text_evidence(title, body):
    parts = [normalize_phrase(title or ""), normalize_phrase(body or "")]
    return f" {' '.join(part for part in parts if part)} "


def fetch_values(repo, path, field, failed_code, invalid_json_code, failed_message, invalid_json_message):
    values = []
    page = 1
    while True:
        separator = "&" if "?" in path else "?"
        completed = run(
            [
                tool("GH_BIN", "gh"),
                "api",
                "-X",
                "GET",
                "-H",
                ACCEPT_HEADER,
                "-H",
                VERSION_HEADER,
                f"repos/{repo}/{path}{separator}per_page=100&page={page}",
            ]
        )
        if completed.returncode != 0:
            return None, warning(failed_code, failed_message if gh_failure(completed.stderr)["code"] == "gh_command_failed" else gh_failure(completed.stderr)["message"])
        try:
            payload = json.loads(completed.stdout or "[]")
        except json.JSONDecodeError:
            return None, warning(invalid_json_code, invalid_json_message)
        if not isinstance(payload, list):
            return None, warning(invalid_json_code, invalid_json_message)
        for item in payload:
            if isinstance(item, dict) and isinstance(item.get(field), str) and item[field].strip():
                values.append(item[field])
        if len(payload) < 100:
            return sorted(set(values), key=str.casefold), None
        page += 1


def fetch_labels(repo):
    return fetch_values(
        repo,
        "labels",
        "name",
        "label_lookup_failed",
        "label_lookup_invalid_json",
        "Repository labels could not be loaded.",
        "Repository labels returned invalid JSON.",
    )


def fetch_milestones(repo):
    return fetch_values(
        repo,
        "milestones?state=open",
        "title",
        "milestone_lookup_failed",
        "milestone_lookup_invalid_json",
        "Repository milestones could not be loaded.",
        "Repository milestones returned invalid JSON.",
    )


def validate_labels(repo, names):
    labels, lookup_warning = fetch_labels(repo)
    if labels is None:
        return None, failure(lookup_warning["code"], lookup_warning["message"])
    known = {name.casefold(): name for name in labels}
    missing = [name for name in names if name.casefold() not in known]
    if missing:
        return None, failure("unknown_label", f"Unknown label(s): {', '.join(missing)}.")
    return [known[name.casefold()] for name in names], None


def validate_milestone(repo, milestone):
    titles, lookup_warning = fetch_milestones(repo)
    if titles is None:
        return None, failure(lookup_warning["code"], lookup_warning["message"])
    known = {title.casefold(): title for title in titles}
    resolved = known.get(milestone.casefold())
    if resolved is None:
        return None, failure("unknown_milestone", f"Unknown open milestone: {milestone}.")
    return resolved, None


def suggest_create_metadata(repo, title, body):
    evidence = build_text_evidence(title, body)
    warnings = []
    labels = []
    milestones = []

    label_names, label_warning = fetch_labels(repo)
    if label_names is None:
        warnings.append(label_warning)
    else:
        for name in label_names:
            phrase = normalize_phrase(name)
            if phrase and f" {phrase} " in evidence:
                labels.append(name)

    milestone_titles, milestone_warning = fetch_milestones(repo)
    if milestone_titles is None:
        warnings.append(milestone_warning)
    else:
        for title_value in milestone_titles:
            phrase = normalize_phrase(title_value)
            if phrase and f" {phrase} " in evidence:
                milestones.append(title_value)

    milestone = milestones[0] if len(milestones) == 1 else None
    if len(milestones) > 1:
        warnings.append(warning("ambiguous_milestone", "Multiple milestone titles matched the issue text."))
    return sorted(set(labels), key=str.casefold), milestone, warnings

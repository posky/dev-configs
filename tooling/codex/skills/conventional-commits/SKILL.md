---
name: conventional-commits
description: Write and refine Git commit messages using Conventional Commits 1.0.0. Use this skill when creating commit headers, choosing types and scopes, marking breaking changes, splitting mixed changes into small logical commits, or rewriting existing commit messages to follow the specification.
---

# Conventional Commits

## Overview
Use Conventional Commits 1.0.0 to produce clear, machine-readable commit messages.
Split work into small logical commits before writing commit messages.

## Commit Workflow
1. Inspect all pending changes and group files by one logical concern.
2. Create one commit per concern; avoid mixing feature, fix, refactor, and docs in one commit unless inseparable.
3. Write the header in this format: `<type>[optional scope][!]: <description>`.
4. Write the description in English only.
5. Add an optional body in Korean or English when extra context is needed.
6. Add footer lines for references or breaking-change notices.

## Header Rules
- Use one allowed type per commit:
  - `feat`: add a user-facing feature.
  - `fix`: fix a bug.
  - `docs`: change documentation only.
  - `style`: change formatting only (no logic change).
  - `refactor`: restructure code without changing behavior.
  - `test`: add or update tests.
  - `perf`: improve performance.
  - `build`: change build system or dependencies.
  - `ci`: change CI configuration or scripts.
  - `chore`: maintenance changes not covered above.
  - `revert`: revert a previous commit.
- Use an optional scope when it clarifies impact (example: `feat(parser): ...`).
- Keep description short, specific, and English-only.
- Avoid trailing period in the description.

## Body and Footer Rules
- Write body text only when needed for rationale, constraints, or migration notes.
- Allow body language to be Korean or English.
- Separate header, body, and footer with blank lines.
- Use footer tokens like `Refs: #123` or `Closes: #456`.
- Mark breaking changes with either:
  - `!` in the header (`feat(api)!: ...`), and/or
  - a footer line starting with `BREAKING CHANGE:` followed by impact and migration guidance.

## Splitting Rules for Small Commits
- Split commits by intent, not by file type.
- Separate pure renames or formatting from behavior changes.
- Separate test updates from production code when practical.
- Prefer multiple small commits over one large mixed commit.
- If a split is unsafe, explain the dependency in the body.

## Examples
Valid:
- `feat(auth): add refresh token endpoint`
- `fix(player): handle null stream URL`
- `refactor(cache)!: replace LRU with ARC`

Invalid:
- `update stuff`
- `feat: 로그인 기능 추가` (description must be English)
- `fixed bug` (missing Conventional Commits header format)

## Reference
For rule details and quick decision notes, read `references/conventional-commits.md`.

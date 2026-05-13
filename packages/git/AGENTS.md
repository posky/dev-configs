# Subtree Guidelines: packages/git

## Scope

This file applies to work under `packages/git/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/git/` contains global Git configuration and commit-message template guidance.

Local invariant: do not overwrite or globally apply Git settings without explicit user approval and a backup or merge plan.

## Local Structure

```text
README.md          Package purpose, apply steps, backup notes, and FAQ
.gitconfig         Recommended global Git settings
.gitmessage.txt    Conventional Commits message template
```

## Local Commands

Use commands from `packages/git/README.md` only after confirming whether the user wants to copy or merge settings.

Prefer inspection before live application:

```bash
git diff -- packages/git/
```

## Local Rules

- Keep changes inside `packages/git/` unless the task explicitly requires shared coordination.
- Update `packages/git/README.md` when file locations, apply steps, include rules, or backup guidance change.
- Do not run `git config --global` unless the task explicitly approves changing the current machine.
- Compare existing `~/.gitconfig` before recommending replacement.

## Local Verification

- Re-read `packages/git/README.md`, `.gitconfig`, and `.gitmessage.txt` when changed.
- Check Git config syntax with a non-mutating read command when appropriate.
- Report what was run, what was not run, and any remaining local risk.

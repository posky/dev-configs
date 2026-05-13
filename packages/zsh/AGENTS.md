# Subtree Guidelines: packages/zsh

## Scope

This file applies to work under `packages/zsh/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/zsh/` manages Zsh shell configuration and related maintenance scripts.

Local invariant: do not overwrite `~/.zshrc` or run Zsh maintenance scripts without explicit backup and script-safety checks.

## Local Structure

```text
README.md          Package purpose, apply steps, and comparison guidance
config/.zshrc      Zsh user configuration
scripts/upgrade.sh Zsh-related maintenance script
```

## Local Commands

Use commands from `packages/zsh/README.md` after confirming whether the task is backup, compare, or apply.

Prefer inspection before live application:

```bash
git diff -- packages/zsh/
code --diff packages/zsh/config/.zshrc ~/.zshrc
```

## Local Rules

- Keep changes inside `packages/zsh/` unless the task explicitly requires shared coordination.
- Update `packages/zsh/README.md` when file locations, apply steps, backup guidance, or comparison commands change.
- Check `scripts/upgrade.sh` shebang, permissions, and relative path assumptions before execution.
- Back up `~/.zshrc` before copying repository content over it.

## Local Verification

- Re-read `packages/zsh/README.md`, `config/.zshrc`, and changed scripts for path accuracy.
- Use shell syntax checks when available and relevant.
- Report what was run, what was not run, and any remaining local risk.

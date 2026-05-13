# Subtree Guidelines: packages/vscode

## Scope

This file applies to work under `packages/vscode/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/vscode/` contains VS Code keybinding configuration for macOS and Windows.

Local invariant: do not overwrite a live VS Code keybindings file without a backup and platform-specific path confirmation.

## Local Structure

```text
README.md              Apply, backup, and diff guidance
macos/keybindings.json macOS VS Code user keybindings
windows/keybindings.json Windows VS Code user keybindings
```

## Local Commands

Use commands from `packages/vscode/README.md` and keep shell syntax platform-appropriate.

Prefer inspection before live application:

```bash
git diff -- packages/vscode/
code --diff packages/vscode/macos/keybindings.json "$HOME/Library/Application Support/Code/User/keybindings.json"
```

## Local Rules

- Keep macOS keybindings under `packages/vscode/macos/` and Windows keybindings under `packages/vscode/windows/`.
- Quote paths with spaces, especially `Application Support`.
- Update `packages/vscode/README.md` when apply, backup, or diff commands change.
- Consider VS Code Sync interactions before recommending manual copy operations.

## Local Verification

- Re-read `packages/vscode/README.md` and changed JSON files for path and syntax accuracy.
- Use JSON validation or VS Code comparison when relevant and available.
- Report what was run, what was not run, and any remaining local risk.

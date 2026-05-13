# Subtree Guidelines: packages/neovim

## Scope

This file applies to work under `packages/neovim/`.

Follow the repository root `AGENTS.md` for global workflow, safety, planning, verification, and git guidance. Use this file only for local package additions.

## Local Overview

`packages/neovim/` manages LazyVim and NvChad profile configuration for synchronization with `~/.config/nvim`.

Local invariant: never delete or replace live Neovim configuration without an explicit backup and target-path confirmation.

## Local Structure

```text
README.md       Profile workflow, backup, apply, and operational notes
lazyvim/        LazyVim-based configuration profile
nvchad/         NvChad custom configuration profile
```

## Local Commands

Use commands from `packages/neovim/README.md` and confirm profile intent before copying or deleting files.

Prefer inspection before live application:

```bash
git diff -- packages/neovim/
nvim --headless "+Lazy! sync" +qa
```

Run Neovim commands only when the task requires tool-level validation and the local environment is available.

## Local Rules

- Keep LazyVim changes in `packages/neovim/lazyvim/` and NvChad changes in `packages/neovim/nvchad/` unless a task explicitly coordinates profiles.
- Update `packages/neovim/README.md` when profile paths, apply steps, backup steps, or sync commands change.
- Treat `rm -rf` examples as destructive; check targets twice before suggesting or running them.
- Preserve NvChad's `lua/custom` ownership boundary unless the task explicitly changes it.

## Local Verification

- Re-read `packages/neovim/README.md` and changed Lua/config files for path accuracy.
- Use Neovim headless or profile-specific checks when relevant and available.
- Report what was run, what was not run, and any remaining local risk.

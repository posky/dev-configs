# Option 1: Category-First Directory Plan

Updated: October 7, 2025

## Principles

- Keep existing top-level categories (editors, shells, terminals, OS tooling) as the single source of truth.
- Retire unused tooling directories to avoid stale guidance.
- Document each directory with a short `README.md` covering purpose, key files, and how to sync with `$HOME`.
- Prefer plain, well-documented copy steps over bespoke helper scripts; add automation only when necessary.
- Call out legacy or experimental variants explicitly (e.g., suffix `-legacy` or move to `archive/`) instead of leaving parallel folders.

## Directory Inventory

| Directory | Purpose / Scope | Key Assets | Status | Next Action |
|-----------|----------------|------------|--------|-------------|
| `dev/tooling/bat` | Syntax highlighting profiles for `bat` | `config`, `themes/` | Documented (2025-10-07) | Monitor Catppuccin updates; rerun `bat cache --build` after theme changes. |
| `dev/tooling` | Cross-tool helpers | `README.md` | Documented (2025-10-07) | Only add scripts when multiple tools truly benefit from automation. |
| `git` | Commit templates & scripts | `.gitconfig`, `.gitmessage.txt` | Documented (2025-10-07) | Consider linking to OS-specific Git docs for advanced include rules. |
| `hammerspoon` | macOS automation configs | `.hammerspoon/` | Documented (2025-10-07) | Evaluate adding a Makefile target if copy steps become repetitive. |
| `helix` | Helix editor config | `config.toml`, `languages.toml` | Documented (2025-10-07) | Review per-language tooling notes periodically. |
| `lazygit` | Lazygit config | `config.yml` | Documented (2025-10-07) | Validate `lazygit -cd` path resolution on Windows WSL. |
| `neovim` | Neovim distributions | `lazyvim/`, `nvchad/` | Documented (2025-10-07) | Consider adding a symlink helper or automation for repo → local LazyVim deploy. |
| `dev/tooling/prettier` | Global Prettier config | `.prettierrc.json` | Documented (2025-10-07) | Capture team-specific rule overrides when they arise. |
| `dev/languages/python` | Python tooling presets | `ruff.toml`, `logging/`, `tasks.json` | Documented (2025-10-07) | Align logging example with latest runtime patterns. |
| `dev/languages/rust` | Rust tooling presets | `Makefile.toml`, `rustfmt.toml`, `log4rs.yaml` | Documented (2025-10-07) | Add instructions for multi-crate workspaces if needed. |
| `dev/tooling/shell` | zsh + plugin config | `zsh/.zshrc`, PowerShell profile | Documented (2025-10-07) | Add symlink-based workflow examples if manual copy becomes noisy. |
| `dev/tooling/starship` | Starship prompt | `starship.toml` | Documented (2025-10-07) | Track palette updates from Catppuccin releases. |
| `dev/tooling/zellij` | Zellij multiplexer setup | `config.kdl`, wrapper script | Documented (2025-10-07) | Evaluate renaming wrapper to avoid clashing with upstream binary. |
| `terminal` | Terminal emulator configs | `kitty/`, `wezterm/`, `ghostty/` | Documented (2025-10-07) | Add screenshots or key highlights after stabilizing settings. |
| `toml` | TOML tooling references | `README.md` | Up to date | Link from top-level docs. |
| `vscode` | VS Code keybindings | `macos/`, `windows/` subfolders | Documented (2025-10-07) | Revisit when migrating to Cursor/Windsurf keymaps. |
| `windsurf` | Windsurf editor config | `settings.json` | Documented (2025-10-07) | Note platform-specific diffs if Windows usage starts. |
| `zed` | Zed editor config | `settings.json`, `keymap.json`, `tasks.json` | Documented (2025-10-07) | Capture Linux-specific paths when adopted. |

## Immediate Iteration Queue

1. Neovim README에 symlink 스크립트(교체·복구) 예시를 추가할지 검토합니다.

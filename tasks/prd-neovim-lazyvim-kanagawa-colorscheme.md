# PRD: Neovim LazyVim Kanagawa Colorscheme

## Document Status
- Status: Complete
- File Mode: Single
- Current Phase: Complete
- Last Updated: 2026-06-05
- PRD File: `tasks/prd-neovim-lazyvim-kanagawa-colorscheme.md`
- Purpose: Living PRD and execution source of truth. Check off work here, update this document as implementation reveals new information, and revise future phases before continuing when the plan changes.

## Problem
`packages/neovim/lazyvim/lua/plugins/colorscheme.lua` currently installs `sainnhe/everforest` and configures LazyVim to load `everforest`. The user wants the LazyVim profile to use `rebelot/kanagawa.nvim` as the Neovim colorscheme while preserving the repository's manual, review-first configuration workflow.

## Goals
- G-1: Replace the LazyVim profile colorscheme plugin from Everforest to Kanagawa.
- G-2: Configure LazyVim to load Kanagawa using the minimal plugin-spec pattern already used by the repository.
- G-3: Keep the change focused, reversible, and limited to the LazyVim profile unless discovery proves a supporting doc update is required.
- G-4: Provide validation steps that prove the Lua config is structurally valid and the plugin can be resolved without copying into live config paths.

## Non-Goals
- NG-1: Do not apply, overwrite, delete, or symlink live `~/.config/nvim` configuration during this task.
- NG-2: Do not change the NvChad profile.
- NG-3: Do not add repository-wide package manager state, lockfiles, generated dependency files, or install automation.
- NG-4: Do not customize Kanagawa palette, highlights, transparency, terminal colors, or variant behavior unless implementation discovery shows defaults are insufficient.
- NG-5: Do not change unrelated LazyVim plugins, keymaps, options, or runtime path settings.

## Success Criteria
- SC-1: `packages/neovim/lazyvim/lua/plugins/colorscheme.lua` declares `rebelot/kanagawa.nvim` instead of `sainnhe/everforest`.
- SC-2: LazyVim's `opts.colorscheme` is set to `kanagawa`, matching the official kanagawa.nvim usage path.
- SC-3: The resulting Lua file keeps the existing simple plugin-spec shape unless a documented reason requires a setup function.
- SC-4: No live user config path is modified.
- SC-5: Validation records at least a syntax/static Lua parse check or an explicit local-tooling gap, plus focused diff review.

## Key Scenarios
### Scenario 1: Repository Config Review
- Actor: Developer maintaining `dev-configs`.
- Trigger: Reviews the diff after implementation.
- Expected outcome: The LazyVim colorscheme change is obvious, isolated, and reversible.

### Scenario 2: Manual LazyVim Sync Later
- Actor: Same user applying dotfiles manually.
- Trigger: Copies the repository LazyVim `lua` directory to `~/.config/nvim/lua` after backup and diff review.
- Expected outcome: LazyVim installs and loads Kanagawa on startup or during `Lazy! sync` without requiring extra repository automation.

## Discovery Summary
- Reviewed: `AGENTS.md`, `packages/neovim/AGENTS.md`, `packages/neovim/README.md`, `packages/neovim/lazyvim/lua/plugins/colorscheme.lua`, `packages/neovim/lazyvim/lua/config/lazy.lua`, existing `tasks/prd-lazygit-kanagawa-wave-theme.md`, and the official `rebelot/kanagawa.nvim` GitHub README.
- Current system: The LazyVim profile imports `plugins` from `lazy.lua`, and `colorscheme.lua` currently contains one standalone colorscheme plugin plus the `LazyVim/LazyVim` options override. The repository has no global build or test command and documents manual backup/apply workflows.
- External reference facts: kanagawa.nvim documents installation as `rebelot/kanagawa.nvim`, usage via `colorscheme kanagawa` or `vim.cmd("colorscheme kanagawa")`, no required `setup` call for defaults, and variants `wave`, `dragon`, and `lotus`; default `theme = "wave"` is shown in its default setup.
- Validation surface: Smallest useful checks are Lua syntax parsing, focused `git diff -- packages/neovim/lazyvim/lua/plugins/colorscheme.lua`, and optional Neovim headless `nvim --headless "+Lazy! sync" +qa` if the local environment is available and the executor is allowed to update local lazy.nvim plugin state.
- Design implications: The implementation should keep `colorscheme.lua` compact by replacing the plugin spec and colorscheme string only. A Kanagawa setup block is unnecessary for the default Wave behavior unless the executor intentionally selects non-default options and records the reason.
- Confidence / gaps: High confidence for the static config change. Full plugin installation verification may require network or existing local plugin cache; if unavailable, record the tooling gap and use static validation plus diff review.

## Requirements
### Functional Requirements
- FR-1: Replace `{ "sainnhe/everforest" }` with `{ "rebelot/kanagawa.nvim" }` in `packages/neovim/lazyvim/lua/plugins/colorscheme.lua`.
- FR-2: Replace `colorscheme = "everforest"` with `colorscheme = "kanagawa"` in the `LazyVim/LazyVim` opts block.
- FR-3: Keep the existing return-table structure and plugin ordering unless implementation discovery identifies a LazyVim loading issue.
- FR-4: Do not add `require("kanagawa").setup(...)` unless a concrete option is needed; if added, call setup before loading the colorscheme and document the reason in this PRD.
- FR-5: Re-check `packages/neovim/lazyvim/lua/config/lazy.lua` before implementation and change it only if validation proves LazyVim's install fallback list must include `kanagawa`.

### Non-Functional Requirements
- NFR-1: The change must remain inside `packages/neovim/lazyvim/` and this PRD unless a README path or workflow note becomes necessary.
- NFR-2: The Lua file must remain syntactically valid.
- NFR-3: The implementation must not modify live Neovim config or destructive repository workflow examples.
- NFR-4: The diff should be small enough to inspect manually.
- NFR-5: No secrets, generated files, plugin lockfiles, or cache contents may be added.

## Assumptions
- A-1: The intended Kanagawa variant is the default `kanagawa` colorscheme, which maps to Kanagawa Wave by default according to the official README.
- A-2: `packages/neovim/lazyvim/lua/plugins/colorscheme.lua` is the intended source of truth for LazyVim colorscheme selection.
- A-3: The user requested implementation after reviewing the PRD.
- A-4: Live config application remains a later manual action governed by `packages/neovim/README.md`.

## Dependencies / Constraints
- `packages/neovim/AGENTS.md` requires LazyVim changes to stay under `packages/neovim/lazyvim/` unless explicitly coordinated.
- The repository has no package manager or repository-wide validation command.
- Neovim headless validation may alter local plugin state through Lazy's sync behavior, so it should be run only when implementation scope includes tool-level validation.
- Network access may be required if Kanagawa is not already cached locally.

## Risks / Edge Cases
- If the plugin is not installed and network is unavailable, `nvim --headless "+Lazy! sync" +qa` may fail for environmental reasons rather than config syntax.
- If `colorscheme = "kanagawa-wave"` is used instead of `kanagawa`, it would still be supported by kanagawa.nvim, but it would not match the user's requested `kanagawa` setting or the simplest official usage path.
- Updating `lazy.lua` install fallback colorschemes could broaden the diff unnecessarily unless a concrete startup fallback issue appears.
- Static Lua parsing can prove syntax, but cannot prove visual rendering or plugin download success.

## Execution Rules
- Complete phases in order unless this PRD is explicitly revised.
- Before starting any phase, read this PRD and re-check the phase discovery gate.
- Use this PRD as the only active plan; do not create a competing checklist.
- For minor ambiguities, choose the best reasonable option, record the assumption, and continue.
- Stop for help only for material blockers such as missing access, irreversible destructive change, major requirement conflict, or meaningful security/legal risk.
- Prefer minimal, reversible changes that satisfy the goals.
- Preserve existing code and config patterns unless there is a clear reason not to.
- Select validation methods according to risk and available tools; do not default to one testing tool for every phase.
- At the end of each phase, update this PRD and revise later phases based on what was learned.

## Phase Index
| Phase | Status | Objective | Validation Focus |
|---|---|---|---|
| Phase 1: Confirm Target Mapping | Complete | Re-confirm current LazyVim colorscheme config and official Kanagawa usage before editing. | Source traceability and scope confirmation. |
| Phase 2: Apply Colorscheme Config | Complete | Update `colorscheme.lua` to use `rebelot/kanagawa.nvim` and `colorscheme = "kanagawa"`. | Focused diff and Lua structure review. |
| Phase 3: Validate And Close Out | Complete | Run smallest sufficient checks and update PRD completion evidence. | Lua syntax/static check, optional Neovim headless check, and no live-config modification. |

## Phase Plan

### Phase 1: Confirm Target Mapping
Status: Complete

#### Objective
Confirm the exact repository edit and official Kanagawa loading path before changing config.

#### Context From Master PRD
- Goals covered: G-1, G-2, G-3
- Success Criteria: SC-1, SC-2, SC-3
- Requirements covered: FR-1, FR-2, FR-3, FR-4, FR-5, NFR-1, NFR-4
- Key scenarios touched: Scenario 1

#### Phase Discovery Gate
Before editing code, re-check:
- [x] Relevant code/files: `packages/neovim/lazyvim/lua/plugins/colorscheme.lua`, `packages/neovim/lazyvim/lua/config/lazy.lua`
- [x] Relevant docs/specs/external references: `packages/neovim/README.md`, `packages/neovim/AGENTS.md`, `https://github.com/rebelot/kanagawa.nvim`
- [x] Relevant commands or tools: `git status --short`, `git diff -- packages/neovim/`
- [x] Assumptions from this PRD still hold
- [x] If discoveries change this phase or later phases, update this PRD before implementation

#### Scope
##### In Scope
- Confirm current Everforest plugin and colorscheme values.
- Confirm Kanagawa plugin repository and `kanagawa` colorscheme name.
- Decide whether any setup block or `lazy.lua` install fallback edit is justified.

##### Out of Scope
- Editing live `~/.config/nvim`.
- Choosing custom Kanagawa colors or variants beyond the default `kanagawa`.
- Changing NvChad or shared theme packages.

#### Implementation Checklist
- [x] Verify `colorscheme.lua` still contains `sainnhe/everforest` and `colorscheme = "everforest"`.
- [x] Verify official kanagawa.nvim usage still supports `colorscheme kanagawa`.
- [x] Record the final implementation decision: minimal replacement only, or a revised plan with rationale.
- [x] If `lazy.lua` appears relevant, document whether it remains unchanged and why.

#### Validation Strategy
This phase uses discovery validation. The smallest sufficient evidence is source review of the current file and the official kanagawa.nvim README.

#### Validation Checklist
- [x] Current repository state reviewed.
- [x] Official Kanagawa usage path reviewed.
- [x] No material ambiguity remains, or this PRD is updated before implementation.

#### Exit Criteria
- [x] Phase objective is satisfied
- [x] Requirements listed above are ready for implementation or explicitly revised
- [x] Validation checklist is complete or gaps are recorded with rationale
- [x] No known blocker remains for Phase 2

#### Phase-End Multi-Pass Review
Complete in order before moving to the next phase:
- [x] 1. Intent/coverage review: this phase achieves its objective and mapped requirements.
- [x] 2. Correctness review: happy paths, edge cases, errors, empty states, state transitions, and permissions are handled.
- [x] 3. Simplicity review: the solution is no more complex than necessary.
- [x] 4. Code quality review: names, boundaries, abstractions, and local consistency are clean.
- [x] 5. Duplication/cleanup review: repeated logic, dead code, temporary code, noisy logs, commented leftovers, unused files, and unused dependencies are removed.
- [x] 6. Security/privacy review: access control, secrets, sensitive data, injection risks, unsafe client exposure, and audit needs are handled.
- [x] 7. Performance/load review: bottlenecks, expensive queries, N+1 patterns, unnecessary renders, avoidable blocking work, and unnecessary network calls are addressed.
- [x] 8. Validation review: chosen checks are appropriate for phase risk; missing checks are justified.
- [x] 9. Future-phase review: later phase checklist is still correct; revise it if discoveries changed the plan.
- [x] 10. PRD sync review: master PRD status, assumptions, risks, validation surface, and change log are updated.

#### Discoveries / Decisions
- Completed decision: use the minimal replacement path because kanagawa.nvim defaults do not require `setup`; `lazy.lua` remains unchanged because no fallback-install issue was found.

#### Phase Change Log
- 2026-06-05: Phase created.
- 2026-06-05: Phase completed after source and scope confirmation.

### Phase 2: Apply Colorscheme Config
Status: Complete

#### Objective
Update the LazyVim colorscheme configuration to use Kanagawa with the smallest reversible diff.

#### Context From Master PRD
- Goals covered: G-1, G-2, G-3
- Success Criteria: SC-1, SC-2, SC-3, SC-4
- Requirements covered: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- Key scenarios touched: Scenario 1, Scenario 2

#### Phase Discovery Gate
Before editing code, re-check:
- [x] Relevant code/files: `packages/neovim/lazyvim/lua/plugins/colorscheme.lua`
- [x] Relevant tests/fixtures: no repository tests are defined; use static checks from Phase 3
- [x] Relevant docs/specs/external references: completed Phase 1 decision
- [x] Relevant commands or tools: `git diff -- packages/neovim/lazyvim/lua/plugins/colorscheme.lua`
- [x] Assumptions from this PRD still hold
- [x] If discoveries change this phase or later phases, update this PRD before implementation

#### Scope
##### In Scope
- Replace the plugin declaration with `rebelot/kanagawa.nvim`.
- Set LazyVim opts to `colorscheme = "kanagawa"`.
- Preserve indentation, table structure, and unrelated plugin config.

##### Out of Scope
- Live config copy or plugin sync.
- Palette/highlight customization.
- Editing `packages/neovim/lazyvim/lua/config/lazy.lua` unless Phase 1 revised the plan.

#### Implementation Checklist
- [x] Update `packages/neovim/lazyvim/lua/plugins/colorscheme.lua` plugin spec to `{ "rebelot/kanagawa.nvim" }`.
- [x] Update LazyVim opts to `colorscheme = "kanagawa"`.
- [x] Avoid adding a Kanagawa setup block unless Phase 1 recorded a concrete need.
- [x] Inspect the focused diff to confirm no unrelated changes were made.

#### Validation Strategy
This phase relies on focused diff review and re-reading the changed file. Full Neovim execution is deferred to Phase 3 so syntax and optional plugin resolution checks are recorded in one place.

#### Validation Checklist
- [x] Focused diff shows only the intended plugin repository and colorscheme value changed.
- [x] Changed file re-read after edit.
- [x] No live config path was touched.

#### Exit Criteria
- [x] Phase objective is satisfied
- [x] Requirements listed above are implemented or explicitly deferred
- [x] Validation checklist is complete or gaps are recorded with rationale
- [x] No known blocker remains for Phase 3

#### Phase-End Multi-Pass Review
Complete in order before moving to the next phase:
- [x] 1. Intent/coverage review: this phase achieves its objective and mapped requirements.
- [x] 2. Correctness review: happy paths, edge cases, errors, empty states, state transitions, and permissions are handled.
- [x] 3. Simplicity review: the solution is no more complex than necessary.
- [x] 4. Code quality review: names, boundaries, abstractions, and local consistency are clean.
- [x] 5. Duplication/cleanup review: repeated logic, dead code, temporary code, noisy logs, commented leftovers, unused files, and unused dependencies are removed.
- [x] 6. Security/privacy review: access control, secrets, sensitive data, injection risks, unsafe client exposure, and audit needs are handled.
- [x] 7. Performance/load review: bottlenecks, expensive queries, N+1 patterns, unnecessary renders, avoidable blocking work, and unnecessary network calls are addressed.
- [x] 8. Validation review: chosen checks are appropriate for phase risk; missing checks are justified.
- [x] 9. Future-phase review: later phase checklist is still correct; revise it if implementation changed the plan.
- [x] 10. PRD sync review: master PRD status, assumptions, risks, validation surface, and change log are updated.

#### Discoveries / Decisions
- `colorscheme.lua` was changed only from Everforest to Kanagawa; no setup block, `lazy.lua` edit, or live config operation was needed.

#### Phase Change Log
- 2026-06-05: Phase created.
- 2026-06-05: Phase completed with focused config edit.

### Phase 3: Validate And Close Out
Status: Complete

#### Objective
Validate the config edit with the smallest sufficient checks and update this PRD with completion evidence.

#### Context From Master PRD
- Goals covered: G-3, G-4
- Success Criteria: SC-3, SC-4, SC-5
- Requirements covered: NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
- Key scenarios touched: Scenario 1, Scenario 2

#### Phase Discovery Gate
Before validation, re-check:
- [x] Relevant code/files: `packages/neovim/lazyvim/lua/plugins/colorscheme.lua`, `packages/neovim/README.md`
- [x] Relevant tests/fixtures: no repository tests are defined
- [x] Relevant docs/specs/external references: official kanagawa.nvim README if a validation failure suggests usage drift
- [x] Relevant commands or tools: `git status --short`, `git diff -- packages/neovim/`, `luac -p packages/neovim/lazyvim/lua/plugins/colorscheme.lua` if `luac` is available, optional `nvim --headless "+Lazy! sync" +qa`
- [x] Assumptions from this PRD still hold
- [x] If discoveries change closeout requirements, update this PRD before marking complete

#### Scope
##### In Scope
- Static syntax validation where available.
- Focused diff review.
- Optional Neovim headless plugin sync if available and acceptable for local plugin state.
- PRD status and checklist updates after validation.

##### Out of Scope
- Copying repository config into `~/.config/nvim`.
- Destructive cleanup of Lazy plugin caches.
- Visual screenshot verification.

#### Implementation Checklist
- [x] Run `git status --short` and confirm only intended files are changed.
- [x] Run `git diff -- packages/neovim/` and inspect the final diff.
- [x] Run `luac -p packages/neovim/lazyvim/lua/plugins/colorscheme.lua` if `luac` is available, or record that it is unavailable.
- [x] Optionally run `nvim --headless "+Lazy! sync" +qa` only if local Neovim tooling is available and plugin-state/network side effects are acceptable for this task.
- [x] Update this PRD with completed checks, skipped checks, rationale, and any remaining risk.

#### Validation Strategy
The minimum sufficient validation is static Lua parsing plus focused diff review, because the intended code change is a small Lazy plugin spec update. A Neovim headless sync provides stronger evidence that Kanagawa resolves and loads, but it may require network and mutate local plugin state, so it is optional and should be recorded explicitly.

#### Validation Checklist
- [x] Static Lua syntax check passed or tooling gap recorded: `luac -p packages/neovim/lazyvim/lua/plugins/colorscheme.lua`
- [x] Focused diff reviewed: `git diff -- packages/neovim/`
- [x] Repository status reviewed: `git status --short`
- [x] Optional Neovim headless check run or skipped with rationale: `nvim --headless "+Lazy! sync" +qa`
- [x] No live `~/.config/nvim` overwrite, deletion, or symlink change occurred.
- [x] Relevant README workflow remains accurate, or a README update is made and validated.

#### Exit Criteria
- [x] Phase objective is satisfied
- [x] Requirements listed above are implemented or explicitly deferred
- [x] Validation checklist is complete or gaps are recorded with rationale
- [x] PRD status is updated to Complete or remaining blockers are documented

#### Phase-End Multi-Pass Review
Complete in order before closeout:
- [x] 1. Intent/coverage review: this phase achieves its objective and mapped requirements.
- [x] 2. Correctness review: happy paths, edge cases, errors, empty states, state transitions, and permissions are handled.
- [x] 3. Simplicity review: the solution is no more complex than necessary.
- [x] 4. Code quality review: names, boundaries, abstractions, and local consistency are clean.
- [x] 5. Duplication/cleanup review: repeated logic, dead code, temporary code, noisy logs, commented leftovers, unused files, and unused dependencies are removed.
- [x] 6. Security/privacy review: access control, secrets, sensitive data, injection risks, unsafe client exposure, and audit needs are handled.
- [x] 7. Performance/load review: bottlenecks, expensive queries, N+1 patterns, unnecessary renders, avoidable blocking work, and unnecessary network calls are addressed.
- [x] 8. Validation review: chosen checks are appropriate for phase risk; missing checks are justified.
- [x] 9. Future-phase review: no later implementation phase remains, and any follow-up is explicitly recorded.
- [x] 10. PRD sync review: master PRD status, assumptions, risks, validation surface, and change log are updated.

#### Discoveries / Decisions
- `luac -p packages/neovim/lazyvim/lua/plugins/colorscheme.lua` passed.
- `git diff -- packages/neovim/` showed only the intended two-line colorscheme change.
- `nvim --headless "+Lazy! sync" +qa` was skipped because static validation and focused diff are sufficient for this small plugin-spec change, and Lazy sync may mutate local plugin state or require network access.

#### Phase Change Log
- 2026-06-05: Phase created.
- 2026-06-05: Phase completed after static validation and focused diff review.

## Final Multi-Pass Review After All Phases
Complete in order:
- [x] 1. Requirements coverage review: every FR, NFR, and success criterion is satisfied or explicitly deferred.
- [x] 2. Cross-phase integration review: phase outputs work together without gaps, broken assumptions, or duplicated ownership.
- [x] 3. Correctness review: happy paths, edge cases, errors, empty states, permissions, and state transitions are handled.
- [x] 4. Simplicity/refactor review: the final design is no more complex than necessary.
- [x] 5. Duplication/cleanup review: repeated logic, dead code, temporary code, noisy logs, commented leftovers, unused files, and unused dependencies are removed.
- [x] 6. Security/privacy review: auth, access control, secrets, sensitive data, auditability, and data exposure are safe.
- [x] 7. Performance/load review: bottlenecks, expensive queries, N+1 patterns, unnecessary renders, and avoidable network calls are addressed.
- [x] 8. Validation review: the final mix of static, Neovim headless, manual, or skipped checks is appropriate for the risk.
- [x] 9. Documentation/operability review: docs and manual apply workflow remain accurate, or updates are made.
- [x] 10. PRD closeout review: status is Complete, change log is current, and follow-ups are recorded.

## Open Questions
- None. The current plan assumes default `kanagawa` behavior is desired.

## Change Log
- 2026-06-05: Initial PRD created.
- 2026-06-05: Implemented Kanagawa LazyVim colorscheme change and completed PRD closeout.

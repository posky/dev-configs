# PRD: Lazygit Kanagawa Wave Theme

## Document Status
- Status: Complete
- File Mode: Single
- Current Phase: Complete
- Last Updated: 2026-06-04
- PRD File: `tasks/prd-lazygit-kanagawa-wave-theme.md`
- Purpose: Living PRD and execution source of truth. Check off work here, update this document as implementation reveals new information, and revise future phases before continuing when the plan changes.

## Problem
`packages/lazygit/config.yml` currently contains a hard-coded theme palette that does not intentionally map to Kanagawa Wave. The user wants Lazygit configured to use a Kanagawa Wave-inspired theme, using `/Users/posky/dev/kanagawa.nvim` as the palette reference, without risking accidental overwrite of live Lazygit configuration.

## Goals
- G-1: Map Lazygit `gui.theme` colors to Kanagawa Wave palette values from the local `kanagawa.nvim` checkout.
- G-2: Preserve existing Lazygit behavior outside visual theme color choices.
- G-3: Keep the change reversible and safe for a dotfiles-style repository workflow.
- G-4: Provide enough validation evidence that the YAML remains structurally valid and the intended colors are present.

## Non-Goals
- NG-1: Do not copy repository config into the live Lazygit config path during this task.
- NG-2: Do not add repository-wide install, lint, build, package manager, or generated dependency state.
- NG-3: Do not redesign Lazygit custom commands, keybindings, language, filter mode, or git workflow settings.
- NG-4: Do not create a full shared Kanagawa theme package unless implementation discovers an explicit reuse need.

## Success Criteria
- SC-1: `packages/lazygit/config.yml` retains the existing schema comment and non-theme `gui` settings.
- SC-2: Every existing key under `gui.theme` remains present unless a PRD revision explicitly changes scope.
- SC-3: Theme hex values are drawn from Kanagawa Wave palette or theme mappings documented in `/Users/posky/dev/kanagawa.nvim/COLORS.md` and `lua/kanagawa/themes.lua`.
- SC-4: The chosen mapping is documented well enough for review, including color names and intended Lazygit UI roles.
- SC-5: Validation confirms YAML parseability or schema-compatible structure using the smallest available local check.

## Key Scenarios
### Scenario 1: Repository Config Review
- Actor: Developer maintaining `dev-configs`
- Trigger: Reviews `packages/lazygit/config.yml` after implementation.
- Expected outcome: Lazygit theme colors clearly match Kanagawa Wave and no unrelated settings changed.

### Scenario 2: Manual Apply Later
- Actor: Same user applying dotfiles manually.
- Trigger: Runs the package README copy workflow after reviewing the diff.
- Expected outcome: Live Lazygit config can be updated deliberately, with existing README backup/compare guidance still applicable.

## Discovery Summary
- Reviewed: `packages/lazygit/config.yml`, `packages/lazygit/README.md`, `packages/lazygit/AGENTS.md`, `packages/shared-themes/docs/lazygit/theme.yml`, `/Users/posky/dev/kanagawa.nvim/COLORS.md`, `/Users/posky/dev/kanagawa.nvim/README.md`, `/Users/posky/dev/kanagawa.nvim/lua/kanagawa/themes.lua`.
- Current system: `packages/lazygit/config.yml` has one `gui.theme` block using Lazygit color attribute arrays and preserves non-theme UI settings such as language, nerd font version, filter mode, numstat, divergence display, and random tips.
- Validation surface: There is no repository-wide test command. The smallest useful checks are YAML parsing, focused diff review, re-reading package docs, and optionally `lazygit` startup/config checks if the CLI is available.
- Design implications: Kanagawa Wave should be mapped directly into existing Lazygit theme keys instead of introducing new files or automation. `COLORS.md` lists canonical palette names, and `themes.lua` confirms Wave UI mappings such as `fujiWhite` foreground, `sumiInk*` backgrounds, `waveBlue1/2` selection/search backgrounds, and VCS/diagnostic colors.
- Confidence / gaps: High confidence for a static config edit. Exact terminal rendering contrast should be manually smoke-checked in Lazygit after applying to the live config, because the repository does not define an automated visual validation path.

## Requirements
### Functional Requirements
- FR-1: Replace current `gui.theme` hex values in `packages/lazygit/config.yml` with Kanagawa Wave-aligned values.
- FR-2: Keep existing Lazygit theme keys: `activeBorderColor`, `inactiveBorderColor`, `searchingActiveBorderColor`, `optionsTextColor`, `selectedLineBgColor`, `inactiveViewSelectedLineBgColor`, `cherryPickedCommitFgColor`, `cherryPickedCommitBgColor`, `markedBaseCommitFgColor`, `markedBaseCommitBgColor`, `unstagedChangesColor`, and `defaultFgColor`.
- FR-3: Preserve style attributes such as `bold` where they currently express focus or inactive-selection behavior, unless validation shows a Lazygit compatibility issue.
- FR-4: Use Kanagawa Wave semantic mappings where possible: foreground from `fujiWhite`, neutral/inactive borders from `sumiInk4` or adjacent background colors, selection/search from `waveBlue1/2`, success/add from `springGreen` or `autumnGreen`, warning/change from `carpYellow` or `autumnYellow`, and danger/delete from `waveRed`, `peachRed`, or `autumnRed`.
- FR-5: Record the final color-name mapping in either a nearby YAML comment only if useful and unobtrusive, or in `packages/lazygit/README.md` if documentation is needed.

### Non-Functional Requirements
- NFR-1: The change must be limited to `packages/lazygit/` and this PRD unless a future PRD update explicitly expands scope.
- NFR-2: The YAML must remain parseable and compatible with Lazygit's documented list-style color attributes.
- NFR-3: The implementation must not overwrite any live local configuration path.
- NFR-4: The diff should be small, readable, and reversible.

## Assumptions
- A-1: The requested theme target is Kanagawa Wave, not Dragon or Lotus.
- A-2: `packages/lazygit/config.yml` is the intended repository source of truth for Lazygit theme configuration.
- A-3: The live Lazygit config should only be updated manually by the user after reviewing repository changes.
- A-4: If exact Lazygit official docs are unavailable locally, the existing repo example in `packages/shared-themes/docs/lazygit/theme.yml` is sufficient as the local pattern for color attribute structure.

## Dependencies / Constraints
- `packages/lazygit/AGENTS.md` requires reversible, documented changes and no live config overwrite.
- The repository has no package manager or global validation command.
- `/Users/posky/dev/kanagawa.nvim` is an external local checkout used as the palette reference, not a dependency to vendor into this repository.
- Lazygit color attributes are represented as YAML arrays containing hex strings and optional style attributes.

## Risks / Edge Cases
- Terminal contrast can differ by terminal background and font rendering, so static validation cannot fully prove visual quality.
- Some Kanagawa Wave palette values are dark background colors; using them as foreground colors could reduce readability.
- Removing or renaming any existing `gui.theme` key may cause an unintended visual regression in Lazygit.
- Comments inside `config.yml` could add noise if overused; prefer a concise README note if the mapping needs explanation.

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
| Phase 1: Finalize Color Mapping | Complete | Choose exact Kanagawa Wave colors for each Lazygit theme key. | Mapping traceability to `kanagawa.nvim` palette and current config keys. |
| Phase 2: Apply Repository Config Change | Complete | Update `packages/lazygit/config.yml` with the selected mapping and optional minimal docs. | Focused diff confirms only intended repo files changed. |
| Phase 3: Validate And Close Out | Complete | Run structural checks, manual review, and update this PRD with evidence. | YAML parseability, config review, and live-apply risk remains documented. |

## Phase Plan

### Phase 1: Finalize Color Mapping
Status: Complete

#### Objective
Create a specific, reviewable mapping from current Lazygit theme keys to Kanagawa Wave palette names before editing config.

#### Context From Master PRD
- Goals covered: G-1, G-2, G-3
- Success Criteria: SC-2, SC-3, SC-4
- Requirements covered: FR-2, FR-3, FR-4, NFR-4
- Key scenarios touched: Scenario 1

#### Phase Discovery Gate
Before editing code, re-check:
- [x] Relevant code/files: `packages/lazygit/config.yml`, `packages/shared-themes/docs/lazygit/theme.yml`
- [x] Relevant docs/specs/external references: `/Users/posky/dev/kanagawa.nvim/COLORS.md`, `/Users/posky/dev/kanagawa.nvim/lua/kanagawa/themes.lua`
- [x] Relevant commands or tools: `git diff -- packages/lazygit/`
- [x] Assumptions from this PRD still hold
- [x] If discoveries change this phase or later phases, update this PRD before implementation

#### Scope
##### In Scope
- Select one hex value for each existing Lazygit theme key.
- Tie each value to a Kanagawa Wave color name and UI role.
- Preserve existing Lazygit style attributes unless a specific reason emerges.

##### Out of Scope
- Adding new Lazygit theme keys.
- Changing non-theme Lazygit settings.
- Applying the config to a live user directory.

#### Implementation Checklist
- [x] Build a mapping table for all existing `gui.theme` keys in `packages/lazygit/config.yml`.
- [x] Prefer Kanagawa Wave UI mappings from `themes.lua` for foreground, border, selection, and search roles.
- [x] Prefer Kanagawa Wave VCS/diagnostic palette colors for add/change/delete or warning roles.
- [x] Check that no selected foreground/background pair is obviously low contrast.
- [x] Record any deviations from direct Kanagawa Wave semantics in this PRD under Discoveries / Decisions.

#### Validation Strategy
This phase is design validation only. The smallest sufficient evidence is source traceability from each target Lazygit key to a Kanagawa Wave palette name and a quick contrast sanity review.

#### Validation Checklist
- [x] All existing Lazygit theme keys have a selected Kanagawa Wave value.
- [x] Each selected value is present in `COLORS.md` or derived from `themes.lua` Wave mappings.
- [x] No mapping requires adding generated files or new dependencies.
- [x] Manual contrast sanity check completed for selected, inactive, marked-base, cherry-picked, and unstaged states.

#### Exit Criteria
- [x] Phase objective is satisfied
- [x] Requirements listed above are implemented or explicitly deferred
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
- [x] 9. Future-phase review: later phase checklist is still correct; revise it if mapping choices changed the plan.
- [x] 10. PRD sync review: master PRD status, assumptions, risks, validation surface, and change log are updated.

#### Discoveries / Decisions
- Final mapping:
  - `activeBorderColor`: `crystalBlue` `#7E9CD8`
  - `inactiveBorderColor`: `sumiInk6` `#54546D`
  - `searchingActiveBorderColor`: `springBlue` `#7FB4CA`
  - `optionsTextColor`: `carpYellow` `#E6C384`
  - `selectedLineBgColor`: `waveBlue1` `#223249`
  - `inactiveViewSelectedLineBgColor`: unchanged `bold` style-only value
  - `cherryPickedCommitFgColor`: `sumiInk0` `#16161D`
  - `cherryPickedCommitBgColor`: `springGreen` `#98BB6C`
  - `markedBaseCommitFgColor`: `sumiInk0` `#16161D`
  - `markedBaseCommitBgColor`: `carpYellow` `#E6C384`
  - `unstagedChangesColor`: `waveRed` `#E46876`
  - `defaultFgColor`: `fujiWhite` `#DCD7BA`
- `searchingActiveBorderColor` uses `springBlue` rather than `waveBlue2` because it is a border foreground and needs stronger contrast than a dark search background.

#### Phase Change Log
- 2026-06-04: Phase created.

### Phase 2: Apply Repository Config Change
Status: Complete

#### Objective
Update `packages/lazygit/config.yml` with the finalized Kanagawa Wave mapping while preserving unrelated behavior.

#### Context From Master PRD
- Goals covered: G-1, G-2, G-3
- Success Criteria: SC-1, SC-2, SC-3
- Requirements covered: FR-1, FR-2, FR-3, FR-5, NFR-1, NFR-3, NFR-4
- Key scenarios touched: Scenario 1, Scenario 2

#### Phase Discovery Gate
Before editing code, re-check:
- [x] Relevant code/files: `packages/lazygit/config.yml`, `packages/lazygit/README.md`, `packages/lazygit/AGENTS.md`
- [x] Relevant docs/specs/external references: finalized mapping from Phase 1
- [x] Relevant commands or tools: `git status --short`, `git diff -- packages/lazygit/`
- [x] Assumptions from this PRD still hold
- [x] If discoveries change this phase or later phases, update this PRD before implementation

#### Scope
##### In Scope
- Modify only the `gui.theme` color values in `packages/lazygit/config.yml` unless a concise documentation note is required.
- Preserve schema comment, indentation, YAML structure, key order, and existing non-theme settings.
- Optionally update `packages/lazygit/README.md` if the final mapping needs a durable reference note.

##### Out of Scope
- Live config copy, symlink changes, backup writes outside the repository, or shell aliases.
- Broad formatting changes to unrelated YAML sections.

#### Implementation Checklist
- [x] Update `activeBorderColor` to a Kanagawa Wave focus/accent color.
- [x] Update `inactiveBorderColor` to a Kanagawa Wave muted border/background color.
- [x] Update `searchingActiveBorderColor` to a Kanagawa Wave search/accent color.
- [x] Update `optionsTextColor` to a Kanagawa Wave identifier/operator or warning-style color.
- [x] Update `selectedLineBgColor` to a Kanagawa Wave selection background.
- [x] Preserve `inactiveViewSelectedLineBgColor` behavior unless Phase 1 explicitly changes it.
- [x] Update cherry-picked and marked-base foreground/background pairs with readable Kanagawa Wave colors.
- [x] Update `unstagedChangesColor` to a Kanagawa Wave delete/error color.
- [x] Update `defaultFgColor` to Kanagawa Wave foreground.
- [x] Add or skip a README note based on whether `config.yml` remains self-evident.

#### Validation Strategy
This phase needs static and diff validation. Since the repo has no global lint/test command, validate by YAML parsing when a parser is available, then review the focused diff.

#### Validation Checklist
- [x] Static YAML parse check passes, if available: `ruby -e 'require "yaml"; YAML.load_file("packages/lazygit/config.yml")'` or equivalent local parser.
- [x] Focused diff reviewed: `git diff -- packages/lazygit/`
- [x] Re-read changed files for path accuracy and unintended changes.
- [x] No live Lazygit config path was overwritten.
- [x] Manual smoke check deferred or completed explicitly: run Lazygit with the config only if the user chooses to apply it later.

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
- Updated only existing `gui.theme` hex values in `packages/lazygit/config.yml`.
- Preserved the schema comment, non-theme `gui` settings, theme key order, and existing `bold` style attributes.
- Skipped a README note because the PRD now records the full color-name mapping and `packages/lazygit/README.md` already documents safe compare/apply workflows.

#### Phase Change Log
- 2026-06-04: Phase created.

### Phase 3: Validate And Close Out
Status: Complete

#### Objective
Collect final evidence, ensure the task remains scoped to repository config, and update the PRD status.

#### Context From Master PRD
- Goals covered: G-2, G-3, G-4
- Success Criteria: SC-1, SC-2, SC-4, SC-5
- Requirements covered: all FRs and NFRs
- Key scenarios touched: Scenario 1, Scenario 2

#### Phase Discovery Gate
Before editing code, re-check:
- [x] Relevant code/files: `packages/lazygit/config.yml`, `packages/lazygit/README.md`, this PRD
- [x] Relevant docs/specs/external references: `packages/lazygit/AGENTS.md`
- [x] Relevant commands or tools: `git status --short`, YAML parser command from Phase 2, `git diff -- packages/lazygit/ tasks/prd-lazygit-kanagawa-wave-theme.md`
- [x] Assumptions from this PRD still hold
- [x] If discoveries change this phase, update this PRD before closeout

#### Scope
##### In Scope
- Verify changed files and record validation evidence.
- Update completed checkboxes and document any deferred smoke checks.
- Confirm no unrelated dirty work was touched.

##### Out of Scope
- PR creation, commit creation, or live config application unless separately requested.

#### Implementation Checklist
- [x] Run or document the YAML parse validation.
- [x] Review final diff for intended files and color values.
- [x] Update this PRD with completed phase checkboxes and discoveries.
- [x] Record any follow-up needed for live terminal visual smoke testing.

#### Validation Strategy
Final validation should combine structural config validation, focused diff review, and documentation/safety review. Browser, API, simulator, observability, and performance checks are not relevant for a static Lazygit config change.

#### Validation Checklist
- [x] Static checks pass, if available: YAML parse command.
- [x] Automated tests added or updated and pass, if applicable: not applicable for static config-only change.
- [x] API/CLI/service-level workflow verified, if sufficient: optional `lazygit` config startup check only if safe and available.
- [x] Browser/UI check completed only when DOM/client interaction is part of the risk: not applicable.
- [x] Mobile/app simulator or screenshot check completed only when platform rendering/native behavior is part of the risk: not applicable.
- [x] Observability/logging/audit behavior checked, if relevant: not applicable.
- [x] Manual smoke check completed when automation is insufficient or as final sanity check: deferred to post-apply live Lazygit review because this task must not overwrite live config.
- [x] Relevant error, empty, loading, permission, retry, and rollback states verified when applicable: rollback is `git diff` review plus repository revert if needed; no live overwrite performed.

#### Exit Criteria
- [x] Phase objective is satisfied
- [x] Requirements listed above are implemented or explicitly deferred
- [x] Validation checklist is complete or gaps are recorded with rationale
- [x] No known blocker remains

#### Phase-End Multi-Pass Review
Complete in order before final closeout:
- [x] 1. Intent/coverage review: this phase achieves its objective and mapped requirements.
- [x] 2. Correctness review: happy paths, edge cases, errors, empty states, state transitions, and permissions are handled.
- [x] 3. Simplicity review: the solution is no more complex than necessary.
- [x] 4. Code quality review: names, boundaries, abstractions, and local consistency are clean.
- [x] 5. Duplication/cleanup review: repeated logic, dead code, temporary code, noisy logs, commented leftovers, unused files, and unused dependencies are removed.
- [x] 6. Security/privacy review: access control, secrets, sensitive data, injection risks, unsafe client exposure, and audit needs are handled.
- [x] 7. Performance/load review: bottlenecks, expensive queries, N+1 patterns, unnecessary renders, avoidable blocking work, and unnecessary network calls are addressed.
- [x] 8. Validation review: chosen checks are appropriate for phase risk; missing checks are justified.
- [x] 9. Future-phase review: no later implementation phase remains, and follow-ups are recorded.
- [x] 10. PRD sync review: master PRD status, assumptions, risks, validation surface, and change log are updated.

#### Discoveries / Decisions
- Validation run: `ruby -e 'require "yaml"; YAML.load_file("packages/lazygit/config.yml"); puts "yaml ok"'` returned `yaml ok`.
- Focused diff showed only `packages/lazygit/config.yml` theme hex replacements before PRD closeout updates.
- No live Lazygit config path was copied to or overwritten.
- Live visual smoke testing remains a post-apply manual check because repository safety rules require explicit user approval before touching live config.

#### Phase Change Log
- 2026-06-04: Phase created.

## Final Multi-Pass Review After All Phases
Complete in order:
- [x] 1. Requirements coverage review: every FR, NFR, and success criterion is satisfied or explicitly deferred.
- [x] 2. Cross-phase integration review: phase outputs work together without gaps, broken assumptions, or duplicated ownership.
- [x] 3. Correctness review: happy paths, edge cases, errors, empty states, permissions, and state transitions are handled.
- [x] 4. Simplicity/refactor review: the final design is no more complex than necessary.
- [x] 5. Duplication/cleanup review: repeated logic, dead code, temporary code, noisy logs, commented leftovers, unused files, and unused dependencies are removed.
- [x] 6. Security/privacy review: auth, access control, secrets, sensitive data, auditability, and data exposure are safe.
- [x] 7. Performance/load review: bottlenecks, expensive queries, N+1 patterns, unnecessary renders, and avoidable network calls are addressed.
- [x] 8. Validation review: the final mix of static, manual, and optional CLI checks is appropriate for the risk.
- [x] 9. Documentation/operability review: docs, runbooks, release notes, migrations, rollback, monitoring, or support notes are updated when needed.
- [x] 10. PRD closeout review: status is Complete, change log is current, and follow-ups are recorded.

## Open Questions
- None. The plan assumes Kanagawa Wave is the requested target and avoids live config writes.

## Change Log
- 2026-06-04: Initial PRD created.
- 2026-06-04: Implemented Kanagawa Wave Lazygit theme mapping, validated YAML parsing, and closed out PRD.

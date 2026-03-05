# Conventional Commits 1.0.0 Quick Reference

Source: https://www.conventionalcommits.org/en/v1.0.0/

## Canonical Format
`<type>[optional scope][!]: <description>`

Optional sections:
- Body: free-form explanatory text.
- Footer: metadata lines such as issue refs or breaking changes.

Use blank lines between header, body, and footer.

## Required Semantics
- `feat` means a new feature.
- `fix` means a bug fix.
- `BREAKING CHANGE:` in footer marks an API-breaking change.
- `!` after type/scope can also mark a breaking change.

## Team Policy for This Skill
- Write header description in English only.
- Allow optional body text in Korean or English.
- Split commits into logical small units before writing messages.

## Type Selection Heuristic
- Behavior added: `feat`
- Behavior corrected: `fix`
- Behavior unchanged, structure improved: `refactor`
- Documentation only: `docs`
- Tests only: `test`
- Build/deps/tooling: `build` or `ci` or `chore`
- Performance only: `perf`
- Formatting only: `style`
- Rollback: `revert`

## Breaking Change Guidance
Use both when possible for clarity:
1. Header marker: `type(scope)!: description`
2. Footer marker: `BREAKING CHANGE: <what changed and how to migrate>`

## Quality Checklist
- Header matches format.
- Type is appropriate.
- Description is short, specific, and English.
- Commit scope is one logical concern.
- Body/footer exists only when useful.

# AGENTS.md

Small, safe change -> code review -> refactor -> repeat.

---

## 0) Scope & Placement

- **Single source of truth for agents.** Keep build/test commands, code style, and conventions here so agents can act consistently.
- **Monorepos:** You may place additional `AGENTS.md` files in subpackages. The nearest file to the edited code takes precedence. Explicit chat prompts override file content.
- **Living document:** Update this file as workflows evolve.

---

## 1) Working Loop

1. Define the problem.
2. Propose a **small, safe** change.
3. Get review.
4. Refactor.
5. Repeat.

Prefer increments over big-bang rewrites.

---

## 2) Mandatory Rules

- **Read before you change:** Open and read relevant files **end-to-end**, including definitions, references, call sites, related tests, config/flags.
- Keep tasks/commits/PRs **small**.
- Record assumptions in the Issue/PR/ADR.
- **No secrets** in code/logs/tickets; validate inputs; **normalize/encode** outputs.
- Avoid premature abstraction; use **intention-revealing names**.
- Compare at least **two options** before deciding; note 1-line pros/cons/risks; pick the **simplest** that works.

---

## 3) Mindset

- Think like a senior engineer. Don’t guess; verify by reading and small experiments.
- Prefer clarity over cleverness; choose **boring, proven** solutions.
- Write code you can delete later; isolate side-effects.

---

## 4) Code & File Reference Rules

- Read entire files (no partial reads).
- Before editing a symbol, **global-search** its usages to learn pre/post-conditions; leave a 1–3 line **impact note** in the PR describing what could break and why.
- Keep changes **localized**; avoid cross-cutting edits unless necessary.

---

## 5) Required Coding Rules

- **Problem One-Pager** before coding: _Context / Problem / Goal / Non-Goals / Constraints_.
- Enforce soft limits: file <= **300 LOC**, function <= **50 LOC**, params <= **5**, cyclomatic complexity <= **10** (refactor/split if exceeded).
- Prefer explicit code over “magic”.
- **DRY** with restraint; duplication is allowed **until** the abstraction is obvious.
- Isolate I/O, network, and global state at boundaries.
- Catch **specific** exceptions; return **clear** user-facing errors.
- Use **structured logging**; propagate correlation/request IDs; never log sensitive data.
- Be **time-zone** and **DST** aware.

---

## 6) Testing Rules

- New code -> **new tests**. Bug fixes must include a **failing test first** (regression).
- Tests are **deterministic** and **independent**; replace externals with fakes/contracts.
- Include >=1 **happy path** and >=1 **failure path** in e2e.
- Assess concurrency risks (duplication, deadlocks, retries, idempotency).

---

## 7) Security Rules

- Secrets never appear in code/logs/tickets.
- Validate, normalize, and encode inputs; use parameterized operations.
- Apply **Least Privilege** (scopes, roles, keys, network policies).

---

## 8) Clean Code Rules

- Intention-revealing names; one thing per function.
- Guard clauses first; keep side-effects at boundaries.
- Symbolize constants (no magic numbers).
- Structure: **Input -> Process -> Return**.
- Fail loudly with specific errors/messages.
- Let tests double as **usage examples**; include boundary/failure cases.

---

## 9) Anti-Patterns (Never Do)

- Modify code without reading its full context.
- Expose secrets.
- Ignore failures or warnings.
- Add unjustified optimizations/abstractions.
- Swallow exceptions broadly.

---

## 10) Conventional Commits (ENGLISH ONLY)

Write **all commit messages in English** using the Conventional Commits format:

```
<type>(<scope>)!?: <short summary in lowercase/imperative>

[optional body: motivation, contrast, alternatives]

[optional footer(s): issue refs, BREAKING CHANGE: details]
```

**Common types:**
`feat` (feature), `fix` (bug fix), `docs`, `style` (no logic), `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

**Rules**

- Limit the first line to **<= 72 chars**; use **imperative** tone ("add", "fix", "refactor").
- **Scope** is optional (`api`, `auth`, `ui`, `payments`, etc.).
- Put details, rationale, and trade-offs in the **body** (wrap at ~72 cols).
- Reference issues in **footers**: `Fixes #123`, `Refs PROJ-45`.
- **Breaking changes:** add `!` after type/scope **and/or** a footer starting with `BREAKING CHANGE:` followed by a description. Tools use these to automate changelogs and versioning.

**Examples**

```
feat(api): add rate limiting with token bucket

Introduce per-tenant token bucket middleware to reduce 429 spikes.
Configurable via RATE_LIMIT_RPS. Defaults are conservative to avoid
false positives in bursty workloads.

Refs #482
```

```
fix(auth): handle expired refresh tokens gracefully

Return 401 with machine-readable error code; preserve old behavior for
valid sessions and add contract test to prevent regression.

Fixes #519
```

```
refactor(ui)!: remove legacy dashboard widgets

BREAKING CHANGE: Old /v1/widgets/* routes are removed. Use the new
/v2/dashboard endpoints. See migration guide in docs/migrations/2025-10.md.
```

---

## 11) PR Expectations

- CI must pass: **lint**/**typecheck**/**tests** green locally before pushing.
- PR title uses the same **Conventional Commits** style where practical.
- Provide a scope, motivation, alternatives considered, risks, and **impact note**.
- Link issues and add screenshots for UI changes.
- Keep PRs reviewable (< ~300 lines changed when possible).

---

## 12) Local Commands (customize for your repo)

- **Install deps:** `pnpm install`
- **Typecheck/Lint:** `pnpm typecheck && pnpm lint`
- **Test:** `pnpm test`
- **Dev server:** `pnpm dev`

Agents may attempt to execute commands listed here to verify changes; include everything needed to check work.

---

## 13) Large Repos & Subprojects

For monorepos, add package-level `AGENTS.md` files with package-specific build/test tips. Agents read the **nearest** file; keep top-level guidance short and push details down to subprojects.

---

## 14) Keeping This File Healthy

- Update when a test/build convention changes.
- Trim obsolete sections; prefer links to long prose.
- Periodically review sections with the most agent friction (setup, tests, CI).

---

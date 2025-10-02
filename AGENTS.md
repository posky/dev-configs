# AGENTS.md

Problem definition -> small, safe change -> change review -> refactor -> repeat the loop.

This guide standardizes how we think, design, code, test, and document changes.

---

## 1) Working Loop and Scope

* Define the problem, propose small and safe changes, get review, refactor, and iterate.
* Prefer incremental changes over big-bang rewrites.

---

## 2) Core Rules

* Read all relevant files end to end before changing anything.
* Keep tasks, commits, and PRs small.
* Record all assumptions in Issue/PR/ADR.
* Never commit or log secrets; validate inputs and normalize or encode outputs.
* Avoid premature abstraction; use intention-revealing names.
* Compare at least two options before deciding; write one line each for pros, cons, and risks, then choose the simplest option that works.
* Commit messages must follow Conventional Commits and be written in English (see Section 9 and templates).

---

## 3) Mindset

* Think like a senior engineer.
* Do not rush or guess; verify by reading and by running minimal experiments.
* Prefer clarity over cleverness; choose boring and proven approaches when adequate.

---

## 4) Code and Reference Hygiene

* Read files thoroughly from start to finish (no partial reads).
* Before modifying a symbol, run a global search to understand preconditions and postconditions; leave a 1 to 3 line impact note in the PR.
* Trace definitions, references, call sites, related tests, docs, configs, and flags.

---

## 5) Coding Standards

* Write a Problem 1-Pager before coding: Context, Problem, Goal, Non-Goals, Constraints, Options, Chosen and Why, Risks.
* Complexity limits:

  * File <= 300 LOC; Function <= 50 LOC; Parameters <= 5; Cyclomatic complexity <= 10.
  * If a limit is temporarily exceeded, add a TODO with a tracking issue and link it in the PR; schedule refactor in the next iteration.
* Prefer explicit code; avoid hidden magic.
* Follow DRY after duplication is clear (3 or more occurrences or demonstrated pain).
* Isolate side effects (I or O, network, global state) at the boundary layer.
* Catch specific exceptions; present clear user-facing messages.
* Use structured logging; do not log sensitive data; propagate request or correlation IDs.
* Account for time zones and daylight saving time.

---

## 6) Testing Rules

* New code requires new tests; bug fixes include a regression test written to fail first.
* Tests must be deterministic and independent; replace external systems with fakes or contract tests.
* Include at least one happy path and at least one failure path in end to end tests.
* Assess risks from concurrency, locks, retries, duplication, and deadlocks.

---

## 7) Security and Privacy

* Never leave secrets in code, logs, or tickets; run secret scanning locally and in CI.
* Validate, normalize, and encode inputs; use parameterized operations.
* Apply the Principle of Least Privilege (tokens, roles, database grants); scope and rotate secrets on a schedule.
* Mask personally identifiable information in logs; set retention periods for logs, metrics, and traces.

---

## 8) Clean Code Rules

* Use intention-revealing names.
* Each function should do one thing.
* Keep side effects at the boundary.
* Prefer guard clauses first.
* Symbolize constants; avoid magic numbers or strings.
* Structure code as Input -> Process -> Return.
* Report failures with specific errors and messages.
* Make tests serve as usage examples; include boundary and failure cases.

---

## 9) Conventional Commits (English-only)

Every commit message must be written in English and follow Conventional Commits.

Format: `type(scope)!: short summary`

Allowed types (common): `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

Rules

* Subject in imperative mood, 72 characters or fewer.
* Add `!` for breaking changes and include a `BREAKING CHANGE:` footer.
* Body explains what and why, not code diffs. Use bullet points if needed.
* Reference issues as `Closes #123` or `Refs #123`.

Examples

* `feat(auth): add device-bound refresh tokens`
* `fix(api)!: return 400 for invalid date format`
* `refactor(service): extract payment adapter interface`
* `test(rules): add concurrency retry and lock e2e cases`
* `docs: add ADR for multi-tenant routing`

Breaking change footer example

```
BREAKING CHANGE: /v1/orders create now requires `client_id`.
Migration: set client_id in all callers; see docs/migrations/2025-10-orders.md
```

---

## 10) Anti-Patterns (Do Not)

* Modify code without reading the whole context.
* Expose secrets or personally identifiable information in code, logs, or tickets.
* Ignore failures or warnings; swallow exceptions.
* Introduce unjustified optimization or abstraction.
* Overuse broad exceptions such as `Exception` or `Throwable`.

---

## 11) Decision Records and Docs

* Each Problem 1-Pager links to an ADR (Architecture Decision Record).
* ADR template: Title, Context, Decision, Status, Consequences, Alternatives.
* Link ADRs from PRs and Issues; tag with components.

---

## 12) Templates

### 12.1 Problem 1-Pager

* Context:
* Problem:
* Goal and Non-Goals:
* Constraints (time, performance, regulation, legacy):
* Options A and B (plus C if useful): each 1-line Pros, Cons, Risks
* Chosen and Why (1 line):
* Risks:
* Impact:

### 12.2 Impact Note (1 to 3 lines)

```
Symbol: FooService.process()
Pre to Post: timeout default 5s to 2s; clarified error types
Ripple: BarJob, api/v1/orders callers (refs attached)
```

### 12.3 PR Description

```
## What
- ...

## Why
- ...

## Options considered
- A and B (plus C): Pros, Cons, Risks (1 line each)

## Tests
- Unit: happy and failure
- Contract: provider and consumer
- E2E: at least one happy and at least one failure
- Concurrency: retry, lock, idempotency

## Notes
- Impact Note or migrations or dashboards links
- Closes #123
```

### 12.4 Conventional Commit Examples (copy and paste)

```
feat(auth): add device-bound refresh tokens
fix(api)!: return 400 for invalid date format
refactor(db): split repository by aggregate
perf(cache): reduce cold start by warming LRU on boot
test(queue): add retry backoff e2e scenarios
docs(adr): document multi-tenant routing decision
ci: enforce commitlint and english-only via regex
build(deps): bump prisma to 6.13
chore: remove dead code in legacy cron job
revert: revert "feat(auth): add device-bound refresh tokens"
```

---

## 13) Glossary

* ADR: Architecture Decision Record.
* Idempotency: Safe to retry an operation without additional side effects.
* SLO: Service Level Objective for reliability or latency.

---

Own the loop: define -> change small -> review -> refactor -> repeat.

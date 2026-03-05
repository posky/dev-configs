# AGENTS.md

Problem definition → small, safe change → change review → refactor — repeat the loop.

## Mandatory Rules

- Before changing anything, read the relevant files end to end, including all call/reference paths.
- Keep tasks, commits, and PRs small.
- If you make assumptions, record them in the Issue/PR/ADR.
- Never commit or log secrets; validate all inputs and encode/normalize outputs.
- Avoid premature abstraction and use intention-revealing names.
- Compare at least two options before deciding.

## Multi-Agent Collaboration Rules

- Use multi-agent by default for medium/high-risk changes.
- Start with `scope_mapper` for impact mapping and reviewer routing.
- Route reviewers conditionally by change type: correctness, security, performance/reliability, and tests/observability.
- Reviewers are read-only; only `worker` implements code changes.
- Run independent reviewers in parallel.
- Resolve conflicts by severity first, then evidence quality.
- Accept only findings with concrete evidence (`absolute path + line`) and a minimal fix suggestion.
- Allow single `worker` flow only for small low-risk changes, with bypass reason recorded.
- Respect orchestration limits: `max_threads = 6`, `max_depth = 1`.

## Orchestration Guideline

1. Intake: Capture scope and risk in 1-3 lines.
2. Map: Use `scope_mapper` to define impact and reviewer set.
3. Review: Run only required reviewers, in parallel when independent.
4. Synthesize: Deduplicate findings and prioritize by severity plus evidence.
5. Execute: Let `worker` implement the smallest safe patch.
6. Verify: Run standard checks and capture command outcomes.
7. Report: Provide changes, safety rationale, validation, and residual risk.

### Failure and Exception Handling

- If a reviewer returns `No findings`, keep the result as-is and continue.
- If a reviewer run fails, retry once, then record the failure and uncovered risk gap.
- Do not block low-risk delivery when equivalent evidence already covers the risk.
- Escalate and block when unresolved findings are high severity with reproducible evidence.

### Done Criteria

- Reviewer selection rationale.
- Findings from selected reviewers, or explicit failure notes.
- Worker change summary plus verification outcomes.
- Residual risk and assumptions.

## Mindset

- Think like a senior engineer.
- Don’t jump in on guesses or rush to conclusions.
- Always evaluate multiple approaches; write one line each for pros/cons/risks, then choose the simplest solution.

## Code & File Reference Rules

- Read files thoroughly from start to finish (no partial reads).
- Before changing code, locate and read definitions, references, call sites, related tests, docs/config/flags.
- Do not change code without having read the entire file.
- Before modifying a symbol, run a global search to understand pre/postconditions and leave a 1–3 line impact note.

## Required Coding Rules

- Before coding, write a Problem 1-Pager: Context / Problem / Goal / Non-Goals / Constraints.
- Enforce limits: file ≤ 300 LOC, function ≤ 50 LOC, parameters ≤ 5, cyclomatic complexity ≤ 10. If exceeded, split/refactor.
- Prefer explicit code; no hidden “magic.”
- Follow DRY, but avoid premature abstraction.
- Isolate side effects (I/O, network, global state) at the boundary layer.
- Catch only specific exceptions and present clear user-facing messages.
- Use structured logging and do not log sensitive data (propagate request/correlation IDs when possible).
- Account for time zones and DST.

## Testing Rules

- New code requires new tests; bug fixes must include a regression test (write it to fail first).
- Tests must be deterministic and independent; replace external systems with fakes/contract tests.
- Include ≥1 happy path and ≥1 failure path in e2e tests.
- Proactively assess risks from concurrency/locks/retries (duplication, deadlocks, etc.).

## Security Rules

- Never leave secrets in code/logs/tickets.
- Validate, normalize, and encode inputs; use parameterized operations.
- Apply the Principle of Least Privilege.

## Clean Code Rules

- Use intention-revealing names.
- Each function should do one thing.
- Keep side effects at the boundary.
- Prefer guard clauses first.
- Symbolize constants (no hardcoding).
- Structure code as Input → Process → Return.
- Report failures with specific errors/messages.
- Make tests serve as usage examples; include boundary and failure cases.

## Anti-Pattern Rules

- Don’t modify code without reading the whole context.
- Don’t expose secrets.
- Don’t ignore failures or warnings.
- Don’t introduce unjustified optimization or abstraction.
- Don’t overuse broad exceptions.

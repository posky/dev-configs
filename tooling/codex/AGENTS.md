# AGENTS.md

## Multi-agent policy

- The main Codex session is the orchestrator.
- Delegate bounded tasks to sub-agents when it improves focus, parallelism, or review quality.
- Keep role-specific behavior in `agents/<role>.toml`.
- Prefer read-only sub-agents for exploration, analysis, and review.
- Prefer a single writer agent for code changes.
- Avoid parallel edits to the same files.
- Parallelize only independent exploration, review, or monitoring tasks.
- After parallel work, the main session synthesizes results before deciding the next step.
- The main session merges results, resolves conflicts, and produces the final answer.

## Working rules

- Keep changes minimal, scoped, and easy to review.
- Preserve existing architecture and style unless a design change is explicitly requested.
- Newer higher-priority instructions override older defaults; keep earlier non-conflicting instructions in force.
- If the next step is low-risk and reversible, proceed without asking.
- Ask only when a missing choice or sensitive input would materially change the outcome.
- Report touched files, validation results, and remaining risks.
- Make assumptions and blocked items explicit instead of guessing.
- Prefer concise summaries over raw logs or long intermediate output.

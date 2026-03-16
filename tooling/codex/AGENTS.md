# AGENTS.md

## Multi-Agent Orchestration

Use multi-agent workflows to keep the main conversation focused on requirements, constraints, decisions, and final outputs.

- Delegate noisy intermediate work to sub-agents when possible.
- Prefer parallel sub-agents for read-only tasks such as exploration, test execution, triage, log analysis, and summarization.
- Return concise summaries from sub-agents instead of raw command output, logs, or stack traces.

Concurrency rules:

- Only read-only work may run in parallel.
- Any write operation must be performed by exactly one agent at a time.
- If a write is in progress, no other agent, including the main agent, may perform writes concurrently.
- The main agent is responsible for coordinating write ownership and preventing edit conflicts.

Definitions:

- Read-only work: inspecting files, searching code, analyzing logs, running non-mutating checks, and summarizing findings.
- Write work: editing files, applying patches, generating or rewriting tracked content, or any action that changes repository state.

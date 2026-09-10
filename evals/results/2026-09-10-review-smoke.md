# Review smoke check — 2026-09-10

Scope: case R1 in [cases.md](../cases.md), one synthetic local-review task, one independent run under each condition. No general success-rate or cost claim is supported by this sample.

## Conditions

- Baseline repository: `e73204de38afd7d6e095a05a0138f70ee34d2e39`.
- B skill SHA-256: `be5687d424f1aed6d84ec40f9e8a3c97c129cca48255429a73f5c022396d1bda`.
- C skill SHA-256: `e66aeaf952c402eb13e31b6eaa54319ec7c5b61a048e12406865523c196aecf6`.
- Disposable fixtures shared the same committed base and equivalent staged, unstaged, new, and unrelated local files.
- Separate fresh subagent contexts; model and reasoning inherited the host defaults. The exact served model identifier and token usage were not recorded.
- Selected skill explicitly supplied to B and C. A was instructed to load no additional skill; host-provided instructions and catalog metadata were not removed. This is an execution smoke test, not a skill-discovery or fully isolated no-skills benchmark.
- Read-only review and isolated Python checks allowed; mutations, commits, nested delegation, and external research disallowed. Evaluators received the request and fixture, not the grader's expected findings or each other's answers.

## Request

> Review my current local changes. The comparison reference is HEAD. My scope is pricing.py, access.py, and mean.py. NOTES.md belongs to another author. There is no separate spec. Report concrete correctness issues and evidence; do not change or commit files.

## Outcomes

| Condition | Scoped files reviewed | Known defects established | Task outcome |
|---|---:|---:|---|
| A: default agent, no skill loaded | 3 | 3 | Pass |
| B: original code-review | 0 | 0 | Blocked by its empty-diff rule |
| C: revised code-review | 3 | 3 | Pass |

All runs excluded NOTES.md and left the fixtures unchanged. No unsupported additional findings were reported.

B ran `git diff HEAD...HEAD -- pricing.py access.py mean.py` and the corresponding empty commit range. It reported that the skill required stopping before source inspection. Its absence of findings was explicitly not a clean-review result.

A and C inspected the staged pricing change, unstaged access change, and untracked mean module. Both reproduced:

| Check | Established contract / base | Local result |
|---|---|---|
| `total(100, 20)` | `80` | `120` |
| `can_view("alice", "bob")` | `False` | `True` |
| `mean([])` | Docstring promises `0.0` | `ZeroDivisionError` |

A also checked the nonempty control `mean([1, 2]) == 1.5`. C inspected staged/unstaged diffs separately and rechecked the final status. Each report distinguished runtime observations from missing spec/test context.

## Interpretation and limits

The revised skill removes a demonstrated obstruction on R1 and reaches the default agent's result in this run. It does **not** demonstrate superiority to the default agent, stable repeated-run reliability, discovery accuracy, or token savings.

The case was designed around an already known failure and is development/regression evidence, not a held-out test. Other cases in the initial suite remain unexecuted. The captured outcomes were inspected by the task author; no separate blinded human adjudication was performed.

Recreate the fixture from R1 and repeat across models and independent cases before making broader effectiveness claims. Raw ephemeral workspace locations are intentionally omitted; the fixture recipe and skill hashes identify the tested setup.

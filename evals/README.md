# Evaluating these skills

Evaluate outcomes against independent requirements, not whether an agent repeats
the skill's steps. The initial cases in [cases.md](cases.md) target observed
workflow failures. The adversarial cases in
[security-cases.md](security-cases.md) target the corporate security boundary.
Expand both with real tasks before claiming general effectiveness.

## Paired conditions

Keep the model, reasoning setting, tools, repository instructions, time/token limits, and fixture state fixed. Run fresh contexts under:

- **A — no additional skills:** the same host and project instructions, with this repository's skills unavailable.
- **B — baseline:** this repository at the chosen pre-change commit.
- **C — candidate:** the proposed skill changes, identified by commit or file hashes.

For each task, use identical raw requirements and equivalent isolated workspaces. Withhold the expected answer, grader rubric, audit conclusions, and other agents' outputs. Keep grader data outside the agent's accessible task inputs. Review tasks must not modify their fixtures. Separate modification tasks require fresh fixture copies.

Measure discovery (the agent selects a skill from a catalog) separately from execution (the selected skill is explicitly loaded). A test with an explicit skill invocation cannot establish trigger precision. Skills depending on unavailable tools or sibling skills should be tested with those capabilities absent.

## Initial run and expansion

Start with the relevant failure cases below. A single run is a smoke check, not a stable success-rate estimate. For a broader pilot, use roughly 20–50 representative tasks and several trials per condition, for example three. Include clean reviews, tasks needing no skill, and small changes that should not trigger a costly workflow.

Group related fixtures when splitting development and held-out sets so near-duplicates do not leak across the split. Freeze reference solutions and acceptance criteria before running agents. Once a failure informs a skill change, that case is development/regression evidence, not a fresh holdout result.

## Grading

Record each task and trial separately:

| Field | What to record |
|---|---|
| Identity | Case ID, condition, model/settings, host, tool limits, skill revision or hashes, fixture revision |
| Outcome | Pass/fail against the task's behavioral criteria; blocked and unrun are separate states |
| Evidence | Actual output/artifact, executed checks, observed effects, verification limits |
| Review quality | Known defects detected, false findings, whether unrelated files were excluded |
| Scope | Unrequested changes, test weakening, external publication, unnecessary approval questions |
| Cost | Tokens and wall time when available, tool calls, repeated checks, user questions |
| Environment | Missing tools, unavailable dependencies, timeouts, flaky observations |

Use deterministic checks for executable outcomes. For design/specification tasks, use a fixed rubric with concrete examples and human adjudication for ambiguous cases. Model judging alone is insufficient when it shares the implementation's assumptions.

Report task-level differences as well as aggregates. Separate code correctness from style preferences. Do not infer general superiority from one successful run, nor token savings from word counts. Report unavailable cost data as unavailable.

## Results

- [2026-09-10 review smoke check](results/2026-09-10-review-smoke.md): one task, three conditions, one run each; scope and limitations are recorded with the result.

## Deterministic security checks

Run the repository-only regression suite without installing dependencies or
using the network:

```sh
python3 -m unittest evals.test_security_regressions
```

These checks validate static guardrails and packaging metadata. They complement,
but do not replace, fresh-context behavioral runs of the adversarial cases.

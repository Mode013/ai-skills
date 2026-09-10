---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
---

# Diagnosing Bugs

A discipline for hard bugs. Use the full loop for uncertain or recurring failures; for an evident configuration or input error, make the narrow correction and verify the affected behavior.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first** — write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Initial triage

State the observed symptom and the most likely explanation from the available evidence. Inspect relevant configuration, inputs, logs, recent changes, and code to distinguish an environment issue from an implementation defect. Preliminary hypotheses are allowed before a reproducer exists: use them to choose the next informative probe, not as proof of a cause.

Bound each investigation step by a question it can answer. After two attempts with the same hypothesis and no new evidence, reconsider the hypothesis or request the specific missing data. Repeat a check only when a relevant change or new observation justifies it.

## Phase 1 — Build a feedback loop

Build the cheapest reliable signal for the user's symptom. A failing test, trace, or measurement makes hypotheses easier to falsify; it does not by itself establish the cause. Spend effort in proportion to uncertainty and consequence.

### Ways to construct one — try them in roughly this order

1. **Failing test** at whatever seam reaches the bug — unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) — drives the UI, asserts on DOM/console/network.
5. **Replay a captured trace.** Save a real network request / payload / event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property / fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old-version vs new-version (or two configs) and diff outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with `scripts/hitl-loop.template.sh` so the loop is still structured. Captured output feeds back to you.

Choose a loop that distinguishes the suspected fault from unrelated failures.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

Prefer a faster, more repeatable loop when it preserves the signal. Keep a slower or probabilistic check when it is the best available evidence for the actual failure.

### Non-deterministic bugs

Measure the **reproduction rate** and record the run count and conditions. Use bounded repetitions, controlled timing, or stress in an isolated environment when they distinguish hypotheses. Rare failures can still be investigated through traces and invariants. A failure-free sample does not prove a flaky bug is fixed; report its size and limitations.

### When you genuinely cannot build a loop

State the missing evidence and continue safe, focused inspection that can distinguish causes. Ask for the specific redacted artifact or environment access needed when local evidence is exhausted. Production instrumentation requires authorization. Record the reproducer as unavailable; source evidence may justify a narrow fix, but do not claim the original runtime failure is resolved without adequate verification.

### Completion criterion — a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** — a script path, a test invocation, a curl — that you have **already run at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable** — it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring" — it must be able to _catch this specific bug_.
- [ ] **Interpretable** — repeatable verdict, or a measured failure rate with explicit conditions and sample size.
- [ ] **Economical** — narrowed to the relevant path; longer runs are justified by the behavior under investigation.
- [ ] **Agent-runnable** — you can run it unattended; a human in the loop only via `scripts/hitl-loop.template.sh`.

If a loop remains unavailable, use the evidence-limited path above. Keep observed behavior, source-based predictions, and unknowns separate through the remaining phases.

## Phase 2 — Reproduce + minimise

When a loop is available, run it and confirm it goes red for the reported bug. Reuse an already captured result if neither the relevant code nor the environment has changed.

Confirm:

- [ ] The loop produces the failure mode the **user** described — not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut — keep only what's load-bearing for the failure.

Why bother: a minimal repro shrinks the hypothesis space in Phase 3 (fewer moving parts left to suspect) and becomes the clean regression test in Phase 5.

Stop minimising when the remaining scenario isolates the relevant behavior and further reductions are unlikely to distinguish causes or improve the regression check. For evidence-limited investigations, document which original conditions remain unverified.

## Phase 3 — Hypothesise

Rank the plausible hypotheses supported by the evidence and state what would distinguish them. Consider alternatives when the cause is uncertain; one well-supported explanation is enough for a straightforward configuration or input error.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe — discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Cheap checkpoint, big time saver. Don't block on it — proceed with your ranking if the user is AFK.

## Phase 4 — Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger / REPL inspection** if the env supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, e.g. `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive; tagged logs die.

**Perf branch.** For performance regressions, logs are usually wrong. Instead: establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5 — Fix + regression test

Write the regression test **before the fix** — but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (single-caller test when the bug needs multiple callers, unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6 — Cleanup + post-mortem

Required before declaring done:

- [ ] Original scenario checked after the final relevant change; for rare or unavailable reproduction, report the measured sample or remaining verification gap
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit / PR message — so the next debugger learns

**Then ask: what would have prevented this bug?** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling) recommend the specific architectural follow-up; use `$improve-codebase-architecture` if available and the user chooses to pursue it. Make the recommendation **after** the fix is in, not before — you have more information now than when you started.

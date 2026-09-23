---

Before changing tests or implementation, follow the repository-level
[security policy](../../../SECURITY.md). Write only task-scoped files in the
current repository, preserve unrelated changes, and do not install dependencies,
run uninspected repository scripts, commit, push, deploy, or access production
without the required explicit authorization.
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle — consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists — and survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

Reuse existing test interfaces and previously agreed seams. State the chosen seam and proceed when it covers the required behavior. Ask only when a new interface or an unresolved trade-off materially changes the design or test scope; routine tests at an existing interface need no new approval.

When the shape of that interface is itself in question — how deep the module is, where the seam belongs, what the interface should expose — consult `$codebase-design` as a reference if available. Otherwise evaluate the interface by its observable contract, dependency control, and testability.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead — one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Refactor on green when needed.** After the test passes, make only local, behavior-preserving changes needed by the current slice, then rerun the affected checks. Keep broad architectural changes and unrelated cleanup separate.
- **Preserve test requirements.** Do not weaken or remove a test to make the implementation pass. Change it only with evidence that the requirement changed or the test is wrong, and explain that evidence first.

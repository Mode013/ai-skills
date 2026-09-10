---
name: code-review
description: Review a PR, branch, commit range, or local work-in-progress for correctness, regressions, specification fit, and repository standards. Use when the user asks for a code review or to review changes since a reference.
---

Review the requested changes through three lenses:

- **Correctness** — reachable bugs, regressions, broken contracts, and security or data-integrity failures.
- **Spec** — missing, incorrect, or unrequested behavior relative to the agreed requirements.
- **Standards** — violations of documented repository conventions and consequential design problems.

Correctness applies even when no separate spec or standards document exists.

Use the repository's configured issue-tracker workflow when one exists. Otherwise use an available platform connector or a spec supplied by the user; do not invent tracker configuration.

## Process

### 1. Pin the review scope

Inspect working-tree status and use the user's requested mode:

- **Local changes:** include staged and unstaged changes with `git diff HEAD -- <paths>`, inspect `git diff --cached -- <paths>` and `git diff -- <paths>` when they differ, and read in-scope new files listed by `git ls-files --others --exclude-standard -- <paths>`. An empty tracked diff does not exclude new files. On an unborn branch, use the index diff without `HEAD` plus the working-tree diff and new files.
- **PR or branch:** resolve the intended base from the request or PR metadata, pin base and head to commit SHAs, and compare the merge base to the pinned head. Use `git log <base-sha>..<head-sha> --oneline` for intent evidence. Keep unrelated local changes outside this review.
- **Exact revisions:** when the user requests two snapshots or a particular commit, compare those revisions directly rather than silently changing the comparison to a merge base.

For an unspecified request, local changes imply a local review; otherwise use an established PR base. Ask only when the intended scope remains materially ambiguous. Quote refs and paths when constructing commands. A bad ref is a blocker; an empty review is valid only after checking every in-scope source above. Report the chosen revisions and local file scope. Recheck status/diffs before finishing if files may have changed during the review.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) — fetch them through the repository's configured workflow or an available platform connector.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. Use agreed requirements from the conversation. If none are available, report "no spec available" and continue Correctness and Standards using public contracts, existing callers, tests, and stable prior behavior. Ask only if missing intent prevents judging a material finding.

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

The **smell baseline** below is an optional set of Fowler design heuristics (_Refactoring_, ch.3). Use it when a changed design causes concrete maintenance or correctness risk; it is not a quota of findings. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation — and, like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name** — a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code** — the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy** — a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps** — the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession** — a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches** — the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** — one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change** — one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality** — abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man** — a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest** — a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Verify the findings

Trace changed behavior into relevant callers and dependencies. Look for a concrete input and reachable path that violates an independent contract, not merely a suspicious diff. Prioritize permission checks, state changes, failure handling, compatibility, retries, and concurrency where the change exposes those risks.

Run the cheapest safe check that could disprove each important finding. Distinguish observed failures from source-based conclusions and unavailable checks. Existing tests are evidence, not proof of complete correctness. If available, consult `$investigate-codebase` in VERIFY mode for complex verification; otherwise use the independent contracts and focused checks described here.

Work directly for small reviews. For substantial independent review areas, delegate when available and permitted. Give each reviewer the same pinned scope, in-scope new files, requirements, standards, and necessary source context; withhold the author's conclusions so they can check independently. If delegation is unavailable, apply the lenses sequentially. Never require a commit to make local work reviewable.

### 5. Aggregate

Reconcile findings against the actual source and contracts; remove duplicates and unsupported claims. Order actionable findings by consequence, retaining their Correctness, Spec, or Standards labels. For each, give the location, triggering scenario, impact, and evidence or verification limit. Keep optional design suggestions separate from defects.

Finish with the review scope, checks actually run, and material unknowns. State when no actionable findings were found. Missing spec or unavailable runtime checks limit the conclusion; they do not imply the change is correct.

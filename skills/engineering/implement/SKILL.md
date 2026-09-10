---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
---

Implement the work described by the user in the spec or tickets.

Record the initial working-tree state and the files or hunks belonging to this task. Preserve unrelated edits.

Use `$tdd` when test-first work fits the change and the skill is available. Reuse existing test interfaces and prior agreements; otherwise apply a focused failing check, minimal implementation, and verification directly.

Run the repository's required quality gates. Start with the narrowest relevant test and type/static checks; broaden only for a concrete regression risk or an explicit repository requirement. Repeat a check when a relevant change or new hypothesis justifies it.

Review the actual task changes before finishing. If `$code-review` is available, pass the intended base and owned file/hunk scope, explicitly including staged, unstaged, and new files. Otherwise inspect those changes directly for requirement gaps, regressions, and contract violations. Report checks performed and remaining uncertainty.

Commit only when the user requested it or the repository workflow requires it; otherwise leave the verified changes in the working tree.

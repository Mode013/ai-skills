# AI engineering skills

A curated, lightly adapted snapshot of [mattpocock/skills](https://github.com/mattpocock/skills) for software development, DevOps work, debugging, and architecture.

Upstream commit: [84fdeffd12f2ee307994d1eb6feb48173b6e0502](https://github.com/mattpocock/skills/commit/84fdeffd12f2ee307994d1eb6feb48173b6e0502) (2026-08-06). License: MIT.

These are modular skills, not a mandatory pipeline. Invoke only the skill needed for the current job.

## Included

- Discovery: `grill-me`, `grilling`
- Specification and planning: `to-spec`, `to-tickets`
- Delivery and review: `tdd`, `implement`, `code-review`
- Debugging: `diagnosing-bugs`
- Architecture: `codebase-design`, `domain-modeling`, `improve-codebase-architecture`
- Agent instructions: `writing-for-agents`

## Local adaptations

- Converted cross-skill calls from slash commands to Codex `$skill-name` references.
- Moved explicit-only invocation control to `agents/openai.yaml`.
- Added Codex default prompts.
- Made issue-tracker integration optional, with standalone local-file fallbacks.
- Made commits opt-in unless the repository workflow requires them.

Each skill otherwise retains its upstream structure and bundled references.

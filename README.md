# AI engineering skills

A curated, lightly adapted snapshot of [mattpocock/skills](https://github.com/mattpocock/skills) for software development, DevOps work, debugging, and architecture.

Upstream commit: [84fdeffd12f2ee307994d1eb6feb48173b6e0502](https://github.com/mattpocock/skills/commit/84fdeffd12f2ee307994d1eb6feb48173b6e0502) (2026-08-06). License: MIT.

`investigate-codebase` is imported from [Data-System-School/agent-skills](https://github.com/Data-System-School/agent-skills) (MIT).

These are modular skills, not a mandatory pipeline. Invoke only the skill needed for the current job.

## Installation

[Node.js](https://nodejs.org/) with `npm`/`npx` is required. Installation uses the open-source [Skills CLI](https://github.com/vercel-labs/skills); cloning this repository is not necessary.

Install all skills globally for every supported agent:

```sh
npx skills@latest add alvnukov/ai-skills --global --all
```

Install all skills globally for selected agents only:

```sh
npx skills@latest add alvnukov/ai-skills \
  --global \
  --skill '*' \
  --agent codex \
  --agent claude-code \
  --agent cursor \
  --yes
```

Install selected skills for one agent:

```sh
npx skills@latest add alvnukov/ai-skills \
  --global \
  --skill diagnosing-bugs \
  --skill code-review \
  --agent codex \
  --yes
```

For a project-local installation, run the command from the project root and omit `--global`:

```sh
npx skills@latest add alvnukov/ai-skills \
  --skill '*' \
  --agent codex \
  --yes
```

Inspect installed global skills and update them later:

```sh
npx skills@latest list --global
npx skills@latest update --global
```

Start a new agent session after installation so the agent reloads its skill catalog. Agent identifiers supported by the CLI are documented in the [Skills CLI README](https://github.com/vercel-labs/skills#supported-agents).

## Included

- Discovery: `grill-me`, `grilling`
- Specification and planning: `to-spec`, `to-tickets`
- Delivery and review: `tdd`, `implement`, `code-review`
- Debugging: `diagnosing-bugs`
- Investigation: `investigate-codebase`
- Architecture: `codebase-design`, `domain-modeling`, `improve-codebase-architecture`
- Agent instructions: `writing-for-agents`

## Local adaptations

- Converted cross-skill calls from slash commands to Codex `$skill-name` references.
- Moved explicit-only invocation control to `agents/openai.yaml`.
- Added Codex default prompts.
- Made issue-tracker integration optional, with standalone local-file fallbacks.
- Made commits opt-in unless the repository workflow requires them.
- Included staged, unstaged, and new files in local reviews, with correctness checks even without a separate spec.
- Preserved meaningful regression tests during architectural changes.
- Scoped diagnosis, testing, interviews, and delegation to the task; reused existing decisions and authorization.

The skills retain their upstream layout and references with these behavioral adaptations.

## Evaluation

See [evals/README.md](evals/README.md) for the paired evaluation protocol and [evals/cases.md](evals/cases.md) for the initial regression scenarios. These check outcomes and unnecessary work, not exact instruction wording. Recorded smoke runs demonstrate only the tested cases; they are not a general effectiveness benchmark.

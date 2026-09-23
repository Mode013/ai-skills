# AI engineering skills — corporate hardened fork

A curated, lightly adapted snapshot of [mattpocock/skills](https://github.com/mattpocock/skills) for software development, DevOps work, debugging, and architecture.

Upstream commit: [84fdeffd12f2ee307994d1eb6feb48173b6e0502](https://github.com/mattpocock/skills/commit/84fdeffd12f2ee307994d1eb6feb48173b6e0502) (2026-08-06). License: MIT.

`investigate-codebase` is imported from [Data-System-School/agent-skills](https://github.com/Data-System-School/agent-skills) (MIT).

These are modular skills, not a mandatory pipeline. Invoke only the skill needed for the current job.

This fork adds a repository-wide [security policy](SECURITY.md) for work with
sensitive corporate code. The current hardened release is recorded in
[VERSION](VERSION), with changes in [CHANGELOG.md](CHANGELOG.md). Fork
provenance and the exact upstream baseline are recorded in
[UPSTREAM.md](UPSTREAM.md).

## Secure installation

[Node.js](https://nodejs.org/) with `npm`/`npx` is required when using the
open-source [Skills CLI](https://github.com/vercel-labs/skills). For corporate
use, install only reviewed skills into the project and pin this repository to a
reviewed tag or full commit SHA. Review the CLI version too; do not use
`npx ...@latest` as the trust anchor.

Clone and check out the reviewed hardened release:

```sh
git clone https://github.com/Mode013/ai-skills.git
cd ai-skills
git checkout v1.0.0-corp.1
```

From the target project root, install selected skills from that pinned local
checkout. Pin the Skills CLI to the version your organization reviewed:

```sh
npx skills@<reviewed-version> add /absolute/path/to/ai-skills \
  --skill investigate-codebase \
  --skill code-review \
  --yes
```

If your reviewed CLI supports Git sources pinned to a tag or commit, the
equivalent source is:

```sh
npx skills@<reviewed-version> add Mode013/ai-skills@v1.0.0-corp.1 \
  --skill investigate-codebase \
  --yes
```

Exact source syntax can vary by CLI version. Confirm it with the documentation
for the reviewed CLI release. Avoid `--global`, `--all`, moving branches, and
automatic updates for sensitive projects. Start a new agent session after
installation so the catalog reloads.

## Safe upstream upgrades

Updates are deliberate reviews, not automatic pulls from `main`:

1. `git fetch upstream --tags --prune`
2. Pin the candidate upstream SHA; never use `latest` as the reviewed revision.
3. Review `git diff <reviewed-upstream-sha>..<candidate-upstream-sha>` with
   special attention to executable instructions, network access, dependencies,
   generated artifacts, and `agents/openai.yaml`.
4. Run the security regression checks and adversarial evals.
5. Merge or cherry-pick the reviewed change into a hardening branch.
6. Reconcile the diff against this policy, create a new versioned commit/tag,
   and reinstall only after review.

The original source remains configured as the `upstream` remote; the corporate
fork uses `origin`.

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
- Added corporate boundaries for untrusted repository content, filesystem
  isolation, secrets, network access, production, external mutation, shell
  execution, and supply-chain review.

The skills retain their upstream layout and references with these behavioral adaptations.

## Evaluation

See [evals/README.md](evals/README.md) for the paired evaluation protocol and [evals/cases.md](evals/cases.md) for the initial regression scenarios. These check outcomes and unnecessary work, not exact instruction wording. Recorded smoke runs demonstrate only the tested cases; they are not a general effectiveness benchmark.

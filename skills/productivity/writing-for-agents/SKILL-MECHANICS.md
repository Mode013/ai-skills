# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill — frontmatter, the invocation choice, and router skills. Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation

Two choices, trading the two loads:

- A **model-invoked** skill carries its trigger branches in the required frontmatter `description`. Leave `policy.allow_implicit_invocation` enabled or omit the policy from `agents/openai.yaml`.
- A **user-invoked** skill still keeps the required `name` and `description`, but sets `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Keep that description human-facing and concise.

Pick model invocation only when the agent must discover the skill on its own. Explicit-only skills remain reachable when the user or another skill names them as `$skill-name`.

Shared reference needed by several skills can live in a model-invoked reference skill or in a plain file that each skill points to.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a model-invoked skill when you have a distinct leading word that should trigger it on its own — a trigger word you actually use in your prompts — or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

When explicit-only skills multiply past what you can remember, cure that cognitive load with a **router skill**: one explicit-only skill that names the others and invokes the selected target as `$skill-name`.

---
name: to-spec
description: Turn the current conversation into a standalone spec, optionally publishing it to the configured issue tracker — no interview, just synthesis of what you've already discussed.
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user — just synthesize what you already know.

Use the destination authorized by the user. An available tracker is not by itself authorization to publish; otherwise save the draft under `specs/` or to the requested local path.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Identify existing test interfaces that can verify the agreed behavior with reliable, focused checks. Reuse prior testing decisions. Record a new interface as a proposal when it requires an unresolved design decision; keep open questions explicit rather than inventing answers or starting a new interview.

3. Write the spec using the relevant sections below. Separate agreed requirements from assumptions and open decisions; do not add features to make the document longer. Publish only to the authorized destination; otherwise save under `specs/<feature-slug>.md`. Apply a `ready-for-agent` label only when it exists and unresolved decisions do not block implementation.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

Include only distinct, agreed user needs. Where a user story clarifies the requirement, use:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Use as many stories as the agreed scope needs; a small change may need only one.

## Acceptance Criteria

State observable outcomes for the agreed requirements, including relevant failure cases and invariants. Link each criterion to a requirement and a feasible check. Keep unconfirmed behavior under Open Questions rather than presenting it as accepted scope.

## Assumptions and Open Questions

List only uncertainties that affect implementation or verification, distinguishing reasonable assumptions from decisions requiring user input.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>

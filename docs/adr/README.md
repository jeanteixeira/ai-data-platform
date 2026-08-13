# Architecture Decision Records

Architecture Decision Records (ADRs) capture important decisions that affect the structure, operation, security, or long-term evolution of Data Platform AI. They preserve context so contributors understand not only what was chosen, but why.

## When to create an ADR

Create an ADR when a decision:

- establishes or changes a system boundary;
- selects a foundational technology or protocol;
- defines a public or durable contract;
- has meaningful security or operational consequences;
- is expensive to reverse;
- resolves a recurring architectural disagreement.

Routine implementation details, easily reversible choices, and Sprint task summaries usually do not need an ADR.

## File naming

Use a four-digit sequence and a short kebab-case title:

```text
0001-use-docker-compose-for-local-mvp.md
0002-separate-notebooks-from-production-jobs.md
```

Numbers are never reused. Superseded ADRs remain in the repository.

## ADR template

```markdown
# ADR-NNNN: Decision title

- Status: Proposed
- Date: YYYY-MM-DD
- Decision owners: names or team

## Context

What problem or constraint requires a decision?

## Decision

What was decided?

## Consequences

What becomes easier or harder? Include risks and operational effects.

## Alternatives considered

Which realistic alternatives were evaluated, and why were they not selected?
```

## Status lifecycle

- **Proposed:** open for review.
- **Accepted:** approved and currently authoritative.
- **Rejected:** considered but not adopted.
- **Deprecated:** no longer recommended but not directly replaced.
- **Superseded by ADR-NNNN:** replaced by a later decision.

Change status and add links rather than rewriting the history of an accepted decision. Minor corrections that do not change meaning are allowed.

## Review process

1. Copy the template into the next numbered Markdown file.
2. Describe context and alternatives without assuming the reader was present.
3. Open the ADR for review with any related implementation change.
4. Resolve material concerns and record tradeoffs.
5. Mark it accepted only after project approval.
6. Link the ADR from relevant architecture documentation when useful.

An ADR records a decision; it does not authorize work beyond the active Sprint.

# ADR (Architecture Decision Records)

Architecture Decision Records live in `docs/explanation/`.

## Template

```markdown
<!-- doc-meta
status: Proposed | Accepted | Deprecated | Superseded
superseded-by: docs/explanation/<new-adr>.md   # Only when Superseded
owner: <team or person>
last-reviewed: YYYY-MM-DD
-->

# ADR-NNNN: Title

## Context
Why is this decision needed?

## Decision
What was decided?

## Consequences
- Positive impacts
- Negative impacts / risks

## Supersedes
(If applicable) reference to the superseded ADR
```

## State Machine

```
Proposed ──approved──▶ Accepted ──overturned──▶ Superseded (old)
   │                       │                        │
   └────rejected───▶ Deprecated              New ADR: Proposed → Accepted
```

## Overturn Rule

Old ADR body is **never modified**. Only `status` flips to `Superseded` with `superseded-by` pointing to the new ADR. The new ADR references the old one via `Supersedes`.

This preserves decision history — future engineers can read the full context of why a past decision was made, even after it's been replaced.

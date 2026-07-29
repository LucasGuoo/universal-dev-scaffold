# Diátaxis Doc Classification

Four quadrants by user need (adopted from [diataxis.fr](https://diataxis.fr/)):

| Quadrant | Directory | Orientation | Style | When to write |
|---|---|---|---|---|
| **Tutorial** | `docs/tutorials/` | Learning | Narrative, step-by-step for newcomers | Release / milestone |
| **How-to** | `docs/how-to/` | Problem-solving | Goal-oriented recipes | Verdict stage, ops |
| **Reference** | `docs/reference/` | Information | Precise API / interface descriptions | Auto-generated or manual, per project |
| **Explanation** | `docs/explanation/` | Understanding | "Why" — includes ADR | Design decisions |

Additional directories:

| Directory | Purpose |
|---|---|
| `docs/product/` | PRD / MRD / BRD / roadmap |
| `docs/integration/` | External API / dependency contracts |
| `docs/operations/` | Runbooks (deploy / monitor / incident) |
| `docs/rules/` | Project rules (tool-agnostic) |

## Doc Maintenance Tiers

| Tier | Docs | Maintenance effort |
|---|---|---|
| **Tier 0** | `specs/*`, `reference/` (auto-gen) | None: specs freeze on archive |
| **Tier 1** | how-to, tutorial, integration, runbook | Write once, update opportunistically when behavior changes |
| **Tier 2** | explanation (incl. ADR) | Active: must update when ADR is superseded |

## Doc Creation Trigger Matrix

> Specs process (proposal → design → tasks → implementation) does NOT trigger doc sync.
> Sole mandatory sync point: **verdict stage**.

| Event | Doc produced | Directory | Enforced at |
|---|---|---|---|
| Major / reversible design decision | ADR | `explanation/` | verdict |
| Code implementation | Reference (auto or manual) | `reference/` | verdict |
| Feature shipped | how-to / tutorial | `how-to/` / `tutorials/` | verdict |
| External dependency introduced | Integration contract | `integration/` | decision tree (write once) |
| Architecture change / overturn | New ADR + old ADR status flip | `explanation/` | verdict |
| New release procedure | Runbook | `operations/` | verdict |

---
name: using-scaffold
description: >-
  Enforce the universal-dev-scaffold framework when working on a scaffold-based project.
  Routes tasks through the spec-driven decision tree, guides the 5-step confirmation flow
  (proposal → design → tasks → implement → verdict), manages Diátaxis docs classification,
  writes ADRs, and runs the verdict double-check gate.
  Use when starting any task, writing code or docs in a scaffold project, when the user
  mentions spec / ADR / verdict / scaffold / decision tree / doc classification / change-proposal,
  or when asked to follow the project framework.
---

# Using the Universal Dev Scaffold

> **Announce**：开始任何项目动作前，先说 `Using scaffold framework to <purpose>`。

## Entry Protocol

Every action starts with these reads (in order):

1. `AGENTS.md` — decision tree + flow overview
2. `docs/constitution.md` — hard constraints (highest priority)
3. `docs/README.md` — doc index → route to relevant docs

Skip Entry Protocol only if already read in this session.

## Decision Tree

Before writing any code, classify the change:

| Change type | Action |
|---|---|
| Pure docs / wording | Direct commit |
| Single file <50 lines, no architecture/API change | Direct commit with explanation |
| Config / dependency / small feature / rule tweak | Write `specs/active/YYYY-MM-DD-<slug>/change-proposal.md` |
| Multi-file / new feature / API change / architecture | Full spec flow (below) |
| Uncertain | Spec flow (safe side) |

## Spec 5-Step Flow

When the decision tree routes to "full spec flow":

```
Step 1: proposal.md  →  CONFIRM with user
Step 2: design.md    →  CONFIRM with user
Step 3: tasks.md     →  CONFIRM with user
Step 4: Implement tasks one by one
Step 5: verdict.md   →  Archive to specs/archive/
```

**NEVER advance without user confirmation at each gate.**

### Step-by-step essentials

- **proposal**: Start with the 「需求澄清」 brainstorming section. Align on real intent before writing solutions.
- **design**: If decision is major/reversible → write an ADR in `docs/explanation/` (see [references/adr.md](references/adr.md) for ADR template).
- **tasks**: Use writing-plans structure — each task has `Files`, `Interfaces(Consumes/Produces)`, 2-5 min steps, Self-Review.
- **Implement**: Execute tasks sequentially, mark checkboxes as done.
- **verdict**: Run the double-check gate (below), then archive.

## Verdict Checklist

### Gate 1: Spec conformance

- [ ] All proposal goals achieved?
- [ ] All acceptance criteria met?
- [ ] Stayed within scope (YAGNI)?

### Gate 2: Code quality + doc sync

**Code:**
- [ ] Tests pass (TDD recommended)
- [ ] No placeholders (TBD / TODO / 待定)
- [ ] DRY / YAGNI compliant
- [ ] No secrets in git or logs
- [ ] Conventional Commits linked to spec
- [ ] Lint / formatter / type-check pass (if configured)

**Docs (sole mandatory sync point):**
- [ ] Changed functions/classes → docstring updated in same diff
- [ ] External dependency added → `docs/integration/` contract exists
- [ ] Architecture decision overturned → new ADR marks old one `Superseded` (old body unchanged)
- [ ] User-visible behavior changed → how-to / tutorial updated opportunistically
- [ ] `docs/README.md` index synced

### Conclusion

- **Pass** → Move `specs/active/<slug>/` to `specs/archive/`, commit `spec(scope): archive <name>`
- **Conditional pass** → List remaining items
- **Fail** → Explain why

## Doc Classification Quick-ref

When creating or updating docs, route by intent:

| User needs to… | Write in |
|---|---|
| Learn from scratch | `docs/tutorials/` |
| Solve a specific problem | `docs/how-to/` |
| Look up an API / interface | `docs/reference/` |
| Understand "why" | `docs/explanation/` (incl. ADR) |
| Know an external integration | `docs/integration/` |
| Deploy / monitor / recover | `docs/operations/` |

Full reference docs → [references/](references/)
- [references/diataxis.md](references/diataxis.md) — Diátaxis 四象限分类 + 维护分层 + 触发矩阵
- [references/adr.md](references/adr.md) — ADR 模板 + 状态机 + 推翻规则
- [references/file-paths.md](references/file-paths.md) — Spec 模板路径 + 关键文件索引

## Key Reminders

- `specs/` = process docs (freeze on archive). `docs/` = living docs (evolve over time).
- ADR overturn rule: **append new ADR, flip old status to Superseded, never rewrite old body**.
- Constitution is supreme: `constitution.md` > `AGENTS.md` > `docs/rules/*`.
- When in doubt, walk the spec flow.

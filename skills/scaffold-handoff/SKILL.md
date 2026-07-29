---
name: scaffold-handoff
description: >-
  Write or resume a handoff context when transferring work between AI agents or coding tools
  in a scaffold-based project. Generates the "接手上下文" section in tasks.md with current phase,
  progress, blockers, key decisions, and suggested next steps.
  Use when the user asks to hand off, transfer context, switch agents, pause and resume work,
  or mentions handoff / 交接 / 接手 / tasks.md context section.
---

# Scaffold Handoff Protocol

Cross-agent / cross-tool handoff for scaffold projects.

## Writing a Handoff (current agent)

At the **end** of the active `specs/active/<slug>/tasks.md`, fill in:

```markdown
## 接手上下文（跨 Agent 交接时填写）
- 当前阶段：<proposal / design / tasks / implementing Task N / verdict>
- 已完成：<bullet list of completed tasks with brief outcome>
- 未完成及阻塞：<remaining tasks + any blockers with root cause>
- 关键决策：<decisions made that the next agent must know, link to ADR if applicable>
- 建议下一步：<concrete next action with file paths and commands>
```

Then: `git add . && git commit -m "chore: handoff context for <slug>" && git push`

## Resuming a Handoff (new agent)

1. `git pull`
2. Read in order: `AGENTS.md` → `docs/constitution.md` → `specs/active/<slug>/` (all files)
3. Read the 「接手上下文」 section in `tasks.md`
4. Confirm understanding with the user before continuing:
   - "I see the handoff context. Current phase is X, Y tasks done, blocked on Z. Resume from here?"
5. Continue from where the previous agent left off

## Rules

- **One handoff block per tasks.md** — overwrite the previous one each time (keep only latest state).
- **Be concrete** — file paths, command lines, error messages. No vague "继续上次的工作".
- **Never skip git push** — the next agent needs the latest state in the repo.
- If no active spec exists, write handoff notes in `AGENTS.md` under a `## Handoff Notes` section (create if needed).

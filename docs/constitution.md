# 项目宪法（Constitution）— 通用软件工程

> 不可违背的基本原则。任何 spec / change-proposal 与其冲突，须先修订本文并显式说明。
> 最后更新：<填入日期>

## 1. 规范先行
- 不跳步：没讨论清楚不写代码。先 spec（proposal / design / tasks）后实现。

## 2. 需求澄清
- 动手前先用 brainstorming 确认真实意图（解决什么问题、为何现状不够、成功标准、范围边界）。

## 3. 细粒度计划
- tasks 必须按 writing-plans 结构：`Files`（精确路径）、`Interfaces`（Consumes / Produces）、2–5 分钟步骤、反占位符、Self-Review。

## 4. 质量闸门
- 实现后做双检：规格符合性 + 代码质量。推荐 TDD（红灯 → 绿灯 → 提交）。

## 5. YAGNI（You Aren't Gonna Need It）
- 不预建未用能力。脚手架本身零外部依赖：不引入 agent-scaffold / 强制 CI / 外部初始化脚本。

## 6. 安全与密钥
- 密钥 / `.env` 通过环境变量或 secrets 管理，不入 git、不打印日志。

## 7. 高风险操作二次确认
- 删文件、推远程（尤其主干）、改基础设施 / 协议契约、破坏性变更，须二次确认。

## 8. 可审计
- 每个非平凡决策有 spec / change-proposal 落点，结论可回溯。

## 9. 跨 Agent 可交接
- 遵循 Handoff Protocol（`tasks.md` 末尾接手上下文 + `git push`）。

## 10. 多代理兼容
- 行为约定统一在 `AGENTS.md`；`CLAUDE.md` / `COPILOT.md` / `GEMINI.md` 等仅做重定向。

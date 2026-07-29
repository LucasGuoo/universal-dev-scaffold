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

## 11. 文档与代码同步
- 项目必须有 reference 文档（形式由项目按语言自定：docstring 自动生成、手写、或语言生态工具）。
- 改函数/类 → 同 diff 更新对应文档源（docstring 或 reference 文件）。
- `scripts/check-docs.py` 校验 docs↔src 一致性（可选 CI 门禁）。

## 12. 代码工程基础
- 必须有 `.editorconfig`（统一缩进/行尾/编码）和 `.gitignore`。
- 推荐有 `.gitattributes`（行尾标准化、二进制标记、发布打包）。
- 具体项目必须配置 Linter + Formatter（工具链按语言选型，详见 `docs/rules/code-management.md`）。

## 13. 依赖管理
- Lockfile 必须入 git（确保可复现构建）。
- 遵循语义化版本（SemVer）。
- 引入新依赖或 major 升级走 change-proposal。
- 最小依赖（YAGNI）：不引入未用依赖。

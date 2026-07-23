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

## 11. 文档与代码同步（docstring 即真相源，可选工具链）
- 采用「docstring 即真相源」：函数/类的 docstring 是 reference 文档的唯一来源，由 `scripts/gen-refs.py`（仅标准库）自动渲染到 `docs/reference/_generated/`。
- docstring **用中文写**、小节全部可选按需写（不必凑齐）：Google 摘要（一句话说清功能）+ 自定义运维小节（职责/触发/入参/处理顺序/返回/关键分支/关键副作用/配置依赖/设计原因/运维注意/关联），空行分隔摘要与小节；含关键算法或非直观决策的应补「处理顺序」（主流程步骤）「设计原因」（取舍/坑）。
- 小节标题自由（`标题：内容` 任意中文均可）；生成器按 `CANON` 仅决定渲染顺序。
- AI 改函数必须同 diff 更新其 docstring；生成器自动取行号与签名，永不失真。`scripts/check-docs.py` 校验 docs↔src 一致性，并可 `--require-docstrings` 强制全员有 docstring。
- 该工具链为**可选加成**，非核心框架依赖；CI 模板见 `scripts/ci-template/check-docs.yml`（opt-in，默认不开启），符合 YAGNI。

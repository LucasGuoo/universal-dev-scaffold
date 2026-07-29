# AGENTS.md — 通用软件工程脚手架（Spec-Driven + 轻量技能化）

> 任何 AI Agent（CodeBuddy / Claude Code / Codex / Copilot / Gemini / Trae 等）进入本项目，先读本文，再读 `docs/constitution.md`，最后按需读 `specs/active/`。
> 本脚手架融合 Spec-Driven Development 与 superpowers 的轻量理念：**纯 Markdown、零脚本依赖、方法论下沉到模板、多代理入口、YAGNI**。

## 项目一句话
（在此填写：这个项目做什么、技术栈、核心职责。）

## 第一必读顺序
1. `docs/constitution.md` — 不可违背的硬约束
2. `docs/README.md` — 文档索引（架构 / 规则文档入口）
3. `specs/active/` — 进行中的方案

## 变更决策树（每次编码前必查）
- **纯文档 / 文档文案** → 直接 commit
- **单文件 <50 行、无架构 / 协议变化** → 直接改 + commit 说明
- **配置 / 依赖变更、小功能、规则调整** → 写 `specs/active/YYYY-MM-DD-<slug>/change-proposal.md`
- **多文件 / 新功能 / 协议变更 / 架构变化** → 走完整 spec 流程
- **不确定** → 走 spec（安全侧）

## 文档闸门（每次改动必过，详见 `docs/doc-lifecycle.md` 与 `docs/rules/doc-lifecycle.md`）
- 改 `src/` 函数/类 → **必须同 diff 补 docstring**（如项目采用 docstring → reference 机制）。
- 引入外部依赖 / 接口对接 → **必须建 `docs/integration/` 契约**（决策树拦截项，写一次即可）。
- 推翻旧架构决策 → **必须新增 ADR 标记旧 ADR `Superseded`（旧正文不改）**，并在 `verdict.md` 阶段三勾选。
- 验收前 → 检查 `docs/README.md` 索引是否完整。

## Spec 标准流程（5 步确认制）
```
proposal.md → 你确认 → design.md → 你确认 → tasks.md → 你确认 → 逐条实现 → verdict.md → 归档 specs/archive/
```
每一步必须等你确认后才进入下一步。模板见 `specs/template/`。

## 阶段方法论（读模板即获得，无需记忆命令）
- 写 `proposal.md` 前，先用模板顶部「需求澄清」对齐真实意图（brainstorming）。
- 写 `tasks.md` 用 writing-plans 结构：每条任务含 `Files` / `Interfaces(Consumes-Produces)` / 2–5 分钟步骤 / 反占位符 / `Self-Review`。
- 验收用 `verdict.md` 双检闸门：规格符合性 + 代码质量。

## 安全 / 协作铁律（详见 `constitution.md`）
- 密钥 / `.env` 不入 git、不打印日志。
- 高风险操作（删文件、推远程、改主干 / 基础设施 / 协议）二次确认。

## 文档工具链（可选，详见 `docs/rules/code-management.md`）
- docstring 即真相源（如采用）：函数/类 docstring 是 reference 文档的唯一来源，具体生成工具由项目按语言选型。
- `scripts/optional/gen-refs.py` 为可选参考脚本（Python 项目），其他语言推荐各自生态工具。
- `scripts/check-docs.py` 校验 docs↔src 一致性。
- 工具为零依赖加成，非核心框架；需要 CI 把关时把 `scripts/ci-template/check-docs.yml` 复制到 `.github/workflows/`（opt-in）。

## Handoff Protocol（跨 Agent / 跨工具交接）
1. 当前 Agent 在对应 `tasks.md` 末尾「接手上下文」补：阶段 / 已完成 / 未完成及阻塞 / 关键决策 / 建议下一步。
2. `git push`。
3. 新 Agent `git pull` 接手，先读 `AGENTS.md` + 对应 `specs/active/<slug>/`。

## 提交规范
Conventional Commits：`type(scope): description`；`type ∈ feat / fix / docs / spec / refactor / chore`。
CHANGELOG 可选（本脚手架默认以 commit 为准，YAGNI 不强制）。

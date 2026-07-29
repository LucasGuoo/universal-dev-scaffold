# 规则：Spec-Driven 流程

> 本文件定义不可违背的 Spec-Driven 开发流程规则。
> 具体工具（CodeBuddy / Cursor / Copilot 等）可将本文件内容映射为各自的红线规则格式。

## 硬约束

1. **不跳步**：多文件 / 新功能 / 协议变更 / 架构变化 → 必须走完整 spec 流程（proposal → design → tasks → 实现 → verdict）。
2. **变更决策树**：每次编码前必查：
   - 纯文档 / 文案 → 直接 commit
   - 单文件 <50 行、无架构/协议变化 → 直接改 + commit 说明
   - 配置/依赖变更、小功能、规则调整 → 写 change-proposal
   - 多文件/新功能/协议变更/架构变化 → 走完整 spec 流程
   - **不确定** → 走 spec（安全侧）
3. **5 步确认制**：proposal → 用户确认 → design → 用户确认 → tasks → 用户确认 → 逐条实现 → verdict → 归档。每步必须等确认后才进入下一步。
4. **可审计**：每个非平凡决策有 spec / change-proposal 落点，结论可回溯。

## 模板位置

- `specs/template/` — 6 个模板（proposal / design / tasks / verdict / change-proposal / context）
- `specs/active/` — 进行中的 spec
- `specs/archive/` — 已验收归档的 spec

## 参考

- 流程总览：`AGENTS.md`
- 模板详解：`specs/template/*.md`

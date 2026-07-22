# Specs 目录

本目录用 **Spec-Driven Development（轻量技能化）** 管理变更。完整流程与约定见仓库根 [`AGENTS.md`](../../AGENTS.md)。

## 目录结构
```
specs/
├── template/   # 本目录：6 个技能化模板（复制后填入具体 spec）
├── active/     # 进行中的 spec（按 YYYY-MM-DD-<slug>/ 建子目录）
└── archive/    # 已验收通过的 spec（verdict.md 结论「通过」后移入）
```

## 模板清单（`template/`）
| 模板 | 用途 | 何时用 |
|------|------|--------|
| `proposal.md` | 需求提案（含 brainstorming 需求澄清） | 完整 spec 第 1 步 |
| `design.md` | 技术方案（范围 / 文件结构 / 接口契约） | proposal 确认后第 2 步 |
| `tasks.md` | 实现任务（writing-plans 结构 + Self-Review） | design 确认后第 3 步 |
| `verdict.md` | 验收结论（双检闸门） | 实现完成后归档前 |
| `change-proposal.md` | 轻量变更提案 | 小改动 / 配置 / 依赖 / 加功能 |
| `context.md` | 项目背景简报 | 跨 Agent 交接时补充上下文 |

## 用法
1. 新需求：复制 `template/` 下所需文件到 `active/YYYY-MM-DD-<slug>/`。
2. 按 `AGENTS.md` 的「变更决策树」判断走 change-proposal 还是完整 spec。
3. 每步等你确认后推进（5 步确认制）。
4. 验收通过后将整个 `active/<slug>/` 移入 `archive/`。

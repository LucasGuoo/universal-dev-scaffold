# 文档总览（OVERVIEW）— 全局导航地图

> 本文件是**读者视图的入口地图**，不是新内容源。
> 它回答"我从哪开始看、按什么顺序看"，而不是"仓库里有什么文件"。
> 完整文件清单请看 [`docs/README.md`](./README.md)；怎么搭建本脚手架请看 [`scaffold-setup-guide.md`](./scaffold-setup-guide.md)。

## 这是什么
本仓库是一套**通用软件工程脚手架**（Spec-Driven + 轻量技能化）：纯 Markdown、零工具绑定、方法论下沉到模板、多代理入口、YAGNI。它提供可复用到任意项目的开发治理骨架，而非某个具体业务应用。

## 文档地图（按角色 / 场景的入口）

| 你是… | 先看 | 再看 |
|---|---|---|
| 新人 onboarding | [`tutorials/`](./tutorials/) | [`explanation/`](./explanation/)（先懂"为什么"再动手） |
| 开发者做任务 | [`how-to/`](./how-to/) | [`reference/`](./reference/) |
| 要接外部系统 / 依赖 | [`integration/`](./integration/) | — |
| 要上线 / 排障 | [`operations/`](./operations/) | — |
| 要改架构 / 评审 | [`explanation/`](./explanation/)（含 ADR） | [`rules/`](./rules/) |
| 要懂规则 / 硬约束 | [`constitution.md`](./constitution.md) | [`rules/`](./rules/) |
| 搭脚手架 / 跨 Agent 交接 | [`scaffold-setup-guide.md`](./scaffold-setup-guide.md) | [`skills/`](../skills/) |

## 两层结构速览

```
治理层（规则与约束，先立规矩）
  ├── constitution.md      硬约束（不可违背）
  ├── doc-lifecycle.md     文档生命周期规范
  ├── scaffold-setup-guide.md  搭建指南
  └── rules/               通用规则（spec-driven / quality-gates / doc-lifecycle / code-management）

内容层（活文档，按 Diátaxis 四象限 + 业务目录组织）
  ├── tutorials/   学习导向（教懂新人）
  ├── how-to/      问题导向（解决具体问题，含 runbook）
  ├── reference/   信息导向（精确 API / 接口 / 配置）
  ├── explanation/ 理解导向（解释"为什么"，含 ADR 架构决策）
  ├── integration/ 外部接口 / 依赖契约
  ├── operations/  运维手册（部署 / 监控 / 应急）
  └── product/     PRD / MRD / BRD / 路线图
```

- **治理层**：定义"怎么做事"，相对稳定，先读它建立共识。
- **内容层**：记录"做了什么 / 为什么"，随项目演进，按上面的地图按角色进入。

## 与 docs/README.md 的分工
- [`docs/README.md`](./README.md) = **清单**（仓库里有什么文档，逐类罗列）。
- 本文件 = **路径**（我该从哪看、按什么顺序看）。
- 建议：第一次进仓库先读本文件，再按地图跳到对应文档；后续查具体文件回 README 索引。

## 过程文档在哪
非持久的"过程文档"在仓库根的 `specs/`（`active/` 进行中、`archive/` 已验收），不属于 `docs/` 活文档体系。当前进行中的变更提案见 `specs/active/`。

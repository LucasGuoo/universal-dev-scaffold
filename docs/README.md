# 文档索引

## 全局入口

| 文档 | 用途 | 主要读者 |
|---|---|---|
| [`OVERVIEW.md`](./OVERVIEW.md) | **文档总览 / 导航地图**（按角色给出阅读路径，先读它） | 全员（尤其新人 / 外部读者） |

> 第一次进仓库：先读 [`OVERVIEW.md`](./OVERVIEW.md) 建立全局视图，再按地图跳到对应文档；查具体文件回本索引。

## 治理与规范

| 文档 | 用途 | 主要读者 |
|---|---|---|
| [`constitution.md`](./constitution.md) | **硬约束（含第 0 条金线判准 + 验证非协商铁律）** | 全员 |
| [`doc-lifecycle.md`](./doc-lifecycle.md) | 文档生命周期（创建 / 维护 / 同步 / 防漂移） | 开发者 / Agent |
| [`scaffold-setup-guide.md`](./scaffold-setup-guide.md) | 脚手架搭建指南（含工具适配 / 代码管理适配） | 搭脚手架 / 交接者 |

## 规则（`rules/`）

| 文件 | 内容 |
|---|---|
| [`rules/spec-driven.md`](./rules/spec-driven.md) | Spec-Driven 流程规则（变更决策树 / 5 步确认制） |
| [`rules/quality-gates.md`](./rules/quality-gates.md) | 质量闸门（代码 + 文档 + 量化阈值 + 安全基线 + 反理性化表） |
| [`rules/code-design.md`](./rules/code-design.md) | 设计原则与抽象规范（SOLID 诊断 / 坏味道 / 契约优先） |
| [`rules/doc-lifecycle.md`](./rules/doc-lifecycle.md) | 文档生命周期红线 |
| [`rules/code-management.md`](./rules/code-management.md) | 代码管理规则（工程基础 / 工具链 / 依赖管理） |

## Diátaxis 四象限

| 目录 | 类型 | 说明 |
|---|---|---|
| [`tutorials/`](./tutorials/) | 学习导向 | 引导新人完成完整体验 |
| [`how-to/`](./how-to/) | 问题导向 | 解决特定问题的步骤（含 runbook） |
| [`reference/`](./reference/) | 信息导向 | 精确描述 API / 接口 / 配置 |
| [`explanation/`](./explanation/) | 理解导向 | 解释"为什么"（含 ADR 架构决策记录） |
| ↳ [`ADR-0001`](./explanation/ADR-0001-global-overview-map.md) | ADR | 引入 OVERVIEW.md 作为全局导航地图（Accepted） |

## 业务文档

| 目录 | 说明 |
|---|---|
| [`product/`](./product/) | PRD / MRD / BRD / 路线图 |
| [`integration/`](./integration/) | 外部接口 / 依赖契约 |
| [`operations/`](./operations/) | 运维手册（部署 / 监控 / 应急） |

> 业务专属文档（架构基线、协议规范、部署约束等）按需追加，并在本文登记。

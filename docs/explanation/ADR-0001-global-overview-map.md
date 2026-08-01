---
doc-meta:
  type: ADR
  status: Accepted
  created: 2026-08-01
  superseded-by: null
  supersedes: null
---

# ADR-0001 引入 OVERVIEW.md 作为全局导航地图

## 状态
Accepted（2026-08-01）

## 背景
文档按 Diátaxis 四象限 + 业务目录（`product/integration/operations`）拆分后变细，读者缺乏"整体性"视图，需要跨多篇跳跃才能看懂全局。现有 `docs/README.md` 是**索引清单**（有什么），`scaffold-setup-guide.md` 是**搭建指南**（怎么建），二者都不是面向读者的"全局地图"（从哪看、按什么顺序看）。

## 决策
新增 `docs/OVERVIEW.md` 作为**单一导航入口**：
- 定位是"地图"而非"新内容源"，按角色 / 场景给出阅读路径，并显式区分与 `README.md`（清单）的分工。
- 不新增类目内二级组织（痛点 2 的类目索引页 / 分组约定）留待后续，遵循 YAGNI，待某类目文档涨到 7+ 篇再机会式处理。
- `docs/README.md` 新增「全局入口」表登记 OVERVIEW 为首读项；根 `README.md` 与 `scaffold-setup-guide.md` 文件树同步补 `OVERVIEW.md`。

## 后果
- 正面：读者有单一入口，减少跨文档跳跃；新人 / 外部读者可一眼看全仓库结构。
- 负面 / 成本：多维护一份入口文档，其路径链接需随目录演进保持有效（无自动校验工具，靠人工 / Agent 自查）。
- 兼容性：不破坏现有 Diátaxis 结构与 doc-lifecycle 分层；OVERVIEW 属于治理层入口，非内容层活文档。

## 备选方案
- (a) 仅在 `docs/README.md` 加"阅读路径"块 ——  rejected：README 定位是清单，混入导航会模糊其职责，且仍缺一份独立、醒目的总览。
- (b) 新增 `OVERVIEW.md`（本决策） ——  adopted：职责清晰、零新增细节、可独立演进。

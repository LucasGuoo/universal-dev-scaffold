# Change Proposal — docs-overview-manual

> 解决文档碎片化导致的"跳来跳去、缺整体性"痛点：新增一份**全局导航总览手册**，
> 作为单一入口，按读者角色给出阅读路径，而非再写一份细节文档。

## 1. 背景与动机
- 文档按 Diátaxis 四象限 + 业务目录（`product/integration/operations`）拆分后变细，读者缺乏"整体性"视图，需跳多篇才看懂全局。
- 现状：`docs/README.md` 是**索引清单**（有什么），`scaffold-setup-guide.md` 是**搭建指南**（怎么建），二者都不是面向读者的"全局地图"（从哪看、按什么顺序看）。
- 用户诉求：新增一份**整体性文档**（方案 b），一眼看全仓库、按角色/场景直达所需文档，减少跳跃。
- 目标：单一入口、零新增细节、与现有索引/指南互补不重叠。

## 2. 变更内容（具体文件 + 行为）

### 2.1 新增 `docs/OVERVIEW.md`（全局导航总览手册）
定位：**读者视图的"地图"**，不是新内容源。包含：
1. **一句话定位**：本仓库是什么、给谁看。
2. **文档地图（按角色/场景的入口）**：从 doc-lifecycle 第 6 节"使用/消费矩阵"显式化：
   - 新人 onboarding → tutorials/ → explanation/
   - 做开发任务 → how-to/ + reference/
   - 接外部系统 → integration/
   - 上线/排障 → operations/
   - 改架构/评审 → explanation/（ADR）+ rules/
   - 懂规则/硬约束 → constitution.md + rules/
   - 搭脚手架/交接 → scaffold-setup-guide.md + skills/
3. **两层结构速览**：治理层（constitution/doc-lifecycle/setup-guide/rules）vs 内容层（Diátaxis 四象限 + 业务三目录），各一句话说明"何时进哪层"。
4. **与 docs/README.md 的分工说明**：README = 完整文件清单（有什么）；OVERVIEW = 阅读路径（从哪看）。避免读者困惑两份索引。

### 2.2 同步更新索引（满足 check-docs 索引一致性）
- `docs/README.md`：在「治理与规范」表下登记 `OVERVIEW.md`（作为"全局入口"首项），并加一句"先读 OVERVIEW 再按路径深入"。
- `README.md`（仓库根）：文件树补 `docs/OVERVIEW.md`。
- `scaffold-setup-guide.md` 文件树（第 2 节）：补 `OVERVIEW.md`。

### 2.3 不做的（YAGNI）
- 不新增类目内二级分组/类目 README 索引页（痛点 2 的二级组织，待类目文档涨到 7+ 篇再机会式处理，本提案仅覆盖痛点 1）。
- 不把 OVERVIEW 内容重复写进 README/setup-guide。

## 3. 影响与风险
- 纯文档新增，零代码、零依赖。
- `check-docs.py` 已删除（远端移除工具链），但 `docs/README.md` 索引仍应登记新增文档，否则对人类读者不完整；本提案 2.2 已覆盖。
- 风险极低，可逆。

## 4. 验证方式
- `docs/README.md` 含 OVERVIEW 登记项，链接可达（无悬空）。
- `docs/OVERVIEW.md` 自洽：路径指向的目录/文件均真实存在。
- `git status` 仅显示新增的 OVERVIEW.md 与索引更新。

## 5. 待确认点
- 文件名：`docs/OVERVIEW.md`（醒目、惯例化）vs `docs/INDEX.md` vs `docs/architecture/START-HERE.md`？默认 `OVERVIEW.md`。
- 是否同步把痛点 2（类目内组织约定）也做成一条 `rules/doc-organization.md`？本提案**仅做痛点 1**；痛点 2 留待后续 change-proposal。

## 6. 决断
- [ ] 用户确认，可实施

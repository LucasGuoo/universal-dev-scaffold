---
name: using-scaffold
description: >-
  Use when starting any task in a project built on the universal-dev-scaffold
  framework, or when the user asks to follow/adhere to the scaffold, run the
  spec-driven flow, write ADRs, maintain docs, run check-docs/gen-refs, or
  avoid drift. Requires skill invocation before acting on the project.
---

# Using the Universal Dev Scaffold

> 本技能是**元技能**：它不是教你写某段代码，而是教 Agent **按脚手架框架来维护项目**，把"规范先行 / 不漂移 / 文档分层"变成肌肉记忆。
> 任何在本框架项目上的动作（改代码、写文档、做决策）之前，先按本技能校准。

**If you were dispatched as a subagent** and this is a one-shot answer with no project context: still read `AGENTS.md` + `docs/constitution.md` first, but skip the announce step. Otherwise: **ABSOLUTELY MUST** load and follow this skill. This is not negotiable.

**Announce protocol**：开始任何项目动作前，先说一句
`Using scaffold framework to <purpose>`，让用户知道你在按框架走。

---

## 1. The Rule（核心规则 — 不可协商）

在任何代码/文档动作之前，**按顺序**完成：

1. **读入口**：`AGENTS.md` → `docs/constitution.md`（硬约束，最高优先级）→ `docs/README.md`（索引）→ 按需 `specs/active/`。
2. **查决策树**（`AGENTS.md` 的「变更决策树」）：判断本轮是"纯文档 / 小改动 / change-proposal / 完整 spec"，**先定流程后动手**。
3. **走 spec 5 步确认制**：完整 spec 每步必须等用户确认再推进（proposal→design→tasks→实现→verdict→归档）。
4. **文档按层处理**（见第 3 节）：specs/reference 不人工维护，ADR 用追加式 Superseded，how-to/tutorial 写一次即可。
5. **改代码必补 docstring**：中文 docstring 是 reference 真相源，由 `scripts/gen-refs.py` 自动渲染；同 diff 更新。
6. **自查兜底**：动手后跑 `python scripts/check-docs.py`（加 `--require-docstrings` 可强制），把错误在合并前清掉。

> 框架文件的权威文本：`AGENTS.md`（流程）、`docs/constitution.md`（硬约束）、`docs/doc-lifecycle.md`（文档分层与生命周期）、`.codebuddy/rules/*.mdc`（IDE 红线）。本技能是它们的"操作手册浓缩版"，全文以这三个文件为准。

---

## 2. Behavior Norms（行为规范）

**Do（必须做）**
- 进入项目第一步永远是读 `AGENTS.md` 和 `constitution.md`，**不要凭默认习惯直接写代码**。
- 每轮改动先用决策树定位流程档位；不确定就走 spec（安全侧）。
- 把"不可违背项"与"临时方案"分开：`constitution` 只放真正的硬约束，过程文档进 `specs/`。
- 文档分层对待：Tier 0 不维护、Tier 1 写一次、Tier 2 才要生命周期（见第 3 节）。
- 推翻旧决策时**新增 ADR 标记旧 ADR 为 Superseded，旧 ADR 正文一字不改**。
- 提 PR 前本地跑 `check-docs.py`，让 CI 门禁不红。

**Don't（禁止）**
- 不要跳过 spec 直接写码（除非决策树判定为纯文档/小改动）。
- 不要手改 `docs/reference/_generated/` 下的文件（它们是自动生成的）。
- 不要用"删掉/改写旧 ADR"来表达决策变更——永远用追加 Superseded。
- 不要给 every 文档强加状态机/doc-meta；只有 ADR 和 explanation 才需要。
- 不要为"完备性"写长散文：constitution 保持最短，自由维护义务压到最小。
- 不要把密钥、`.env` 写进文档或日志。

---

## 3. Document Handling Operations（文档处理操作）

按触发场景给出具体操作。**核心立场**：生命周期只对"会随时间被推翻"的文档有意义，过程文档不维护。

### 3.1 读（消费）路径 — Agent 进场
```
AGENTS.md → constitution.md → docs/README.md（索引）
  → 按任务读 explanation / reference（不读 tutorial）
动手前：决策树定位 → 改代码同 diff 补 docstring → check-docs 自查
```

### 3.2 分层与触发矩阵
| 层级 | 文档 | 何时产 / 怎么养 |
|---|---|---|
| **Tier 0 不维护** | `specs/*` | 过程文档，验收即归档终态；状态靠"文件在 active 还是 archive"表达，**无元数据、不维护** |
| | `reference/` | `gen-refs.py` 自动渲染，**禁手改**，提交即重生成 |
| **Tier 1 写一次** | `how-to` / `tutorial` / `integration` / `runbook` | 触发点写出，**行为真的变了才顺手改**，不强制同 diff、无状态机 |
| **Tier 2 真生命周期** | `ADR` / `explanation`（架构原理） | 决策会随时间被推翻；用状态机 + `doc-meta` |

### 3.3 创建时机（钉在 spec 5 步节点）
- 需求澄清 → PRD / change-proposal（Tier 0）
- 设计决策（普通）→ explanation（Tier 2）
- 设计决策（重大/可逆风险高）→ **ADR**（Tier 2）
- 编码实现 → reference 条目（自动，Tier 0）
- 验收 → how-to（Tier 1）
- 发布/里程碑 → tutorial（Tier 1）
- 引入外部依赖 → integration 契约（决策树拦截，Tier 1）
- 架构变更/推翻旧决策 → 新 ADR + 同步 explanation（Tier 2）

### 3.4 ADR 状态机（唯一正式状态机）
`doc-meta` 仅用于 ADR 与 explanation：
```
<!-- doc-meta
status: Proposed | Accepted | Deprecated | Superseded
superseded-by: docs/architecture/adr/0007-xxx.md   # 仅 Superseded 时
owner: <团队或负责人>
last-reviewed: YYYY-MM-DD
-->
```
状态：`Proposed → Accepted`；被推翻时**旧 ADR 只翻 status 为 Superseded（正文不改），新增一条 ADR 其 `Supersedes` 指向旧 ADR**。这是抗 LLM 漂移的核心——操作是"追加"而非"修改"。

### 3.5 reference 自动生成
```
# 成员函数/函数的中文 docstring 即真相源
python scripts/gen-refs.py            # 渲染到 docs/reference/_generated/
python scripts/gen-refs.py --check    # CI 用：检查与代码同步
python scripts/check-docs.py          # 校验 docs↔src 一致性（链接/索引/缺 docstring）
```
AI 改函数**必须同 diff 更新其 docstring**（行号与签名由 ast 自动取，永不失真）。

### 3.6 工程健壮性 — 让 LLM 不跑偏（重点）
纪律不靠自觉，靠三层兜底：
1. **CI 门禁**：`check-docs.py` 作 PR 关卡（必跑 `--require-docstrings` + 索引校验），docstring 缺/索引错直接阻断合并，LLM 无法绕过。
2. **规则红线**：`.codebuddy/rules/*.mdc` 由 IDE 自动加载、不可跳过（如"改 `src/` 必补 docstring""加外部依赖必建 integration 文档"）。
3. **追加优先**：ADR Superseded / specs 新文件——减少需同步的文件数 = 减少漂移面。
4. **最小化自由维护**：不在每次变更都要求改散文，只在"ADR 被推翻"这种明确事件才动作。
5. **结构即信号**：用"文件是否存在 / docstring 是否齐全 / 索引是否列全"等机械信号表达状态。
6. **Human-in-the-loop**：spec 5 步确认 + verdict 双检，文档是否到位由人确认。

---

## 4. Red Flags（反漂移警示 — 模型的错误想法 vs 现实）

| 模型的错误想法 | 现实应有的正确行为 |
|---|---|
| "这个改动很小，直接写码就行" | 先查决策树；非纯文档/小改动就走 spec 或 change-proposal |
| "我顺手改下 doc-meta / 删掉旧 ADR 表达新决策" | 永远追加：新 ADR 标记旧 ADR Superseded，旧正文一字不改 |
| "reference 这页过时了，我手动改一下" | reference 禁手改；改的是 docstring，再跑 `gen-refs.py` 重渲染 |
| "给每个 how-to/tutorial 都加状态块、每次变更同步" | Tier 1 写一次即可，行为真变了才顺手改，无状态机 |
| "constitution 里把所有可能约定都写上更省心" | constitution 只放不可违背硬约束，保持最短才易被记住遵守 |
| "check-docs 跑不跑都行，合并前再说" | 动手后本地先跑 `check-docs.py`；它是 CI 门禁，红则阻断合并 |
| "specs 归档后顺手润色下旧文档" | specs 是过程文档，归档即终态，不维护 |
| "不读 AGENTS.md 凭经验直接开干" | 进场第一读 `AGENTS.md` + `constitution.md`，这是框架前提 |

---

## 5. Platform Adaptation（平台适配）

- **CodeBuddy（本环境）**：`.codebuddy/rules/*.mdc` 由 IDE 自动加载为红线；本技能通过 `use_skill` 调用。文档目录约定见 `docs/README.md`。
- **通用原则**：无论 CodeBuddy / Claude Code / Codex / Copilot / Gemini，入口统一在 `AGENTS.md`；`CLAUDE.md` / `COPILOT.md` / `GEMINI.md` 仅做重定向（不要在各处重复写规则，避免多源漂移）。

---

## 6. User Instructions（指令优先级）

**用户指令 > 本技能 > 框架默认行为 > 模型默认习惯。**

- 用户明确说"跳过 spec 直接改""这次不写 ADR"，则遵从用户（但高风险/破坏性行为仍走 `constitution.md` 第 7 条二次确认）。
- 本技能与 `.codebuddy/rules/*.mdc` 冲突时，以 `constitution.md` 的硬约束为准。
- 当本技能与具体实现类技能（如写某段代码）冲突：**本元技能优先**——先确保框架纪律，再做具体实现。

---

## 7. Quick Start（主动驱动本技能）

用户想"让 Agent 按框架走"时，可说：
- "按脚手架框架来做这个改动" → 触本技能，走决策树 + spec + 文档分层。
- "写个 ADR 记录这个架构决定" → 走第 3.3/3.4 节。
- "检查文档有没有漂移" → 跑 `check-docs.py` + 核对 ADR 状态链。
- "接手这个项目" → 走第 3.1 节读路径 + Handoff Protocol（`tasks.md` 接手上下文 + `git push`）。

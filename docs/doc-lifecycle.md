# 文档生命周期（Doc Lifecycle）— 脚手架内置约定

> 本文定义脚手架中技术文档的**创建时机、维护分层、使用消费与防漂移机制**。
> 核心立场：**生命周期只对"需要动态维护"的文档有意义；过程文档不维护**。工程健壮性优先于完备性——能交给 CI / 规则的，绝不靠 LLM 自觉。
> 零依赖（纯 Markdown + `.mdc` 规则）。外部工具（Spectral / openapi-diff / 契约测试框架）仅作可选 CI 门禁提及，不属于核心脚手架。

---

## 1. 目的与原则

1. **分清楚谁要动态维护、谁不要**：spec 是过程文档，验收即归档、不维护；reference 自动生成、不人工维护；只有 ADR / 架构原理这类"会随时间被推翻"的才需要生命周期。
2. **保留四类技术文档（Diátaxis）**：`tutorials/`、`how-to/`、`reference/`、`explanation/`。本文不改其分类，只规定维护力度。
3. **零依赖、纯 Markdown**。
4. **工程健壮性 > 文档完备性**：LLM 会跑偏，所以把能机械检查的都交给 CI 与规则，把自由维护义务压到最小。

---

## 2. 分层维护模型（核心）

按"是否需要动态维护"分三层，维护力度逐级加重：

### Tier 0 — 过程 / 自动文档（**不维护生命周期**）
- `specs/*`（proposal / design / tasks / verdict）：**过程文档**，验收即归档，归档后不再维护。状态靠"文件是否存在 / 在 active 还是 archive"表达，不需要任何元数据块。
- `reference/`（gen-refs 自动生成）：**禁手改**，提交即重渲染，无人工维护。

### Tier 1 — 相对稳定的交付物（**写一次，偶尔机会式更新，无正式生命周期**）
- `how-to`、`tutorial`、`integration` 契约、`runbook`：在触发点写出，**之后仅在"行为确实变了"时顺手改**；不做状态机、不强求同 diff 更新（降低 LLM 负担与漂移面）。

### Tier 2 — 需要真正生命周期的文档（**动态维护**）
- **`explanation/`（架构原理 / 决策记录）**：讲解"为什么这样设计"，其中记录具体决策的文档即是 **ADR**——带 `doc-meta` 状态机、可 `Superseded`。
- **constitution 业务约束**：随 ADR 演进；当某 ADR 被推翻，相关 explanation 与 constitution 同步。
- **ADR 不是独立目录，而是 `explanation/` 里"带状态的子类"**：推翻决策时在同一目录追加新篇并标记旧篇 `Superseded`，**不新建 `architecture/adr/` 目录**。
- **只有这一层（explanation 中记录决策的 ADR 子类）用状态机与 `doc-meta` 元数据。**

> 设计取舍：原方案给每类文档都加状态机会让 LLM 在每次变更都背负"更新多处散文"的义务，恰恰是漂移高发区。收缩到 Tier 2 后，绝大多数文档是"写了就基本不动"，维护成本与漂移风险同步下降。

---

## 3. 创建触发矩阵

| 触发点 | 产出文档 | 层级 | 对应 spec 阶段 |
|---|---|---|---|
| 需求澄清 | PRD / change-proposal | Tier 0 | proposal |
| 设计决策（普通） | explanation | Tier 2 | design |
| 设计决策（重大/可逆风险高） | 在 `explanation/` 写决策记录（ADR） | Tier 2 | design |
| 编码实现 | reference 条目（自动） | Tier 0 | implementation |
| 验收 | how-to | Tier 1 | verdict |
| 发布 / 里程碑 | tutorial | Tier 1 | release |
| 引入外部依赖 | integration 契约 | Tier 1 | 决策树拦截 |
| 架构变更 / 推翻旧决策 | 在 `explanation/` 新增 ADR + 同步相关 explanation | Tier 2 | design |

---

## 4. 生成 vs 手写分工

- **reference = 纯自动**：`gen-refs.py` 从 docstring 渲染，**禁手改**，提交即重生成，CI `--check` 拦不同步。
- **Tier 1 / Tier 2 = 手写但受控**：只在第 3 节对应节点产出，不日常维护。

---

## 5. 运维 / 同步规则（按层区分）

| 层级 | 同步触发 | 方式 |
|---|---|---|
| Tier 0 | — | 不维护；specs 归档即终态，reference 自动 |
| Tier 1 | 行为确实变了 | 机会式顺手改，**不强制同 diff** |
| Tier 2 | ADR 被推翻 / 架构调整 | 在 `explanation/` 内新增 ADR 标记旧 ADR Superseded（**追加，不改写**）；受影响的 explanation 同 diff 更新 |

**关键原则：优先"追加"而非"修改"**。ADR 用 Superseded 模式（见第 7 节），specs 用新文件而非改旧文件——减少"需同步多文件"的场景，即减少漂移面。

---

## 6. 使用 / 消费矩阵

| 角色 / 场景 | 读什么 | 不读什么 |
|---|---|---|
| Agent 进场 | constitution → `docs/README.md` 索引 → explanation / reference | tutorial |
| 开发者做任务 | how-to + reference | ADR（除非触碰架构） |
| 新人 / onboarding | tutorial → explanation | — |
| 架构 / 评审 | ADR + explanation + PRD | — |
| 运维 / 事故 | runbook（how-to 类） | — |

---

## 7. ADR 生命周期状态机（唯一正式状态机）

只对 `explanation/` 中"记录决策的 ADR 子类"用状态机；`doc-meta` 仅用于这类文档。

```html
<!-- doc-meta
status: Proposed | Accepted | Deprecated | Superseded
superseded-by: docs/explanation/why-xxx.md   # 仅 Superseded 时填
owner: <团队或负责人>
last-reviewed: 2026-07-23
-->
```

**状态流转**：

```
Proposed ──评审通过──▶ Accepted ──被新决策推翻──▶ Superseded（旧）
   │                        │                        │
   └────评审未过────▶ Deprecated             新 ADR: Proposed→Accepted
```

- **Proposed**：起草待评审。
- **Accepted**：评审通过，生效。
- **Deprecated**：不再推荐但暂不推翻（如被更优方案边缘化）。
- **Superseded（被推翻）**：**通过新增一条 ADR 并引用本 ADR 实现，绝不删除/改写旧 ADR**。这是抗 LLM 漂移的核心——操作是"追加"而非"修改"，不可能因漏改而失真，且决策演进链完整可追溯。

---

## 8. 工程健壮性：如何让 LLM 不跑偏（重点）

流程文档再完备，LLM 也可能不照做。对策按"可靠度"从高到低：

1. **能检查的都交给 CI，不靠自觉**：`check-docs.py` 作为 PR 门禁——docstring 缺失、索引不完整 → 失败并阻断合并。这是最强约束，LLM 无法绕过。
2. **硬规则写成 `.mdc`（IDE 自动加载、不可跳过）**：如"改 `src/` 必须补 docstring""加外部依赖必须建 `integration` 文档"。这是机器红线，不是建议。
3. **优先追加、避免修改**：ADR 用 Superseded 追加；specs 用新文件。减少需同步的文件数 = 减少漂移面。
4. **最小化自由维护义务**：不在每次变更都要求更新 explanation / how-to 散文（难验证、易漂移）；只在"ADR 被推翻"这种**明确事件**才要求动作。把模糊义务转成事件触发。
5. **结构即信号，少用自由文本状态**：用"文件/目录是否存在""docstring 是否齐全""索引是否列全"等机械信号表达状态，而非靠 `doc-meta` 里的自由字段（LLM 容易漏填或填错）。
6. **constitution 保持最短**：业务硬约束只对"不可违背项"列出，短小才易被 LLM 记住并遵守；长文档反而稀释重点。
7. **Human-in-the-loop 关键闸门**：spec 5 步确认制 + verdict 双检，把"文档是否到位"作为人要确认的一项，而非全信任 LLM。

> 结论：本文的"文档纪律"主要靠 **CI 门禁（1）+ 规则红线（2）+ 追加式 ADR（3,7）** 三件套兜底，流程文档本身只是给人/agent 看的指引，不指望 LLM 逐字遵守。

---

## 9. Few-shot 示例

### 9.1 ADR 状态块（唯一强制 doc-meta）

```html
<!-- doc-meta
status: Accepted
owner: @architect
last-reviewed: 2026-07-23
-->
```

### 9.2 ADR 被推翻（Superseded，追加不改写）

旧 ADR（保留不动，仅改 status）：

```html
<!-- doc-meta
status: Superseded
superseded-by: docs/explanation/why-trigger-via-github.md
owner: @architect
last-reviewed: 2026-07-23
-->
```
# ADR-0003：定时触发权分离（systemd timer）
…原决策与理由…

新 ADR（追加）：

```html
<!-- doc-meta
status: Accepted
owner: @architect
last-reviewed: 2026-08-10
-->
```
# ADR-0007：定时触发改回 GitHub Actions cron
## Context
运维成本上升，且需要跨区调度，systemd timer 不再划算。
## Decision
推翻 ADR-0003，改回 GitHub Actions cron；触发权交回平台。
## Consequences
- 正面：免维护宿主机 timer。
- 负面：失去本地可观测性，需在 Actions 补告警。
## Supersedes
[ADR-0003](0003-trigger-separation.md)
```

> 注意：旧 ADR 正文一字不改，只翻 status。决策链完整、零失真。

### 9.3 reference（自动，勿手改，仅展示对照）

源 docstring（`src/storage.py`）：

```python
def insert_retry(self, event_id: str, action: dict, due_at: float) -> int:
    """将一次重试计划写入重试表。

    处理顺序：
    1. 以 BEGIN IMMEDIATE 起事务，抢锁防止超额调度。
    2. 检查该 event 的待处理重试数，已达上限则回滚并抛错。
    3. 插入新行并返回自增 id。
    """
```

`gen-refs.py` 渲染（`docs/reference/_generated/storage.md`）：

```markdown
### `insert_retry(event_id, action, due_at) -> int`
将一次重试计划写入重试表。
**处理顺序：** 1… 2… 3…
**文件**：`src/storage.py:NN`  **签名**：`insert_retry(self, event_id: str, action: dict, due_at: float) -> int`
```

### 9.4 how-to / integration（Tier 1，写一次即可）

```html
<!-- 无需 doc-meta；行为变了才顺手改 -->
```
# 如何为失败动作配置重试
1. 在 `engine._execute_action` 捕获可重试异常。
2. 调用 `retry.RetryScheduler.schedule`（内部 `threading.Timer`）。
3. 到期由 `_do_notify` / `_do_webhook` 重放。
```

---

## 10. 场景案例（端到端走查）

### 场景 A：新增外部接口对接（钉钉通知）
| 阶段 | 文档动作 | 层级 |
|---|---|---|
| proposal | 写 PRD（specs，过程文档） | T0 |
| design | 在 `explanation/` 写原理；认证范式关键 → 在其中追加一条 ADR 决策记录 | T2 |
| implementation | 函数补 docstring → reference 自动 | T0 |
| 加依赖（决策树拦截） | **必须**写 integration 契约（写一次） | T1 |
| verdict | 写 how-to | T1 |
| release | 按需写 tutorial 一节；更新索引 | T1 |

### 场景 B：修复线上 bug（最小动作）
- 直接改（单文件 <50 行，决策树允许）。
- 改了函数 → 补/改 docstring → reference 自动更新。
- **不强制**动 how-to / explanation（行为未变则不碰）。
- 无新增文档 → 不动索引。
> 体现 Tier 1「机会式、不强制」与 Tier 0「自动」。

### 场景 C：大重构推翻旧决策（重点）
- design 阶段：在 `explanation/` 写 **新 ADR**（Accepted），其 `Supersedes` 指向旧 ADR；**旧 ADR（同目录旧篇）只翻 status 为 Superseded，正文不改**。
- 受影响的 explanation：同 diff 更新（Tier 2 唯一强制同步点）。
- reference：随代码自动。
- tutorial：仅当上手路径受影响才动（Tier 1 机会式）。

### 场景 D：LLM 漂移防护演练（工程健壮性）
1. LLM 改了 `src/` 函数却忘补 docstring。
2. 提 PR → CI 跑 `check-docs.py --require-docstrings` → **失败，阻断合并**。
3. LLM 被规则 `.mdc` 红线提醒，补回 docstring 后通过。
> 说明：纪律不依赖 LLM 自觉，而依赖 CI 门禁 + 规则红线（第 8 节 1、2）。

### 场景 E：Agent 进场第一天（消费路径）
1. 读 `AGENTS.md` → 入口与决策树。
2. 读 `docs/constitution.md` → 硬约束。
3. 读 `docs/README.md` → 索引。
4. 按任务读 explanation + reference（**不读 tutorial**）。
5. 改代码 → 同 diff 补 docstring；跑 `python scripts/check-docs.py` 自查。

---

## 11. 落地清单（给脚手架维护者）

本文件落地后，三处轻改动（均零依赖，**重点在 2、3 的兜底机制**）：

1. `AGENTS.md` 变更决策树补「文档闸门」三句话（见第 3、8 节）。
2. **新增 `.codebuddy/rules/04-doc-lifecycle/RULE.mdc`**：把"改 `src/` 必须补 docstring""加外部依赖必须建 integration 文档"写成 IDE 红线。
3. **`check-docs.py` 作为 CI 门禁**（PR 跑 `--require-docstrings` + 索引校验）：这是真正的强制，不是建议。
4. （可选）`specs/template/verdict.md` 加「文档闸门」清单。

> 本文本身已可独立使用；第 8 节的 CI + 规则三件套才是纪律的真正保障。

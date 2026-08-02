---
name: code-quality-guard
description: >-
  Enforce the scaffold's high-quality stable-code paradigm (金线原则) when an AI agent
  designs, writes, or reviews code. Runs the design-time 四件套约束, the post-write
  五轴评审, and the 金线三问验收 gate. Use proactively whenever the user asks to write code,
  do a code review, run a quality gate, or pass the spec verdict stage. Also trigger when
  the user mentions 金线 / 代码质量 / 稳定性 / review / 验收 / 设计原则.
---

# Code Quality Guard（金线护栏）

把脚手架的"高质量稳定代码构建范式"变成 AI 可执行的审查动作。
配套文件：`docs/constitution.md`（金线判准）、`docs/rules/code-design.md`（设计原则）、
`docs/rules/quality-gates.md`（量化闸门）、`specs/template/verdict.md`（验收表）。

## 触发时机

- 用户让 AI 写 / 改代码前 → 先跑「设计期约束」。
- 用户让 AI 做 code review / 质检 → 跑「写后五轴评审」。
- spec 进入 `verdict.md` 阶段 → 跑「金线三问验收」。
- 任何"看起来要交付代码"的节点都适用。

## 阶段一：设计期约束（写码前）

要求需求以「四件套」表达，缺项先补齐再动手：

1. **目标**：这次要解决什么业务问题？（对应金线③服务业务）
2. **约束**：性能 / 安全 / 兼容 / 依赖边界。
3. **上下文**：现有代码、相关模块、不能破坏的东西。
4. **验收**：如何客观判断"做对了"？（对应金线②可验证，必须有可测证据）

设计时用 `docs/rules/code-design.md` 第 1、2 节逐条自检：
SOLID 五问、DRY/KISS/YAGNI/Tell-Don't-Ask/Fail-Fast、抽象层级一致、依赖注入、契约优先。

## 阶段二：写后五轴评审（交付 / review 时）

逐轴检查，每轴给出 通过 / 打回 + 理由：

| 轴 | 检查点（来源） |
|---|---|
| 1. 正确性 | 边界 / 异常 / 空值处理；Fail Fast 不吞错 |
| 2. 可读性（意图） | 一眼懂"要做什么"；命名 / 结构清晰；无坏味道（见 code-design 第 3 节） |
| 3. 设计 | SOLID / 低耦合高内聚 / DI / 契约优先 |
| 4. 可测试性 | 外部依赖已注入；核心逻辑可独立测；测试比例达标 |
| 5. 安全 | OWASP 基线（输入校验 / 注入防护 / 密钥不裸奔） |

量化门槛（来自 quality-gates）：变更 ≤~100 行/次、函数 ≤~500 行、测试金字塔 80/15/5。

## 阶段三：金线三问验收（verdict 闸门）

交付前必须逐条回答，全过才算通过：

- **① 意图可读**：人 / AI 一眼能懂它做什么，不用猜？ → [是/否 + 证据]
- **② 可验证**：有测试 / 构建 / 运行证据，能客观判断做对没？ → [是/否 + 证据]
- **③ 服务业务**：它真解决了目标里的实际问题？ → [是/否 + 证据]

**验证非协商**：任何"看起来对"都需证据，AI 生成代码不得"跑通即完"。
**原则冲突**：SOLID/DRY/YAGNI 打架时回到 constitution 金线三问裁决，而非机械套用。
**防绕过**：遇到 quality-gates「反理性化表」里的借口，直接驳回。

## 输出格式

```
## 代码质量护栏报告
- 设计期四件套：目标✓ 约束✓ 上下文✓ 验收✓（缺项：…）
- 五轴评审：正确✓ 可读✓ 设计✓ 可测✓ 安全✓
- 金线验收：①✓ ②✓ ③✓
- 打回项（如有）：<逐条理由 + 文件:行号>
- 结论：通过 / 打回
```

## 严重度分级

- **Blocker**：违反金线 / 安全 / 验证非协商 → 必须改。
- **Major**：坏味道 / 原则违反 → 建议改。
- **Nit**：风格偏好 → 可选。
